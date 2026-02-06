import socket, json

def send_msg(addr, msg):
    s = socket.socket()
    s.connect(addr)
    s.send(json.dumps(msg).encode())
    data = s.recv(65536)
    s.close()
    return json.loads(data.decode())

def recv_msg(conn):
    data = conn.recv(65536)
    return json.loads(data.decode())
