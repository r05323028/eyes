# Eyes Helm Charts

helm charts for deploying eyes on kubernetes.

## Deploy Eyes

Simply use one line command:

```bash
helm install eyes eyes
```

## Settings

You can use `eyes/values.yaml` to change settings in `eyes`. For example, if you want to use AWS RDS rather than self-hosted MySQL, you can simply set `mysql.enabled=false` and `config.mysql.host=YOUR_AWS_RDS_HOST` or use following command:

```bash
helm install eyes eyes \
    --set mysql.enabled=false \
    --set config.mysql.host=MYSQL_HOST \
    --set config.mysql.user=MYSQL_USER \
    --set config.mysql.password=MYSQL_PASSWORD \
    --set config.mysql.password=MYSQL_PASSWORD \
    ...
```
