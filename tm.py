# The module, that help us to interact with csgo.market.com API
import requests

API_URL = "https://market.csgo.com/api/v2/"

# Basic request return None or dict (parsed json)
def request(url, params=None):
	r = requests.get(url, params=params)
	if not r.ok:
		print("Problems with connection")
		return None
	return r.json()

# ONLINE AND OFFLINE
def online(api_key):
	return request(API_URL + "ping", {"key": api_key})

def offline(api_key):
	return request(API_URL + "go-offline", {"key": api_key})

# UPDATE INVENTORY AFTER EVERY TRADEOFFER
def update(api_key):
	r = request(API_URL + "update-inventory/", {"key": api_key})
	if r['success']:
		return True
	return False

# TESTING ALL INDICATORS
def test(api_key):
	r = request(API_URL + "test", {"key": api_key})
	if r['success']:
		return r['status']
	return r.get('error')

# Returns item ids too
def my_inventory(api_key):
	r = request(API_URL + "my-inventory/", {"key": api_key})
	if r['success']:
		return r['items']
	return r.get('error')

# item ids obtained by my_inventory function, price in roubles (float or int). ROUBLES
def add_to_sale(api_key, item_id, price):
	r = request(API_URL + "add-to-sale", {"key": api_key,
		"id": item_id, "price": price * 100, "currency": "RUB"})
	if r['success']:
		return r['item_id']
	return r['error']

def set_price(api_key, item_id, price):
	return request(API_URL + "set-price", {"key": api_key,
		"item_id": item_id, "price": price * 100, "currency": "RUB"})

def remove_all_from_sale(api_key):
	return request(API_URL + "remove-all-from-sale", {"key": api_key})

# Outcome and income tradeoffers requests
def trades(api_key):
	r = request(API_URL + "trades/", {"key": api_key})
	if r['success']:
		return r['trades']
	return r['error']

# Balance
def get_money(api_key):
	return request(API_URL + "get-money", {"key": api_key})

# SEARCH
def search_item_by_hash_name(api_key, market_hash_name):
	r = request(API_URL + "search-item-by-hash-name", {"key": api_key, "hash_name": market_hash_name})
	if r['success']:
		return r['list']
	return None

if __name__ == "__main__":
	api_key = "rDXV18zV8Y00xkN9L6591r39c4zlF20"
	print(test(api_key))