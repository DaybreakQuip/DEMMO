# 6.08 Final Project: DEMMO
Dungeon Exploration MMO

Our goal was to create a multiplayer dungeon exploration game that featured players armed with their own ESP32s fighting for survival inside a
dangerous world filled with deadly monsters, riveting narration, and a dynamic shop system. The gameplay involves traversing the game world and defeating
monsters to achieve the ultimate goal: defeating all bosses scattered throughout the map.

The main features of this game include exciting turn-based combat with beautiful animations,
respawning and farmable monsters, a portable shop system to purchase player stat upgrades, and a mini map where you can neighboring players that are online and monsters.

[Gameplay Video](https://youtu.be/rPcvFmMMvDs)

 Directory files & What they do

     DEMMO/
        - containers/
            `game.py`
                Game - class representing ongoing DEMMO game, has fields: id_to_players, id_to_monsters, map (Map object)
                Map - class representing map of the game, has fields: rows, columns, tiles (2D array of Tile objects)
                Tile - class representing a single tile on the map, has fields: players and monsters (set of player_ids and monster_ids respectively)
            `game_object.py`
                GameObject - Super class for all objects in the game, each object has fields: id (str), row (int), col (int), health (int), power (int)
            `monster.py`
                Monster(GameObject) - Class that represents monsters, has additional fields: is_boss (bool), defeated_by (set)
            `player.py`
                Player(GameObject) - Class that represents players, has additional fields: gold (int), num_boss_defeated(int)

        - resources/
            `game_info.db`: gitignored, but should be generated automatically when you run reset_game_database.py (or Database.create_game_object_tables()
                            for a clean database without any entries at all), contains database for the game
            `map.json`: contains number of map rows and columns information
            `monsters.json`: contains list of default monster information

        - test_resources/
            `test_game_info.db`: gitignored, but should be generated locally when you run test.py, contains test database for test cases
            `test_map.json`: contains number of map rows and columns information for test cases

        - `constants.py`: contains constants for the project, please add new constants to this file under their class (if applicable)
        - `database.py`: contains database operations
            Database - class that conatins static methods for direct database interactions for retrieving / saving to the database
            Serialize - class with static methods to save GameObjects to database
            Deserialize - class with static methods methods to retrieve GameObjects from database
        - `request_handler.py`: contains methods for handling GET and POST requests (user actions will most likely be processed in POST)
        - `reset_game_database.py`: run this script to reset the database to initial state with default monsters and no players (IS_SERVER must be False)
        - `temp.py`: gitignored, but feel free to add the project to test things out
        - `test.py`: contains tests for the project, please run before commiting and pushing (also add test cases if possible when new features are added)
      

 Goal relationships (x -> y indicates x calls methods in y)
    
        - classes Serialize and Deserialize -> Database class
        - classes Serialize and Deserialize -> Game containers (GameObject, Game, Player, Monster)
        - request_handler.py -> Serialize and Deserialize
        - request_handler.py -> Game containers (GameObject, Game, Player, Monster)
        - Game containers <-> Game containers 
        
