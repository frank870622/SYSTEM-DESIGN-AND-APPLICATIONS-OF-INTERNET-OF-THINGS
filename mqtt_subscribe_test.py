import paho.mqtt.client as mqtt
import cv2

morse_code = [1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1]
mores_input_image = []
image_num = 0

def load_image():
    for dot in morse_code:
        if dot == 1:
            mores_input_image.append(cv2.resize(cv2.imread('./image_on.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
        elif dot == 2:
            mores_input_image.append(cv2.resize(cv2.imread('./image_on.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
            mores_input_image.append(cv2.resize(cv2.imread('./image_on.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
        elif dot == 0:
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
        else:
            print('error in load image')
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))
            mores_input_image.append(cv2.resize(cv2.imread('./image_off.png'), (800, 800), interpolation=cv2.INTER_CUBIC))


# 當地端程式連線伺服器得到回應時，要做的動作
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
    global image_num
    global mores_input_image
    if image_num < len(mores_input_image):
        cv2.imshow('image', mores_input_image[image_num])
        cv2.waitKey(1)
        image_num += 1
    else:
        black_image = cv2.imread('./black.png')
        cv2.imshow('image', black_image)
        cv2.waitKey(1)
    


if __name__ == "__main__":
    #imput_url = sys.argv[1]
    load_image()
    image_num = 0


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