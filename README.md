# An example repo for maintaining ACC plugins

# Disclaimer: the contents of this repository are unsupported and come with no express or implied warranty.

## plugin.json - configure plugin metadata 
### Keys (\*=required) 
- \*pluginName - name to assign; best practice would be to match the git repo name, e.g. "monitoring-plugin-awscloud"
- \*dirs - directories to include in archive -- minimally "bin" and "allow_list"
- os - OS to receive the plugin; default choices are "all", "windows", "linux", "darwin" (MacOS)
- platform - specific platform to receive the plugin; default choices are "all", "ubuntu", "debian", "centos", "redhat", "microsoft_windows_10_enterprise", "microsoft_Windows_server_2012_r2_standard", "suse", "sles"

## bin - binary directory
This directory contains the scripts/executables which constitute your plugin.

## allow_list - allow list directory
This directory contains the check-allow-list.json file which controls what plugins can be execute (optionally with what arguments are allowed).

## bundle-plugin.py
This script performs the commands required to bundle and sign the content for use by the Agent Client Collector, then uploads the new bundle to your ServiceNow instance, creating/updating the corresponding ACC Plugin record as applicable.  It relies on a scoped app named "pluggy" which instantiates a purpose-built REST API endpoint.
