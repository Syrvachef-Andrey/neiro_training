#include "DHT.h"

#define DHTPIN 2     // вывод, к которому подключается датчик
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#include <Servo.h> 
 
Servo myservo;  

int flag = 1;
int pos = 0;    

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(13, OUTPUT);
  pinMode(A1, INPUT);
  Serial.begin(9600);
  dht.begin();
  myservo.attach(9);  
}

void loop() {
  delay(250);

  // считывание температуры или влажности занимает примерно 250 мс!
  // считанные показания могут отличаться от актуальных примерно на 2 секунды (это очень медленный датчик)
  float h = dht.readHumidity();
  // Считывание температуры в цельсиях
  float t = dht.readTemperature();

  // проверяем, были ли ошибки при считывании и, если были, начинаем заново
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
   if (digitalRead(A1) == HIGH) {
      digitalWrite (13, HIGH);
  }
   if (digitalRead(A1) == LOW) {
      digitalWrite (13, LOW);
  }

  //выводим информацию в Монитор последовательного порта
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" *C ");

  if (t >= 30.00 and flag == 1)
  {
    for(pos = 0; pos <= 180; pos += 1)  
  {                                 
    myservo.write(pos);              
    delay(15);                      
  } 
  flag = 0;
  }
  if (t < 30.00 and flag == 0){
    for(pos = 180; pos>=0; pos-=1)     
  {                                
    myservo.write(pos);             
    delay(15);                     
  } 
  flag = 1;
  }
  
}