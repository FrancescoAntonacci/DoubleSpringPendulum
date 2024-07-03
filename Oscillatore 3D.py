## Libraries

import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time as tm
from numba import cuda
from mpl_toolkits.mplot3d import Axes3D

start= tm.time() # to check how slowly we are going :)

## Elapsed time
def timelaw(t,A,omega,phi,c):
    return A*np.sin(omega*t+phi)+c

## motion parameters

class motionparameters():       #DON'T BLAME ME! I created a class because I am a lazy ass. I hate to repeat!
    def __init__(self,A,omega,phi,c):
        self.A=A
        self.w=omega
        self.p=phi
        self.c=c
        self.v=[self.A,self.w,self.p,self.c]


mp1x=motionparameters(20,2,3,4)
mp1y=motionparameters(12,23,311,14)
mp1z=motionparameters(11,34,43,4)

##
duration=1000
frames=1000000

tt=np.linspace(0, duration,frames)

xx1=timelaw(tt,*mp1x.v)
yy1=timelaw(tt,*mp1y.v)
zz1=timelaw(tt,*mp1z.v)


##Happy plotting
fig= plt.figure(1)

d3 = fig.add_subplot(111,projection='3d')
dot, = d3.plot([], [], [], 'k.', markersize=10)
curve, = d3.plot([], [], [], 'k-', alpha=0.7, linewidth=2)

# d3.plot(xx1,yy1,zz1)

d3.set_xlabel('X',)
d3.set_ylabel('Y')
d3.set_zlabel('Z',)


d3.set_xlim(np.min(xx1), np.max(xx1))
d3.set_ylim(np.min(yy1), np.max(yy1))
d3.set_zlim(np.min(zz1), np.max(zz1))
# plt.show()


## What a gourgeous animation!



def init():
    curve.set_data([], [])
    curve.set_3d_properties([])
    dot.set_data([], [])
    dot.set_3d_properties([])
    return curve, dot

def animate(i):
    curve.set_data(xx1[:i], yy1[:i])
    curve.set_3d_properties(zz1[:i])
    dot.set_data(xx1[i], yy1[i])
    dot.set_3d_properties(zz1[i])
    return curve, dot

video = anim.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=0.001, blit=True, repeat=True,)


plt.show()







print(f"Elapsed time: {tm.time() - start:.2f} seconds")





