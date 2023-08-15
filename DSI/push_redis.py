import redis
import requests
import os
import json


def push_json_to_redis(json_path, data_key, host, port, db):
	'''
	测试用，把本地json推送到服务器上redis中
	:param json_path:
	:param data_key:
	:param host:
	:param port:
	:param db:
	:return:
	'''
	r = redis.StrictRedis(host=host, port=port, db=db)
	with open(json_path, 'r', encoding='utf-8') as f:
		json_str = f.read()

	# r.set(data_key, json_str)
	r.rpush(data_key, json_str)


if __name__ == '__main__':
	print("--------push data to redis...")
	# 设置参数信息
	json_dir = "json/"
	data_key = "data_test"
	host = "192.168.25.27"
	port = 6379
	db = 15

	# 遍历目录下的json文件
	file_list = os.listdir(json_dir)
	json_file_list = [f for f in file_list if f.endswith('.json')]

	# push data
	for i in json_file_list:
		json_path = json_dir + i
		push_json_to_redis(json_path, data_key, host, port, db)
		print("push {} success!".format(json_path))

