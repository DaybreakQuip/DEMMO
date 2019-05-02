class Player{
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
  void drawMap(){
    const uint16_t BACKGROUND_COLOR = TFT_GREEN;
    const int SQUARE_SIZE = 4;
    draw->fillScreen(BACKGROUND_COLOR);
    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        draw->drawRect(i*5, j*5, SQUARE_SIZE, SQUARE_SIZE, TFT_BLACK);
      }
    }
  }
};
