FROM nginx:latest

RUN apt update && apt install -y curl && \
    echo "server { \
        listen 8080; \
        location /metrics { \
            stub_status; \
        } \
    }" > /etc/nginx/conf.d/metrics.conf

CMD ["nginx", "-g", "daemon off;"]
