import socket, threading, sys, json
from storage import Storage
from hash_ring import HashRing
from replication import replicate
from quorum import quorum_write, quorum_read
from membership import heartbeat
from recovery import recover
from protocol import recv_msg
from config import *

# Khởi tạo Node ID từ tham số dòng lệnh
NODE_ID = int(sys.argv[1])

storage = Storage()
ring = HashRing(NODES)

# Tự động phục hồi dữ liệu khi khởi động lại
recover(storage, NODE_ID, NODES)
# Chạy luồng kiểm tra trạng thái các node khác (Heartbeat)
threading.Thread(target=heartbeat, args=(NODE_ID,), daemon=True).start()

def handle(conn):
    try:
        msg = recv_msg(conn)
        t = msg["type"]

        # --- Xử lý ghi dữ liệu ---
        if t == "PUT":
            key = msg["key"]
            replicas = ring.get_replicas(key, REPLICATION_FACTOR)
            responses = replicate([NODES[r] for r in replicas],
                                  {"type": "LOCAL_PUT", "key": key, "value": msg["value"]})
            ok = quorum_write(responses, WRITE_QUORUM)
            conn.send(json.dumps({"status": "OK" if ok else "FAIL"}).encode())

        elif t == "LOCAL_PUT":
            storage.put(msg["key"], msg["value"])
            conn.send(json.dumps({"ok": 1}).encode())

        # --- Xử lý đọc dữ liệu ---
        elif t == "GET":
            key = msg["key"]
            replicas = ring.get_replicas(key, REPLICATION_FACTOR)
            values = []
            for r in replicas:
                try:
                    # Lấy từ bộ nhớ cục bộ nếu là chính mình, ngược lại hỏi node khác
                    v = storage.get(key) if r == NODE_ID else \
                        replicate([NODES[r]], {"type": "LOCAL_GET", "key": key})[0]
                    values.append(v)
                except:
                    pass
            result = quorum_read(values)
            conn.send(json.dumps({"value": result}).encode())

        elif t == "LOCAL_GET":
            val = storage.get(msg["key"])
            conn.send(json.dumps(val).encode())

        # --- Xử lý xóa dữ liệu (MỚI BỔ SUNG) ---
        elif t == "DELETE":
            key = msg["key"]
            replicas = ring.get_replicas(key, REPLICATION_FACTOR)
            responses = replicate([NODES[r] for r in replicas],
                                  {"type": "LOCAL_DELETE", "key": key})
            ok = quorum_write(responses, WRITE_QUORUM)
            conn.send(json.dumps({"status": "OK" if ok else "FAIL"}).encode())

        elif t == "LOCAL_DELETE":
            storage.delete(msg["key"])
            conn.send(json.dumps({"ok": 1}).encode())

        # --- Quản lý hệ thống ---
        elif t == "SNAPSHOT_REQ":
            conn.send(json.dumps({"data": storage.snapshot()}).encode())

        elif t == "PING":
            conn.send(json.dumps({"alive": 1}).encode())

    except Exception as e:
        print(f"Lỗi xử lý request: {e}")
    finally:
        conn.close()

def server(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Cho phép chạy lại port nhanh
    s.bind(("localhost", port))
    s.listen()
    print(f"Node {NODE_ID} đang chạy tại port {port}...")

    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn,)).start()

if __name__ == "__main__":
    server(NODES[NODE_ID][1])