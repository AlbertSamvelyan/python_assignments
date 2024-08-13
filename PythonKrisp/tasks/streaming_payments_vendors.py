from threading import Thread
from queue import Queue

def stream_payments(callback_fn):
    for i in range(10):
        callback_fn(i)


def store_payments(amount_iterator):
    for i in amount_iterator:
        print(i)


def callback_example(amount):
    print(amount)
    return True

class PaymentProcessor:

    class EndTag:
        pass

    def __init__(self, bufferSize, stream_function, store_function):
        self.bufer = Queue(bufferSize)
        self.producer = Thread(target = stream_function, args = [self._callback])
        self.consumer = Thread(target = store_function, args = [self])
        self.producer.start()
        self.consumer.start()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.bufer.get()
        if type(item) is PaymentProcessor.EndTag:
            raise StopIteration
        return item
    
    def _callback(self, amount):
        self.bufer.put(amount)


    def waitForComletion(self):
        self.producer.join()
        self.bufer.put(PaymentProcessor.EndTag())
        self.consumer.join()


def process_payments_2():
    processor = PaymentProcessor(1, stream_payments, store_payments)
    processor.waitForComletion()

process_payments_2()