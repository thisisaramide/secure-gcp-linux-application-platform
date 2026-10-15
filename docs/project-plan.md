# Project Plan

## Project

Secure GCP Linux Application Platform

## Objective

Build a small internal inventory application on GCP that demonstrates Linux system administration, automation, containerization, Kubernetes fundamentals, and cloud-security practices.

## Phase 1: Linux Foundation

- Create a GCP project and budget alert
- Deploy one Linux virtual machine
- Create a non-root administrative user
- Secure SSH access
- Install and configure Nginx
- Configure basic host firewall rules
- Create system health-check and patch-report scripts
- Document every decision and command

## Phase 2: Automation

- Create Ansible playbooks for Linux configuration
- Automate user management, Nginx, SSH hardening, and logging
- Store infrastructure configuration in Git

## Phase 3: Application and Backup

- Deploy a small internal inventory application
- Add a PostgreSQL database
- Create, test, and document backup and restore procedures

## Phase 4: Containers and Kubernetes

- Containerize the application with Docker
- Deploy it to GKE
- Configure health checks, replicas, configuration, and secrets

## Phase 5: Cloud Security

- Apply least-privilege IAM
- Use Secret Manager
- Review Security Command Center findings
- Document a threat model and incident-response runbooks
