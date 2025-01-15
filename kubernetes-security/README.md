# Последовательный запуск

## В namespace homework создать service account monitoring и дать ему доступ к ÿндпоинту /metrics ваúего кластера

Создаем роль `metric`
Примените роль-binding

```
kubectl apply -f service-account-monitoring.yaml
```

## Добавить в deployment.yaml привязку с сервис аккаунту

```
      serviceAccountName: monitoring
```

## В namespace homework создатþ service account с именем cd и датþ ему ролþ admin в рамках namespace homework

```
kubectl apply -f service-account-cd.yaml
```

## Создатþ kubeconfig длā service account cd

Создаем для роли токен и получаем его
```
kubectl apply -f token-secret.yaml
kubectl -n homework get secret cd-token -o jsonpath='{.data.token}'
```

Адрес API сервера:
```
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'
```


CA сертификат (в base64):

```
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}'
```
Если пусто, тогда
1. Найти путь к сертификату
```
kubectl config view --minify
```
2. Запустить 

```power shell
[convert]::ToBase64String((Get-Content -Path "C:\Users\boris\.minikube\profiles\minikube\client.crt" -Encoding Byte)) > ca.crt.base64.txt
```

Токен ServiceAccount:

```
kubectl -n homework get secret cd-token -o jsonpath='{.data.token}'
```

Создаем cd-kubeconfig.yaml

```powershell
$env:KUBECONFIG="cd-kubeconfig.yaml"
kubectl get pods -n homework
```

Чтобы удалить конфиг
```
Remove-Item env:KUBECONFIG
```