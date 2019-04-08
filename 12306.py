#!/usr/bin/python
#-*- coding:utf-8 -*-
import requests
import json
import sys
from prettytable import PrettyTable

reload(sys)
sys.setdefaultencoding('utf8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}

def Get_stations():
	global stations
	urlPre = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9047'
	placetext = requests.get(url=urlPre, headers=headers).text
	placelist = placetext.split('=')
	statext = placelist[1][1:-2]
	stationlist = statext.split('@')
	stationlist.pop(0)

	final = {}
	for i in xrange(0, len(stationlist)):
		tmp = stationlist[i].split('|')
		final[tmp[1]] = tmp[2]
	return final

def Get_train_text():
	global stations 
	try:
		from_station = stations.get(sys.argv[1].decode(sys.stdin.encoding))
		to_station = stations.get(sys.argv[2].decode(sys.stdin.encoding))
		date = sys.argv[3]
	except:
		#from_station = stations.get(u'西安北')
		from_station = stations.get(raw_input("请输入出发站: ").decode(sys.stdin.encoding))
		to_station = stations.get(raw_input("请输入终点站: ").decode(sys.stdin.encoding))
		date = raw_input("请输入出发日期: ")

	url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
			'leftTicketDTO.train_date={}&'
			'leftTicketDTO.from_station={}&'
			'leftTicketDTO.to_station={}&'
			'purpose_codes=ADULT').format(date, from_station, to_station)

	r = requests.get(url=url, headers=headers)
	trains_text = r.json()['data']['result']
	return trains_text

def Get_train_infomation():
	key_list = []
	value_list = []
	table = PrettyTable()
	table._set_field_names('车次 出发地点 到达地点 出发时间 到达时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split())
	for key, value in stations.iteritems():
		key_list.append(key)
		value_list.append(value)
	for raw_train in Get_train_text():
		data_list = raw_train.split('|')
		train_number = data_list[3]
		from_station_code = data_list[6]
		to_station_code = data_list[7]
		from_station_index = value_list.index(from_station_code)
		to_station_index = value_list.index(to_station_code)
		from_station_name = key_list[from_station_index]
		to_station_name = key_list[to_station_index]

		start_time = data_list[8]
		arrive_time = data_list[9]
		time_duration = data_list[10]
		first_class_seat = data_list[31]
		second_class_seat = data_list[30]
		soft_sleeper = data_list[23] or '--'
		hard_sleeper = data_list[28] or '--'
		hard_seat = data_list[29] or '--'
		no_seat = data_list[26] or '--'

		table.add_row([
			train_number,
			from_station_name, 
			to_station_name,
			start_time, 
			arrive_time,
			time_duration,
			first_class_seat,
			second_class_seat,
			soft_sleeper,
			hard_sleeper,
			hard_seat,
			no_seat
			])

	print table

if __name__ == '__main__':
	stations = Get_stations()
	Get_train_infomation()
