# Kubernetes Label Standards

Consistent labeling ensures proper resource tracking, ownership, and management.

---

## Required Labels

Every Kubernetes resource **must** have these 5 labels:

| Label | Purpose | Example |
|-------|---------|---------|
| `app` | Application identifier | `sage-avatar`, `sage-api` |
| `system` | System/product grouping | `aicompanion`, `sage-b2b` |
| `component` | Application tier | `backend`, `frontend`, `database` |
| `owner` | Responsible person/team | `FirstName LastName` |
| `version` | Deployed version | `1.0.0`, `2.1.3` |

---

## Label Format

```yaml
metadata:
  labels:
    app: sage-avatar
    system: aicompanion
    component: backend
    owner: "FirstName LastName"
    version: "1.0.0"
```

---

## Label Values

### `app` - Application Name

Use the application's unique identifier:

```yaml
# Good
app: sage-avatar
app: sage-api
app: sage-worker
app: sage-frontend

# Bad
app: backend        # Too generic
app: my-app         # Not descriptive
app: sage           # Too vague
```

### `system` - System/Product

Use the product or system name:

```yaml
# Good
system: aicompanion
system: sage-b2b
system: dataplatform

# Bad
system: prod        # This is environment, not system
system: app         # Too generic
```

### `component` - Application Tier

Use one of these standard values:

| Value | Usage |
|-------|-------|
| `backend` | API services, business logic |
| `frontend` | Web UIs, SPAs |
| `mobile` | Mobile backends |
| `database` | Databases, caches |
| `worker` | Background job processors |
| `ingress` | Ingress controllers |
| `monitoring` | Observability tools |

```yaml
# Good
component: backend
component: frontend
component: database
component: worker

# Bad
component: api          # Use 'backend'
component: web          # Use 'frontend'
component: mongo        # Use 'database'
component: jobs         # Use 'worker'
```

### `owner` - Responsible Party

Use the service lead's name or team:

```yaml
# Good
owner: "FirstName LastName"
owner: "Platform Team"
owner: "Backend Squad"

# Bad
owner: fl              # Not clear
owner: team            # Too vague
```

### `version` - Semantic Version

Use semantic versioning:

```yaml
# Good
version: "1.0.0"
version: "2.1.3"
version: "1.0.0-beta"

# Bad
version: latest        # Not specific
version: v1            # Not semantic
version: "1"           # Incomplete
```

---

## Where Labels Go

Labels must be present in:

1. **Metadata** (resource-level)
2. **Spec selector** (Deployments, Services)
3. **Template metadata** (Pod templates)

### Complete Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sage-avatar
  labels:                         # 1. Resource-level labels
    app: sage-avatar
    system: aicompanion
    component: backend
    owner: "FirstName LastName"
    version: "1.0.0"
spec:
  selector:
    matchLabels:                  # 2. Selector labels (subset)
      app: sage-avatar
  template:
    metadata:
      labels:                     # 3. Pod template labels
        app: sage-avatar
        system: aicompanion
        component: backend
        owner: "FirstName LastName"
        version: "1.0.0"
```

---

## Label Selector Rules

### Deployment Selector

Selector should match **at minimum** the `app` label:

```yaml
spec:
  selector:
    matchLabels:
      app: sage-avatar  # Must match pod template
```

### Service Selector

Service selector must match the pod's `app` label:

```yaml
spec:
  selector:
    app: sage-avatar  # Matches Deployment's pod labels
```

---

## Database Labeling

Database resources follow the pattern `{app}-{database}`:

```yaml
# Application
app: sage-avatar

# Application's database
app: sage-avatar-mongodb
component: database  # Note: 'database' not 'backend'
```

---

## Namespace Labels

Namespaces use `system` and `environment`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: aicompanion-dev
  labels:
    system: aicompanion
    environment: dev
```

---

## Query Examples

### List all resources for an application

```bash
kubectl get all -l app=sage-avatar
```

### List all resources in a system

```bash
kubectl get all -l system=aicompanion
```

### List all backends

```bash
kubectl get all -l component=backend
```

### List all resources by owner

```bash
kubectl get all -l owner="FirstName LastName"
```

### List specific version

```bash
kubectl get all -l app=sage-avatar,version=1.0.0
```

---

## Validation Checklist

Before deploying, verify:

- [ ] All 5 labels present (`app`, `system`, `component`, `owner`, `version`)
- [ ] Labels match between Deployment metadata, selector, and pod template
- [ ] Service selector matches pod `app` label
- [ ] Database resources labeled with `component: database`
- [ ] Owner value is a real name or team name
- [ ] Version follows semantic versioning
