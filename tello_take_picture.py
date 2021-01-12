import cv2
from djitellopy import Tello
from morse_burger_light_base64 import load_image_base64, mos_burger
import threading
import time
import paho.mqtt.client as mqtt


image_list = []
answer_flag = 0
final_command = ''
final_answer = ''

def main():
    tello = Tello()
    tello.connect()

    tello.streamon()

    global image_list
    while len(image_list) < 30:
        frame_read = tello.get_frame_read()
        if frame_read.frame.shape[0] > 0:
            image_list.append(frame_read.frame)
    #cv2.imshow("picture.png", frame_read.frame)

    load_image_base64(image_list)
    mos_burger()

    global answer_flag
    global final_command
    global final_answer # final answer = 'SOS'
    answer_flag = 1
    

    while len(final_command) <= 0:
        time.sleep(1)
    # publish answer
    # subscribe command

    tello.takeoff()
    if 'corret' in final_command:
        tello.move_left(50)
    else:
        tello.move_left(50)

    tello.land()

    tello.end()


def server_func():
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()

    # 設定登入帳號密碼
    client.username_pw_set("try","xxxx")

    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("127.0.0.1", 1883, 60)
    global answer_flag

    while True:
        if answer_flag == 1:
            global final_answer
            payload = final_answer
            print (payload)
            #要發布的主題和內容
            client.publish("Try/MQTT", payload)
            time.sleep(5)
            break

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe("Answer/MQTT")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    print(msg.topic+" "+ msg.payload.decode('utf-8'))
    global final_command
    if len(msg.payload.decode('utf-8')) > 0:
        final_command = msg.payload.decode('utf-8')

def client_func():
    time.sleep(5)
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()

    # 設定連線的動作
    client.on_connect = on_connect

    # 設定接收訊息的動作
    client.on_message = on_message

    # 設定登入帳號密碼
    client.username_pw_set("try","xxxx")

    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("127.0.0.1", 1883, 60)
    #client.connect("127.0.0.1", 1883, 60)

    # 開始連線，執行設定的動作和處理重新連線問題
    # 也可以手動使用其他loop函式來進行連接
    client.loop_forever()        
    
if __name__ == "__main__":
    t1 = threading.Thread(target = server_func)
    t1.start()
    t2 = threading.Thread(target = client_func)
    t2.start()



    main()

    t1.join()
    t2.join()