## Requirements
* Python 3.6
* aioredis
* aiomongodel
* motor
* aiohttp
* aiojobs
* aioprometheusGetBill

## version
* dqg-tax_crawl-v14[prod]
* dqg-tax_crawl_test-v4[test]

## Deploy
   * celery -A tasks worker -Q tax:linux --loglevel=debug
   * with docker
     * docker-compose up （cluster deploy: docker-compose scale worker=n）

## Prometheus
celery-prometheus-exporter --broker redis://127.0.0.1:6379/0 --transport-options '{"master_name": "redis://127.0.0.1:6379/0"}' --enable-events


## Terminate
pkill -9 -f 'celery -A tasks worker -Q tax:linux'




