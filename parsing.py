# The module, that will parse some data from skinstable
# Parser for parser jajaja
import requests
import db
import steam_ops
import json
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# skinstable places ids CONSTANTS
MARKET = "23"
STEAMCOMMUNITY = "52"

CURRENCIES = {}

# It doesn't matter what account will used to parse data
# so we take first account of first user
DEFAULT_ACCOUNT = db.get_random_account()

# Login to skinstable by grabbing SteamClient session and posting form in OAuth. Returns session
def login_to_skinstable(steamid=DEFAULT_ACCOUNT['steamid']):
	ua = UserAgent() # Just ensuring
	ua = ua.random
	login_url = 'https://skins-table.xyz/steam/?login' # Redirecting to Steam OAuth page
	client = steam_ops.check_or_login(steamid)
	session = client._session # requests.session() with steam cookies to authenticate
	session.headers['User-Agent'] = ua
	response = session.get(login_url)
	soup = BeautifulSoup(response.text, 'html.parser')
	form = {}
	form['action'] = 'steam_openid_login'
	form['openid.mode'] = 'checkid_setup'
	form['openidparams'] = soup.find('input', {'name': 'openidparams'}).get('value')
	form['nonce'] = soup.find('input', {'name': 'nonce'}).get('value')
	session.post('https://steamcommunity.com/openid/login', form)
	return session

# Scrape global variables from skins-table.xyz/table, returns dict with vars like link_config, discount_config etc.
def scrape_global_variables(html):
	list_of_vars = ['link_config', 'discount_config', 'commission_config', 'opskins_sales',
		'bitskins_sales', 'steam_sales', 'market_sales', 'item_names']
	soup = BeautifulSoup(html, 'html.parser')
	variables = str(soup.script).replace('<script>', '').replace('</script>',
		'').replace('        ', '').replace('\n', '').split(';')
	# Last variable is empty string
	if variables[-1].replace(' ', '') == "":
		variables.pop()
	variables_dict = {}
	for var_str in variables:
		for var in list_of_vars:
			if var in var_str:
				var_str = var_str.replace("var {0} = ".format(var), '')
				variables_dict.update({var: json.loads(var_str)})
	# item_names variable format is "item_id": ["Glock-19"], I turn it into "item_id": "Glock-19"
	item_names = {}
	for item_id in variables_dict['item_names'].keys():
		item_names.update({item_id: variables_dict['item_names'][item_id][0]})
	variables_dict['item_names']['item_names'] = item_names
	return variables_dict

# Skins-table doesn't provide data as is, we need to rebuild it according on common.js file
def rebuild_ajax(global_variables, ajax_data, first=STEAMCOMMUNITY, second=MARKET):
	print("Rebuilding AJAX...")
	global CURRENCIES
	CURRENCIES = ajax_data[2]
	# Setup global variables
	item_names = global_variables['item_names']
	steam_sales = global_variables['steam_sales']
	market_sales = global_variables.get('market_sales')
	link_config = global_variables['link_config']
	discount_config = global_variables['discount_config']
	commission_config = global_variables['commission_config']
	price_rub = [23,24,62,84,94,137,148,151]
	price_eur = [27,74,153,154]
	price_cny = [29,31,140,158,159]
	price_steam = [52,53]
	csgotm = [23, 24]
	game_id = 1
	dif1 = commission_config[str(second)]
	dif2 = commission_config[str(first)]

	item_list_data = []
	for item_id in ajax_data[0]:
		if item_id in item_names:
			value = ajax_data[0][item_id]
			item = {}
			item['i'] = item_names[item_id][0]
			item['id'] = item_id
			# Last sales
			item["c7_sc"] = 0
			if item_id in steam_sales:
				item["c7_sc"] = steam_sales[item_id][0]
			item['c7_tm'] = 0
			if item_id in market_sales:
				item['c7_tm'] = market_sales[item_id][0]
			# Price
			item['p1'] = None
			if value[0]:
				item['p1'] = value[0] / 100
			item['b1'] = {}
			# Quantity
			item['c1'] = 0
			if value[1]:
				values = value[1].split(',')
				for value1 in values:
					bot = value1.split(':')
					bot[1] = int(bot[1])
					item['b1'][bot[0]] = bot[1]
					item['c1'] += bot[1]
			item['d1'] = None
			if value[2]:
				item['d1'] = datetime.fromtimestamp(value[2])
				# item['d1'] = value[2]
			# Second
			if ajax_data[1] and item_id in ajax_data[1]:
				item['p2'] = None
				if ajax_data[1][item_id]:
					item['p2'] = ajax_data[1][item_id][0] / 100
					# Quantity
					item['b2'] = {}
					item['c2'] = 0
					if ajax_data[1][item_id][1]:
						values = ajax_data[1][item_id][1].split(',')
						for value1 in values:
							bot = value1.split(':')
							bot[1] = int(bot[1])
							item['b2'][bot[0]] = bot[1]
							item['c2'] += bot[1]
					item['d2'] = None
					if ajax_data[1][item_id][2]:
						item['d2'] = datetime.fromtimestamp(ajax_data[1][item_id][2])
						# item['d2'] = ajax_data[1][item_id][2]
			else:
				item['p2'] = 0
				item['b2'] = 0
				item['c2'] = 0
				item['d2'] = None
			item_list_data.append(item)

	new_item_list = []
	for item in item_list_data:
		if item['p2']:
			price1 = 0
			price2 = 0
			if first in price_rub:
				price1 = round(item['p1'] * 100 / CURRENCIES['USD'])
			elif first in price_eur:
				price1 = round(item['p1'] * 100 * CURRENCIES['EUR'] / CURRENCIES['USD'])
			elif first in price_cny:
				price1 = round(item['p1'] * 100 / CURRENCIES['CNY'])
			else:
				price1 = round(item['p1'] * 100)

			if second in price_rub:
				price2 = round(item['p2'] * 100 / CURRENCIES['USD'])
			elif second in price_eur:
				price2 = round(item['p2'] * 100 * CURRENCIES['EUR'] / CURRENCIES['USD'])
			elif second in price_cny:
				price2 = round(item['p2'] * 100 / CURRENCIES['CNY'])
			else:
				price2 = round(item['p2'] * 100)

			price1_1 = price1
			price2_2 = price2

			if first in csgotm and discount_config['csgotm']:
				price1_1 = round(price1 * (1 - discount_config['csgotm'] / 100) * 100) / 100
			if second in csgotm and discount_config['csgotm']:
				price2_2 = round(price2 * (1 - discount_config['csgotm'] / 100) * 100) / 100

			# Rent formule
			if link_config['nf'] or price2 > 2 * price1 or price1 > price2 * 2:
				item['r1'] = round(((1 - dif1 / 100) * price2 - price1_1) / max(price1_1, (1 - dif1 / 100) * price2) * 10000) / 100
				item['r2'] = round(((1 - dif2 / 100) * price1 - price2_2) / max((1 - dif2 / 100) * price1, price2_2) * 10000) / 100
			else:
				item['r1'] = round(((1 - dif1 / 100) * price2) / price1_1 * 10000 - 10000) / 100
				item['r2'] = round(((1 - dif2 / 100) * price1) / price2_2 * 10000 - 10000) / 100
		else:
			item['r1'] = -9999
			item['r2'] = -9999
		new_item_list.append(item)
	new_item_list.sort(key=lambda x: x['i']) # Sort by name
	return new_item_list

