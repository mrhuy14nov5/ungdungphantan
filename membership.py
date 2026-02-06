import time
import threading
from protocol import send_msg
from config import NODES, HEARTBEAT_INTERVAL

alive = {i: True for i in range(len(NODES))}

def heartbeat(node_id):
    while True:
        for i, node in enumerate(NODES):
            if i == node_id:
                continue
            try:
                send_msg(node, {"type": "PING"})
                alive[i] = True
            except:
                alive[i] = False
        time.sleep(HEARTBEAT_INTERVAL)
