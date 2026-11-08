# Phase 2: Ansible Automation

## Objective

Convert the manual Linux configuration from Phase 1 into repeatable, version-controlled Ansible automation.

## Design

- Ansible control node: `raitbin-web-01`
- Managed host: `localhost`
- Inventory: `ansible/inventory/hosts.yml`
- Playbook: `ansible/playbooks/linux-foundation.yml`

## Automated Configuration

The playbook ensures that:

- the APT package cache is refreshed;
- Nginx and unattended upgrades are installed;
- Nginx is enabled and running;
- the `appoperator` user exists;
- `/opt/raitbyne-inventory` exists with restricted permissions;
- automatic updates are scheduled;
- the health-check and patch-report scripts are deployed;
- the health-check systemd service and daily timer are deployed and enabled.

## Validation

- The Ansible inventory resolved `localhost`.
- The Ansible ping module returned `pong`.
- Playbook syntax validation passed.
- Check mode completed without failures.
- The playbook applied successfully.
- A repeat run returned `changed=0` and `failed=0`.
- The health-check service confirmed Nginx was active and returned HTTP 200.
- The daily health-check timer was scheduled successfully.

## Runbook

```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/linux-foundation.yml
