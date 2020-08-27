from blinker import signal
import uuid


class RetrySignal(object):
    def __init__(self):
        self.name = uuid.uuid5(uuid.NAMESPACE_DNS, 'crawl_signal')
        self.retry = False
        self._signal = signal(self.name)
        self._signal.connect(self._signal_subscriber)

    def send(self, retry=False):
        self._signal.send(self, retry=retry)

    def _signal_subscriber(self, sender, retry=False):
        self.retry = retry

    def __del__(self):
        self._signal.disconnect(self._signal_subscriber)


