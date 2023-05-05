from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# example function for controlling PTZ movement
def move_ptz(pan, tilt, zoom):
    # code for controlling PTZ movement goes here
    print(f"Moving PTZ to: pan={pan}, tilt={tilt}, zoom={zoom}")

# example function for emitting laser
def emit_laser():
    # code for emitting laser goes here
    print("Laser emitted!")

# web socket event for PTZ movement
@socketio.on('ptz movement')
def handle_ptz_movement(data):
    pan = data['pan']
    tilt = data['tilt']
    zoom = data['zoom']
    move_ptz(pan, tilt, zoom)

# web socket event for emitting laser
@socketio.on('emit laser')
def handle_emit_laser():
    emit_laser()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
