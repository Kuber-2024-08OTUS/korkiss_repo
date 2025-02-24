FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install kopf kubernetes pyyaml
CMD ["kopf", "run", "--verbose", "mysql-operator.py"]
