import sys
sys.path.append('__HOME__/DEMMO')

import unittest
import constants
from database import Database, Deserialize, Serialize
from containers.game import Game
from containers.player import Player
from containers.monster import Monster
from response_creator import ResponseCreator

# constants for test cases
test_database = constants.Database.TEST_DATABASE_PATH
test_map_path = constants.Database.TEST_MAP_PATH
db_constants = constants.Database

class TestGame(unittest.TestCase):

    def test_get_server_map(self):
        rows = 5
        columns = 5
        players = [
            Player("Lucian", 0, 0),
            Player("Caitlyn", 1, 1),
            Player("Teemo", 2, 4),
            Player("Ze", 4, 2)
        ]
        monsters = [
            Monster("Baron", 0, 0, 9001, 200),
            Monster("Dragon", 1, 2, 1000, 100),
            Monster("Raptor", 4, 3, 100, 5)
        ]

        game = Game(rows, columns, players, monsters)
        expected = '<xmp>---------------------\n|  0|  1|  2|  3|  4|\n---------------------\n|  5|  6|  7|  8|  9|\n---------------------\n| 10| 11| 12| 13| 14|\n---------------------\n| 15| 16| 17| 18| 19|\n---------------------\n| 20| 21| 22| 23| 24|\n---------------------\n\n[0]:\n\tPlayer(s):\n\t\t(id: Lucian, health: 5, power: 5, luck: 5, gold: 0, bosses defeated: 0)\n\tMonster(s):\n\t\t(id: Baron, health: 9001, power: 200, is boss: False, defeated by: {})\n[6]:\n\tPlayer(s):\n\t\t(id: Caitlyn, health: 5, power: 5, luck: 5, gold: 0, bosses defeated: 0)\n[7]:\n\tMonster(s):\n\t\t(id: Dragon, health: 1000, power: 100, is boss: False, defeated by: {})\n[14]:\n\tPlayer(s):\n\t\t(id: Teemo, health: 5, power: 5, luck: 5, gold: 0, bosses defeated: 0)\n[22]:\n\tPlayer(s):\n\t\t(id: Ze, health: 5, power: 5, luck: 5, gold: 0, bosses defeated: 0)\n[23]:\n\tMonster(s):\n\t\t(id: Raptor, health: 100, power: 5, is boss: False, defeated by: {})</xmp>'
        result = game.get_server_map()
        self.assertEqual(expected, result)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)

    def test_create_and_delete_game_objects(self):
        # Test game object creation
        Database.create_game_object_tables(test_database)
        Database.create_or_update_player("Lucian", 0, 0, 5, 5, 5, 0, 0, test_database)
        Database.create_or_update_monster("Baron", 0, 0, 9999, 9999, db_constants.FALSE, "{'Lucian'}", test_database)
        player = Database.get_player_info("Lucian", test_database)
        monster = Database.get_monster_info("Baron", test_database)
        expected_player = ('Lucian', 0, 0, 5, 5, 5, 0, 0)
        expected_monster = ('Baron', 0, 0, 9999, 9999, 'False', "{'Lucian'}")
        self.assertEqual(expected_player, player)
        self.assertEqual(expected_monster, monster)
        # Test get all
        players = Database.get_all_players(test_database)
        monsters = Database.get_all_monsters(test_database)
        self.assertEqual([expected_player], players)
        self.assertEqual([expected_monster], monsters)
        # Test modifying game objects
        Database.create_or_update_player("Lucian", 1, 1, 100, 5, 5, 1, 0, test_database)
        Database.create_or_update_monster("Baron", 0, 0, 9999, 9999, db_constants.TRUE, "{}", test_database)
        player = Database.get_player_info("Lucian", test_database)
        monster = Database.get_monster_info("Baron", test_database)
        expected_player = ('Lucian', 1, 1, 100, 5, 5, 1, 0)
        expected_monster = ('Baron', 0, 0, 9999, 9999, 'True', "{}")
        self.assertEqual(expected_player, player)
        self.assertEqual(expected_monster, monster)
        # Test adding more than one player and monster
        Database.create_or_update_player("Thresh", 5, 5, 100, 5, 5, 1, 0, test_database)
        Database.create_or_update_monster("Dragon", 10, 10, 9999, 9999, db_constants.TRUE, "{}", test_database)
        players = Database.get_all_players(test_database)
        monsters = Database.get_all_monsters(test_database)
        expected_players = [('Lucian', 1, 1, 100, 5, 5, 1, 0), ('Thresh', 5, 5, 100, 5, 5, 1, 0)]
        expected_monsters = [('Baron', 0, 0, 9999, 9999, 'True', '{}'), ('Dragon', 10, 10, 9999, 9999, 'True', '{}')]
        self.assertEqual(expected_players, players)
        self.assertEqual(expected_monsters, monsters)

        # delete all tables created in this test
        Database.delete_tables(test_database)

