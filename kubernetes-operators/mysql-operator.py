import kopf
import kubernetes.client as k8s
import yaml

NAMESPACE = "default"

def create_mysql_deployment(name, spec):
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": NAMESPACE},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {
                            "name": "mysql",
                            "image": spec.get("image", "mysql:latest"),
                            "env": [
                                {"name": "MYSQL_ROOT_PASSWORD", "value": spec["password"]},
                                {"name": "MYSQL_DATABASE", "value": spec["database"]},
                            ],
                            "ports": [{"containerPort": 3306}],
                            "volumeMounts": [{"mountPath": "/var/lib/mysql", "name": "mysql-storage"}],
                        }
                    ],
                    "volumes": [{"name": "mysql-storage", "emptyDir": {}}],
                },
            },
        },
    }

@kopf.on.create('otus.homework', 'v1', 'mysqls')
def create_mysql(spec, name, namespace, logger, **kwargs):
    api = k8s.AppsV1Api()
    deployment = create_mysql_deployment(name, spec)
    api.create_namespaced_deployment(namespace=NAMESPACE, body=deployment)
    logger.info(f"MySQL instance {name} created.")

@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_mysql(spec, name, namespace, logger, **kwargs):
    api = k8s.AppsV1Api()
    api.delete_namespaced_deployment(name, namespace)
    logger.info(f"MySQL instance {name} deleted.")