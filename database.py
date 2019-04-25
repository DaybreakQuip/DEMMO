import sys
sys.path.append('__HOME__/DEMMO')

import sqlite3
import json
import constants
from constants import Database as db_constants

from containers.player import Player
from containers.monster import Monster
from containers.game import Game

class Database:
	"""
	This class contains class methods for operating on the database directly
	"""
	@classmethod
	def create_game_object_tables(cls, database=db_constants.DATABASE_PATH):
		'''
		Player table:
			id: text
			row: int
			coL: int
			health: int
			power: int
			gold: int
			num_bosses_defeated: int
		Monster table:
			id: text
			row: int
			col: int
			health: int
			power: int
			is_boss: (text) -> "False" or "True"
			defeated_by: (text) -> "{}" set of ids
		'''
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		c.execute(
			'''CREATE TABLE IF NOT EXISTS player_table (id text, row int, col int, health int, power int, gold int, num_bosses_defeated int);''')  # run a CREATE TABLE command
		c.execute(
			'''CREATE TABLE IF NOT EXISTS monster_table (id text, row int, col int, health int, power int, is_boss text, defeated_by text);''')  # run a CREATE TABLE command
		conn.commit()  # commit commands
		conn.close()  # close connection to database

	@classmethod
	def create_or_update_player(cls, id, row, col, health, power, gold, num_bosses_defeated, database=db_constants.DATABASE_PATH):
		"""
		Updates a player entry in the player_table if the player exists or creates a new entry otherwise
		:param id: (string) the player id to update or create
		:param row: (int) player's row
		:param col: (int) player's col
		:param health: (int) player's health
		:param power: (int) player's power
		:param gold: (int) player's gold
		:param num_bosses_defeated: (int) player's number of bosses defeated
		:return: None
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)

		# Determine whether the player exists in the database
		player_exists = c.execute(
			'''SELECT EXISTS(SELECT 1 FROM player_table WHERE id = ?)''', (id, )).fetchone()[0]
		if not player_exists: # Create a new player entry if the player does not exist
			c.execute(
				'''INSERT into player_table VALUES(?, ?, ?, ?, ?, ?, ?)''',
				(id, row, col, health, power, gold, num_bosses_defeated))
		else: # Update the existing player if the player exists
			c.execute(
				'''UPDATE player_table SET row = ?, col = ?, health = ?, power = ?, gold = ?, num_bosses_defeated = ? WHERE id = ?''',
				(row, col, health, power, gold, num_bosses_defeated, id))

		conn.commit()  # commit commands
		conn.close()  # close connection to database

	@classmethod
	def create_or_update_monster(cls, id, row, col, health, power, is_boss, defeated_by, database=db_constants.DATABASE_PATH):
		"""
		Updates a monster entry in the monster_table if the monster exists or creates a new entry otherwise
		:param id: (string) the monster id to update or create
		:param row: (int) monster's row
		:param col: (int) monster's col
		:param health: (int) monster's health
		:param power: (int) monster's power
		:param is_boss: (string) "True" or "False" indicating whether or not the monster is a boss
		:param defeated_by: (string) string representation of a set of player ids that have defeated it (strings)
		:return: None
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)

		# Determine whether the player exists in the database
		monster_exists = c.execute(
			'''SELECT EXISTS(SELECT 1 FROM monster_table WHERE id = ?)''', (id, )).fetchone()[0]
		if not monster_exists: # Create a new player entry if the player does not exist
			c.execute(
				'''INSERT into monster_table VALUES(?, ?, ?, ?, ?, ?, ?)''',
				(id, row, col, health, power, is_boss, defeated_by))
		else: # Update the existing player if the player exists
			c.execute(
				'''UPDATE monster_table SET row = ?, col = ?, health = ?, power = ?, is_boss = ?, defeated_by = ? WHERE id = ?''',
				(row, col, health, power, is_boss, defeated_by, id))

		conn.commit()  # commit commands
		conn.close()  # close connection to database

	@classmethod
	def get_all_players(cls, database=db_constants.DATABASE_PATH):
		"""
		:return: (list) of all entries from the player database (empty if no players exist)
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Query for all players
		players = c.execute('''SELECT * FROM player_table''').fetchall()
		conn.commit()  # commit commands
		conn.close()  # close connection to database

		return players

	@classmethod
	def get_all_monsters(cls, database=db_constants.DATABASE_PATH):
		"""
		:return: (list) of all entries from the monster databsae (empty if no monsters exist)
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Query for all monsters
		monsters = c.execute('''SELECT * FROM monster_table''').fetchall()
		conn.commit()  # commit commands
		conn.close()  # close connection to database

		return monsters

	@classmethod
	def get_monsters_within_range(cls, row, col, database=db_constants.DATABASE_PATH):
		"""
		:param row: the current row
		:param col: the current col
		:return: (list) of all monsters within range of (row, col)
		# TODO (if needed for performance reasons): Implement this
		"""
		pass

	@classmethod
	def get_players_within_range(cls, row, col, database=db_constants.DATABASE_PATH):
		"""
		:param row: the current row
		:param col: the current col
		:return: (list) of players within range of (row, col)
		# TODO (if needed for performance reasons): Implement this
		"""
		pass

	@classmethod
	def get_player_info(cls, player_id, database=db_constants.DATABASE_PATH):
		"""
		Returns a specific player's information
		:param player_id: the player id
		:return: (tuple) of player info or None if player does not exist in database
				player info format = (id, row, col, health, power, gold, num_bosses_defeated)
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Query for player information
		player_info = c.execute('''SELECT * FROM player_table WHERE id = ?;''',(player_id,)).fetchone()
		conn.commit()  # commit commands
		conn.close()  # close connection to database

		return player_info

	@classmethod
	def get_monster_info(cls, monster_id, database=db_constants.DATABASE_PATH):
		"""
		Returns a specific mosnter's information
		:param monster_id: the monster_id
		:return: (tuple) of monster info or None if monster does not exist in database
				monster info format  = (id, row, col, health, power, is_boss, defeated_by)
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Query for monster information
		monster_info = c.execute('''SELECT * FROM monster_table WHERE id = ?;''',(monster_id,)).fetchone()
		conn.commit()  # commit commands
		conn.close()  # close connection to database

		return monster_info

	@classmethod
	def delete_monster(cls, monster_id, database=db_constants.DATABASE_PATH):
		"""
		Delete the entry with monster_id in the monster table if the monster exists
		:param monster_id: the monster id to delete
		:return: None
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Delete monster from monster table with given id
		c.execute('''DELETE FROM monster_table WHERE id = ?;''',(monster_id,))
		conn.commit()  # commit commands
		conn.close()  # close connection to database

	@classmethod
	def delete_player(cls, player_id, database=db_constants.DATABASE_PATH):
		"""
		Delete the entry with player_id in the player table if the player exists
		:param player_id: the player id to delete
		:return:
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Delete player from player table with given id
		c.execute('''DELETE FROM player_table WHERE id = ?;''',(player_id,))
		conn.commit()  # commit commands
		conn.close()  # close connection to database

	@classmethod
	def delete_tables(cls, database=db_constants.DATABASE_PATH):
		"""
		DANGER AHEAD! Deletes the game database if it exists
		:return: None
		"""
		conn = sqlite3.connect(database)  # connect to that database (will create if it doesn't already exist)
		c = conn.cursor()  # make cursor into database (allows us to execute commands)
		# Delete the database
		c.execute(
			'''DROP TABLE IF EXISTS player_table'''
		)
		c.execute(
			'''DROP TABLE IF EXISTS monster_table'''
		)

		conn.commit()  # commit commands
		conn.close()  # close connection to database

