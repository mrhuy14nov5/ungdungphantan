from protocol import send_msg

def recover(storage, self_id, nodes):
    for i, node in enumerate(nodes):
        if i == self_id:
            continue
        try:
            snap = send_msg(node, {"type": "SNAPSHOT_REQ"})
            storage.load(snap["data"])
            return
        except:
            pass
