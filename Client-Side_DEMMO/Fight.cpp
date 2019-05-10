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
  float critMultiplier = 0.5;
    
  public:
  Fight(Player* player, Monster* monster, TFT_eSPI* tft_to_use){
    this->player = player;
    this->monster = monster;
    draw = tft_to_use;
    fightState = 0;
  }

  int getFightState() { return fightState; }

  void setFightState(int fightState) { this->fightState = fightState; }
  
  void drawPlayerAttack(){
     int period = 20;
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_WHITE);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
     for (int i = 15; i < 97; i = i + 2){
        int timer = millis();
        draw->fillCircle(i, 70, 5,TFT_BLUE);
        while (millis() - timer < period) {}
        draw->fillCircle(i, 70, 5, TFT_BLACK);
     }
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_WHITE);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
  }

  void drawMonsterAttack(){
     int period = 20;
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_WHITE);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
     for (int i = 110; i > 25; i= i - 2){
        int timer = millis();
        draw->fillCircle(i, 70, 5,TFT_RED);
        while (millis() - timer < period) {}
        draw->fillCircle(i, 70, 5, TFT_BLACK);
     }
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_WHITE);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
  }

  void drawPlayerDeath(){
     int period = 5;
     for (int i = 5; i < 26; i= i + 2){
        for (int j = 50; j < 91; j++){
            int timer = millis();
            draw->fillRect(i,j, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(26-i+5,j, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(i,91-j+50, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(26-i+5,91-j+50, 1,1, TFT_BLACK);

        }
     }
  }

  void drawMonsterDeath(){
    int period = 5;
    for (int i = 101; i < 122; i= i + 2){
        for (int j = 50; j < 91; j++){
            int timer = millis();
            draw->fillRect(i,j, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(122-i+101,j, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(i,91-j+50, 1,1, TFT_BLACK);
            while (millis() - timer < period) {}
            draw->fillRect(122-i+101,91-j+50, 1,1, TFT_BLACK);

        }
     }
  }

  int randomizeAttack(int attack) {
    int randomNum = random(80, 120);
    return int(attack * (randomNum / 100.0));
  }

  boolean startFight(Monster* monster) {
    while (fightState != FIGHT_END) {
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
              int randNumber = random(100);
              if (randNumber < player->getLuck()) {
                playerAttack = ((1 + critMultiplier) * player->getPower());
              } else {
                playerAttack = player->getPower();
              }
              playerAttack = randomizeAttack(playerAttack);
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
              int monsterAttack = monster->getPower(); // test damage
              monsterAttack = randomizeAttack(monsterAttack);
              player->setHealth(player->getHealth() - monsterAttack);
              fightState = PLAYER_TURN;
            } else { // monster is dead
              fightState = FIGHT_END; 
            }
            break;
          }
      }
    } 
    
    fightState = IDLE;
    // return true if player wins, false otherwise
    return player->getHealth() > 0;
  }
};
#endif