class Deserialize:
	"""
	This class contains class methods that deserialize objects from the database
	"""
	@classmethod
	def createPlayerObject(cls, player_info):
		"""
		Returns a Player object using player_info
		:param player_info: (tuple) of (id, row, col, health, power, gold, num_bosses_defeated)
		:return: a new Player object
		"""
		id, row, col, health, power, gold, num_bosses_defeated = player_info
		return Player(id, row, col, health, power, gold, num_bosses_defeated)

	@classmethod
	def createMonsterObject(cls, monster_info):
		"""
		Returns a Monster object using monster_info
		:param monster_info: (tuple) of (id, row, col, health, power, is_boss, defeated_by)
		:return: a new Monster object
		"""
		id, row, col, health, power, is_boss, defeated_by = monster_info
		is_boss = eval(is_boss) # is_boss was a string of "True" or "False"
		defeated_by = eval(defeated_by) # convert from string to set
		return Monster(id, row, col, health, power, is_boss, defeated_by)

	@classmethod
	def createGameFromDatabase(cls, map_path=db_constants.MAP_PATH, database=db_constants.DATABASE_PATH):
		"""
		Creates and returns a new Game object that contains all game objects in the database
		:return: new Game object populated with all game objects in the database
		"""
		with open(map_path) as f:
			map_data = json.load(f)
			rows, columns = map_data['rows'], map_data['columns']

			# Get player and monster information
			monsters = []
			players = []
			for monster_info in Database.get_all_monsters(database):
				monsters.append(cls.createMonsterObject(monster_info))
			for player_info in Database.get_all_players(database):
				players.append(cls.createPlayerObject(player_info))

			return Game(rows, columns, players, monsters)

	@classmethod
	def createGameWithinRange(cls, row, col):
		"""
		Creates and returns a new Game object that only contains game object within range of (row, col)
		:param row: (int) current row in the game
		:param col: (int) current col in the game
		:return: a new Game object populated only with game objects within range
		"""
		# TODO (if needed for performance reasons): Implement me!
		pass

