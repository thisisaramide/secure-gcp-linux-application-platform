# Phase 5: Cloud Security

## Goal

Phase 5 hardens the Raitbyne Inventory platform by applying least-privilege identity controls, centralised secret management, container security controls, and security-focused validation across Google Cloud and GKE.

## Security controls implemented

### IAM and service account audit

The project IAM policy was reviewed.

- The Compute Engine default service account was identified as:

  `358293596927-compute@developer.gserviceaccount.com`

- No user-managed service account keys exist for that account.
- Google-managed keys may exist internally for Google Cloud services, but they are not downloadable JSON credentials.
- The Compute Engine default service account was granted `roles/logging.logWriter` so Cloud Build activity can be written to Cloud Logging.
- This role allows log writing only; it does not grant access to secrets, compute administration, or IAM administration.

### SSH access protection

The VM SSH firewall rule permits TCP port 22 only from Google's Identity-Aware Proxy range:

```text
35.235.240.0/20
The rule targets only instances with the iap-ssh network tag. This prevents unrestricted direct SSH exposure to the public internet.
GKE security posture
The GKE cluster uses:
- GKE Autopilot, which manages node hardening and baseline security configuration.
- Workload Identity, using the workload pool:
  strong-surge-513519-q5.svc.id.goog
- Google Cloud logging for system components and workloads.
- Google Cloud managed Prometheus monitoring.
- A private control-plane endpoint for internal VPC communication.
- Security Command Center enabled for security posture visibility.
The cluster also has a public control-plane endpoint. Access still requires Google Cloud authentication and Kubernetes authorisation, but a production environment should consider restricting authorised control-plane networks or using private-only cluster access.
Dedicated Kubernetes service accounts
The application no longer uses Kubernetes' generic default service account.

Two dedicated Kubernetes service accounts were created:
- raitbyne-inventory for the Inventory API Pods.
- raitbyne-postgres for the PostgreSQL StatefulSet.
These identities make it possible to grant access only to the workload that needs it.
Secret Manager and workload identity access
The database password is stored in Google Secret Manager as:
raitbyne-db-password
The Secret Manager add-on is enabled in GKE with secret rotation enabled.

Only these Kubernetes service account identities have the roles/secretmanager.secretAccessor role for this secret:
- ns/raitbyne/sa/raitbyne-inventory
- ns/raitbyne/sa/raitbyne-postgres
This follows least privilege: the Inventory API and PostgreSQL workload can read the password, while unrelated Pods cannot.
Secrets Store CSI Driver integration
The Secret Manager secret is mounted into both workloads as a file:
/var/secrets/db-password
The secret is not committed to Git, printed in terminal output, or stored in a Kubernetes Secret.

The Inventory API uses DB_PASSWORD_FILE and reads the password file whenever it creates a new database connection.

PostgreSQL uses POSTGRES_PASSWORD_FILE during container startup.
Password rotation process
The mounted secret file can receive updated Secret Manager versions, but rotating a database password is a coordinated operation:
1. Generate a new password securely.
2. Add the new value as a Secret Manager secret version.
3. Update the PostgreSQL role password.
4. Ensure the API opens new database connections using the updated secret file.
5. Restart PostgreSQL if required so its startup configuration uses the current secret.
Secret Manager updates the secret source. It does not automatically change the password stored inside PostgreSQL.
Container hardening
The Inventory API container uses these security controls:
- Runs as a non-root user.
- Uses runAsNonRoot: true.
- Disables privilege escalation.
- Drops all Linux capabilities.
- Uses the RuntimeDefault seccomp profile.
- Applies CPU, memory, and ephemeral-storage requests and limits.
- Uses readiness and liveness probes at /healthz.
Network exposure
The Inventory API Kubernetes Service is ClusterIP.

This means the application is reachable only from inside the Kubernetes cluster unless a separate Ingress, Gateway, or LoadBalancer is deliberately created.

PostgreSQL is also exposed only through an internal Kubernetes Service on port 5432.
Managed GKE firewall rules
The GKE-created firewall rules were reviewed and retained.
- The gke-...-all rule supports Pod-to-Pod networking.
- The gke-...-vms rule supports networking between GKE nodes and Pods.
These rules are managed by GKE and should not be manually deleted.
Validation performed
The following checks were completed successfully:
kubectl get pods -n raitbyne
Confirmed that both Inventory API Pods and the PostgreSQL Pod were running.
kubectl get deployment raitbyne-inventory -n raitbyne \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
Confirmed that the Inventory API Deployment uses the phase5.1 image.
kubectl exec -n raitbyne deployment/raitbyne-inventory -- \
  sh -c 'test -s /var/secrets/db-password && echo "Secret file is mounted"'
Confirmed that the API Pod receives the database password through the mounted Secret Manager file.
kubectl exec -n raitbyne raitbyne-postgres-0 -- \
  sh -c 'test -s /var/secrets/db-password && echo "PostgreSQL secret file is mounted"'
Confirmed that the PostgreSQL Pod receives the database password through the mounted Secret Manager file.
kubectl exec -n raitbyne deployment/raitbyne-inventory -- \
  python -c 'from urllib.request import urlopen; print(urlopen("http://127.0.0.1:8080/api/items", timeout=5).read().decode())'
Confirmed that the API could authenticate to PostgreSQL and retrieve inventory data.
Remaining production improvements
This portfolio phase establishes a secure foundation. A production implementation should additionally include:
- Replace broad project Owner access with narrower administrator roles.
- Restrict or remove the public GKE control-plane endpoint.
- Create alerting policies for failed workload health checks, suspicious IAM changes, and Secret Manager access anomalies.
- Add NetworkPolicies to explicitly restrict Pod-to-Pod traffic.
- Use a managed CI/CD trigger that builds automatically after reviewed GitHub pull requests are merged.
- Define and test a formal secret-rotation runbook.
