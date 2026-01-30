#   Addverb's Cobot Python Client Library

This project provides a Python-based client library designed to interface with Addverb's cobot. It allows for remote control of joint jogging, Cartesian movements, gripper operations, querying positions and velocity scaling over a network using a custom TCP protocol.

### Overview

The system operates on a client-server architecture:

* **The Backend (C++):** A control server runs directly on Addverb's cobot hardware or controller. It handles hardware safety states, and listens for incoming TCP instructions on port 5000. It utilizes a dedicated thread to process network packets while maintaining the real-time control loop.
* **The Client (Python):** This library provides a high-level `Cobot` class that abstracts the TCP socket communication into simple method calls. Users can control the robot without needing to manage raw byte buffers or manual socket states.

### Requirements

To use this library, the cobot must be running the backend control in the dockerfile on the cobot.
Ensure your cobot and the client machine are on the same network. Support for different networks will be added later through hole punching if I have free time :)

### Installation

1. **Clone the repository:**
```bash
git clone git@github.com:HrishabhMittal/cobot.git
cd cobot

```

2. **Ensure Python is installed:**
This library is verified with Python 3.x.

3. **Install the package in development mode:**
You can install the library locally so it is accessible within your Python environment:
```bash
pip install -e .

```

### Basic Usage

```python
from cobot import Cobot, Dirn

# Using a context manager ensures the connection is closed automatically
# the ip to be used can be found by running ip addr, or ifconfig
# local IPs start from 10. 
# look for inet 10.x.y.z
with Cobot(host="10.x.y.z") as arm:
    # set speed multiplier
    arm.setVelocity(1.5)
    
    # jog the first joint in a positive direction
    arm.jogJoint(Dirn.POSITIVE, 0)

    # let it jog for a bit
    time.sleep(5)

    # stop all movement
    arm.stopJogging()

    # move to base ~ 10s
    arm.baseRigid()

    # +x dirn
    arm.jogCartesian(Dirn.NEGATIVE, 0)
    
    # let it jog for a bit
    time.sleep(10)
    
    # stop all movement
    arm.stopJogging()
    
    # Open gripper ~ 5s
    arm.gripperOpen()
    
    # Close the gripper ~ 5s
    arm.gripperClose()
```
