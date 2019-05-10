#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include <HTTPClient.h>
#include <string>
using std::string;
#include "Player.cpp"
#include "Monster.cpp"
#include "Fight.cpp"
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
char network[] = "MIT";  //SSID for 6.08 Lab
string player = "Ze";
//char password[] = "iesc6s08"; //Password for 6.08 Labconst uint8_t IUD = 32; //pin connected to button
const uint8_t IUD = 32; //pin connected to button 
const uint8_t ILR = 33; //pin connected to button
const uint8_t BUTTON_1 = 16; //button 1
const uint8_t BUTTON_2 = 5; //button 2 
int state = 0;
MPU9255 imu; //imu object called, appropriately, imu
#define START 0
#define MOVE 1 //state of player's action
#define FIGHT 2 //state of player's action
#define END 3
#define QUIT 4
unsigned long moveTimer;
int randNumber;
unsigned long buttonTimer; //timer to make sure multiple button presses do not occur
Player me(&tft, player);

void setup() {
  Serial.begin(115200); //for debugging if needed.
  pinMode(IUD, INPUT_PULLUP); //set input pin as an input!
  pinMode(ILR, INPUT_PULLUP); //set input pin as an input!
  pinMode(BUTTON_1,INPUT_PULLUP);
  pinMode(BUTTON_2,INPUT_PULLUP);
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
  string server_response = post_request(me.getPlayerName(), " ");
  int token_index = server_response.find('|');
  string player_stats = server_response.substr(0, token_index);
  string test_map = server_response.substr(token_index + 1);
  randNumber = random(0, 11);
  me.drawMap(test_map);
  me.drawStats(player_stats);
  me.drawFlavorText(randNumber);
  moveTimer = millis();
  buttonTimer = millis();
}

void loop() {
      if (digitalRead(BUTTON_2)==0 && (millis() - buttonTimer > 500) && state == MOVE){
          state = QUIT;
          buttonTimer = millis();
      }
      string server_response = action();
      if (server_response.length() > 0){
          Serial.print("server response: ");
          Serial.println(server_response.c_str());
        
          int token_index = server_response.find('|');
          string player_stats = server_response.substr(0, token_index);
          
          string remaining_info = server_response.substr(token_index+1);
          token_index = remaining_info.find('|');
          
          string test_map = remaining_info.substr(0, token_index + 1);
          //string monster_info = remaining_info.substr(token_index+1);

          //if (monster_info.at(0) == 'T') {
            //Serial.println("monster here");
          //} else {
            //Serial.println("monster already killed");
          //}

          Serial.print("monster info");
          //Serial.println(monster_info.c_str());
          
          randNumber = random(0, 11);
          moveTimer = millis();
          me.drawMap(test_map);
          me.drawStats(player_stats);
          me.drawFlavorText(randNumber);
    }
} 

string action(){
  Serial.print("state: ");
  Serial.println(state);
  switch(state){
    case START:
      tft.drawString("Welcome to the Game! Press button to continue.", 0, 0, 1);
      if (digitalRead(BUTTON_1) == 0 && (millis() - buttonTimer > 500)){
          Serial.println("Button has been pressed, starting the game!");
          state = MOVE;
          return post_request(me.getPlayerName(), " ");
      }
      return "";
    case MOVE:
        Serial.println("Trying to move!");
        if (millis() - moveTimer > 1500) {
          int LR = analogRead(ILR);
          int UD = analogRead(IUD);
          Serial.println(LR);
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
            Monster monster(5,10); // dummy monster
            Fight fight(&me, &monster, &tft); // dummy fight
            boolean playerWins = fight.startFight(&monster);
            string action = "fight_result&health=" + me.getHealth();
            if (playerWins) {
              // go to some state
            } else {
              // go to state that wipes player
            }
            return post_request(me.getPlayerName(), action);
          }
     case END:
          state = START;
          return "";
     case QUIT:
          if (digitalRead(BUTTON_1) && (millis() - buttonTimer > 500)){
              state = START;
              buttonTimer = millis();
              
          }
          else if (digitalRead(BUTTON_1) && (millis() - buttonTimer > 500)){
              state = MOVE;
              buttonTimer = millis();
          }
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