class TestDeserialize(unittest.TestCase):

    def setUp(self):
        Database.delete_tables(test_database)

    def _create_expected_game(self):
        players = [
            Player("Ze", 4, 4, 5, 5, 0, 0),
            Player("Teemo", 2, 1, 10, 100, 1, 5)
        ]
        monsters = [
            Monster("A_monster", 2, 1, 10, 5, False, {"Teemo"}),
            Monster("Boss", 0, 1, 10, 5, True, {})
        ]
        rows = 5
        columns = 5

        return Game(rows, columns, players, monsters)

    def _populate_test_database(self):
        # Create the tables
        Database.create_game_object_tables(test_database)
        # Populate it
        Database.create_or_update_player("Ze", 4, 4, 5, 5, 0, 0, 0, test_database)
        Database.create_or_update_player("Teemo", 2, 1, 10, 100, 1, 5, 0, test_database)
        Database.create_or_update_monster("A_monster", 2, 1, 10, 5, db_constants.FALSE, "{'Teemo'}", test_database)
        Database.create_or_update_monster("Boss", 0, 1, 10, 5, db_constants.TRUE, "{}", test_database)

    def testCreateGameFromDatabase(self):
        expected_game = self._create_expected_game()
        self._populate_test_database()
        game = Deserialize.createGameFromDatabase(test_map_path, test_database)

        # haven't implemented __eq__ in game, so use map render to compare... for now
        self.assertEqual(expected_game.get_server_map(), game.get_server_map())

        # delete all tables created in this test
        Database.delete_tables(test_database)

class TestSerialize(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)

    def testUpdateGameObjects(self):
        # Create the tables
        Database.create_game_object_tables(test_database)
        # Assert there's nothing in them right now
        self.assertEqual([], Database.get_all_players(test_database))
        self.assertEqual([], Database.get_all_monsters(test_database))

        # Create players and monsters to serialize
        players = [
            Player("NotZe", 2, 4, 1000, 5, 0, 0, 0),
            Player("DefinitelyZe", 2, 1, 1, 999, 1, 100, 0)
        ]
        monsters = [
            Monster("NotAMonster", 2, 1, 10, 1, False, {}),
            Monster("NotABoss", 0, 1, 10, 5, True, {"NotZe"})
        ]
        game_objects = players + monsters
        # Serialize and check if database is updated
        Serialize.updateGameObjects(game_objects, test_database)

        self.assertEqual([('NotAMonster', 2, 1, 10, 1, 'False', '{}'), ('NotABoss', 0, 1, 10, 5, 'True', "{'NotZe'}")],
                         Database.get_all_monsters(test_database))
        self.assertEqual([('NotZe', 2, 4, 1000, 5, 0, 0, 0), ('DefinitelyZe', 2, 1, 1, 999, 1, 100, 0)],
                         Database.get_all_players(test_database))

        # delete all tables created in this test
        Database.delete_tables(test_database)

class TestAction(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)

    def testUpdateGameObjects(self):
        # Create the tables
        Database.create_game_object_tables(test_database)
        # Assert there's nothing in them right now
        self.assertEqual([], Database.get_all_players(test_database))
        self.assertEqual([], Database.get_all_monsters(test_database))

        # Create players and monsters to serialize
        players = [
            Player("MoveLeftWall", 3, 0, 1, 1000, 5, 0, 0),
            Player("MoveRightWall", 1, 9, 2, 1, 999, 1, 100),
            Player("MoveUpWall", 0, 5, 3, 1000, 5, 0, 0),
            Player("MoveDownWall", 9, 3, 4, 1000, 5, 0, 0),
            Player("MoveLeft", 3, 2, 5, 1000, 5, 0, 0),
            Player("MoveRight", 1, 7, 6, 1, 999, 1, 100),
            Player("MoveUp", 3, 5, 7, 1000, 5, 0, 0),
            Player("MoveDown", 5, 3, 8, 1000, 5, 0, 0),
        ]
        monsters = [
            Monster("NotAMonster", 2, 1, 10, 1, False, {}),
            Monster("NotABoss", 0, 1, 10, 5, True, {"NotZe"})
        ]
        new_game = Game(10,10, players, monsters)
        game_objects = []
        game_objects.extend(new_game.execute("MoveLeftWall", "left"))
        game_objects.extend(new_game.execute("MoveRightWall", "right"))
        game_objects.extend(new_game.execute("MoveUpWall", "up"))
        game_objects.extend(new_game.execute("MoveDownWall", "down"))
        game_objects.extend(new_game.execute("MoveLeft", "left"))
        game_objects.extend(new_game.execute("MoveRight", "right"))
        game_objects.extend(new_game.execute("MoveUp", "up"))
        game_objects.extend(new_game.execute("MoveDown", "down"))
        game_objects = game_objects + monsters
        # Serialize and check if database is updated
        Serialize.updateGameObjects(game_objects, test_database)

        self.assertEqual([('NotAMonster', 2, 1, 10, 1, 'False', '{}'), ('NotABoss', 0, 1, 10, 5, 'True', "{'NotZe'}")],
                         Database.get_all_monsters(test_database))
        self.assertEqual([('MoveLeftWall', 3, 0, 1, 1000, 5, 0, 0), ('MoveRightWall', 1, 9, 2, 1, 999, 1, 100),
                          ('MoveUpWall', 0, 5, 3, 1000, 5, 0, 0), ('MoveDownWall', 9, 3, 4, 1000, 5, 0, 0),
                          ('MoveLeft', 3, 1, 5, 1000, 5, 0, 0), ('MoveRight', 1, 8, 6, 1, 999, 1, 100),
                          ('MoveUp', 2, 5, 7, 1000, 5, 0, 0), ('MoveDown', 6, 3, 8, 1000, 5, 0, 0)],
                         Database.get_all_players(test_database))

        # delete all tables created in this test
        Database.delete_tables(test_database)

