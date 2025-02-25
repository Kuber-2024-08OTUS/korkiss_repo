# Создадим Dockerfile для кастомного Nginx

```
FROM nginx:latest

RUN apt update && apt install -y curl && \
    echo "server { \
        listen 8080; \
        location /metrics { \
            stub_status; \
        } \
    }" > /etc/nginx/conf.d/metrics.conf

CMD ["nginx", "-g", "daemon off;"]
```

# Соберем образ и загрузим в Docker Hub

docker build -t shutovba/nginx-metrics .
docker push shutovba/nginx-metrics

# Установка Prometheus Operator

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```


Проверим, что всё работает

```
kubectl get pods -n monitoring

```

# Создание Deployment и Service для Nginx

nginx-deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-metrics
  labels:
    app: nginx-metrics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-metrics
  template:
    metadata:
      labels:
        app: nginx-metrics
    spec:
      containers:
      - name: nginx
        image: shutovba/nginx-metrics
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-metrics
  labels:
    app: nginx-metrics
spec:
  selector:
    app: nginx-metrics
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

Применим
`kubectl apply -f nginx-deployment.yaml`

# Настройка ServiceMonitor

nginx-service-monitor.yaml

```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: nginx-metrics-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: nginx-exporter
  endpoints:
    - port: "9113"
      interval: 10s

```

`kubectl apply -f nginx-service-monitor.yaml`

Найдите Prometheus-сервис

`kubectl get svc -n monitoring`

# Проверка

Откройте в браузере Prometheus Web UI (/targets) и убедитесь, что nginx-exporter отображается.






