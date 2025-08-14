
set -e
service=$1
if [ "$service" = "main" ]; then
    gunicorn main.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
elif [ "$service" = "service" ]; then
    gunicorn service.main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:9000
else
    echo "Unknown service: $service"
    exit 1
fi

