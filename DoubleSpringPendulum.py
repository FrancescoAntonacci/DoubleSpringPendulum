import os
import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time as tm
from numba import cuda
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter

start = tm.time()  # to check how slowly we are going :)

## Elapsed time
def timelaw(t, A, omega, phi, c):
    return A * np.sin(omega * t + phi) + c

## Physics (I'm not yet a fan of Hamilton. So, Fr4nci, I will ignore completely your despise for Newton!)
def uniform_acc(dt, a, v, x):
    return 0.5 * a * dt ** 2 + v * dt + x, a * dt + v

g = 10  # along z
k1 =1
k2 =1
x0 = 0
y0 = 0
z0 = 0

class body():
    def __init__(self, m, x, y, z, vx, vy, vz):
        self.m = m
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def mechanics(self, dt, fx, fy, fz):
        self.ax = fx / self.m
        self.ay = fy / self.m
        self.az = fz / self.m

        self.x, self.vx = uniform_acc(dt, self.ax, self.vx, self.x)
        self.y, self.vy = uniform_acc(dt, self.ay, self.vy, self.y)
        self.z, self.vz = uniform_acc(dt, self.az, self.vz, self.z)

## Bodies
m1 = body(1, 5, 0, -10, 0, 1, 0)  # Anchored to a fixed point
m2 = body(1, 0, 0, -15, 2,0 , 0)  # Anchored to m1

## Iterations
xx1, yy1, zz1 = [], [], []
xx2, yy2, zz2 = [], [], []

duration = 100
frames = 100000  # Reduced number of frames for quicker animation

dt = duration / frames

tt = np.linspace(0, duration, frames)

for i in tt:
    xx1.append(m1.x)
    yy1.append(m1.y)
    zz1.append(m1.z)

    xx2.append(m2.x)
    yy2.append(m2.y)
    zz2.append(m2.z)

    fx1 = k1 * (x0 - m1.x) - k2 * (m1.x - m2.x)
    fy1 = k1 * (y0 - m1.y) - k2 * (m1.y - m2.y)
    fz1 = k1 * (z0 - m1.z) - k2 * (m1.z - m2.z) - g * m1.m

    fx2 = k2 * (m1.x - m2.x)
    fy2 = k2 * (m1.y - m2.y)
    fz2 = k2 * (m1.z - m2.z) - g * m2.m

    m1.mechanics(dt, fx1, fy1, fz1)
    m2.mechanics(dt, fx2, fy2, fz2)

## Plotting
fig = plt.figure(1)
d3 = fig.add_subplot(111, projection='3d')

dot1, = d3.plot([], [], [], 'k.', markersize=10)
line1, = d3.plot([], [], [], 'k-', lw=2)

dot2, = d3.plot([], [], [], 'b.', markersize=10)
line2, = d3.plot([], [], [], 'b-', lw=2)

# Set labels and limits
d3.set_xlabel('X')
d3.set_ylabel('Y')
d3.set_zlabel('Z')

d3.set_xlim(np.min(xx1 + xx2), np.max(xx1 + xx2))
d3.set_ylim(np.min(yy1 + yy2), np.max(yy1 + yy2))
d3.set_zlim(np.min(zz1 + zz2), np.max(zz1 + zz2))

def init():
    line1.set_data([], [])
    line1.set_3d_properties([])
    dot1.set_data([], [])
    dot1.set_3d_properties([])

    line2.set_data([], [])
    line2.set_3d_properties([])
    dot2.set_data([], [])
    dot2.set_3d_properties([])

    return line1, dot1, line2, dot2

def animate(i):
    # Update m1 position and line from origin to m1
    line1.set_data([x0, xx1[i]], [y0, yy1[i]])
    line1.set_3d_properties([z0, zz1[i]])
    dot1.set_data([xx1[i]], [yy1[i]])
    dot1.set_3d_properties([zz1[i]])

    # Update m2 position and line from m1 to m2
    line2.set_data([xx1[i], xx2[i]], [yy1[i], yy2[i]])
    line2.set_3d_properties([zz1[i], zz2[i]])
    dot2.set_data([xx2[i]], [yy2[i]])
    dot2.set_3d_properties([zz2[i]])

    return line1, dot1, line2, dot2

# Create the animation
video = anim.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=0.00001, blit=True, repeat=True)

# Display the plot

# # Set the directory path where the script is located
# script_dir = os.path.dirname(os.path.abspath("DoubleSpringPendulum.py"))
# os.chdir(script_dir)
#
# # Save the animation
# video.save("DoubleSpringPendulum.gif", writer=PillowWriter(fps=5))

plt.show()

# Print the elapsed time
print(f"Elapsed time: {tm.time() - start:.2f} seconds")


