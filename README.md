# UDP Client-Server Messaging System
Client-server system built upon basic UDP socket calls. 

## Running the application
** Note that these steps are done automatically if ran as a container **

[from the networks_client_server directory] <br>

To set up the environment: <br>
1. Install virtualenv with pip: `python3 -m pip install --user virtualenv`
2. `sudo apt-get install python3-venv`
3. Create a blank environment: `python3 -m venv env`
4. Activate the environment: `source env/bin/activate`
5. Install dependencies: `pip3 install -r requirements.txt`

While the environment is activated: <br>
To run the server: `python -m messaging_system.server` <br>
To run the client(s): `python -m messaging_system.client`

Configurations defined in messaging_system.client/server.config.

## Docker Setup (Windows)
To setup docker on WSL: <br>
Follow the tutorial at: https://medium.com/@sebagomez/installing-the-docker-client-on-ubuntus-windows-subsystem-for-linux-612b392a44c4 <br>
Note that windows docker desktop must be installed and running on port 2375 beforehand.

## Project Details
This project features an architecture where multiple clients can login and subscribe to messages posted by other users. <br>
The core commands are as follows:
1. <b>[login]</b> - <i>(username, password)</i> - if valid, logs in the user by generating a session token, and returning that to the client
2. <b>[logout]</b> - invalidates the session token currently active for a certain user
3. <b>[subscribe]</b> - <i>(subscribe-target)</i> - subscribes a user to subscribe-target, allowing that user to receive all that user's posts and are forwarded the messages if logged in
4. <b>[unsubscribe]</b> - <i>(unsubscribe-target)</i> - stop receiving posts from unsubscribe-target
5. <b>[retrieve]</b> - <i>(num_messages)</i> - retrieve the num_messages most recent messages for this user
6. <b>[post]</b> - <i>(message)</i> - send out the message to all users subscribed to this current user

* Note that if a logged-in user A is subscribed to user B, and user B posts a message m, user A will be directly forwarded message m.

## Client Architecture
The main difficulty of the client architecture is the existence of two blocking operations - (a) receiving input and (b) receiving packets from the server. However, these should be processed simultaneously, since the client should process responses while it is listening for input. 


Obviously, the solution is to place each of these blocking operations on a separate thread. The issue is now that if a response is received and processed at the same time in which the input is being received and processed, it could lead to certain memory being in a bad state -- a race condition. To solve this, we must identity the specific memory that, if both threads modify simultaneously, will cause a bad state, and introduce thread safety through locking.


For this application, the point of danger starts at the state objects. Essentially, the client follows an architecture such that, depending on what state the input/responses are in, it expects for a certain input to come in. For example, entering something like 'login#ac1&pass1' would put it into a state that expects a login_ack that tells it whether the login operation was successful or not. So the login input would put it into the login_state, and a successfully structured response will allow it to transition back to the default state. These states are encapsulated in the messaging_system.client.state_handler package. Imagine if the user input thread transitions the current state while the response thread is acting on that state -- this can lead to the response thread acting on bad memory!


We introduce that class that contains the memory that we <i> don't </i> want both threads from operating on simultaneously -- the messaging_system.state_transition_manager. This contains the dangerous current_state variable, and all public operations in this class are guaranteed to be enacted on by a single thread! This solves the threading issue with very minimal overhead, since all of the dangerous variables are encapsulated in one place.

## Server Architecture
Synchronization wise, the server is simpler in the sense that there is only a single thread that handles the requests end to end. It receives a request, and runs it through the large black box until it sends back a response to the client as necessary. As a resulit, the architecture is much more linear, with a simple pattern of receiving the data, processing it for errors, update the relavant data store, and sending a response back to the client if there are or are not errors.
