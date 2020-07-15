import socket
import os
import sys
import struct
import cv2
import numpy as np
from Config import opt




def ClientSender():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((opt.serverip, opt.port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(">>>>> Connect Success!")



    while 1:
        print(">>>>> Taking Pic And Send.")
        capture = cv2.VideoCapture(2)
        ret, frame = capture.read()
        encodeParam = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
        result, imgencode = cv2.imencode('.jpg', frame, encodeParam)
        data = np.array(imgencode)
        stringData = data.tostring()
        fhead = struct.pack('l', len(stringData))
        s.send(fhead)
        s.sendall(stringData)
        print('>>>>> Send Over.')





if __name__ == '__main__':
    ClientSender()

