def quorum_write(responses, required):
    return len([r for r in responses if r]) >= required

def quorum_read(values):
    # chọn value mới nhất theo timestamp
    values = [v for v in values if v]
    if not values:
        return None
    return max(values, key=lambda x: x[1])
