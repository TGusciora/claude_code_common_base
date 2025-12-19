---
name: k8s-dev
description: Kubernetes development guide for cloud-agnostic deployments. Covers manifest structure, resource limits, labeling standards, and provider-specific patterns (Azure Phase 1).
---

# Kubernetes Development Guide

## Purpose

Guide Kubernetes resource creation following team standards: cloud-agnostic patterns with provider-specific configurations. Ensures consistent manifests across all deployments.

> **Detailed Standards:** See [K8S_OPERATIONS.md](.claude/repo_specific/K8S_OPERATIONS.md) (create project-specific K8s operations doc)
> **Current Phase:** Azure deployment (Phase 1)

## When to Use This Skill

- Writing Kubernetes manifests (Deployments, Services, etc.)
- Creating Helm chart templates
- Setting up new applications in K8s
- Reviewing K8s configurations
- Troubleshooting K8s deployments

## Quick Reference

### Application Structure

Every application needs:

| Resource | Purpose |
|----------|---------|
| Service | ClusterIP network access |
| Deployment | Application pods |
| ConfigMap | Configuration (non-sensitive) |
| Secret | Sensitive values |
| PVC | Database storage |

### Required Labels

```yaml
labels:
  app: sage-avatar           # Application name
  system: aicompanion        # System/product
  component: backend         # backend | frontend | mobile | database
  owner: "FirstName LastName"    # Service lead
  version: "1.0.0"           # Version
```

### Service Pattern

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # Always ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8000
```

### Resource Limits (Required)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Namespace Naming

```
{systemname}-{environment}
```

Examples: `aicompanion-dev`, `sage-staging`, `aicompanion-prod`

---

## Core Rules

### 1. One Container Per Pod

- One business logic container per Pod
- Database in **separate Pod** with own Service
- Never combine app + database in same Pod

### 2. ClusterIP Only

- All services use `type: ClusterIP`
- External traffic via **Ingress only**
- No LoadBalancer or NodePort

### 3. Resource Limits Always

Every container must define:
- `resources.requests.memory`
- `resources.requests.cpu`
- `resources.limits.memory`
- `resources.limits.cpu`

### 4. Labels on Everything

All resources must have all 5 labels:
- `app`, `system`, `component`, `owner`, `version`

---

## Cloud-Specific Patterns

### Azure (Phase 1)

```yaml
# Storage
storageClassName: azure-managed-disk

# Registry
image: molsageengine.azurecr.io/my-app:latest
```

### GCP (Future)

```yaml
storageClassName: standard  # or pd-ssd
```

### AWS (Future)

```yaml
storageClassName: gp2  # or gp3
```

---

## Common Patterns

### Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
    system: aicompanion
    component: backend
    owner: "Team Lead"
    version: "1.0.0"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
        system: aicompanion
        component: backend
        owner: "Team Lead"
        version: "1.0.0"
    spec:
      containers:
        - name: my-app
          image: molsageengine.azurecr.io/my-app:latest
          imagePullPolicy: IfNotPresent
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          ports:
            - containerPort: 8000
          env:
            - name: CONFIG_VALUE
              valueFrom:
                configMapKeyRef:
                  name: my-app-config
                  key: CONFIG_VALUE
            - name: SECRET_VALUE
              valueFrom:
                secretKeyRef:
                  name: my-app-secrets
                  key: SECRET_VALUE
```

### Database Deployment Pattern

```yaml
# Separate Pod for database
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-mongodb
  labels:
    app: my-app-mongodb
    system: aicompanion
    component: database
    owner: "Team Lead"
    version: "1.0.0"
spec:
  selector:
    matchLabels:
      app: my-app-mongodb
  strategy:
    type: Recreate  # Important for databases
  template:
    metadata:
      labels:
        app: my-app-mongodb
        system: aicompanion
        component: database
        owner: "Team Lead"
        version: "1.0.0"
    spec:
      containers:
        - name: mongo
          image: mongo:latest
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
      volumes:
        - name: mongodb-data
          persistentVolumeClaim:
            claimName: my-app-mongodb-pvc
```

### PVC Pattern (Azure)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-mongodb-pvc
  labels:
    app: my-app-mongodb
    system: aicompanion
    component: database
    owner: "Team Lead"
    version: "1.0.0"
spec:
  storageClassName: azure-managed-disk
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### Secret Reference Pattern

```yaml
env:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: my-app-secrets
        key: API_KEY
  - name: DATABASE_URI
    valueFrom:
      secretKeyRef:
        name: my-app-secrets
        key: DATABASE_URI
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| App + DB in same Pod | Can't scale independently | Separate Deployments |
| No resource limits | Pod eviction, cluster instability | Always define limits |
| Missing labels | Hard to track ownership | Use all 5 required labels |
| LoadBalancer Service | Direct exposure, no control | Use ClusterIP + Ingress |
| Secrets in ConfigMap | Security risk | Use Secret resources |
| Hardcoded values | Environment coupling | Use ConfigMap/Secret refs |

---

## Validation Checklist

Before applying manifests:

- [ ] All Services are `type: ClusterIP`
- [ ] All containers have resource limits
- [ ] All resources have 5 required labels
- [ ] Database is in separate Pod
- [ ] Namespace follows `{system}-{environment}`
- [ ] Sensitive values in Secrets (not ConfigMaps)
- [ ] Correct StorageClass for target cloud

---

## Resource Files

| File | Content | When to Use |
|------|---------|-------------|
| [MANIFEST_TEMPLATES.md](resources/MANIFEST_TEMPLATES.md) | Complete manifest examples | Creating new deployments |
| [LABEL_STANDARDS.md](resources/LABEL_STANDARDS.md) | Label conventions | Reviewing/creating resources |
| [COMMON_ISSUES.md](resources/COMMON_ISSUES.md) | Troubleshooting guide | Debugging problems |

---

## Quick Commands

| Command | Purpose |
|---------|---------|
| `/k8s-dev` | Activate this skill |
| `kubectl apply -f manifest.yaml` | Apply manifest |
| `kubectl get pods -n {namespace}` | List pods |
| `kubectl describe pod {name}` | Pod details |
| `kubectl logs {pod-name}` | View logs |
