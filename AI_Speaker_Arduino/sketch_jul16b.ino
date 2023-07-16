#include <Adafruit_NeoPixel.h>

const int buttonPin1 = 4; //  4 번핀 스위치 입력 테스트 (PLC의 ready신호)
#define LED_PIN 6     //네오픽셀에 신호를 줄 핀번호
#define LED_COUNT 60  //아두이노에 연결된 네오픽셀의 개수  
int flag = 0;

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN);

void setup() {
  Serial.begin(9600);              //  시리얼 통신의 시작, 보레이트 입력
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // 네오픽셀에 빛을 출력하기 위한 것인데 여기서는 모든 네오픽셀을 OFF하기 위해서 사용한다.
  strip.setBrightness(50); // 네오픽셀의 밝기 설정(최대 255까지 가능)
}

void rainbow(int wait) {  
  for (long firstPixelHue = 0; firstPixelHue < 5 * 65536; firstPixelHue += 256) {
    for (int i = 0; i < strip.numPixels(); i++) { 
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());      
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show();
    delay(wait);
  }
}

void loop() {
  char c = Serial.read();           //  PC로부터온 값을 읽음.
  int buttonValue1 = digitalRead(4); //  4번 핀에서 읽음.
  
  if(buttonValue1 == HIGH )           //  스위치가 눌릴때 ready신호를 보냄. (PLC -> PC)
  {
    flag = 1;
  }
  if(flag == 1)
  {
      Serial.println("ready");  //  준비가 되었다고 PC에 신호를 보냄.
      rainbow(10);
      delay(500);
      flag = 0;
  }
}
