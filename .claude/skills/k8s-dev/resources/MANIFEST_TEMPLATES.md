# Kubernetes Manifest Templates

Complete, copy-paste ready templates following team standards.

---

## Full Application Stack (Azure)

Complete example with app, database, services, and storage:

```yaml
# ============================================
# Application Service
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
  namespace: aicompanion-dev
  labels:
    app: my-app
    system: aicompanion
    component: backend
    owner: "Team Lead"
    version: "1.0.0"
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
---
# ============================================
# Application Deployment
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: aicompanion-dev
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
            - name: DATABASE_NAME
              value: "my_app_db"
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
---
# ============================================
# Database PVC
# ============================================
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-mongodb-pvc
  namespace: aicompanion-dev
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
---
# ============================================
# Database Service
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: my-app-mongodb
  namespace: aicompanion-dev
  labels:
    app: my-app-mongodb
    system: aicompanion
    component: database
    owner: "Team Lead"
    version: "1.0.0"
spec:
  type: ClusterIP
  ports:
    - port: 27017
      targetPort: 27017
  selector:
    app: my-app-mongodb
---
# ============================================
# Database Deployment
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-mongodb
  namespace: aicompanion-dev
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
    type: Recreate
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
          image: mongo:7
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              valueFrom:
                secretKeyRef:
                  name: my-app-secrets
                  key: MONGO_ROOT_USERNAME
            - name: MONGO_INITDB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-app-secrets
                  key: MONGO_ROOT_PASSWORD
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
      volumes:
        - name: mongodb-data
          persistentVolumeClaim:
            claimName: my-app-mongodb-pvc
```

---

## Service Template

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-service
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
spec:
  type: ClusterIP
  selector:
    app: ${APP_NAME}
  ports:
    - protocol: TCP
      port: 80
      targetPort: ${TARGET_PORT}
```

---

## Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        system: ${SYSTEM}
        component: ${COMPONENT}
        owner: "${OWNER}"
        version: "${VERSION}"
    spec:
      containers:
        - name: ${APP_NAME}
          image: molsageengine.azurecr.io/${APP_NAME}:${VERSION}
          imagePullPolicy: IfNotPresent
          resources:
            requests:
              memory: "${MEMORY_REQUEST}"
              cpu: "${CPU_REQUEST}"
            limits:
              memory: "${MEMORY_LIMIT}"
              cpu: "${CPU_LIMIT}"
          ports:
            - containerPort: ${CONTAINER_PORT}
          env:
            # Add environment variables here
            - name: ENV_VAR
              value: "value"
```

---

## ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
data:
  CONFIG_KEY: "config_value"
  ANOTHER_KEY: "another_value"
  # For multi-line config files:
  app.properties: |
    key1=value1
    key2=value2
```

---

## Secret Template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
type: Opaque
stringData:
  API_KEY: "your-api-key"
  DATABASE_URI: "mongodb://user:pass@host:27017/db"
```

---

## PVC Template

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${APP_NAME}-pvc
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
spec:
  storageClassName: azure-managed-disk  # Change per cloud
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: ${STORAGE_SIZE}
```

---

## Ingress Template

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}-ingress
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    system: ${SYSTEM}
    component: ${COMPONENT}
    owner: "${OWNER}"
    version: "${VERSION}"
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - ${DOMAIN}
      secretName: ${APP_NAME}-tls
  rules:
    - host: ${DOMAIN}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${APP_NAME}-service
                port:
                  number: 80
```

---

## Namespace Template

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${SYSTEM}-${ENVIRONMENT}
  labels:
    system: ${SYSTEM}
    environment: ${ENVIRONMENT}
```

---

## Resource Size Presets

### Small (API endpoints, lightweight services)

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "250m"
```

### Medium (Standard backends)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Large (Workers, heavy processing)

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### XLarge (ML models, heavy compute)

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### Database (MongoDB/PostgreSQL)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```
