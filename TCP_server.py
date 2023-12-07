import socket
import os
import time


def receive_file(conn):
    buffer_size = 4096
    data = b""
    save_list = 'saved_file.txt'
    while True:
        chunk = conn.recv(buffer_size)
        if not chunk:
            break
        data += chunk
        # Check for "END" marker
        if b"END" in data:
            start_index = data.find(b"START")
            data_index = data.find(b"DATA")
            time_index = data.find(b"TIME\n")
            end_index = data.find(b"\nEND\n")

            if start_index != -1 and end_index != -1:
                start_index += len(b"START")
                data_indext = data_index+ len(b"DATA")
                filename = data[start_index:data_index].decode()
                pre_time = data [data_indext:time_index].decode()
                file_data = data[time_index+len(b"TIME\n"):end_index]
                pro_time = round(time.time()*1000000)
                # Save the file
                with open(filename, "wb") as file:
                    file.write(file_data)
                with open(save_list, "a") as save_list_file:
                    curr_time = round(time.time()*1000000)
                    con_time=curr_time-int(pre_time)
                    print(curr_time)
                    print(pre_time)
                    print(con_time)
                    data = filename  + " " + str(con_time) + " " + str(curr_time-pro_time) + '\n'
                    save_list_file.write(data)
                print(f"File '{filename}' received and saved.")
                data = b""  # Reset data for the next file

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(1)

    print(f"Server listening on {host}:{port}")

    conn, addr = server_sock.accept()
    print(f"Connection from {addr}")

    receive_file(conn)


    conn.close()
    server_sock.close()
