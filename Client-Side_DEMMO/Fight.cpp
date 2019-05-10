#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <string>
using namespace std;

#define IDLE 0
#define PLAYER_TURN 1
#define MONSTER_TURN 2
#define PLAYER_WIN 3
#define MONSTER_WIN 4

class Fight{
  Player player;
  Monster monster;
  int fightState;
  public:
  Fight(Player player, Monster monster){
    this->player = player;
    this->monster = monster;
    fightState = 0;
  }

  int getFightState() { return fightState; }

  void setFightState(int fightState) { this->fightState = fightState; }

  void startFight(Monster monster) {
    switch (fightState) {
      case IDLE:
        {
          
          break;
        }
      case PLAYER_TURN:
        {
          if (player.getHealth() > 0) { // player is alive
            // player attacks
            fightState = MONSTER_TURN;
          } else { // player is dead
            fightState = MONSTER_WIN;
          }
          break;
        }
      case MONSTER_TURN:
        {
          if (monster.getHealth() > 0) { // monster is alive
            // monster attacks
            fightState = PLAYER_TURN;
          } else { // monster is dead
            fightState = PLAYER_WIN; 
          }
          break;
        }
      case PLAYER_WIN:
        {
          fightState = IDLE;
          return true;
          break;
        }
      case MONSTER_WIN:
        {
          fightState = IDLE;
          return false;
          break;
        }
    }
  }
};
