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
  }
};
