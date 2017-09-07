import numpy as np
import random
import matplotlib.pylab as plt

a,b = random.random() * 2 * np.pi - np.pi, random.random() * 2 * np.pi - np.pi
# x = np.linspace(min(a,b), max(a,b), 201)
# plt.plot(x, np.sin(x))

print(min(a,b))
print(max(a,b))
print(np.sin(min(a,b)))
print(np.sin(max(a,b)))
print()
for x in range(1,30):
  print(int(np.sin(min(a,b) + x/30.0*abs(a-b)) * 3))