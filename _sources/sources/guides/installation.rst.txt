Installation
============

Kubernetes (Recommended)
------------------------

**Kubernetes** is widely used in several famous services. We also recommended you install **Eyes** in a Kubernetes cluster.

Create namespace
################

First, we need to create an namespace.

.. code-block:: bash

    kubectl create ns eyes

Argo workflows
##############

Second, install **Argo Workflows**. Our service mainly use it to manage ETL jobs.

.. code-block:: bash

    # add repo
    helm repo add argo https://argoproj.github.io/argo-helm

    # update
    helm repo update

    # install 
    helm install -n eyes argo argo/argo-workflows

Deploy services
###############

Finally, deploy services of **Eyes**.

.. code-block:: bash

    # configmap
    helm install -n eyes config helm-charts/config

    # mysql
    helm install -n eyes mysql bitnami/mysql -f helm-charts/mysql/values.yaml

    # redis
    helm install -n eyes redis bitnami/redis -f helm-charts/redis/values.yaml

    # celery worker
    helm install -n eyes celery-worker helm-charts/celery

    # api
    helm install -n eyes api helm-charts/api

    # cron-workflows
    helm install -n eyes crawlers helm-charts/crawlers

Docker Compose
--------------

WIP
