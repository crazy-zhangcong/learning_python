#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com

from conf import settings

import pika
import json


class RpcServer:

    def __init__(self):
        self.ex_name = settings.RabbitMQ_exchange   # 服务端监听的exchange名称
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RabbitMQ_Host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.ex_name, type='fanout')  # 通过设置exchange来与队列通信
        self.recv_status = False

    def send(self, value):
        """
        给RabbitMQ中与exchange为self.value绑定的队列发送消息
        :param value: 给绑定exchange的队列发送的消息
        :return:
        """
        self.channel.basic_publish(exchange=self.ex_name, routing_key='', body=value)

    def recv(self):
        """
        从队列中获取客户端执行命令返回的结果
        :return:
        """
        self.channel.basic_consume(self.callback, queue=settings.RabbitMQ_client_queue, no_ack=True)
        while True:
            self.recv_status = False
            self.connection.process_data_events(time_limit=2)
            if not self.recv_status:  # 判断该状态是否为Flase,如果为Flase表明没用从队列中取到数据
                break

    def callback(self, ch, method, properties, recv_value):
        """
        回调函数
        :param ch:  self.channel对象
        :param method:
        :param properties:
        :param recv_value: 从队列中拿到的内容
        :return:
        """
        self.recv_status = True
        print(recv_value)


def run():
    rpcServer = RpcServer()
    while True:
        command = input("请输入客户端需要执行的指令 >>")
        send_value = json.dumps([command, settings.RabbitMQ_client_queue])
        rpcServer.send(send_value)
        rpcServer.recv()

