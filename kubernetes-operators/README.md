# Собираем образ приложения с оператором

docker build -t shutovba/mysql-operator:1.0.0 .
docker push shutovba/mysql-operator:1.0.0 .


# MySQL Operator Helm Chart

## Установка
helm install mysql-operator ./mysql-operator


# Проверка создания CRD: Убедитесь, что CRD был создан

kubectl get crd mysqls.otus.homework

kubectl get pods
kubectl get deployments
kubectl get services
kubectl get persistentvolumes
kubectl get persistentvolumeclaims

# Удаление

helm uninstall mysql-operator
