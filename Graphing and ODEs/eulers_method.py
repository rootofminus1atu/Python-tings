import numpy as np
import matplotlib.pyplot as plt
# from scipy.integrate import solve_ivp

plt.style.use('default')


# dy/dt = f(y,t)
def f(y, t):
    return y + t


def actual_sol(t):
    return -t + 2*np.exp(t) - 1


t0 = 0    # initial conditions
y0 = 1    # (t0,y0) = (0,1)

h = 0.1   # step size
t = np.arange(t0, 2 + h, h)  # set up points on the x; axis

y = np.zeros(len(t))  # the same an array filled with 0's, its length is len(t)
y[0] = y0

for i in range(0, len(t) - 1):
    y[i + 1] = y[i] + h * f(y[i], t[i])

plt.figure(figsize=(8, 5))
plt.plot(t, y, 'bo--', markersize=4, linewidth=1, label='Approximate')
plt.plot(t, actual_sol(t), 'g', label='Exact')
plt.title('Approximate and Exact Solution for a Simple ODE')
plt.xlabel('t')
plt.ylabel('y = f(t)')
plt.grid()
plt.legend(loc='lower right')
plt.show()



