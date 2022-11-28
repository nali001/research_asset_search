from __future__ import absolute_import
from celery import Celery
app = Celery('kagglecrawler',broker='amqp://admin:notebookcrawler2022@rabbit:5672',backend='rpc://',include=['kagglecrawler.tasks'])