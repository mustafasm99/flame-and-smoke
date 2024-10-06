#include "esp_camera.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char* ssid      = "Ares_Wifi";
const char* password  = "SM99sm99";
bool streaming = false;

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  Serial.println("Scanning for available networks...");

  // Start scanning for networks
  int networksFound = WiFi.scanNetworks();

  if (networksFound == 0) {
    Serial.println("No networks found");
  } else {
    Serial.printf("%d networks found:\n", networksFound);
    for (int i = 0; i < networksFound; ++i) {
      Serial.printf("%d: %s (Signal: %d dBm)\n", i + 1, WiFi.SSID(i).c_str(), WiFi.RSSI(i));
    }
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.printf("Connecting to ....");
  }
  Serial.println("Connected to WiFi");

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t *s = esp_camera_sensor_get();
  Serial.printf("Camera Model: %u\n", s->id);

  server.on("/video", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send_P(200, "text/html", "<html><body><img src='/video_feed'></body></html>");
  });

 server.on("/video_feed", HTTP_GET, [](AsyncWebServerRequest *request) {
    AsyncWebServerResponse *response = request->beginResponse(200, "multipart/x-mixed-replace; boundary=frame");
    response->addHeader("Cache-Control", "no-store, private");
    response->addHeader("Access-Control-Allow-Origin", "*");

    while (true) {
      camera_fb_t *fb = esp_camera_fb_get();
      if (!fb) {
        Serial.println("Camera capture failed");
        break;
      }

      response->write((const char *)fb->buf, fb->len, "image/jpeg");
      esp_camera_fb_return(fb);
      delay(10); // Adjust the delay as needed for the desired frame rate
    }

    request->send(response);
  });

  server.begin();
}

void loop() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Serve the image on "/video_feed"
 

  esp_camera_fb_return(fb);

  delay(1000);
}
