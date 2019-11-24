# This class provides an asynchronous mechanism for other classes to change state
# It holds the current state, and allows multiple threads to interact with this state without deadlocking
# The threads that currently interact with this class are:
# (a) The user input thread
# (b) The response listener thread

from threading import Lock

class StateTransitionManager:
    def __init__(self):
        self.curr_state = None
        self.state_lock = Lock()

    def transition_to_state(self, state ):
        with self.state_lock:
            if( not self.curr_state is None and not self.curr_state.state_transition_permitted() ):
                raise Exception("Invalid state change")

            self.curr_state = state
            self.curr_state.start_state()

    def process_response(self, response):
        with self.state_lock:
            if( self.curr_state is None ):
                raise Exception("Cannot process response from an empty state")

            self.curr_state.process_response(response)

    def reset(self):
        with self.state_lock:
            self.curr_state = None