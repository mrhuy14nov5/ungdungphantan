from protocol import send_msg
from config import NODES
import random

def send(cmd):
    node = random.choice(NODES)
    print(send_msg(node, cmd))

while True:
    x = input(">>> ").split()

    if x[0] == "put":
        send({"type":"PUT","key":x[1],"value":x[2]})
    elif x[0] == "get":
        send({"type":"GET","key":x[1]})
