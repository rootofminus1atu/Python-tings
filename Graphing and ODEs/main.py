import matplotlib.pyplot as plt
import numpy as np


def f(t):
    return -t + 2 * np.exp(t) - 1


# dy/dt = f(y,t)
def g(y, t):
    return y + t


# actual graph
h1 = 0.05

t1 = np.arange(-2, 2 + h1, h1)
y1 = f(t1)
plt.plot(t1, y1)


# approx graph

# dy/dt = y + t
# g(y,t) = y + t
# start with (t,y) = (0,1)
# the slope dy/dt at 0  is 1+0 = 1
# y0 = 1
# y1 = 1 + h*g(y0, t0) = 1 + h*(1 + 0) = 1 + h
# y2 = 1 + h + h*g(y1, t1) =





h2 = 1
t2 = np.arange(-2, 2 + h2, h2)

i=0
while i < 100:
    slope = g(y,t)

    y2 = 1


plt.plot(t2, y2)











plt.grid()
plt.xlabel('t')
plt.ylabel('y = f(t)')
plt.title('idk anymore')

plt.show()

