import sys
import sqlite3

conn = sqlite3.connect("database.db", isolation_level=None)
cur = conn.cursor()

# User, he has api key of TM, and can have multiple steam_accounts (or not?)
cur.execute("""CREATE TABLE IF NOT EXISTS users
	(id INTEGER PRIMARY KEY AUTOINCREMENT, 
	username varchar, 
	password varchar,
	apikey varchar
	);
	""")

# Steam Account (P.S. One user can have multiple steam accounts)
cur.execute("""CREATE TABLE IF NOT EXISTS steam_accounts
	(id INTEGER primary key AUTOINCREMENT,
	username varchar,
	password varchar,
	steamid varchar,
	user_id int,
	FOREIGN KEY(user_id) REFERENCES users(id)
	);
	""")

# User ops

def create_user(username, password, apikey=None):
	cur.execute("INSERT INTO users (username, password, apikey) VALUES (?,?,?);", (username, password, apikey))

def get_all_users():
	cur.execute("SELECT * FROM users;")
	return cur.fetchall()

# Account ops

# def create_steam_account(username, password)

# def get_steam_accounts_by_user(username):


if __name__ == '__main__':
	username, password = sys.argv[1:3]
	create_user(username, password)
	print(get_all_users())