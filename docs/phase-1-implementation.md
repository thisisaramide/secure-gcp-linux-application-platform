# Phase 1 Linux Foundation

## Objective

Build and administer a secure Linux web server in Google Cloud.

## Infrastructure

- GCP project: RAITBIN
- Custom VPC: raitbin-vpc
- Subnet: raitbin-subnet
- Private subnet range: 10.10.0.0/24
- VM: raitbin-web-01
- Operating system: Ubuntu 26.04 LTS
- Machine type: e2-micro

## Network Security

- Created a custom VPC instead of using the default VPC.
- Created an IAP-only SSH firewall rule.
- Restricted SSH access to Google IAP TCP forwarding.
- Applied the `iap-ssh` network tag to the VM.
- Did not enable public HTTP or HTTPS firewall access.

## Linux Administration

- Connected to the VM through IAP using Cloud Shell.
- Applied system updates and rebooted to load the updated kernel.
- Installed Nginx and confirmed it starts automatically after reboot.
- Created the restricted `appoperator` account.
- Created `/opt/acme-inventory` with restricted permissions.
- Enabled unattended security updates.
- Verified Nginx log rotation.

## Automation

- Created `/usr/local/bin/health-check`.
- Created `/usr/local/bin/patch-report`.
- Created a systemd health-check service and daily timer.
- Verified health-check output through the system journal.

## Validation

- Nginx service status: active
- Local web-server response: HTTP 200
- Internal VM IP: 10.10.0.2
- Failed system services: none
