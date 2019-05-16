#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include <HTTPClient.h>
#include <string>
#include <math.h>
using std::string;
#include "Player.cpp"
#include "Monster.cpp"
//#include "Fight.cpp"
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
char network[] = "MIT";
//char network[] = "6s08";  //SSID for 6.08 Lab
string player = "Max";
//char password[] = "iesc6s08"; //Password for 6.08 Labconst uint8_t IUD = 32; //pin connected to button
const uint32_t pwm_channel = 0; 
const uint8_t IUD = 32; //pin connected to button 
const uint8_t ILR = 33; //pin connected to button
const uint8_t BUTTON_1 = 16; //button 1
const uint8_t BUTTON_2 = 5; //button 2 
const int SQUARE_SIZE = 15;
const int options_y = 3*SQUARE_SIZE + 20;
const uint16_t OPTIONS_COLOR = TFT_YELLOW;
int state = 0;
int previous_state = 0;
int buy_state = 20;
MPU9255 imu; //imu object called, appropriately, imu
#define START 0
#define MOVE 1 //state of player's action
#define FIGHT 2 //state of player's action
#define END 3
#define QUIT 4
#define OFF 5
#define CHOOSE_QUIT 6
#define CHOOSE_BUY 7
#define BUY 8
#define IDLE 10
#define PLAYER_TURN 11
#define MONSTER_TURN 12
#define FIGHT_END 13
#define BUY_HEALTH 20
#define BUY_POWER 21
#define BUY_LUCK 22
unsigned long moveTimer;
int randNumber;
int pwmTimer;
unsigned long buttonTimer; //timer to make sure multiple button presses do not occur
Player me(&tft, player);
Monster monster(5,10); // dummy monster
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
    fightState = 10;
  }

  int getFightState() { return fightState; }

  void setFightState(int fightState) { this->fightState = fightState; }
  
  void drawPlayerAttack(){
     int period = 20;
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_RED);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
     for (int i = 15; i < 97; i = i + 2){
        int timer = millis();
        draw->fillCircle(i, 70, 5,TFT_BLUE);
        while (millis() - timer < period) {}
        draw->fillCircle(i, 70, 5, TFT_BLACK);
     }
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_RED);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
  }

  void drawMonsterAttack(){
     int period = 20;
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_RED);
     draw->fillCircle(103, 54, 1, TFT_PURPLE);
     for (int i = 110; i > 25; i= i - 2){
        int timer = millis();
        draw->fillCircle(i, 70, 5,TFT_RED);
        while (millis() - timer < period) {}
        draw->fillCircle(i, 70, 5, TFT_BLACK);
     }
     draw->fillRect(5, 50, 20, 40, TFT_BLUE);
     draw->fillRect(100, 50, 20, 40,TFT_RED);
     draw->fillCircle(20, 54, 1, TFT_RED);
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
    for (int i = 101; i < 124; i= i + 2){
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

  void drawHP() {
    draw->setCursor(30, 20);
    draw->println("                     ");
    draw->setCursor(30, 20);
    draw->printf("Player HP: %d", player->getHealth());
    draw->setCursor(25, 110);
    draw->println("                     ");
    draw->setCursor(25, 110);
    draw->printf("Monster HP: %d", monster->getHealth());
  }
  void drawPlayerDamage(int playerAttack){
    draw->setCursor(5, 10);
    draw->println("                     ");
    draw->setCursor(5, 10);
    draw->printf("You dealt %d dmg", playerAttack);
  }
  void drawMonsterDamage(int monsterAttack){
    draw->setCursor(5, 10);
    draw->println("                     ");
    draw->setCursor(5, 10);
    draw->printf("Enemy dealt %d dmg", monsterAttack);
  }
  boolean startFight(Monster* monster) {
    draw->fillScreen(TFT_BLACK);
    draw->fillRect(5, 50, 20, 40, TFT_BLUE);
    draw->fillRect(100, 50, 20, 40,TFT_RED);
    draw->fillCircle(20, 54, 1, TFT_RED);
    draw->fillCircle(103, 54, 1, TFT_PURPLE);
    draw->setCursor(0,140);
    draw->println("1: Attack");
    draw->println("2: Forfeit");
    drawHP();
    while (fightState != FIGHT_END) {
      switch (fightState) {
        case IDLE:
          {
            fightState = PLAYER_TURN; // player goes first
            break;
          }
        case PLAYER_TURN:
          {
            if (millis() - pwmTimer > 5000){
              if (state == previous_state){
                  previous_state = state;
              }
              state = OFF;
              ledcWrite(pwm_channel, 0);
            }
            if (state == OFF && digitalRead(BUTTON_1) == 0){
                state = previous_state;
                ledcWrite(pwm_channel,4095);
                pwmTimer = millis();
                buttonTimer = millis();
            }
            if (state != OFF){
                if (digitalRead(BUTTON_2) == 0 && millis() - buttonTimer > 500){
                    pwmTimer = millis();
                    player->setHealth(0);
                    drawHP();
                    pwmTimer = millis();
                }
                if (player->getHealth() > 0) { // player is alive
                  // <player attacks on button press>
                  // <insert button logic here>
                  int playerAttack = 100; // test damage
                  if (digitalRead(BUTTON_1) == 0 && millis() - buttonTimer > 500){
                    pwmTimer = millis();
                    int randNumber = random(100);
                    if (randNumber < player->getLuck()) {
                      playerAttack = ((1 + critMultiplier) * player->getPower());
                    } else {
                      playerAttack = player->getPower();
                    }
                    drawPlayerAttack();
                    playerAttack = randomizeAttack(playerAttack);
                    monster->setHealth(monster->getHealth() - playerAttack);
                    fightState = MONSTER_TURN;
                    drawHP();
                    drawPlayerDamage(playerAttack);
                    pwmTimer = millis();
                  }
                } else { // player is dead
                  pwmTimer = millis();
                  drawPlayerDeath();
                  fightState = FIGHT_END;
                  pwmTimer = millis();
                }
            }
            break;
          }
        case MONSTER_TURN:
          {
            pwmTimer = millis();
            if (monster->getHealth() > 0) { // monster is alive
              // monster responds automatically if alive
              int monsterAttack = monster->getPower(); // test damage
              monsterAttack = randomizeAttack(monsterAttack);
              player->setHealth(player->getHealth() - monsterAttack);
              fightState = PLAYER_TURN;
              drawMonsterAttack();
              drawHP();
              drawMonsterDamage(monsterAttack);
              pwmTimer = millis();
            } else { // monster is dead
              pwmTimer = millis();
              fightState = FIGHT_END; 
              drawMonsterDeath();
              pwmTimer = millis();
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
Fight fight(&me, &monster, &tft); // dummy fight

void setup() {
  Serial.begin(115200); //for debugging if needed.
  pinMode(IUD, INPUT_PULLUP); //set input pin as an input!
  pinMode(ILR, INPUT_PULLUP); //set input pin as an input!
  pinMode(BUTTON_1,INPUT_PULLUP);
  pinMode(BUTTON_2,INPUT_PULLUP);
  ledcSetup(pwm_channel, 50, 12);//create pwm channel, @50 Hz, with 12 bits of precision
  ledcAttachPin(14, pwm_channel); //link pwm channel to IO pin 14
  pinMode(14, OUTPUT); //controlling TFT with hardware PWM (second part of lab)
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK); 
  if (imu.setupIMU(1)){
    Serial.println("IMU Connected!");
  }else{
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart(); // restart the ESP (proper way)
  }
  WiFi.begin(network);
  uint8_t count = 0; //count used for Wifi check times
  Serial.print("Attempting to connect to ");
  Serial.println(network);
  while (WiFi.status() != WL_CONNECTED && count<12) {
    delay(500);
    Serial.print(".");
    count++;
  }
  delay(2000);
  if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    Serial.println("CONNECTED!");
    Serial.println(WiFi.localIP().toString() + " (" + WiFi.macAddress() + ") (" + WiFi.SSID() + ")");
    delay(500);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
  randomSeed(analogRead(0));
  randNumber = random(0, 11);
  moveTimer = millis();
  buttonTimer = millis();
  pwmTimer = millis();
  ledcWrite(pwm_channel,4095);
}

void loop() {
      if (millis() - pwmTimer > 5000 && state != START){
        if (state == previous_state){
            previous_state = state;
        }
        state = OFF;
        ledcWrite(pwm_channel, 0);
      }
      if (millis() - pwmTimer > 15000 && state == START){
        if (state == previous_state){
            previous_state = state;
        }
        state = OFF;
        ledcWrite(pwm_channel, 0);
      }
      if (state == OFF && digitalRead(BUTTON_1) == 0){
          state = previous_state;
          ledcWrite(pwm_channel,4095);
          pwmTimer = millis();
          buttonTimer = millis();
      }
      if (state != OFF){
          if (digitalRead(BUTTON_2)==0 && (millis() - buttonTimer > 500) && state == MOVE){
              pwmTimer = millis();
              state = CHOOSE_QUIT;
              previous_state = state;
              tft.drawRect(10, options_y, 105, 20, OPTIONS_COLOR);
              tft.setCursor(30, options_y + 6);
              tft.print("BUY");
              tft.print("    ");
              tft.setTextColor(TFT_GREEN, TFT_RED); 
              tft.print("QUIT");
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              buttonTimer = millis();
              pwmTimer = millis();
          }
          if (digitalRead(BUTTON_1)==0 && (millis() - buttonTimer > 500) && state == MOVE){
              pwmTimer = millis();
              state = CHOOSE_BUY;
              previous_state = state;
              tft.drawRect(10, options_y, 105, 20, OPTIONS_COLOR);
              tft.setCursor(30, options_y + 6);
              tft.setTextColor(TFT_GREEN, TFT_RED); 
              tft.print("BUY");
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              tft.print("    ");
              tft.print("QUIT");
              buttonTimer = millis();
              pwmTimer = millis();
          }
          string server_response = action();
          if (server_response.length() > 0){
              pwmTimer = millis();
              Serial.print("server response: ");
              Serial.println(server_response.c_str());
            
              int token_index = server_response.find('|');
              string player_stats = server_response.substr(0, token_index);
              
              string remaining_info = server_response.substr(token_index+1);
              token_index = remaining_info.find('|');
              
              string test_map = remaining_info.substr(0, token_index);
              string monster_info = remaining_info.substr(token_index+1);
    
              if (monster_info.at(0) == 'T') {
                tft.fillScreen(TFT_BLACK);
                state = FIGHT;
                previous_state = state;
                token_index = monster_info.find(',');
                remaining_info = monster_info.substr(token_index+1);
                Serial.println(remaining_info.c_str());
                token_index = remaining_info.find(',');
                monster.setHealth(atoi(remaining_info.substr(0,token_index).c_str()));
                monster.setPower(atoi(remaining_info.substr(token_index+1).c_str()));
              } else {
                Serial.println("no monster");
              }
              
              randNumber = random(0, 11);
              moveTimer = millis();
              me.drawMap(test_map);
              me.drawStats(player_stats);
              me.drawFlavorText(randNumber);
        }
     }
} 

string action(){
  //Serial.print("state: ");
  //Serial.println(state);
  switch(state){
    case START:
      tft.setCursor(0,0,1);
      tft.println("Welcome to DEMMO! Press button to continue.");
      if (digitalRead(BUTTON_1) == 0 && (millis() - buttonTimer > 500)){
          pwmTimer = millis();
          Serial.println("Button has been pressed, starting the game!");
          tft.fillScreen(TFT_BLACK);
          string server_response = post_request(me.getPlayerName(), " ");
          int token_index = server_response.find('|');
          string player_stats = server_response.substr(0, token_index);
          string test_map = server_response.substr(token_index + 1);
          me.drawMap(test_map);
          me.drawStats(player_stats);
          me.drawFlavorText(randNumber);
          state = MOVE;
          previous_state = state;
      }
      return "";
    case MOVE:
        //Serial.println("Trying to move!");
        if (millis() - moveTimer > 1500) {
          int LR = analogRead(ILR);
          int UD = analogRead(IUD);
          //Serial.println(LR);
          if (LR >= 3000){
            return post_request(me.getPlayerName(), "right");
          }
          else if (LR < 1000){
           return post_request(me.getPlayerName(),"left");
    
          }
          else if (UD >= 3000){
           return post_request(me.getPlayerName(),"down");
          }
          else if (UD < 1000){
           return post_request(me.getPlayerName(),"up");
          }
          else {
            return "";
          }
       } else {
          return "";
       }
     case FIGHT:
          {
            boolean playerWins = fight.startFight(&monster);
            pwmTimer = millis();
            Serial.print("player wins the fight? ");
            if (playerWins) {
              Serial.println("yes");
            } else {
              Serial.println("no");
            }
            char buffer[20];
            string action = "fight_result&health=" + string(itoa(me.getHealth(), buffer, 10));
            Serial.println(action.c_str());
            string server_response = post_request(me.getPlayerName(), action);
            pwmTimer = millis();
            if (playerWins) {
                int token_index = server_response.find('|');
                string player_stats = server_response.substr(0, token_index);
                string test_map = server_response.substr(token_index + 1);
                me.drawMap(test_map);
                me.drawStats(player_stats);
                me.drawFlavorText(randNumber);
                state = MOVE;
                previous_state = state;

            } else {
              tft.fillScreen(TFT_BLACK);
              state = END;
              previous_state = state;
            }
            return "";
          }
     case END:
          tft.drawString("yOu LoSt!", 0, 0, 1);
          if (digitalRead(BUTTON_1) == 0 && millis() - buttonTimer > 500){
             pwmTimer = millis();
             state = START;
             previous_state = state;
             tft.fillScreen(TFT_BLACK);
             buttonTimer = millis();
          }
          return "";
     case CHOOSE_BUY:
           if (digitalRead(BUTTON_1) == 0 && (millis() - buttonTimer > 500)){
              pwmTimer = millis();
              state = BUY;
              previous_state = state;
              tft.fillScreen(TFT_BLACK);
              me.drawShopStats();
              buttonTimer = millis(); 

          }
          else if (digitalRead(BUTTON_2) == 0 && (millis() - buttonTimer > 500)){
              pwmTimer = millis();
              state = MOVE;
              previous_state = state;
              string server_response = post_request(me.getPlayerName(), " ");
              int token_index = server_response.find('|');
              string player_stats = server_response.substr(0, token_index);
              string test_map = server_response.substr(token_index + 1);
              me.drawMap(test_map);
              me.drawStats(player_stats);
              me.drawFlavorText(randNumber);
              buttonTimer = millis();
          }
          return "";
     case BUY:
          if (millis() - moveTimer > 300){
              int UD = analogRead(IUD);
              if (UD >= 3000){
                  pwmTimer = millis();
                  tft.setCursor(0,110);
                  tft.println("                               ");
                  if (buy_state == BUY_HEALTH){
                      buy_state = BUY_POWER;
                  }
                  else if (buy_state == BUY_POWER){
                      buy_state = BUY_LUCK;
                  }
                  else if (buy_state == BUY_LUCK){
                      buy_state = BUY_HEALTH;
                  }
              }
              else if (UD < 1000){
                  pwmTimer = millis();
                  tft.setCursor(0,110);
                  tft.println("                               ");
                  if (buy_state == BUY_HEALTH){
                      buy_state = BUY_LUCK;
                  }
                  else if (buy_state == BUY_POWER){
                      buy_state = BUY_HEALTH;
                  }
                  else if (buy_state == BUY_LUCK){
                      buy_state = BUY_POWER;
                  }
              }
             moveTimer = millis();
          }
          if (buy_state == BUY_HEALTH){
              tft.setCursor(0, 50);
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_RED); 
              tft.printf("5 HP:   %d Gold     ", int(pow(me.getHealth(),1.05)));
              tft.println();
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              tft.printf("1 PWR:  %d Gold     ", int(pow(me.getPower(),1.05)));
              tft.println();
              tft.println();
              tft.printf("1 Luck: %d Gold     ", int(pow(me.getLuck(),1.05)));

          }
          if (buy_state == BUY_POWER){
              tft.setCursor(0, 50);
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              tft.printf("5 HP:   %d Gold     ", int(pow(me.getHealth(),1.05)));
              tft.println();
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_RED); 
              tft.printf("1 PWR:  %d Gold     ", int(pow(me.getPower(),1.05)));
              tft.println();
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              tft.printf("1 Luck: %d Gold     ", int(pow(me.getLuck(),1.05)));
          }
          if (buy_state == BUY_LUCK){
              tft.setCursor(0, 50);
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
              tft.printf("5 HP:   %d Gold     ", int(pow(me.getHealth(),1.05)));
              tft.println();
              tft.println();
              tft.printf("1 PWR:  %d Gold     ", int(pow(me.getPower(),1.05)));
              tft.println();
              tft.println();
              tft.setTextColor(TFT_GREEN, TFT_RED); 
              tft.printf("1 Luck: %d Gold     ", int(pow(me.getLuck(),1.05)));
              tft.setTextColor(TFT_GREEN, TFT_BLACK); 
          }
          if (digitalRead(BUTTON_1) == 0 && millis() - buttonTimer > 500){
              pwmTimer = millis();
              tft.setCursor(0, 110);
              switch(buy_state){
                  case BUY_HEALTH:
                    if (me.getGold() < int(pow(me.getHealth(),1.05))){
                        tft.println("Not enough gold!");
                    }
                    else{
                        //send a post request
                        string server_response = post_request(me.getPlayerName(), "buy&stat=health");
                        int token_index = server_response.find('|');
                        string player_stats = server_response.substr(0, token_index);
                        string test_map = server_response.substr(token_index + 1);
                        me.setStats(player_stats);
                        me.drawShopStats();
                        tft.setCursor(0, 110);                        
                        tft.println("Success!");
                    }
                    break;
                  case BUY_POWER:
                       if (me.getGold() < int(pow(me.getPower(),1.05))){
                        tft.println("Not enough gold!");
                    }
                    else{
                        //send a post request
                        string server_response = post_request(me.getPlayerName(), "buy&stat=power");
                        int token_index = server_response.find('|');
                        string player_stats = server_response.substr(0, token_index);
                        string test_map = server_response.substr(token_index + 1);
                        me.setStats(player_stats);
                        me.drawShopStats();
                        tft.setCursor(0, 110);
                        tft.println("Success!");
                    }
                    break;
                  case BUY_LUCK:
                    if (me.getGold() < int(pow(me.getLuck(),1.05))){
                        tft.println("Not enough gold!");
                    }
                    else{
                        //send a post request
                        string server_response = post_request(me.getPlayerName(), "buy&stat=luck");
                        int token_index = server_response.find('|');
                        string player_stats = server_response.substr(0, token_index);
                        string test_map = server_response.substr(token_index + 1);
                        me.setStats(player_stats);
                        me.drawShopStats();
                        tft.setCursor(0, 110);
                        tft.println("Success!");
                    }
                    break;
              }
              buttonTimer = millis();
          }
          if (digitalRead(BUTTON_2) == 0){
              state = MOVE;
              previous_state = state;
              pwmTimer = millis();
              string server_response = post_request(me.getPlayerName(), " ");
              int token_index = server_response.find('|');
              string player_stats = server_response.substr(0, token_index);
              string test_map = server_response.substr(token_index + 1);
              me.drawMap(test_map);
              me.drawStats(player_stats);
              me.drawFlavorText(randNumber);
              buttonTimer = millis();
          }
          return "";
     case CHOOSE_QUIT:
          if (digitalRead(BUTTON_1) == 0 && (millis() - buttonTimer > 500)){
              pwmTimer = millis();
              state = QUIT;
              previous_state = state;
              tft.fillScreen(TFT_BLACK);
              buttonTimer = millis(); 
          }
          else if (digitalRead(BUTTON_2) == 0 && (millis() - buttonTimer > 500)){
              pwmTimer = millis();
              state = MOVE;
              previous_state = state;
              string server_response = post_request(me.getPlayerName(), " ");
              int token_index = server_response.find('|');
              string player_stats = server_response.substr(0, token_index);
              string test_map = server_response.substr(token_index + 1);
              me.drawMap(test_map);
              me.drawStats(player_stats);
              me.drawFlavorText(randNumber);
              buttonTimer = millis();
          }
          return "";
     case QUIT:
          pwmTimer = millis();
          state = START;
          previous_state = state;
          buttonTimer = millis();
          tft.fillScreen(TFT_BLACK);
          return "";
  }
        
}

string post_request(string player, string action){
  //Note to self, to convert integer to string: string boss = "Boss: " + string(itoa(numBossDefeated, buffer, 10));
  WiFiClient client;
  string body = "player_id=" + player + "&action=" + action;
  if (client.connect("608dev.net", 80)) {
    client.println("POST http://608dev.net/sandbox/sc/yanniw/DEMMO/request_handler.py HTTP/1.1");
    client.println("Host: 608dev.net");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(body.length());
    client.println();
    client.println(body.c_str());
    //Serial.println(body.c_str());

  }
  string buff = "";
  buff = "  ";
  string response = "";
  bool canRespond = false;
  while(!client.available()){}
   while ( client.available())
    {
      char resp = client.read();
      buff += resp;
      if (canRespond){
        response += resp;
      }
      if (buff.substr(buff.length()-2, buff.length()) == "\n\r"){
        canRespond = true;
      }
    }
  return response.substr(1, response.length());
}
