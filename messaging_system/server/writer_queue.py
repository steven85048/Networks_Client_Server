# This class handles the queueing of writer jobs sent from the request handler, and
# handles locking of the queue as necessary; the writer job will continually listen for new pushes
# to this class

class WriterQueue:
    def __init__(self):
        pass