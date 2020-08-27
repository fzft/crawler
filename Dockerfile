FROM registry.cn-shanghai.aliyuncs.com/dqg/tax:crawl-3.7alpine-base-v5


COPY . /app
WORKDIR /app

CMD  celery -A tasks worker -Q tax:linux --loglevel=info --autoscale=64,4