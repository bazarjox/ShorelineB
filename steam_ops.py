# Core
import json
import sys
import os
import pickle
# The module, that helps to interact with the steam API
import steam # Steam WebAPI
from steampy.client import SteamClient, Asset # Steam Trades API
from steampy.utils import GameOptions
import db
import requests

USER_DATA_FOLDER = 'userdata' # Folder, where store accounts secrets and saved sessions

GAME = GameOptions.CS # This bot made only for market.csgo.com
TRADEOFFER_URL = "https://steamcommunity.com/tradeoffer/new/?partner={0}&token={1}"

LOGGED = {} # Don't use this directly, use check_or_login

# Saving session for efficiency and non-detecting purposes
def _save_session(client):
	steamid = client.steam_guard['steamid']
	cookies = client._session.cookies
	path = os.path.join(USER_DATA_FOLDER, steamid + ".session")
	with open(path, "wb") as f:
		pickle.dump(cookies, f)

# Loading pickle file and create new SteamClient object and return it
def _login_from_session(steamid):
	print("Logging {0} from session file".format(db.get_account_username_by_steamid(steamid)))
	account = db.get_all_creds_by_steamid(steamid)
	path = os.path.join(USER_DATA_FOLDER, steamid + ".session")
	if not os.path.exists(path):
		return None
	sg_path = os.path.join(USER_DATA_FOLDER, steamid + ".json")
	session = requests.session()
	with open(path, 'rb') as f:
		session.cookies.update(pickle.load(f))
	client = SteamClient(account['steamapikey'], account['username'], account['password'], sg_path)
	client._session = session
	client.was_login_executed = True
	if client.is_session_alive():
		print("LOGGED FROM SESSION")
		return client

# Logging to Steam Web API and returns SteamClient instance via steampy
# ONLY FOR check_or_login FUNCTION!!! INSTEAD OF THIS USE check_or_login
def _login(steamid):
	print("Logging {0}".format(db.get_account_username_by_steamid(steamid)))

	username, password, steamapikey = db.get_login_creds_by_steamid(steamid)
	client = SteamClient(steamapikey)
	client.login(username, password, generate_path_by_steamid(steamid))
	_save_session(client)
	print("LOGGED")
	return client

# Login only with that function
def check_or_login(steamid):
	client = _login_from_session(steamid)
	if client:
		LOGGED[steamid] = client
		return LOGGED[steamid]
	if steamid in LOGGED:
		if not LOGGED[steamid].is_session_alive():
			LOGGED[steamid] = _login(steamid)
	else:
		LOGGED[steamid] = _login(steamid)
	return LOGGED[steamid]

# Generates steam64id from profile url
def steamid_from_url(url):
	return steam.steamid.steam64_from_url(url)

# Generates from maFile (SDA) new file only with shared_secret,
# identity secret and steam64id 
def generate_from_mafile(path):
	new_data = {}
	with open(path, 'r', encoding='utf-8') as f:
		data = json.loads(f.read())
		new_data['steamid'] = str(data['Session']['SteamID'])
		new_data['shared_secret'] = data['shared_secret']
		new_data['identity_secret'] = data['identity_secret']

	store_filename = os.path.join(USER_DATA_FOLDER, new_data['steamid'] + '.json')
	with open(store_filename, 'w', encoding='utf-8') as f:
		f.write(json.dumps(new_data, ensure_ascii=False, sort_keys=True, indent=4))
	return new_data

# Helper for generate path to shared_secret file by steamid
def generate_path_by_steamid(steamid):
	return os.path.join(USER_DATA_FOLDER, steamid + ".json")

# partner, token, message - are provided by tm 
# items_ids == [item_assetid1, item_assetid2, ...], same provided by tm
def make_offer(steamid, partner, token, message, items_ids):
	url = TRADEOFFER_URL.format(partner, token)
	assets = [Asset(item_id, GAME) for item_id in items_ids]
	client = check_or_login(steamid)
	tradeoffer = client.make_offer_with_url(assets, [], url, message)
	if tradeoffer.get('success'):
		return True
	else:
		return False

if __name__ == '__main__':
	# if not os.path.exists(USER_DATA_FOLDER):
	# 	os.mkdir(USER_DATA_FOLDER)
	# path = sys.argv[1]
	# generate_from_mafile(path)
	client = check_or_login("76561198983927239")
	item = 'M4A1-S | Cyrex (Factory New)'
	print(client.market.fetch_price(item, game=GameOptions.CS))