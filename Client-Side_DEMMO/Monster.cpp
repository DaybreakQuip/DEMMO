#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <string>
#ifndef MONSTER_CPP
#define MONSTER_CPP
class Monster{
  private:
  int health;
  int power;
  public:
  Monster(int health, int power) {
    this->health = health;
    this->power = power;
  }
  int getHealth(){
    return health;
  }
  void setHealth(int health) {
    this->health = health;
  }
  int getPower(){
    return power;
  }
  void setPower(int power) {
    this->power = power;
  }
};
#endif
