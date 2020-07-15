import socket
import threading
import sys
import struct
from os import path
import io
from PIL import Image
import numpy as np
from Config import opt
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import time



def ServerReceiver():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((opt.serverip, opt.port))
        s.listen(5)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('>>>>> Waiting')

    conn, addr = s.accept()
    dealData(conn, addr)

    # while 1:
    #     conn, addr = s.accept()
    #     dealData(conn, addr)
        # print('>>>>>', conn, addr)
        # t = threading.Thread(target=dealData, args=(conn, addr))
        # t.start()

def dealData(conn, addr):
    print('>>>>> Accept new connection from', addr)
    while 1:
        fileInfoSize = struct.calcsize('i')
        buf = conn.recv(fileInfoSize)
        if buf:
            fileSize = struct.unpack('i', buf)[0]
            recvdSize = 0
            img = b''
            while not recvdSize == fileSize:
                if fileSize - recvdSize > 1024:
                    data = conn.recv(1024)
                    recvdSize += len(data)
                else:
                    data = conn.recv(fileSize - recvdSize)
                    recvdSize = fileSize
                img += data
            print(">>>>> Received One Image.")
            image = Image.open(io.BytesIO(img))
            fileName = './res/%s.jpg' % str(time.time()).split('.')[0]
            image.save(fileName)
            print(">>>>> Saved One Image As ", fileName)
            # Image._show(image)

        # conn.close()
        # break

if __name__ == '__main__':
    ServerReceiver()