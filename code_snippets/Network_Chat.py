# This snippet of the code was written for my bigger project.

import socket
import select
import pickle
import re

# Start server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
host = '127.0.0.1'
port = 12345
server.bind((host, port))
server.listen(4)

is_readable = [server]
is_writable = []
is_err = []
message_list = {}
print('Server is up and running !')
while True:
    ready_to_read, ready_to_write, soc_err = select.select(is_readable, is_writable, is_err, 0.5)
    for soc in ready_to_read:
        if soc is server:
            conn, addr = soc.accept()
            conn.setblocking(0)
            is_readable.append(conn)
        else:
            if soc not in is_writable:
                is_writable.append(soc)
            data = soc.recv(1024)
            if data:
                # Look for code: 0001 = message, 0002 = pickled object
                # Code system ensures that the server and client will know what to do
                # and how to translate the data.
                lookfor_code = re.search(b'^0001|^0002', data)
                if lookfor_code:
                    if data[:5] == b'0001 ':
                        message_list[soc] = data
                        print(data[5:])
                    elif data[:5] == b'0002 ':
                        processed_data = pickle.loads(data)
            print(message_list)
        for soc in is_writable:
            if message_list:
                for message in message_list:
                    soc.send(message_list[message])
        message_list.clear()
