#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
class Player{
  public:
  int health;
  int power;
  int gold;
  int numBossDefeated;
  TFT_eSPI *draw;
  Player(TFT_eSPI* tft_to_use, int hp, int atk, int money, int numBoss){
    draw = tft_to_use;
    health = hp;
    power = atk;
    gold = money;
    numBossDefeated = numBoss;
  }
  void drawMap(String player_map, String flavor_text){
    const uint16_t BACKGROUND_COLOR = TFT_BLACK;
    const uint16_t MAP_OUTLINE_COLOR = TFT_WHITE;
    const uint16_t PLAYER_COLOR = TFT_GREEN;
    const uint16_t MONSTER_COLOR = TFT_RED;
    const int SQUARE_SIZE = 15;
    draw->fillScreen(BACKGROUND_COLOR);

    // draw player map
    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        draw->drawRect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, MAP_OUTLINE_COLOR);

        // draw monster
        int start = (j*3 + i)*3;
        if (player_map.charAt(start) == 'M') {
          draw->fillRect(i*SQUARE_SIZE + 1, j*SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2, MONSTER_COLOR);
        }

        // draw player
        if (player_map.charAt(start + 1) == 'P') {
          draw->fillCircle(i*SQUARE_SIZE + SQUARE_SIZE/2, j*SQUARE_SIZE + SQUARE_SIZE/2, 2, PLAYER_COLOR);
        }
      }
    }

    // draw player stats
    const int text_x = 3*SQUARE_SIZE + 10;
    for (int i = 0; i < 5; i++) {
      draw->setCursor(text_x, i*10);
      if (i == 0) {
        draw->println("   Stats   ");
      } else if (i == 1) {
        draw->println("HP:   " + String(health));
      } else if (i == 2) {
        draw->println("PWR:  " + String(power));
      } else if (i == 3) {
        draw->println("Gold: " + String(gold));
      } else if (i == 4) {
        draw->println("Boss: " + String(numBossDefeated));
      } 
    }

    // draw player options
    const int options_y = 3*SQUARE_SIZE + 10;
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
    const int flavor_y = options_y + 30;
    draw->setCursor(0, flavor_y);
    draw->println(flavor_text);
  }
};
