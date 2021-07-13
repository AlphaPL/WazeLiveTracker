

import json
import requests
import pgeocode
import datetime
import os

BOT_API_KEY = os.environ['BOT_API_KEY']
CHAT_ID = os.environ['CHAT_ID']

def telegram_bot_sendtext(bot_message):
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/' + BOT_API_KEY+'/sendMessage?chat_id=' + CHAT_ID +'&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()

events = []
print('Starting scrape!')
while True:
	for zip_code in open('postcodes.csv').readlines():
		try:
			zip_code = zip_code.strip()
			print('Fetching coordinates of ', zip_code)
			if len(zip_code) > 0:
				nomi = pgeocode.Nominatim('au')
				resp = nomi.query_postal_code(zip_code)
				print(zip_code, 'is located ing lat:%s, long: %s' % (resp['latitude'], resp['longitude']))


				headers = {
				    'authority': 'www.waze.com',
				    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				    'dnt': '1',
				    'sec-ch-ua-mobile': '?0',
				    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
				    'accept': '*/*',
				    'sec-fetch-site': 'same-origin',
				    'sec-fetch-mode': 'cors',
				    'sec-fetch-dest': 'empty',
				    'referer': 'https://www.waze.com/pl/live-map',
				    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
				    '$cookie': '_ga=GA1.2.1067729638.1624428090; _web_visitorid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMTM4N2M2ZDAtN2Y4ZC00OGI0LWE0ZDEtZGQwNGNkMjdlZTM4IiwiaWF0IjoxNjI0NDI4MDkwfQ.PTYW5dmkPEUQ8qb7Pd5TEVxciUZ6fTLpq_JPJG5VWQ8; _gcl_au=1.1.19070213.1625502943; _gaexp=GAX1.2.npw3GmbPQa6wOcNOpygvlQ.18829.1\\u0021TzlpaauERsm2n9EhgeG-kA.18902.0; _gid=GA1.2.1262733924.1625623730; _csrf_token=mSaBzc0b3qj1SzYrfahDqi3oqT5wa60nZMTm_AtKizU; _web_session=cGQ1b0U2UDNPQ1hETmJhQnZHREtZUmlzcWlORDZESWZlOWl0TFQ1RmYxSVVwVzNMem5VK2dacDZPMnBkems4dG9TcXlXVG9naWNPQUF4WGUrdlAwSnBaeXNmdGVlbU5sZG9ZcEQ4WG45NDA9LS1MNGVSbjkweUlMYWhHU0hwQWdqblVBPT0%3D--fa2e9142fcec1e70e12d51b2a96f4868510ac054; _gat_UA-6698700-1=1',
				}
				params = (
				    ('bottom', resp['latitude']-1),
				    ('left', resp['longitude']-1),
				    ('ma', '200'),
				    ('mj', '100'),
				    ('mu', '20'),
				    ('right', resp['longitude'] + 1),
				    ('top', resp['latitude'] + 1),
				    ('types', 'alerts,traffic,users'),
				)
				print('Getting waze events for window:', resp['latitude']-0.1, resp['longitude']-0.1, resp['latitude'] + 0.1, resp['longitude'] + 0.1)
				response = requests.get('https://www.waze.com/row-rtserver/web/TGeoRSS', headers=headers, params=params).json()
				#NB. Original query string below. It seems impossible to parse and
				#reproduce query strings 100% accurately so the one below is given
				#in case the reproduced version is not "correct".
				# response = requests.get('https://www.waze.com/row-rtserver/web/TGeoRSS?bottom=-31.975502766805263&left=115.82096958160402&ma=200&mj=100&mu=20&right=115.87133502960205&top=-31.896399239662113&types=alerts%2Ctraffic%2Cusers', headers=headers)
				alerts = response['alerts']
				for i in alerts:
					print(zip_code, i['type'], str(datetime.datetime.fromtimestamp(i['pubMillis']/1000.0)), 'Accident?', 'ACCIDENT' in str(i['type']))
					if('ACCIDENT' in str(i['type'])):
						print(i)
						street = i['street'] if 'street' in i else 'latitude %s longitude %s' % (i['location']['x'], i['location']['y'])
						event = " ".join([i['type'], street, 'https://www.waze.com/pl/live-map/directions?to=' + str(i['location']['y']) + '%2C'+ str(i['location']['x'])])
						if event not in events:
							print('Found event', event, 'sending it to telegram')
							print('Response from telegram:',telegram_bot_sendtext(event))
							events = events[:99]
							events = events + [event]
		except KeyboardInterrupt as e:
			raise e
		except Exception as e:
			print(e)


