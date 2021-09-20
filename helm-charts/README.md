# Eyes Helm Charts

helm charts for deploying eyes on kubernetes.

## Deployments

### Create Namespace

```bash
kubectl create ns eyes
```

### Deploy services

- Configmap: `helm install -n eyes config config`
- MySQL: `helm install -n eyes mysql bitnami/mysql -f mysql/values.yaml`
- Redis: `helm install -n eyes redis bitnami/redis -f redis/values.yaml`
- Dev Server: `helm install -n eyes dev dev`
- API: `helm install -n eyes api api`

### Argo workflow

```bash
# add repo
helm repo add argo https://argoproj.github.io/argo-helm

# update repo
helm repo update

# install
helm install -n eyes argo argo/argo-workflows

# deploy workflows
helm install -n eyes crawlers crawlers
```
