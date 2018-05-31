from time import sleep
from flask import Flask, render_template, request, jsonify, Response
import paho.mqtt.client as mqtt
from RPi.GPIO as GPIO
# from camera_pi import Camera
from camera import Camera

app = Flask(__name__)

# GPIO 設定
GPIO.setwarning(False)
GPIO.setmode(GPIO.BCM)

# GPIO 腳位號碼
IN1 = 18
IN2 = 23
IN3 = 24
IN4 = 25 

delay = 1

# 定義一個馬達類別，之後可對各個馬達進行操作
class Motor:
    
    def __init__(self, positive=positive, negative=negative):
        self.positive = positive
        self.negative = negative
        GPIO.setup(self.positive, GPIO.OUT)
        GPIO.setup(self.negative, GPIO.OUT)
    
    def forward(self):
        GPIO.output(self.positive, True)
        GPIO.output(self.negative, False)
        
    def backward(self):
        GPIO.output(self.positive, False)
        GPIO.output(self.negative, True)
        
    def stop(self):
        GPIO.output(self.positive, False)
        GPIO.output(self.negative, False)

# 建立兩個 Motor 實例，分別是左右輪的馬達
left_motor = Motor(positive=IN1, negative=IN2)
right_motor = Motor(positive=IN3, negative=IN2)

# 後續所有的 route 方向操作，只要被此 decorator 修飾，都會休息一秒後停止
def decorate_direction(func, delay=1):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        sleep(delay)
        left_motor.stop()
        right_motor.stop()
        return result
    return wrapper

def generate_streaming(camera):
    """
    一個 generator，持續送出最新的影像
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def createImage(filename):
#     camimage = cv2.VideoCapture(0)
#     if camimage.isOpened():
#         ret, img = camimage.read()
#         # 此處可能用讀檔的方式,或是有辦法持續傳遞鏡頭的圖像
#         bytearray(img)

@app.route('/')
def index():
    """
    home page!
    """
    platform = request.user_agent.platform
    if platform == 'android' or platform == 'iphone':
        return render_template('mobile.html')
    return render_template('index.html')

@app.route('/stop')
def go_stop():
    left_motor.stop()
    right_motor.stop()
    return 'stop'

@app.route('/forward')
@decorate_direction()
def go_forward():
    left_motor.forward()
    right_motor.forward()
    return 'forward'

@app.route('/backward')
@decorate_direction()
def go_backward():
    left_motor.backward()
    right_motor.backward()
    return 'backward'

@app.route('/right')
@decorate_direction()
def go_turn_right():
    left_motor.forward()
    right_motor.stop()
    return 'turn_right'

@app.route('/left')
@decorate_direction()
def go_turn_left():
    left_motor.stop()
    right_motor.forward()
    return 'turn_left'

@app.route('/video')
def get_video():
    """
    回傳一個 Response，內容是影像
    """
    return Response(generate_streaming(Camera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)


