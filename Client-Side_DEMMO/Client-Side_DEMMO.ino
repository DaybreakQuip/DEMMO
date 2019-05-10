#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include <HTTPClient.h>
#include <string>
using std::string;
#include "Player.cpp"
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
char network[] = "MIT";  //SSID for 6.08 Lab
string player = "Ze";
//char password[] = "iesc6s08"; //Password for 6.08 Labconst uint8_t IUD = 32; //pin connected to button
const uint8_t IUD = 32; //pin connected to button 
const uint8_t ILR = 33; //pin connected to button 
int state = 0;
MPU9255 imu; //imu object called, appropriately, imu
#define START 0
#define MOVE 1 //state of player's action
#define FIGHT 2 //state of player's action
#define END 3
unsigned long timer;
int randNumber;
Player me(&tft);

void setup() {
  Serial.begin(115200); //for debugging if needed.
  pinMode(IUD, INPUT_PULLUP); //set input pin as an input!
  pinMode(ILR, INPUT_PULLUP); //set input pin as an input!
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
  string server_response = post_request(" ");
  int token_index = server_response.find('|');
  string player_stats = server_response.substr(0, token_index);
  string test_map = server_response.substr(token_index + 1);
  randNumber = random(0, 11);
  me.drawMap(test_map);
  me.drawStats(player_stats);
  me.drawFlavorText(randNumber);
  timer = millis();
}

void loop() {
    if (millis() - timer > 1500) {
      string server_response = action();
      if (server_response.length() > 0){
          int token_index = server_response.find('|');
          string player_stats = server_response.substr(0, token_index);
          string test_map = server_response.substr(token_index + 1);
          randNumber = random(0, 11);
          timer = millis();
          me.drawMap(test_map);
          me.drawStats(player_stats);
          me.drawFlavorText(randNumber);
      }
    }
}

string action(){
  switch(state){
    case MOVE:
      int LR = analogRead(ILR);
      int UD = analogRead(IUD);
      Serial.println(LR);
      if (LR >= 3000){
        return post_request("right");
      }
      else if (LR < 1000){
       return post_request("left");

      }
      else if (UD >= 3000){
       return post_request("down");
      }
      else if (UD < 1000){
       return post_request("up");
      }
      else{
        return "";
      }
      break;
    }
}
