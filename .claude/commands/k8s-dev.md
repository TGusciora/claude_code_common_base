Activate the k8s-dev skill to help with Kubernetes development following team standards and cloud-agnostic patterns.

Read the skill file at `.claude/skills/k8s-dev/SKILL.md` and apply its guidance.

## Task Detection

Determine what the user needs:

**Creating manifests:**
- Apply cloud-agnostic patterns (Azure Phase 1)
- Ensure ClusterIP services only
- Include all 5 required labels (app, system, component, owner, version)
- Add resource limits to all containers

**Setting up deployments:**
- Separate application and database into different Pods
- Use Secrets for sensitive data
- Use ConfigMaps for configuration
- Apply correct StorageClass for target cloud

**Reviewing K8s resources:**
- Check for missing resource limits
- Verify label compliance
- Ensure service type is ClusterIP
- Confirm database separation pattern

**Troubleshooting:**
- Reference common issues guide
- Check pod status and logs
- Verify service endpoints

## Resource Files

Reference these for deeper guidance:

- `.claude/skills/k8s-dev/resources/MANIFEST_TEMPLATES.md` - Complete manifest examples
- `.claude/skills/k8s-dev/resources/LABEL_STANDARDS.md` - Labeling conventions
- `.claude/skills/k8s-dev/resources/COMMON_ISSUES.md` - Troubleshooting guide

Also reference:
- `.claude/repo_specific/K8S_OPERATIONS.md` - Full operational standards

## Key Rules

- **ClusterIP Only**: All services use ClusterIP, traffic through Ingress
- **Resource Limits**: Required on all containers
- **One Container Per Pod**: Separate app and database
- **5 Required Labels**: app, system, component, owner, version
- **Namespace Naming**: `{system}-{environment}` format
