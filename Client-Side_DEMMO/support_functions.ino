string post_request(string player, string action){
  //Note to self, to convert integer to string: string boss = "Boss: " + string(itoa(numBossDefeated, buffer, 10));
  WiFiClient client;
  string body = "player_id=" + player + "&action=" + action;
  if (client.connect("608dev.net", 80)) {
    client.println("POST http://608dev.net/sandbox/sc/zehang/DEMMO/request_handler.py HTTP/1.1");
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
