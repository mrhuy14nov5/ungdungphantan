from protocol import send_msg

def replicate(nodes, msg):
    responses = []
    for n in nodes:
        try:
            res = send_msg(n, msg)
            responses.append(res)
        except:
            pass
    return responses
