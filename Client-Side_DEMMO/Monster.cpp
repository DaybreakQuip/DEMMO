#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <string>

class Monster{
  private:
  int health;
  int power;
  int gold;
  boolean isBoss;
  public:
  Monster(int health, int power, int gold, boolean isBoss){
    this->health = health;
    this->power = power;
    this->gold = gold;
    this->isBoss = isBoss;
  }
  int getHealth(){
    return health;
  }
  int setHealth(int health){
    this->health = health;
  }
  int getPower(){
    return power;
  }
  int getGold(){
    return gold;
  }
  boolean getMonsterStatus(){
    return isBoss;
  }
};
