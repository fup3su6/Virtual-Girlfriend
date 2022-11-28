#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import requests
import configparser
import json
import logging
import time
from hashlib import md5
import random
'''param'''
try:
    import xml.etree.cElementTree as ET
except ImpotError:
    import xml.etree.ElementTree as ET

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def monoNum():
	final_news = ""
	for n in range (3):
		con = requests.get('https://news.ltn.com.tw/rss/entertainment.xml')
		tree = ET.fromstring(con.text)
		items = list(tree.iter(tag='item'))
		title = items[n][0].text
		ptext = items[n][1].text
		link_text = items[n][2].text
		date_text = items[n][3].text
		ptext = ptext.replace('<description>','').replace('</description','\n')
		final_news += title+ptext+"\n\n"+link_text+"\n\n"+date_text+"\n\n"
	return final_news

def monoWea(chk):
	final_wea = ""
	con = requests.get('https://www.cwb.gov.tw/rss/forecast/36_05.xml')
	con.encoding='utf-8'
	tree = ET.fromstring(con.text)
	items = list(tree.iter(tag='item'))
	title = items[chk][1].text
	ptext = items[chk][3].text
	ptext = ptext.replace('<description>','').replace('<br>','').replace('<BR>','').replace('</description','\n')
	final_wea = title+"\n"+ptext+"\n\n"
	return final_wea
	
def monoMus(chk2):
	songTitle=[["Eric周興哲《怎麼了》-｜YouTube FanFest 2020｜","https://www.youtube.com/watch?v=i4LdeOdTxpY"],
				["Eric周興哲《我很快樂 I'm Happy》Official Music Video","https://www.youtube.com/watch?v=Ezd_DLawfHI"],
				["Eric周興哲《In the Works》Official Music Video","https://www.youtube.com/watch?v=vtVWs2npVAs"],
				["Eric周興哲《相信愛 Always Believe in Love》MV Teaser","https://www.youtube.com/watch?v=lZeuJTv-3fI"],
				["Eric周興哲《其實你並沒那麼孤單 You Are Not Alone》Official Music Video","https://www.youtube.com/watch?v=YB6g7HtJmvY"]]
	ptext = "推薦你這首歌陪你度過寂靜的時光：" + songTitle[chk2][0] +"\n" +songTitle[chk2][1]
	return ptext
	
def monoMov(chk3):
	movTitle=['空中謎航(2D)','拆彈專家2(2D)','水漾的女人(2D)','靈魂急轉彎','真愛鄰距離','腿(2D)','神力女超人1984','魔物獵人(2D)']
	ptext = "我想看" + movTitle[chk3] +" 霸脫~~"
	return ptext

'''param'''
config = configparser.ConfigParser()
config.read('config.ini')
logger = logging.getLogger(__name__)
class NliStatusError(Exception):
    """The NLI result status is not 'ok'"""
class Olami:
	URL = 'https://tw.olami.ai/cloudservice/api'
	def __init__(self, app_key="832879bd6a33499fa9103d9809d2af19", app_secret="e86a40ce206d4c3799483d5fefe94b17", input_type=1):
			self.app_key = app_key
			self.app_secret = app_secret
			self.input_type = input_type
	def nli(self, text, cusid=None):
			response = requests.post(self.URL, params=self._gen_parameters('nli', text, cusid))
			response.raise_for_status()
			response_json = response.json()
			if response_json['status'] != 'ok':
				raise NliStatusError("NLI responded status != 'ok': {}".format(response_json['status']))
			else:
				nli_obj = response_json['data']['nli'][0]
				return self.intent_detection(nli_obj)
	def _gen_parameters(self, api, text, cusid):
			timestamp_ms = (int(time.time() * 1000))
			params = {'appkey': self.app_key,
					  'api': api,
					  'timestamp': timestamp_ms,
					  'sign': self._gen_sign(api, timestamp_ms),
					  'rq': self._gen_rq(text)}
			if cusid is not None:
				params.update(cusid=cusid)
			return params
	def _gen_sign(self, api, timestamp_ms):
			data = self.app_secret + 'api=' + api + 'appkey=' + self.app_key + 'timestamp=' +                str(timestamp_ms) + self.app_secret
			return md5(data.encode('ascii')).hexdigest()
	def _gen_rq(self, text):
			obj = {'data_type': 'stt', 'data': {'input_type': self.input_type, 'text': text}}
			return json.dumps(obj)
	def intent_detection(self, nli_obj):
		def handle_selection_type(type):
			if type == 'poem':
				return desc['result'] + '\n\n' + '\n'.join(
					str(index + 1) + '. ' + el['poem_name'] + '，作者：' + el['author'] for index, el in enumerate(data))
			elif type == 'cooking':
				return desc['result'] + '\n\n' + '\n'.join(
					str(index + 1) + '. ' + el['name'] for index, el in enumerate(data))
			else:
				return '對不起，你說的我還不懂，能換個說法嗎？'

		type = nli_obj['type']
		desc = nli_obj['desc_obj']
		data = nli_obj.get('data_obj', [])
		semantic_ = nli_obj.get('semantic',[])
		
		if type == 'kkbox':
			id = data[0]['id']
			return ('https://widget.kkbox.com/v1/?type=song&id=' + id) if len(data) > 0 else desc['result']
		elif type == 'weather':
			slots_ = semantic_[0]['slots']
			value = slots_[0]['value']
			if (value == "一週" or value == "一周"):
				return monoWea(1)
			else:
				return monoWea(0)
		elif type == 'music':
			chk2 = random.randint(0,5)
			return monoMus(chk2)
		elif type == 'news':
			return monoNum()
		elif type == 'movie':
			chk3 = random.randint(0,8)
			return monoMov(chk3)
		elif type == 'selection':
			return handle_selection_type(desc['type'])
		elif type == 'shut':
			return ''
		elif type == 'ds':
			return desc['result'] + '\n 輸入"功能表"可以告訴你小優可以做到的事哦~'
		else:
			return desc['result']