import socket
import os
import time
from time import sleep

def send_file(sock, filename):
    curr_time = round(time.time()*1000000)
    try:
        with open(filename, "rb") as file: 
            data = b"START" +filename.encode()+ b"DATA"+ repr(curr_time).encode() + b"TIME\n" + file.read() + b"\nEND\n"
            sock.sendall(data)
    except IOError:
        print(f'Error reading file: {filename}')

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    files_list_filename = '/home/zhangyanyu/UDP/00_MP_TXT/allMPs.txt'

    try:
        with open(files_list_filename, "r") as files_list_file:
            file_names = files_list_file.read().splitlines()

        for filename in file_names:
            
            send_file(sock, filename+ ".txt")
            sleep(0.05)
    except IOError:
        print(f'Error reading file list: {files_list_filename}')

    sock.close()