# Filtering by quantity, price etc.
def filtering_data(ajax_data, filters=None, first=STEAMCOMMUNITY, second=MARKET):
	print("Filtering data..")
	# "Global vars"
	price_rub = [23,24,62,84,94,137,148,151]
	price_eur = [27,74,153,154]
	price_cny = [29,31,140,158,159]
	price_steam = [52,53]
	default_filters = {
		"name": None,
		"price1_from": None,
		"price1_to": None,
		"price2_from": None,
		"price2_to": None,
		"time1": 360,
		"time2": 360,
		"n1": 1,
		"n2": 1,
		"n_1": None,
		"n_2": None,
		"per1_from": None,
		"per1_to": None,
		"per2_from": None,
		"per2_to": None,
		"tm1": 0,
		"sc1": 0,
		"stattrak": True,
		"stikers": True,
		"souvenir": True,
		"black_list": []
	}

	if filters:
		default_filters.update(filters)
	filters = default_filters

	if not filters['stattrak']:
		ajax_data = list(filter(lambda x: 'StatTrak' not in x['i'], ajax_data))

	if not filters['stikers']:
		ajax_data = list(filter(lambda x: 'Sticker' not in x['i'], ajax_data))

	if not filters['souvenir']:
		ajax_data = list(filter(lambda x: 'Souvenir' not in x['i'], ajax_data))

	if filters['n1']:
		ajax_data = list(filter(lambda x: x['c1'] >= filters['n1'], ajax_data))

	if filters['n2']:
		ajax_data = list(filter(lambda x: x['c2'] >= filters['n2'], ajax_data))

	if filters['n_1']:
		ajax_data = list(filter(lambda x: x['c1'] <= filters['n_1'], ajax_data))

	if filters['n_2']:
		ajax_data = list(filter(lambda x: x['c2'] <= filters['n_2'], ajax_data))

	def price1_from(x):
		p = None
		if first in price_rub:
			p = x['p1'] / CURRENCIES['USD']
		elif first in price_eur:
			p = x['p1'] * CURRENCIES['EUR'] / CURRENCIES['USD']
		elif first in price_cny:
			p = x['p1'] / CURRENCIES['CNY']
		else:
			p = x['p1']
		return p >= filters['price1_from']

	if filters['price1_from']:
		ajax_data = list(filter(price1_from, ajax_data))

	def price2_from(x):
		p = None
		if first in price_rub:
			p = x['p2'] / CURRENCIES['USD']
		elif first in price_eur:
			p = x['p2'] * CURRENCIES['EUR'] / CURRENCIES['USD']
		elif first in price_cny:
			p = x['p2'] / CURRENCIES['CNY']
		else:
			p = x['p2']
		return p >= filters['price2_from']

	if filters['price2_from']:
		ajax_data = list(filter(price2_from, ajax_data))

	def price1_to(x):
		p = None
		if first in price_rub:
			p = x['p1'] / CURRENCIES['USD']
		elif first in price_eur:
			p = x['p1'] * CURRENCIES['EUR'] / CURRENCIES['USD']
		elif first in price_cny:
			p = x['p1'] / CURRENCIES['CNY']
		else:
			p = x['p1']
		return p <= filters['price1_to']

	if filters['price1_to']:
		ajax_data = list(filter(price1_to, ajax_data))

	def price2_to(x):
		p = None
		if first in price_rub:
			p = x['p2'] / CURRENCIES['USD']
		elif first in price_eur:
			p = x['p2'] * CURRENCIES['EUR'] / CURRENCIES['USD']
		elif first in price_cny:
			p = x['p2'] / CURRENCIES['CNY']
		else:
			p = x['p2']
		return p <= filters['price2_to']

	if filters['price2_to']:
		ajax_data = list(filter(price1_to, ajax_data))

	if filters['per1_from']:
		ajax_data = list(filter(lambda x: x['r1'] >= filters['per1_from']))

	if filters['per2_from']:
		ajax_data = list(filter(lambda x: x['r2'] >= filters['per2_from']))

	if filters['per1_to']:
		ajax_data = list(filter(lambda x: x['r1'] <= filters['per1_to']))

	if filters['per2_to']:
		ajax_data = list(filter(lambda x: x['r2'] >= filters['per2_to']))

	if filters['name']:
		ajax_data = list(filter(lambda x: filters['name'].lower() in x['i'].lower()))

	def time1(x):
		if not x['d1']:
			return True
		diff = datetime.now() - x['d1']
		return diff.microseconds / 1000 / 60 <= filters['time1']
	if filters['time1'] and first != 28 and first != 95:
		ajax_data = list(filter(time1, ajax_data))

	def time2(x):
		if not x['d2']:
			return True
		diff = datetime.now() - x['d2']
		return diff.microseconds / 1000 / 60 <= filters['time2']
	if filters['time2'] and second != 28 and second != 95:
		ajax_data = list(filter(time2, ajax_data))

	if filters['sc1']:
		ajax_data = list(filter(lambda x: x['c7_sc'] >= filters['sc1'], ajax_data))

	if filters['tm1']:
		ajax_data = list(filter(lambda x: x['c7_tm'] >= filters['tm1'], ajax_data))

	def black_list(x):
		for stopword in filters['black_list']:
			if stopword.lower() in x['i'].lower():
				return False
		return True

	if filters['black_list']:
		ajax_data = list(filter(black_list, ajax_data))

	# Sorting by revenue
	ajax_data.sort(key=lambda x: x['r1'], reverse=True)

	return ajax_data

