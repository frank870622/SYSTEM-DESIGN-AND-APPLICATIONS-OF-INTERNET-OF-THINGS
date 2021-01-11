import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time
import threading

match_flag = 0

def server_func():
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()

    # 設定登入帳號密碼
    client.username_pw_set("try","xxxx")

    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("140.116.82.164", 1883, 60)

    while True:
        payload = 'SOS'
        print (payload)
        #要發布的主題和內容
        client.publish("Try/MQTT", payload)
        time.sleep(5)

def answer_func():
    time.sleep(5)
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()

    # 設定登入帳號密碼
    client.username_pw_set("try","xxxx")

    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("140.116.82.164", 1883, 60)
    global match_flag
    while True:
        payload = {}
        if match_flag == 1:
            payload = {'do' : 'the answer is corret'}
            print (json.dumps(payload))
            client.publish("Answer/MQTT", json.dumps(payload))
            time.sleep(5)
        elif match_flag == 2:
            payload = {'do' : 'the answer is wrong'}
            print (json.dumps(payload))
            client.publish("Answer/MQTT", json.dumps(payload))
            time.sleep(5)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe("Try/MQTT")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    print(msg.topic+" "+ msg.payload.decode('utf-8'))
    global match_flag
    if 'SOS' in msg.payload.decode('utf-8'):
        match_flag = 1
    else:
        match_flag = 2

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
    client.connect("140.116.82.164", 1883, 60)
    #client.connect("127.0.0.1", 1883, 60)

    # 開始連線，執行設定的動作和處理重新連線問題
    # 也可以手動使用其他loop函式來進行連接
    client.loop_forever()


if __name__ == "__main__":
    t1 = threading.Thread(target = client_func)
    t1.start()
    #t2 = threading.Thread(target = server_func)
    #t2.start()

    answer_func()

    t1.join()
    #t2.join()

    print('done')

    




