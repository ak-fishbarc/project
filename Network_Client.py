import socket
import asyncio
import re
import pickle

client = socket.socket(socket.AF_INET)
server_addr = '127.0.0.1'
port = 12345
message = ''

# This was a temporary solution for testing. Main code is not using this sort of user input.
nickname = input('Type in your nickname: ')

try:

  async def write_message(message):
    if message:
        client.send(message)
    await asyncio.sleep(0.5)


  async def listen_to_server():
    try:
        data = client.recv(1024)
        lookfor = re.search(b'^0001|^0002', data)
        if lookfor:
            if data[:5] == b'0001 ':
                clean_data = data[5:]
                print(str(clean_data, errors='ignore'))
            if data[:5] == b'0002 ':
                clean_data = data[5:]
                processed_data = pickle.loads(clean_data)
    except Exception:
        await asyncio.sleep(0.5)
except Exception as e:
    print(e)
client.connect((server_addr, port))
client.send(b'0001 ' + bytes(nickname, 'utf-8') + b' said: Hello from Hawaii')

while True:
    client.setblocking(0)
    asyncio.run(write_message(message))
    asyncio.run(listen_to_server())