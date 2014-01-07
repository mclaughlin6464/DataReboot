'''
Created on Jun 7, 2013

@author: swm2
I am trying to find a way to live-update matplotlib plots
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_line(num, data, line):#num is the frame number and implicit first argument!
    line.set_data(data[...,:num])
    return line,

fig1 = plt.figure()

data = np.random.rand(2, 25)
l, = plt.plot([], [], 'bo')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, frames=25, fargs=(data, l),interval=50, blit=True)  


plt.show()

'''
Ok so I think I've finally got an idea for how to do the animated live update of the plot. What this function is doing
is taking an array, and gradually feeding it into the line. What I can do instead is have the measurement calls inside the the update
function, and append them to the data array. The next thing to figure out is how to save the last frame of the image as a final plot of sorts. 
'''