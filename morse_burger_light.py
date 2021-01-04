import sys
import cv2
import numpy as np
import urllib.request
import time

morse_code = [1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1]
mores_input_image = []

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


class MorseImageDecoder(object):
    def __init__(self, image_list):
        self.morseCodeData = {'01': 'A', '1000': 'B', '1010': 'C', '100': 'D', '0': 'E', '0010': 'F', '110': 'G', '0000': 'H', '00': 'I', '0111': 'J', '101': 'K', '0100': 'L', '11': 'M', '10': 'N', '111': 'O', '0110': 'P', '1101': 'Q', '010': 'R',
                              '000': 'S', '1': 'T', '001': 'U', '0001': 'V', '011': 'W', '1001': 'X', '1011': 'Y', '1100': 'Z', '01111': '1', '00111': '2', '00011': '3', '00001': '4', '00000': '5', '10000': '6', '11000': '7', '11100': '8', '11110': '9', '00000': '0'}

        # test url :"https://raw.githubusercontent.com/frank870622/SYSTEM-DESIGN-AND-APPLICATIONS-OF-INTERNET-OF-THINGS/main/image_b.png"
        
        self.image = []
        for image_in in image_list:
            self.image.append(image_in)
        

        self.finalData = []
        self.changeSizeflag = 0

    def filterImage(self):
        for i in range(0, len(self.image)):
            print(self.image[i].shape)

            grayImage = cv2.cvtColor(self.image[i], cv2.COLOR_BGR2GRAY)
            #cv2.imshow('Gray Image', grayImage)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            self.image[i] = grayImage

    def mainAlgo(self):
        count_on = 0
        count_off = 0
        word_count = ''

        for i in range(0, len(self.image)):
            frame = self.image[i]
            #print('frame: ' + str(frame[225][225]))
            #cv2.imshow(str(i), self.image[i])
            #cv2.waitKey()

            if frame[225][225] <= 125:
                #the light is on

                if count_off > 0:
                    count_off = 0

                count_on += 1
            else:
                #the light is off
                if count_on > 0:
                    if count_on > 1:
                        word_count += '1'
                    else:
                        word_count += '0'
                    count_on = 0

                count_off += 1
                
                
                # next word
                if count_off > 1:
                    count_off = 0

                    if word_count != '':
                        #print('word_count: ' + word_count)
                        self.finalData.append(self.morseCodeData[word_count])
                    word_count = ''

    def printFinalData(self):
        for item in self.finalData:
            print(item)


def find_keypoint(input_keypoint):
    max_x = 0
    min_x = 99999
    max_y = 0
    min_y = 99999
    for a, b in input_keypoint:
        if a > max_x:
            max_x = a
        if a < min_x:
            min_x = a
        if b > max_y:
            max_y = b
        if b < min_y:
            min_y = b
    return max_x, min_x, max_y, min_y


def cut_picture(input_obj):
    for i in range(0, len(input_obj.image)):
        frame = input_obj.image[i]

        frame = cv2.convertScaleAbs(frame)

        params = cv2.SimpleBlobDetector_Params()
        params.minArea = 30.0
        params.maxArea = 100000.0
        params.filterByCircularity = True
        params.minCircularity = 0.83
        params.filterByArea = True
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(frame)

        print(keypoints)

        all_keypoints = []
        for each_key in keypoints:
            keyx, keyy = each_key.pt
            keyx, keyy = int(keyx), int(keyy)
            print([keyx, keyy])
            all_keypoints.append([keyx, keyy])

        print(all_keypoints)
        max_keypoint_x, min_keypoint_x, max_keypoint_y, min_keypoint_y = find_keypoint(
            all_keypoints)
        keypoints = [[min_keypoint_x, min_keypoint_y], [max_keypoint_x, min_keypoint_y], [
            max_keypoint_x, max_keypoint_y], [min_keypoint_x, max_keypoint_y]]
        print(keypoints)
        """
        for each_key in keypoints:
            keyx, keyy = each_key
            keyx, keyy = int(keyx), int(keyy)
            cv2.rectangle(frame, (keyx-5, keyy-5),
                        (keyx+5, keyy+5), (0, 0, 255), 2)
            frame = cv2.line(frame, (keyx-5, keyy), (keyx+5, keyy), [0, 0, 255], 2)
            frame = cv2.line(frame, (keyx, keyy-5), (keyx, keyy+5), [0, 0, 255], 2)
            print([keyx, keyy])
            """
        # print(keypoints[0])
        # im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), flags = 0)

        retval, mask = cv2.findHomography(np.float32(
            keypoints), np.float32([[0, 0], [550, 0], [550, 550], [0, 550]]))
        dst = cv2.warpPerspective(src=frame, M=retval, dsize=(550, 550))

        input_obj.image[i] = dst[25:525, 25:525]
        #cv2.imshow(str(i), input_obj.image[i])
        #cv2.waitKey()
    


def mos_burger():
    obj = MorseImageDecoder(mores_input_image)
    cut_picture(obj)

    obj.filterImage()
    obj.mainAlgo()
    obj.printFinalData()

def load_image():
    for dot in morse_code:
        if dot == 1:
            mores_input_image.append(cv2.imread('./image_on.png'))
            mores_input_image.append(cv2.imread('./image_off.png'))
        elif dot == 2:
            mores_input_image.append(cv2.imread('./image_on.png'))
            mores_input_image.append(cv2.imread('./image_on.png'))
            mores_input_image.append(cv2.imread('./image_off.png'))
        elif dot == 0:
            mores_input_image.append(cv2.imread('./image_off.png'))
            mores_input_image.append(cv2.imread('./image_off.png'))
        else:
            print('error in load image')
    mores_input_image.append(cv2.imread('./image_off.png'))


if __name__ == "__main__":
    #imput_url = sys.argv[1]
    load_image()
    mos_burger()