# Requires logged in skinstable session, returns filtered data
# Filters are appending to default filters
def get_data(session, filters=None, first=STEAMCOMMUNITY, second=MARKET):
	table_url = "https://skins-table.xyz/table"
	data_url = "https://skins-table.xyz/table/ajax.php"
	# Setup cookies to filter data (WIP)
	session.cookies.set("first", first)
	session.cookies.set("second", second)
	for filter_ in filters:
		session.cookies.set(filter_, str(filters[filter_]))

	# Get variables
	response = session.get(table_url)
	global_variables = scrape_global_variables(response.text)

	response = session.post(data_url, {"site1": first, "site2": second})
	ajax_data = response.json()

	first = int(first)
	second = int(second)
	ajax_data = rebuild_ajax(global_variables, ajax_data, first, second)
	filtered_data = filtering_data(ajax_data, filters, first, second)

	return filtered_data

# Generates human-readable JSON file
def human_view(data, first=STEAMCOMMUNITY, second=MARKET):
	new_list = []
	for item in data:
		if first == MARKET:
			p1 = item['p1']	* CURRENCIES['USD']
			p2 = item['p2'] 
		else:
			p1 = item['p1']
			p2 = item['p2'] * CURRENCIES['USD']
		new_list.append({
			"id": item['id'],
			"name": item['i'],
			"price1": p1,
			"price2": p2,
			"rent1": item['r1'],
			"rent2": item['r2'],
			"date1": item['d1'],
			"date2": item['d2'],
			"quantity1": item['c1'],
			"quantity2": item['c2'],
			"sold_steam": item['c7_sc'],
			"sold_tm": item['c7_tm'],
			})
	return new_list

if __name__ == '__main__':
	session = login_to_skinstable()
	data = get_data(session, filters={"black_list": ["Graffiti"], "price1_from": 5.5}, first=MARKET, second=STEAMCOMMUNITY)
	data = human_view(data)
	with open('dump.json', 'w', encoding='utf-8-sig') as f:
		f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, default=str))
