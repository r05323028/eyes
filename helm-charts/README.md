# Eyes Helm Charts

helm charts for deploying eyes on kubernetes.

## Deployments

### Create Namespace

```bash
kubectl create ns eyes
```

### Deploy services

- MySQL: `helm install -n eyes db bitnami/mysql -f database/values.yaml`
- Redis: `helm install -n eyes redis bitnami/redis -f redis/values.yaml`
