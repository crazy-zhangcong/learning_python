#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com

from conf import settings

import pika
import json
import subprocess


class RpcClient:

    def __init__(self):
        self.ex_name = settings.RabbitMQ_exchange   # 需要将自己的队列绑定到这个exchange的名称上
        self.send_queue = ''  # 给服务器返回的数据写入到这个队列中,该队列名服务端会发送到队列中
        self.command = ''   # 从队列中获取到服务器发送到队列的指令
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RabbitMQ_Host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.ex_name, type='fanout')  # 通过设置exchange来与队列通信

        # 创建随机queue
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue

        # 将随机生成的queue与exchange名为self.ex_name进行绑定
        self.channel.queue_bind(exchange=self.ex_name, queue=self.queue_name)

    def callback(self, ch, method, properties, recv_value):
        """
        回调函数
        :param ch:  self.channel对象
        :param method:
        :param properties:
        :param recv_value: 从队列中拿到的内容
        :return:
        """
        recv_value = str(recv_value, encoding="utf-8")
        recv_value = json.loads(recv_value)
        self.command, self.send_queue = recv_value

        self.ExecuteCommand()

    def recv(self):
        """
        给RabbitMQ中与exchange为self.value绑定的队列发送消息
        :return:
        """
        self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()

    def send(self, send_value):
        print("发送数据", send_value)
        self.channel.queue_declare(queue=self.send_queue)
        self.channel.basic_publish(exchange='', routing_key=self.send_queue, body=send_value)  # 给队列发送消息

    def ExecuteCommand(self):
        """
        使用subprocess执行command系统命令
        """
        obj = subprocess.Popen(self.command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = obj.stdout.read()  # 正确的输出
        err = obj.stderr.read()  # 错误的输出

        if out:  # 命令执行正确的输出有值
            send_value = out
        else:  # 命令执行错误的输出有值
            send_value = err

        self.send(send_value)


def run():
    rpcClient = RpcClient()
    rpcClient.recv()    # 从队列中获取数据




