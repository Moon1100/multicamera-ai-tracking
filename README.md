
## Multicamera Tracking Web App Documentation

### Table of Contents
1. [Introduction](#introduction)
2. [Hardware Setup](#hardware-setup)
3. [Software Setup](#software-setup)
   - [Main Server Setup](#main-server-setup)
   - [Raspberry Pi Setup](#raspberry-pi-setup)
   - [Camera Streaming](#camera-streaming)
4. [Initialization Procedure](#initialization-procedure)
5. [Calibration](#calibration)
6. [Running the Web App](#running-the-web-app)
7. [Troubleshooting](#troubleshooting)
8. [Conclusion](#conclusion)

### Introduction<a name="introduction"></a>

This documentation provides a comprehensive guide for setting up and running a multicamera tracking web app using Flask. The system involves Raspberry Pi modules, camera streaming, and a main server.

### Hardware Setup<a name="hardware-setup"></a>

1. Assemble the Alphabot camera unit properly.

2. Boot each camera Raspberry Pi.

### Software Setup<a name="software-setup"></a>

#### Main Server Setup<a name="main-server-setup"></a>

1. Clone the repository on the main server.

   ```bash
   git clone <repository_url>
   ```

2. Create and activate a virtual environment.

   ```bash
   cd <repository_directory>
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Redis server.

   ```bash
   redis-server --protected-mode no
   ```

#### Raspberry Pi Setup<a name="raspberry-pi-setup"></a>

1. Access each Raspberry Pi either through a monitor or using VNC on the same network.

2. Clone the repository on each Raspberry Pi.

   ```bash
   git clone <repository_url>
   ```

3. Create and activate a virtual environment.

   ```bash
   cd <repository_directory>/pi_script
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

#### Camera Streaming<a name="camera-streaming"></a>

1. Start the camera streaming script on each Raspberry Pi.

   ```bash
   cd Documents/mjpg-streamer/mjpg-streamer-experimental
   ./start.sh
   ```

### Initialization Procedure<a name="initialization-procedure"></a>

1. Obtain the current IP address of the main server.

2. Update the host IP in each `main_Alphabot<bot_channel_number>.py` script on the Raspberry Pi.

   ```python
   r = redis.Redis(host='main_server_ip', port=6379, db=0)
   ```

3. Run the angle correction script on each Raspberry Pi.

4. Repeat steps 2-3 for each Raspberry Pi involved in the setup.

5. On the main server, navigate to `web_face_detection` and run `app.py`.

### Calibration<a name="calibration"></a>

To calibrate manually:

1. On each Raspberry Pi, navigate to `Alphabot2-Demo/RapsberryPi/Alphabot2/Web-Control`.

2. Run `main.py` to perform manual calibration.

### Running the Web App<a name="running-the-web-app"></a>

After completing the initialization and calibration steps, the web app is ready to run. Open a browser and access the web app using the IP address of the main server.

### Troubleshooting<a name="troubleshooting"></a>

- If any issues arise during setup or runtime, refer to the troubleshooting section in the README file or seek assistance from the project community.

### Conclusion<a name="conclusion"></a>

Congratulations! You have successfully set up and configured the multicamera tracking web app. For any further customization or troubleshooting, refer to the project documentation and community resources.



Authorship
Muhammad Aliff Izzuddin: University of Malaya, Matriculation Number: 17203058 (2024)