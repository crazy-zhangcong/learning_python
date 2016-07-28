#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com


# rabbitMQ主机ip
RabbitMQ_Host = "127.0.0.1"

# 服务端监听的exchange名称
RabbitMQ_exchange = "task"

# 客户端执行命令返回的结果将会存在该队列中
RabbitMQ_client_queue = "cmd_result"
