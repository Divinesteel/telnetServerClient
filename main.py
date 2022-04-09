import socket
import threading


def readsentence(line_message, data , last_index,name):
    print(data.decode('utf'))
    decoded_char = data.decode('utf')
    if decoded_char == '\r\n':
        if line_message != '':
            allmes.append(f'{name}:{line_message}')
            last_index+=1;
            line_message = ''
    elif decoded_char == '\x08':
        if len(line_message) > 0:
            line_message = line_message[:-1]
    else:
        line_message += data.decode('utf-8')

    return line_message, last_index

def readname(line_message, data,name):
    print(data.decode('utf'))
    decoded_char = data.decode('utf')
    if decoded_char == '\r\n':
        name = line_message
    elif decoded_char == '\x08':
        if len(line_message) > 0:
            line_message = line_message[:-1]
    else:
        line_message += data.decode('utf-8')

    return line_message, name


allmes = []

host = ''
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))

s.listen(5)
print('Waiting for connection')


def threaded_client(conn):
    print('thread created')
    conn.send(str.encode('Connected to the chatroom! \r\n'))
    conn.send(str.encode('...\r\n..\r\n.\r\n'))
    conn.send(str.encode('Type your name:\r\n'))

    name = ''
    line_message_name=''
    while name == '':
        data = conn.recv(2048)
        line_message_name, name = readname(line_message_name, data,name)

    allmes.append(f'{name} joined the chatroom!\r\n')
    line_message = ''
    last_index = 0
    while True:
        while last_index < len(allmes):
            conn.send(str.encode(allmes[last_index] + '\r\n'))
            last_index += 1;

        data = conn.recv(2048)
        line_message,last_index = readsentence(line_message,data,last_index,name)

        # reply = "So your favorite color is "+data.decode('utf-8')
        if not data:
            break
        # conn.send(str.encode(reply))

    conn.close
    print('connection is closed')
    print(allmes)


while True:
    conn, addr = s.accept()
    print(f'connected to: {addr[0]}:{addr[1]}')
    threading.Thread(target=threaded_client, args=(conn,),daemon=True).start()



