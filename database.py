import sqlite3
import datetime

game_db = 'game_info.db'

def create_tables():
	'''
	Player table: 
		coordinates: (x,y)
		id: #
		health: #
		power: #
		gold: #
		num_bosses_defeated: #
	Monster table:
		coordinates: (x,y)
		health: #
		power: #
		defeated_by: []
	'''
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	c.execute('''CREATE TABLE IF NOT EXISTS player_table (coordinates text, id int, health int, power int, gold int, num_bosses_defeated int);''') # run a CREATE TABLE command
	c.execute('''CREATE TABLE IF NOT EXISTS monster_table (coordinates text, health int, power int, defeated_by text);''') # run a CREATE TABLE command
	conn.commit() # commit commands
	conn.close() # close connection to database

def new_player(player_id):
	start_coordinates = (1,1)
	start_health = 5
	start_power = 5
	start_gold = 0
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''',(str(start_coordinates), player_id, start_health, start_power, start_gold, 0)) # insert row into table
	conn.commit() # commit commands
	conn.close() # close connection to database

def update_player(player_id, coordinates, health, power, gold, num_bosses_defeated):
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	c.execute('''UPDATE player_table SET coordinates = ?, health = ?, power = ?, gold = ?, num_bosses_defeated = ? WHERE id = ?;''',(str(coordinates), health, power, gold, num_bosses_defeated, player_id))
	conn.commit() # commit commands
	conn.close() # close connection to database

def delete_player(player_id):
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	c.execute('''DELETE FROM player_table WHERE id = ?;''',(player_id,))
	conn.commit() # commit commands
	conn.close() # close connection to database

def get_player_info(player_id):
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	info = c.execute('''SELECT * FROM player_table WHERE id = ?;''',(player_id,)).fetchone()
	conn.commit() # commit commands
	conn.close() # close connection to database
	if info is None:
		return info
	return [info[1]] + [eval(info[0])] + list(info[2:])

def get_monster_info(coordinates):
	conn = sqlite3.connect(game_db)  # connect to that database (will create if it doesn't already exist)
	c = conn.cursor()  # make cursor into database (allows us to execute commands)
	info = c.execute('''SELECT * FROM monster_table WHERE coordinates = ?;''',(str(coordinates),)).fetchone()
	conn.commit() # commit commands
	conn.close() # close connection to database
	return coordinates

# dummy player
player_id = 1
new_player(player_id)
print(get_player_info(player_id))
update_player(player_id, (0,0), 2, 3, 4, 5)
print(get_player_info(player_id))
delete_player(player_id)
print(get_player_info(player_id))
