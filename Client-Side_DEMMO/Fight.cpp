#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <string>
#ifndef FIGHT_CPP
#define FIGHT_CPP
#include "Player.cpp"
#include "Monster.cpp"
using namespace std;

#define IDLE 0
#define PLAYER_TURN 1
#define MONSTER_TURN 2
#define FIGHT_END 3

class Fight{
  Player *player;
  Monster *monster;
  TFT_eSPI *draw;
  int fightState;
    
  public:
  Fight(Player* player, Monster* monster, TFT_eSPI* tft_to_use){
    this->player = player;
    this->monster = monster;
    draw = tft_to_use;
    fightState = 0;
  }

  int getFightState() { return fightState; }

  void setFightState(int fightState) { this->fightState = fightState; }

  boolean startFight(Monster* monster) {
    this->monster = monster;
    switch (fightState) {
      case IDLE:
        {
          fightState = PLAYER_TURN; // player goes first
          break;
        }
      case PLAYER_TURN:
        {
          if (player->getHealth() > 0) { // player is alive
            // <player attacks on button press>
            // <insert button logic here>
            int playerAttack = 100; // test damage
            monster->setHealth(monster->getHealth() - playerAttack);
            fightState = MONSTER_TURN;
          } else { // player is dead
            fightState = FIGHT_END;
          }
          break;
        }
      case MONSTER_TURN:
        {
          if (monster->getHealth() > 0) { // monster is alive
            // monster responds automatically if alive
            int monsterAttack = 100; // test damage
            player->setHealth(player->getHealth() - monsterAttack);
            fightState = PLAYER_TURN;
          } else { // monster is dead
            fightState = FIGHT_END; 
          }
          break;
        }
      case FIGHT_END:
        {
          fightState = IDLE;
          // return true if player wins, false otherwise
          return player->getHealth() > 0;
          break;
        }
    }
  }
};
#endif
