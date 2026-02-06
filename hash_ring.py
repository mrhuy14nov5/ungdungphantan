import hashlib

class HashRing:
    def __init__(self, nodes):
        self.nodes = nodes

    def hash(self, key):
        return int(hashlib.sha1(key.encode()).hexdigest(), 16)

    def get_replicas(self, key, n):
        h = self.hash(key)
        start = h % len(self.nodes)
        return [(start + i) % len(self.nodes) for i in range(n)]
