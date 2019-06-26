import numpy as np



s = np.random.dirichlet(np.ones(row * col),size=1).flatten()
print(s)
launching_rate = 2
res = launching_rate * s
print(res)
