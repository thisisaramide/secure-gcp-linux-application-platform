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

## Repository Layout

```text
ansible/
├── files/
│   ├── health-check
│   └── patch-report
├── inventory/
│   └── hosts.yml
├── playbooks/
│   └── linux-foundation.yml
└── templates/
    ├── health-check.service.j2
    └── health-check.timer.j2
