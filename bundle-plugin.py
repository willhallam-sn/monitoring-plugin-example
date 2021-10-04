#!/usr/bin/env python3

import argparse
import base64
import getpass
import json
import logging
import os
import requests
import subprocess
import sys

# bundle up an ACC plugin

# standard metadata file
metaDataFile='plugin.json'

# signature file
sigFile='sign.txt.sha256'

# base64 signature file
b64SigFile='sign.txt.sha256_encode64.sig'

# bundle subdir
bundleDir='./bundle'

# required metadata keys
requiredKeys=['pluginName','dirs']

# target table for attachment
targetTable='sn_agent_asset'

# initialize logging
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)

parser = argparse.ArgumentParser(usage='bundle-plugin.py --user user [--password <password>] --instance myinstance.service-now.com --keyfile keyfile.key')
parser.add_argument('-u','--user',dest='user')
parser.add_argument('-p','--password',dest='pwd')
parser.add_argument('-k','--keyfile',dest='keyfile')
parser.add_argument('-i','--instance',dest='instance') # e.g. "myinstance.service-now.com"

args = parser.parse_args()

if not args.user or not args.instance or not args.keyfile:
    parser.print_help()
    sys.exit(1) 

# Set the request parameters
url = 'https://'+args.instance+'/api/x_snc_pluggy/pluggy/plugin'
signingKeyFile=args.keyfile

# user from args
user=args.user
# prompt for password
if not args.pwd:
    pwd = getpass.getpass(prompt='Password:')
else:
    pwd=args.pwd

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# open metadata file
try:
    f=open(metaDataFile)
except Exception as e:
    logging.error(e)
    raise(e)

# parse metadata file
try:
    metaDataJson=json.loads(f.read())
    f.close()
except Exception as e:
    logging.error(e)
    raise(e)

# make sure required values are included
for reqKey in requiredKeys:
    if reqKey not in metaDataJson:
        logging.error('Metadata is missing required key '+reqKey)
        raise(e)

# create a tar archive consisting of the dirs from metadata
try:
    tarArgs=["tar","-C",".","-zcvf",metaDataJson['pluginName']+".tar.gz"]
    for dirName in metaDataJson['dirs']:
        tarArgs.append(dirName)
    (subprocess.run(tarArgs)).check_returncode()
except Exception as e:
    logging.error(e)
    raise(e)

# sign the tar archive
try:
    (subprocess.run(["openssl","dgst","-sha256","-sign",signingKeyFile,"-out",sigFile,metaDataJson['pluginName']+".tar.gz"])).check_returncode()
except Exception as e:
    logging.error(e)
    raise(e)

# encode the signature
try:
    f=open(b64SigFile,'w') 
    (subprocess.run(["base64",sigFile],stdout=f)).check_returncode()
    f.close()
except Exception as e:
    logging.error(e)
    raise(e)

# create tmpdir for new archive if it does not exist
try:
    if not os.path.isdir(bundleDir):
        os.mkdir(bundleDir,mode=0o777)
except Exception as e:
    logging.error(e)
    raise(e)

# create the new archive with the original archive and signature
try:
    (subprocess.run(["tar","-C",".","-zcvf",bundleDir+"/"+metaDataJson['pluginName']+".tar.gz",metaDataJson['pluginName']+".tar.gz","sign.txt.sha256_encode64.sig"])).check_returncode()
except Exception as e:
    logging.error(e)
    raise(e)

# read in the new archive
f=open(bundleDir+"/"+metaDataJson['pluginName']+".tar.gz",'br')
attachment=f.read()
f.close()

b64Attachment=base64.b64encode(attachment)
strAttachment=str(b64Attachment)

requestJson={'name':metaDataJson['pluginName'],'attachment':strAttachment[1:]}

# Do the HTTP request
response = requests.post(url, auth=(user, pwd), headers=headers,json=requestJson)

# Check for HTTP codes other than 200
if response.status_code != 200: 
    logging.warn('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    sys.exit(10)
