'''An example repo for maintaining ACC plugins'''

=== plugin.json - configure plugin metadata ===
==== Keys (\*=required) ====
\*pluginName - name to assign; best practice would be to match the git repo name, e.g. "monitoring-plugin-awscloud"
\*dirs - directories to include in archive -- minimally "bin" and "allow_list"
os - OS to receive the plugin; default choices are "all", "windows", "linux", "darwin" (MacOS)
platform - specific platform to receive the plugin; default choices are "all", "ubuntu", "debian", "centos", "redhat", "microsoft_windows_10_enterprise", "microsoft_Windows_server_2012_r2_standard", "suse", "sles"