class TestGetSurroundings(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)
    def testGetSurroundingEntities(self):
        Database.create_game_object_tables(test_database)
        # Assert there's nothing in them right now
        self.assertEqual([], Database.get_all_players(test_database))
        self.assertEqual([], Database.get_all_monsters(test_database))

        # Create players and monsters to serialize
        players = [
            Player("One", 3, 0, 1000, 5, 0, 0),
            Player("OneNeighbor", 4, 0, 100, 5, 0, 0),
            Player("Two", 1, 9, 1, 999, 1, 100),
            Player("Three", 0, 5, 1000, 5, 0, 0),
            Player("Four", 9, 3, 1000, 5, 0, 0),
            Player("Five", 3, 2, 1000, 5, 0, 0),
            Player("Six", 1, 7, 1, 999, 1, 100),
            Player("Seven", 3, 5, 1000, 5, 0, 0),
            Player("Eight", 5, 3, 1000, 5, 0, 0),
            Player("Nine", 0, 1, 1000, 5, 0, 0),
            Player("Ten", 0, 1, 1000, 5, 0, 0)
        ]
        monsters = [
            Monster("NotAMonster", 2, 1, 10, 1, False, {}),
            Monster("NotABoss", 0, 1, 10, 5, True, {"NotZe", "Ten"}),
            Monster("OnTopOfEight", 5, 3, 3, 3, True, {"One"})
        ]
        new_game = Game(10,10, players, monsters)
        response_creator = ResponseCreator(new_game)
        self.assertEqual("XX,__,M_,XX,_P,__,XX,_P,__,", response_creator.get_surrounding_entities("One"))
        self.assertEqual("__,__,__,__,_P,__,__,__,__,", response_creator.get_surrounding_entities("Seven"))
        self.assertEqual("XX,XX,XX,__,BP,__,__,__,__,", response_creator.get_surrounding_entities("Nine"))
        self.assertEqual("XX,XX,XX,__,_P,__,__,__,__,", response_creator.get_surrounding_entities("Ten"))
        self.assertEqual("__,__,__,__,BP,__,__,__,__,", response_creator.get_surrounding_entities("Eight"))
        game_objects = players + monsters
        Serialize.updateGameObjects(game_objects, test_database)


        # delete all tables created in this test
        Database.delete_tables(test_database)

class TestGetPlayerStats(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)
    def testGetSurroundingEntities(self):
        Database.create_game_object_tables(test_database)
        # Assert there's nothing in them right now
        self.assertEqual([], Database.get_all_players(test_database))
        self.assertEqual([], Database.get_all_monsters(test_database))

        # Create players and monsters to serialize
        players = [
            Player("One", 3, 0, 1000, 5, 0, 0),
            Player("Two", 1, 9, 1, 999, 1, 100),
            Player("Three", 0, 5, 50, 50, 50, 50),
            Player("Four", 9, 3, 1000, 5, 0, 0),
            Player("Five", 3, 2, 1000, 5, 0, 0),
            Player("Six", 1, 7, 1, 5, 1, 50),
            Player("Seven", 3, 5, 1000, 5, 0, 0),
            Player("Eight", 5, 3, 1000, 5, 0, 0),
        ]
        monsters = [
            Monster("NotAMonster", 2, 1, 10, 1, False, {}),
            Monster("NotABoss", 0, 1, 10, 5, True, {"NotZe"}),
        ]
        new_game = Game(10,10, players, monsters)
        self.assertEqual((1000,5,0,0,0),new_game.get_player_stats("One"))
        self.assertEqual((1,999,1,100,0), new_game.get_player_stats("Two"))
        self.assertEqual((50,50,50,50,0), new_game.get_player_stats("Three"))
        self.assertEqual((1000, 5, 0, 0,0), new_game.get_player_stats("Four"))
        self.assertEqual((1,5,1,50,0), new_game.get_player_stats("Six"))
        game_objects = players + monsters
        Serialize.updateGameObjects(game_objects, test_database)


        # delete all tables created in this test
        Database.delete_tables(test_database)