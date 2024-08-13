import os

def get_payments_storage():
    if os.name == 'nt':  # Windows
        return open(os.devnull, 'wb')
    else:  # Unix-like
        return open('/dev/null', 'wb')

def stream_payments_to_storage(storage):
    for i in range(10):
        storage.write(bytes([1, 2, 3, 4, 5]))

class Wrapper:
    def __init__(self, storage):
        self.storage = storage
        self.hash = 0

    def __enter__(self):
        self.hash = 0
        return self

    def __exit__(self, *args):
        print(self.hash)

    def write(self, bytes):
        for b in bytes:
            self.hash = self.hash + b
        self.storage.write(bytes)

def process_payments():
    with Wrapper(get_payments_storage()) as wrapper:
        stream_payments_to_storage(wrapper)


process_payments()