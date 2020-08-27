from core.app import Crawl
import logging
import loggingConfig
from spider import *
from core.core_utils import log
from core.consistant import SPECIAL_STATUS, Framework
from ext import config
from core.exceptions import CHANGE_CHANNEL

import celery

logger = logging.getLogger(__name__)


class MyCrawl(Crawl):
    async def generate_tasks(self, task):
        result = tax_task.apply_async(args=[task], task_id=f"{task['token']}_{task['phase']}")
        f_w = self.config.TASK_FRAMEWORK
        if f_w == 'celery':
            while True:
                if result.status == 'PENDING':
                    break
        if f_w == 'rq':
            while True:
                if result.status == 'queued':
                    break


def main_task(task):
    try:
        spider = eval(task['province'])
        final_code = crawl(task, spider)
        # f"        {task['token']} finished with final_code{final_code}"
        return dict(token=task['token'], final_code=final_code)
    except NameError:
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(log(task['token'], SPECIAL_STATUS.DIY_STATUS.value, message=f'{task["province"]}尚未开发'))


crawl = MyCrawl(__name__, 'celeryconfig')
app = crawl.app

if config.TASK_FRAMEWORK == 'celery':

    @app.task()
    def tax_task(task):
        try:
            return main_task(task)
        except CHANGE_CHANNEL as e:
            tax_task.delay(e.task)


    @app.task()
    def pdf_test(task):
        print(task)
        return {'asd':'123'}


    crawl.run()

# if config.get(Framework.TASK_FRAMEWORK.value) == 'rq':
#     import os
#     import sys
#     import signal
#     import redis
#     from rq import Worker, Queue, Connection
#     from rq.decorators import job
#     from concurrent.futures import ProcessPoolExecutor
#     import multiprocessing
#
#     listen = ['yys']
#     redis_url = os.getenv('REDISTOGO_URL', crawl.app.conf.broker_read_url)
#     conn = redis.from_url(redis_url)
#
#
#     def sigint_handler(signum, frame):
#         for i in pid_list:
#             os.kill(i, signal.SIGKILL)
#         logging.info("rq exit...")
#         sys.exit()
#
#
#     def worker():
#         with Connection(conn):
#             worker = Worker(map(Queue, listen))
#             worker.work()
#
#
#     @job('yys', connection=conn, timeout=5)
#     def mobile_task(task):
#         return main_task(task)
#
#
#     pid_list = []
#     signal.signal(signal.SIGINT, sigint_handler)
#     if __name__ == '__main__':
#         pool = multiprocessing.Pool(processes=4)  # multiprocessing pool多进程池，processes=4 指定进程数
#         for i in range(3):
#             pool.apply_async(worker, )
#         pool.apply_async(crawl.run, )
#         for i in multiprocessing.active_children():
#             pid_list.append(i.pid)
#         pid_list.append(os.getpid())
#         pool.close()
#         pool.join()
