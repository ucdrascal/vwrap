"""
Demonstrates basic usage of vwrap including simulation state control, and
control of joints in the example scene.
"""

import sys
import time
import math

try:
    import vwrap
except:
    sys.path.insert(0, '..')
    import vwrap


if __name__ == '__main__':
    with vwrap.VrepSimulation() as sim:
        ts = time.time()
        scene = vwrap.Scene(sim.client_id)

        joint = scene.get_joint("Jaco_joint2")
        joint.position = joint.initial_position + math.radians(-10)
        joint.update()

        time.sleep(2)
