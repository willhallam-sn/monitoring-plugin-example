#!/usr/bin/env python3
import boto
import boto.ec2
import boto.vpc
import sys
if len(sys.argv) < 4:
    print('Usage: check_vpn.py ')
    sys.exit()
IP1 = sys.argv[1]
IP2 = sys.argv[2]
ec2_region = sys.argv[3]
aws_access_key_id =
aws_secret_access_key =
def test_vpc_status():
    ec2_conn = boto.vpc.connect_to_region(ec2_region,
    aws_access_key_id=
    aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
    x = []
    for vpn_connection in ec2_conn.get_all_vpn_connections():
        for tunnel in vpn_connection.tunnels:
            if tunnel.outside_ip_address == IP1 or tunnel.outside_ip_address == IP2:
                name = vpn_connection.id
                x.append(tunnel.status)
            if 'UP' in x:
                print('Ok - at least one tunnel is UP in ' + name)
                sys.exit(0)
            else:
                print('Critical - there is no up tunnels in ' + name)
                sys.exit(2)
if __name__ == "__main__":
test_vpc_status()
