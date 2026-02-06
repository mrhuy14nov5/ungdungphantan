import socket, threading, sys
from storage import Storage
from hash_ring import HashRing
from replication import replicate
from quorum import quorum_write, quorum_read
from membership import heartbeat
from recovery import recover
from protocol import recv_msg
from config import *

NODE_ID = int(sys.argv[1])

storage = Storage()
ring = HashRing(NODES)

recover(storage, NODE_ID, NODES)
threading.Thread(target=heartbeat, args=(NODE_ID,), daemon=True).start()

def handle(conn):
    msg = recv_msg(conn)
    t = msg["type"]

    if t == "PUT":
        key = msg["key"]
        replicas = ring.get_replicas(key, REPLICATION_FACTOR)

        responses = replicate([NODES[r] for r in replicas],
                              {"type": "LOCAL_PUT", "key": key, "value": msg["value"]})

        ok = quorum_write(responses, WRITE_QUORUM)
        conn.send(b'{"status":"OK"}' if ok else b'{"status":"FAIL"}')

    elif t == "LOCAL_PUT":
        storage.put(msg["key"], msg["value"])
        conn.send(b'{"ok":1}')

    elif t == "GET":
        key = msg["key"]
        replicas = ring.get_replicas(key, REPLICATION_FACTOR)

        values = []
        for r in replicas:
            try:
                v = storage.get(key) if r == NODE_ID else \
                    replicate([NODES[r]], {"type": "LOCAL_GET", "key": key})[0]
                values.append(v)
            except:
                pass

        result = quorum_read(values)
        conn.send(str({"value": result}).encode())

    elif t == "LOCAL_GET":
        conn.send(str(storage.get(msg["key"])).encode())

    elif t == "SNAPSHOT_REQ":
        conn.send(str({"data": storage.snapshot()}).encode())

    elif t == "PING":
        conn.send(b'{"alive":1}')

    conn.close()

def server(port):
    s = socket.socket()
    s.bind(("localhost", port))
    s.listen()

    print("Node", NODE_ID, "running")

    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn,)).start()

server(NODES[NODE_ID][1])
