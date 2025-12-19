# Kubernetes Common Issues

Troubleshooting guide for common K8s deployment problems.

---

## Pod Issues

### Pod stuck in `Pending`

**Symptoms:**
```
NAME           READY   STATUS    RESTARTS   AGE
my-pod-abc12  0/1     Pending   0          5m
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Insufficient resources | Reduce resource requests or add nodes |
| No matching nodes | Check node selectors, taints, tolerations |
| PVC not bound | Check PVC status and StorageClass |

**Debug:**
```bash
kubectl describe pod my-pod-abc12
kubectl get events --field-selector involvedObject.name=my-pod-abc12
```

---

### Pod stuck in `ContainerCreating`

**Symptoms:**
```
NAME           READY   STATUS              RESTARTS   AGE
my-pod-abc12  0/1     ContainerCreating   0          5m
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Image pull failure | Check image name, registry access |
| Secret not found | Verify Secret exists in namespace |
| ConfigMap not found | Verify ConfigMap exists in namespace |
| PVC not bound | Check PVC status |

**Debug:**
```bash
kubectl describe pod my-pod-abc12
kubectl get pvc
kubectl get secret
```

---

### Pod in `CrashLoopBackOff`

**Symptoms:**
```
NAME           READY   STATUS             RESTARTS   AGE
my-pod-abc12  0/1     CrashLoopBackOff   5          10m
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Application crash | Check logs for errors |
| Missing env vars | Verify all required env vars are set |
| Wrong container port | Match containerPort to app's listen port |
| Resource limits too low | Increase memory/CPU limits |

**Debug:**
```bash
kubectl logs my-pod-abc12
kubectl logs my-pod-abc12 --previous  # Previous crash logs
kubectl describe pod my-pod-abc12
```

---

### Pod in `ImagePullBackOff`

**Symptoms:**
```
NAME           READY   STATUS             RESTARTS   AGE
my-pod-abc12  0/1     ImagePullBackOff   0          5m
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Wrong image name | Check image name and tag |
| Registry auth failed | Create/check imagePullSecrets |
| Image doesn't exist | Push image to registry |

**Fix for Azure ACR:**
```bash
# Verify image exists
az acr repository show-tags --name molsageengine --repository my-app

# Check registry secret
kubectl get secret acr-secret -o yaml
```

---

## Service Issues

### Service not routing traffic

**Symptoms:**
- Requests to service return connection refused
- No endpoints on service

**Debug:**
```bash
# Check endpoints
kubectl get endpoints my-service

# Should show pod IPs. If empty:
kubectl get pods -l app=my-app  # Check selector matches
```

**Common causes:**

| Cause | Solution |
|-------|----------|
| Selector mismatch | Ensure Service selector matches Pod labels |
| Wrong port | Ensure targetPort matches containerPort |
| No ready pods | Check Pod status |

---

### Service returns 503

**Symptoms:**
- Ingress returns 503 errors
- Service has no endpoints

**Debug:**
```bash
kubectl get endpoints my-service
kubectl get pods -l app=my-app -o wide
kubectl describe ingress my-ingress
```

---

## Storage Issues

### PVC stuck in `Pending`

**Symptoms:**
```
NAME          STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS
my-pvc        Pending                                      azure-managed-disk
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Invalid StorageClass | Use `azure-managed-disk` for Azure |
| Quota exceeded | Check storage quotas |
| No available storage | Check cloud provider limits |

**Debug:**
```bash
kubectl describe pvc my-pvc
kubectl get storageclass
```

---

### Volume mount permission denied

**Symptoms:**
```
Error: permission denied on /data/db
```

**Solutions:**

```yaml
# Add security context
spec:
  containers:
    - name: my-app
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
```

Or for MongoDB:
```yaml
securityContext:
  fsGroup: 999  # MongoDB group
```

---

## Configuration Issues

### Secret not found

**Symptoms:**
```
Error: secret "my-secret" not found
```

**Solutions:**

1. Check secret exists:
```bash
kubectl get secret my-secret -n my-namespace
```

2. Check namespace matches:
```bash
# Secret must be in same namespace as Pod
kubectl get secret -n aicompanion-dev
```

3. Create if missing:
```bash
kubectl create secret generic my-secret \
  --from-literal=KEY=value \
  -n aicompanion-dev
```

---

### Environment variable not set

**Symptoms:**
- Application fails with "missing config" errors
- Env var shows as empty

**Debug:**
```bash
kubectl exec my-pod -- printenv | grep MY_VAR
```

**Common causes:**

| Cause | Solution |
|-------|----------|
| Wrong secret key | Check secretKeyRef.key matches actual key |
| Secret not found | Verify secret exists |
| ConfigMap not found | Verify configMap exists |

---

## Resource Issues

### OOMKilled

**Symptoms:**
```
Last State:     Terminated
  Reason:       OOMKilled
```

**Solution:**
Increase memory limits:

```yaml
resources:
  limits:
    memory: "1Gi"  # Increase this
```

---

### CPU Throttling

**Symptoms:**
- Slow response times
- High latency

**Debug:**
```bash
kubectl top pod my-pod
```

**Solution:**
Increase CPU limits:

```yaml
resources:
  limits:
    cpu: "1000m"  # Increase this
```

---

## Network Issues

### Cannot resolve service name

**Symptoms:**
```
Error: getaddrinfo ENOTFOUND my-service
```

**Debug:**
```bash
# From inside a pod
kubectl exec my-pod -- nslookup my-service
kubectl exec my-pod -- nslookup my-service.my-namespace.svc.cluster.local
```

**Solutions:**

| Cause | Solution |
|-------|----------|
| Wrong service name | Use exact Service name |
| Cross-namespace | Use full DNS: `service.namespace.svc.cluster.local` |
| CoreDNS issues | Check CoreDNS pods |

---

### Connection refused to database

**Symptoms:**
```
Error: connect ECONNREFUSED 10.0.0.5:27017
```

**Debug:**
```bash
# Check database pod is running
kubectl get pods -l app=my-app-mongodb

# Check database service
kubectl get svc my-app-mongodb

# Check connectivity from app pod
kubectl exec my-app-pod -- nc -zv my-app-mongodb 27017
```

---

## Quick Debug Commands

```bash
# Pod status and events
kubectl describe pod <pod-name>

# Pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl logs <pod-name> -f  # Follow

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh

# Get all resources in namespace
kubectl get all -n <namespace>

# Events (sorted by time)
kubectl get events --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods
kubectl top nodes

# Check endpoints
kubectl get endpoints

# Describe service
kubectl describe svc <service-name>
```

---

## Prevention Checklist

- [ ] Resource limits set (memory and CPU)
- [ ] Health checks configured (readiness, liveness)
- [ ] Secrets exist before deployment
- [ ] Image pushed to registry
- [ ] StorageClass valid for cloud provider
- [ ] Service selector matches pod labels
- [ ] Correct ports configured
