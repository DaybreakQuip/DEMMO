#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include <HTTPClient.h>
#include "Player.cpp"
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
char network[] = "MIT";  //SSID for 6.08 Lab
String player = "Ze";
//char password[] = "iesc6s08"; //Password for 6.08 Labconst uint8_t IUD = 32; //pin connected to button
const uint8_t IUD = 32; //pin connected to button 
const uint8_t ILR = 33; //pin connected to button 
int state = 0;
MPU9255 imu; //imu object called, appropriately, imu
#define MOVE 0 //state of player's action
#define FIGHT 1 //state of player's action
int flag = 0;

Player ze(&tft, 11, 5, 3, 10);

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
  Serial.print("AtUDting to connect to ");
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

}

void loop() {
    action();
    delay(1000);
    if (flag == 0) {
      // change server_response when implemented
      String server_response = "11, 5, 3, 10,|M_,__,__,__,_P,__,__,M_,__,";
      // String test_map = "M_,__,__,__,_P,__,__,M_,__,";
      int token_index = server_response.indexOf('|');
      String player_stats = server_response.substring(0, token_index);
      String test_map = server_response.substring(token_index + 1);
      String story = "Once upon a time, Ze was thrown into a dungeon";
      ze.drawMap(test_map, story);
      flag = 1;
    }
}

void action(){
  switch(state){
    case MOVE:
      int LR = analogRead(ILR);
      int UD = analogRead(IUD);
      if (LR >= 3000){
        post_request("right");
      }
      else if (LR < 1000){
        post_request("left");

      }
      else if (UD >= 3000){
        post_request("down");
      }
      else if (UD < 1000){
        post_request("up");
      }
      break;
    }
}
String post_request(String action){
  HTTPClient http;
  http.begin("http://608dev.net/sandbox/sc/zehang/DEMMO/request_handler.py");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
  int httpResponseCode = http.POST("player_id=" + player + "&action=" + action);
  if(httpResponseCode>0){
    String response = http.getString();
    return response;
  }
  else{
    return "Error on sending POST: ";
  }
  http.end();
}
