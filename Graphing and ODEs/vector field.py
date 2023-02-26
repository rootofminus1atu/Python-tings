import numpy as np
import matplotlib.pyplot as plt

x, y = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))

u = -y
v = x

plt.quiver(x, y, u, v)
plt.show()
