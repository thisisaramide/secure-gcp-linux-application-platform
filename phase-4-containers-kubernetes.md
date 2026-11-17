# Phase 4: Containers and Kubernetes

## Goal

Package the Raitbyne Inventory API as a Docker container, store the image securely in Google Artifact Registry, and deploy the API and PostgreSQL database to Google Kubernetes Engine (GKE).

## What was built

- A Docker image for the Flask and Gunicorn inventory API
- A hardened container that runs as a non-root user
- A private Artifact Registry repository for Docker images
- Cloud Build image builds and pushes
- A GKE Autopilot cluster
- Kubernetes resources for:
  - Namespace
  - ConfigMap
  - Secret
  - PostgreSQL StatefulSet
  - Persistent storage claim
  - API Deployment
  - Internal ClusterIP Services
- Two running API replicas
- One persistent PostgreSQL database Pod

## Docker container

The application Dockerfile is located at:

```text
app/Dockerfile

