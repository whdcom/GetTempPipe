import win32file
import win32pipe
import struct
import threading
import cv2
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import time
# from ishow import ishow
path=r"D:\vs\GuTest\x64\Release\GuTest.exe"
def recv_pipe(PIPE_NAME, PIPE_BUFFER_SIZE):
    while True:
        named_pipe = win32pipe.CreateNamedPipe(PIPE_NAME,
                                               win32pipe.PIPE_ACCESS_DUPLEX,
                                               win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_MESSAGE,
                                               win32pipe.PIPE_UNLIMITED_INSTANCES,
                                               PIPE_BUFFER_SIZE,
                                               PIPE_BUFFER_SIZE, 500, None)
        try:
            while True:
                try:
                    win32pipe.ConnectNamedPipe(named_pipe, None)
                    # os.system(path)
                    data = win32file.ReadFile(named_pipe, PIPE_BUFFER_SIZE, None)
                    if data is None:
                        continue
                    # print("Received msg:", data)
                    #将C++传来的二进制数据进行格式化为字符串数据相当于元组字符串,<表示小端内存存储，而>表示大端内存存储
                    recv_msg = struct.unpack('<245759s', data[1])
                    #对二进制字符串进行解码
                    recv_msg = recv_msg[0].decode("utf-8")
                    list = []
                    arr = recv_msg.split(',')
                    list.append(arr)
                    list = np.array(list)
                    list = list.astype(float)
                    list = np.array(list).reshape((192, 256))
                    # recv_msg = recv_msg[0].split(',')
                    # recv_msg = np.array(recv_msg)
                    print("Parsed list message:", list)

                    plt.imshow(list, interpolation=None, cmap=plt.cm.gray, origin='upper')
                    plt.colorbar()
                    plt.axis('off')
                    #plt.show()
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    print(timestr)
                    # list = cv2.cvtColor(list, cv2.COLOR_BGR2GRAY)
                    with open("cup"+timestr+".txt",'w') as f:
                        f.write(str(recv_msg))
                        f.close()
                    # plt.imsave('cup'+timestr+'.png',list)
                    # ishow(recv_msg)
                except BaseException as e:
                    print("Exception1:", e)
                    break
        finally:
            try:
                win32pipe.DisconnectNamedPipe(named_pipe)
            except BaseException as e:
                print("Exception2:", e)
                break
# //启动程序
def run():
    os.system(path)

if __name__ == "__main__":
    pipe_name = r"\\.\pipe\test_pipe"
    pipe_buffer_size = 245759
    receive_thread = threading.Thread(target=recv_pipe, args=(pipe_name, pipe_buffer_size))
    write_thread = threading.Thread(target=run)
    write_thread.start()
    receive_thread.start()