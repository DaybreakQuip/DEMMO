import sys
sys.path.append('__HOME__/DEMMO')

import unittest
import constants
from database import Database, Deserialize, Serialize
from containers.game import Game
from containers.player import Player
from containers.monster import Monster

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
        expected = '--------------------------<br>|&nbsp&nbsp&nbsp&nbsp0|&nbsp&nbsp&nbsp&nbsp1|&nbsp&nbsp&nbsp&nbsp2|&nbsp&nbsp&nbsp&nbsp3|&nbsp&nbsp&nbsp&nbsp4|<br>--------------------------<br>|&nbsp&nbsp&nbsp&nbsp5|&nbsp&nbsp&nbsp&nbsp6|&nbsp&nbsp&nbsp&nbsp7|&nbsp&nbsp&nbsp&nbsp8|&nbsp&nbsp&nbsp&nbsp9|<br>--------------------------<br>|&nbsp&nbsp10|&nbsp&nbsp11|&nbsp&nbsp12|&nbsp&nbsp13|&nbsp&nbsp14|<br>--------------------------<br>|&nbsp&nbsp15|&nbsp&nbsp16|&nbsp&nbsp17|&nbsp&nbsp18|&nbsp&nbsp19|<br>--------------------------<br>|&nbsp&nbsp20|&nbsp&nbsp21|&nbsp&nbsp22|&nbsp&nbsp23|&nbsp&nbsp24|<br>--------------------------<br><br>[0]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlayer(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Lucian, health: 5, power: 5, gold: 0, bosses defeated: 0)<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMonster(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Baron, health: 9001, power: 200, is boss: False, defeated by: {})<br>[6]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlayer(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Caitlyn, health: 5, power: 5, gold: 0, bosses defeated: 0)<br>[7]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMonster(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Dragon, health: 1000, power: 100, is boss: False, defeated by: {})<br>[14]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlayer(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Teemo, health: 5, power: 5, gold: 0, bosses defeated: 0)<br>[22]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlayer(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Ze, health: 5, power: 5, gold: 0, bosses defeated: 0)<br>[23]:<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMonster(s):<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(id: Raptor, health: 100, power: 5, is boss: False, defeated by: {})<br'
        result = game.get_server_map()
        self.assertEqual(expected, result)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        Database.delete_tables(test_database)

    def test_create_and_delete_game_objects(self):
        # Test game object creation
        Database.create_game_object_tables(test_database)
        Database.create_or_update_player("Lucian", 0, 0, 5, 5, 5, 0, test_database)
        Database.create_or_update_monster("Baron", 0, 0, 9999, 9999, db_constants.FALSE, "{'Lucian'}", test_database)
        player = Database.get_player_info("Lucian", test_database)
        monster = Database.get_monster_info("Baron", test_database)
        expected_player = ('Lucian', 0, 0, 5, 5, 5, 0)
        expected_monster = ('Baron', 0, 0, 9999, 9999, 'False', "{'Lucian'}")
        self.assertEqual(expected_player, player)
        self.assertEqual(expected_monster, monster)
        # Test get all
        players = Database.get_all_players(test_database)
        monsters = Database.get_all_monsters(test_database)
        self.assertEqual([expected_player], players)
        self.assertEqual([expected_monster], monsters)
        # Test modifying game objects
        Database.create_or_update_player("Lucian", 1, 1, 100, 5, 5, 1, test_database)
        Database.create_or_update_monster("Baron", 0, 0, 9999, 9999, db_constants.TRUE, "{}", test_database)
        player = Database.get_player_info("Lucian", test_database)
        monster = Database.get_monster_info("Baron", test_database)
        expected_player = ('Lucian', 1, 1, 100, 5, 5, 1)
        expected_monster = ('Baron', 0, 0, 9999, 9999, 'True', "{}")
        self.assertEqual(expected_player, player)
        self.assertEqual(expected_monster, monster)
        # Test adding more than one player and monster
        Database.create_or_update_player("Thresh", 5, 5, 100, 5, 5, 1, test_database)
        Database.create_or_update_monster("Dragon", 10, 10, 9999, 9999, db_constants.TRUE, "{}", test_database)
        players = Database.get_all_players(test_database)
        monsters = Database.get_all_monsters(test_database)
        expected_players = [('Lucian', 1, 1, 100, 5, 5, 1), ('Thresh', 5, 5, 100, 5, 5, 1)]
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
        Database.create_or_update_player("Ze", 4, 4, 5, 5, 0, 0, test_database)
        Database.create_or_update_player("Teemo", 2, 1, 10, 100, 1, 5, test_database)
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
            Player("NotZe", 2, 4, 1000, 5, 0, 0),
            Player("DefinitelyZe", 2, 1, 1, 999, 1, 100)
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
        self.assertEqual([('NotZe', 2, 4, 1000, 5, 0, 0), ('DefinitelyZe', 2, 1, 1, 999, 1, 100)],
                         Database.get_all_players(test_database))

        # delete all tables created in this test
        Database.delete_tables(test_database)