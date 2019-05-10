#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <string>
#ifndef PLAYER_CPP
#define PLAYER_CPP
using namespace std;
class Player{
  string playerName;
  int health = 5;
  int power = 5;
  int luck = 5;
  int gold = 5;
  int numBossDefeated = 0;
   string explorationText[11] = {"You sit down to take a break.", "You feel as if something is watching you.",
      "It is currently daytime. No maybe night. You are not sure.", "You ate food that you found in the dungeon. It was gross.", "You thought you found treasure. It was monster remains.", 
      "You fall asleep on the cold hard floor due to exhaustion.", "You thought you heard a monster. It was your stomach.", "A voice whispers: Give up.",
      "You found a dead body along your path.", "You try to dig through the dungeon with your weapon. It didn't work.", "You got up and tripped over yourself."};
  TFT_eSPI *draw;
  
  public:
  Player(TFT_eSPI* tft_to_use, string playerName){
    draw = tft_to_use;
    this->playerName = playerName;
  }

  string getPlayerName() {
    return playerName;
  }

  void setPlayerName(string playerName) {
    this->playerName = playerName;
  }

  int getHealth() { 
    return health; 
  }
  
  void setHealth(int health) { 
    this->health = health; 
  }

  int getPower() { 
    return power; 
  }

  void setPower(int power) { 
    this->power = power; 
  }

  int getLuck() { 
    return luck; 
  }

  void setLuck() { 
    this->luck = luck; 
  }

  int getGold() { 
    return gold; 
  }

  void setGold() { 
    this->gold = gold; 
  }

  int getNumBossDefeated() { 
    return numBossDefeated; 
  }

  void setNumBossDefeated() { 
    this->numBossDefeated = numBossDefeated; 
  }
  
  void drawMap(string player_map){
    const uint16_t BACKGROUND_COLOR = TFT_BLACK;
    const uint16_t MAP_OUTLINE_COLOR = TFT_WHITE;
    const uint16_t PLAYER_COLOR = TFT_GREEN;
    const uint16_t MONSTER_COLOR = TFT_RED;
    const uint16_t BOSS_COLOR = TFT_ORANGE;
    const int SQUARE_SIZE = 15;
    draw->fillScreen(BACKGROUND_COLOR);

    // draw player map
    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        draw->drawRect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, MAP_OUTLINE_COLOR);

        // draw monster
        int start = (j*3 + i)*3;
        if (player_map.at(start) == 'M') {
          draw->fillRect(i*SQUARE_SIZE + 1, j*SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2, MONSTER_COLOR);
        }

        if (player_map.at(start) == 'B') {
          draw->fillRect(i*SQUARE_SIZE + 1, j*SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2, BOSS_COLOR);
        }

        // draw player
        if (player_map.at(start + 1) == 'P') {
          draw->fillCircle(i*SQUARE_SIZE + SQUARE_SIZE/2, j*SQUARE_SIZE + SQUARE_SIZE/2, 2, PLAYER_COLOR);
        }

        if (player_map.at(start) == 'X'){
          draw->fillRect(i*SQUARE_SIZE + 1, j*SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2, TFT_YELLOW);
        }
      }
    }
  }

  void drawStats(string playerStats){
    // draw player stats
    int token_index = playerStats.find(',');
    health = atoi(playerStats.substr(0, token_index).c_str());
    playerStats = playerStats.substr(token_index+1);
    token_index = playerStats.find(',');
    power = atoi(playerStats.substr(0, token_index).c_str());
    playerStats = playerStats.substr(token_index+1);
    token_index = playerStats.find(',');
    luck = atoi(playerStats.substr(0, token_index).c_str());
    playerStats = playerStats.substr(token_index+1);
    token_index = playerStats.find(',');
    gold = atoi(playerStats.substr(0, token_index).c_str());
    playerStats = playerStats.substr(token_index+1);
    token_index = playerStats.find(',');
    numBossDefeated = atoi(playerStats.substr(0, token_index).c_str());
    const int SQUARE_SIZE = 15;
    const int text_x = 3*SQUARE_SIZE + 10;
    char buffer[20];
    for (int i = 0; i < 6; i++) {
      draw->setCursor(text_x, i*10);
      if (i == 0) {
        draw->println("   Stats   ");
      } else if (i == 1) {
        draw->printf("HP:   %d", health);
      } else if (i == 2) {
        draw->printf("PWR:  %d", power);
      } else if (i == 3) {
        draw->printf("Luck: %d", luck);
      } else if (i == 4) {
        draw->printf("Gold: %d", gold);
      } else if (i == 5) {
        draw->printf("Boss: %d", numBossDefeated);
      } 
    }
  }

  void drawFlavorText(int randomIndex){
      // draw player options
      const int SQUARE_SIZE = 15;
      const int options_y = 3*SQUARE_SIZE + 20;
      const uint16_t OPTIONS_COLOR = TFT_YELLOW;
      draw->drawRect(10, options_y, 105, 20, OPTIONS_COLOR);
      draw->setCursor(30, options_y + 6);
      draw->println("BUY    QUIT");
      // cursor options for later
      //draw->setCursor(20, options_y + 6);
      //draw->println(">");
      //draw->setCursor(60, options_y + 6);
      //draw->println(">");
  
      // draw flavor text
      string flavor_text = explorationText[randomIndex];
      const int flavor_y = options_y + 30;
      draw->setCursor(0, flavor_y);
      draw->println(flavor_text.c_str());
   }
};
#endif
