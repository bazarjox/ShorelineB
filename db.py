import sys
import sqlite3
import random

conn = sqlite3.connect("database.db", isolation_level=None)
cur = conn.cursor()

# User, he has api key of TM, and can have only one steam_accounts (or not?)
cur.execute("""CREATE TABLE IF NOT EXISTS users
	(id INTEGER PRIMARY KEY AUTOINCREMENT, 
	username varchar, 
	password varchar
	);
	""")

# Steam Account (P.S. One user can have multiple accounts)
cur.execute("""CREATE TABLE IF NOT EXISTS accounts
	(id INTEGER primary key AUTOINCREMENT,
	username varchar,
	password varchar,
	steamid varchar,
	steamapikey varchar,
	tmapikey varchar,
	user_id int,
	FOREIGN KEY(user_id) REFERENCES users(id)
	);
	""")

# Item
cur.execute("""CREATE TABLE IF NOT EXISTS items
	(id INTEGER PRIMARY KEY AUTOINCREMENT,
	date_of_sell timestamp,
	asset_id varchar,
	market_hash_name varchar,
	buy_price REAL,
	prediction_price REAL,
	sold_price REAL,
	account_id INTEGER,
	FOREIGN KEY(account_id) REFERENCES accounts(id)
	);
	""")
#
# User ops
#

def create_user(username, password):
	cur.execute("INSERT INTO users (username, password) VALUES (?,?);", (username, password))

def get_all_users():
	cur.execute("SELECT * FROM users;")
	return cur.fetchall()

def get_user_by_id(user_id):
	cur.execute("SELECT * FROM users WHERE (id=?);", (user_id, ))
	user = cur.fetchall()
	if user:
		id_, username, password = user[0]
		return id_, username, password
	return None

def get_username_by_id(user_id):
	id_, username, password = get_user_by_id(user_id)
	return username

#
# Account ops
#

# creds == {"username", "password", "steamid", "steamapikey", "tmapikey", "user_id"}
def create_account(creds):
	cur.execute("""INSERT INTO accounts 
		(username, password, steamid, steamapikey, tmapikey, user_id) 
		VALUES (?, ?, ?, ?, ?, ?);""", (creds['username'], creds['password'], creds['steamid'],
			creds['steamapikey'], creds['tmapikey'], creds['user_id']))

def get_all_creds_by_steamid(steamid):
	cur.execute("SELECT * FROM accounts WHERE (steamid=?);", (steamid, ))
	account = cur.fetchall()
	if account:
		id_, username, password, steamid, steamapikey, tmapikey, user_id = account[0]
		return {
			"id": id_,
			"username": username,
			"password": password,
			"steamid": steamid,
			"steamapikey": steamapikey,
			"tmapikey": tmapikey,
			"user_id": user_id
		}
	return None

# Helper for login to steam API via steampy (steamapikey, username, password)
def get_login_creds_by_steamid(steamid):
	creds = get_all_creds_by_steamid(steamid)
	return creds['username'], creds['password'], creds['steamapikey']

def get_account_username_by_steamid(steamid):
	username, password, steamapikey = get_login_creds_by_steamid(steamid)
	return username

def get_all_user_accounts(user_id):
	cur.execute("SELECT * FROM accounts WHERE (user_id=?);", (user_id, ))
	return cur.fetchall()

# Used to parsing some data with authentication
def get_random_account():
	cur.execute("SELECT * FROM accounts;")
	accounts = cur.fetchall()
	account = random.choice(accounts)
	id_, username, password, steamid, steamapikey, tmapikey, user_id = account
	return {
		"id": id_,
		"username": username,
		"password": password,
		"steamid": steamid,
		"steamapikey": steamapikey,
		"tmapikey": tmapikey,
		"user_id": user_id
	}

#
# Item ops
#

def create_item(specs):
	cur.execute("""INSERT INTO items
		(date_of_sell, asset_id, market_hash_name, buy_price, prediction_price, sold_price, account_id)
		VALUES (?,?,?,?,?,?,?);""", (specs['date_of_sell'], specs['asset_id'], specs['market_hash_name'],
			specs['buy_price'], specs['prediction_price'], specs['sold_price'], specs['account_id']))

def get_all_items_by_steamid(steamid):
	creds = get_all_creds_by_steamid(steamid)
	if creds:
		cur.execute("SELECT * FROM items WHERE (account_id=?);", (creds['id']))
		return cur.fetchall()
	return None

if __name__ == '__main__':
	# username, password = sys.argv[1:3]
	# create_user(username, password)
	print(get_all_users())
	print(get_account_by_steamid("7656119898327239"))