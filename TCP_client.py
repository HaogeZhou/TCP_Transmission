import socket
import os
import time
from time import sleep

def send_file(sock, filename):
    
    try:
        curr_time = round(time.time()*1000000)
        with open(filename, "rb") as file: 
            data = b"START" +filename.encode()+ b"DATA"+ repr(curr_time).encode() + b"TIME\n" + file.read() + b"\nEND\n"
            sock.sendall(data)
        end_time = round(time.time()*1000000)

    except IOError:
        print(f'Error reading file: {filename}')

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    files_list_filename = '/home/haoge/UDP/00_KF_BIN/allKFs.txt'
    save_list = "send_files.txt"
    try:
        with open(files_list_filename, "r") as files_list_file:
            file_names = files_list_file.read().splitlines()

        for filename in file_names:
            curr_time = round(time.time()*1000000)
            send_file(sock, filename+ ".bin")
            end_time = round(time.time()*1000000)
            with open(save_list, "a") as save_list_file:
                con_time=end_time-curr_time
                # print(con_time)
                data = filename+".bin"  + " " + str(con_time) + '\n'
                save_list_file.write(data)
            sleep(0.05)
    except IOError:
        print(f'Error reading file list: {files_list_filename}')

    sock.close()
