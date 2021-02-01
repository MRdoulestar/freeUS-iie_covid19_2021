import os
import requests
import json
import pickle
import datetime
from urllib.parse import quote,unquote

class IIE_COVID:
	def __init__(self, mid):
		self.mid = mid
		self.user_file = 'userinfo.pkl'
		self.users_data = ''
		self.user_data = ''
		# date
		self.today = str(datetime.date.today())
		self.yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
		# 0-9
		self.gid_range = 9

		self.url = 'http://39.102.85.186/LoisCOVID/'
		self.info_path = '/sta/list?gid='
		self.get_single_path = '/rpt/get'
		self.add_path = '/rpt/add'
		self.post_header = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36",
		    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
		}

		# Init the db
		if os.path.exists(self.user_file):
			with open(self.user_file, 'rb') as f:
				self.users_data = pickle.load(f)
		else:
			tmp_data = {}
			for gid in range(self.gid_range):
				res = requests.get(self.url + self.info_path + str(gid))
				data = json.loads(res.content)['d']
				tmp_data[str(gid)] = data
			self.users_data = tmp_data
			with open(self.user_file, 'wb') as f:
				pickle.dump(self.users_data, f)

		# Check user mid
		for gid in self.users_data.keys():
			users = self.users_data[gid]
			for user in users:
				if user['mid'] == self.mid:
					self.user_data = user
					break
		if self.user_data == '':
			print('Not find you...')
			exit(0)
		else:
			print('Find you: ' + self.user_data['mid'])
			print('Today: ' + self.today)

	# Submit daily infomation
	def submit(self):
		# Get location from yesterday data
		res = requests.get(self.url + self.get_single_path + '?uid={}&dat={}'.format(self.user_data['uid'], self.yesterday))
		res_data = json.loads(res.content)['d']
		loc = res_data['loc']
		print('Last location: ' + quote(loc))

		print('Submit start...')
		add_data = {
			'uid': self.user_data['uid'],	# uid
			'gid': self.user_data['gid'],	# gid
			'uni': 'false',	# in school?
			'con': 'true',	# in China?
			'loc': loc,	# your location
			'temp': 1,	# temperature range 2: 35-36.5
			'sit': 0,	# 0: normal
			'sym': 'false',	#
			'inf': 'false',	#
			'note': 'false',	#
			'area': 'false',	#
			'toge': 0,	# 0: normal
			'oth': '',	#
			'dat': self.today	# date
		}
		# print(add_data)
		res = requests.post(self.url + self.add_path, headers=self.post_header, data=add_data)
		res_data = json.loads(res.content)
		if res_data['r'] == 0:
			print('Sumbit Success ! :)')
		else:
			print('Sumbit Fail ! :(')
		print('Submit end...')



me = IIE_COVID('*Change your mid here*')
me.submit()