class Serialize:
	"""
	This class contains class methods to serialize and save objects to the database
	"""
	@classmethod
	def updateMonster(cls, monster, database=db_constants.DATABASE_PATH):
		"""
		Updates a single monster information in the database
		:param monster: (Monster) monster object to be saved
		:return: None

		:param monster_info: (tuple) of (id, row, col, health, power, is_boss, defeated_by)
		"""
		id = monster.id
		row = monster.row
		col = monster.col
		health = monster.health
		power = monster.power
		is_boss = db_constants.FALSE if not monster.is_boss else db_constants.TRUE
		defeated_by = repr(monster.defeated_by)

		Database.create_or_update_monster(id, row, col, health, power, is_boss, defeated_by, database)

	@classmethod
	def updatePlayer(cls, player, database=db_constants.DATABASE_PATH):
		"""
		Updates a single player information in the database
		:param Player: (Player) player object to  be saved
		:return: None
		"""
		# if the player died, delete the player's entry from the database
		if not player.isAlive:
			Database.delete_player(player.id, database)
			return

		# otherwise update the player's information
		id = player.id
		row = player.row
		col = player.col
		health = player.health
		power = player.power
		gold = player.gold
		num_bosses_defeated = player.num_boss_defeated

		Database.create_or_update_player(id, row, col, health, power, gold, num_bosses_defeated, database)

	@classmethod
	def updateGameObjects(self, game_objects, database=db_constants.DATABASE_PATH):
		"""
		Updates the provided game_objects in the database
		:param game_objects: (list) of game objects that require updating
		:return: None
		"""
		for game_object in game_objects:
			if isinstance(game_object, Monster):
				self.updateMonster(game_object, database)
			elif isinstance(game_object, Player):
				self.updatePlayer(game_object, database)

if __name__ == "__main__":

	if constants.TESTING:
		print(Database.get_all_monsters())
