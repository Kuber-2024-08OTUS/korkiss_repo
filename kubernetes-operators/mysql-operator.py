import kopf
import kubernetes.client as k8s
import kubernetes.config as k8s_config

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
                    "volumes": [{"name": "mysql-storage", "persistentVolumeClaim": {"claimName": name}}],
                },
            },
        },
    }

def create_mysql_service(name):
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name, "namespace": NAMESPACE},
        "spec": {
            "selector": {"app": name},
            "ports": [{"protocol": "TCP", "port": 3306, "targetPort": 3306}],
            "type": "ClusterIP",
        },
    }

def create_mysql_pvc(name, size):
    return {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {"name": name, "namespace": NAMESPACE},
        "spec": {
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": size}},
        },
    }

@kopf.on.create('mysqls.otus.homework', 'v1')
def create_mysql(spec, name, namespace, logger, **kwargs):
    k8s_config.load_incluster_config()
    api_apps = k8s.AppsV1Api()
    api_core = k8s.CoreV1Api()

    # PVC
    pvc = create_mysql_pvc(name, spec.get("storage", "1Gi"))
    api_core.create_namespaced_persistent_volume_claim(namespace=NAMESPACE, body=pvc)

    # Service
    service = create_mysql_service(name)
    api_core.create_namespaced_service(namespace=NAMESPACE, body=service)

    # Deployment
    deployment = create_mysql_deployment(name, spec)
    api_apps.create_namespaced_deployment(namespace=NAMESPACE, body=deployment)

    logger.info(f"MySQL instance {name} created with PVC, Deployment, and Service.")

@kopf.on.delete('mysqls.otus.homework', 'v1')
def delete_mysql(spec, name, namespace, logger, **kwargs):
    k8s_config.load_incluster_config()
    api_apps = k8s.AppsV1Api()
    api_core = k8s.CoreV1Api()

    try:
        api_apps.delete_namespaced_deployment(name, namespace)
        api_core.delete_namespaced_service(name, namespace)
        api_core.delete_namespaced_persistent_volume_claim(name, namespace)
        logger.info(f"MySQL instance {name} and all resources deleted.")
    except k8s.rest.ApiException as e:
        logger.error(f"Error deleting MySQL {name}: {e}")
