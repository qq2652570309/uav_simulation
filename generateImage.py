import numpy as np
import matplotlib.pyplot as plt

def virtualize(x,y,n):
    cols = ['Simple {}'.format(col) for col in range(1, n+1)]
    rows = ['{}'.format(row) for row in ['True labels', 'Predictions']]

    plt.figure(figsize=(15, 4))
    for i in range(1, n+1):
        # display original
        ax = plt.subplot(2, n, i)
        plt.imshow(x[i-1])
        plt.gray()
        ax.set_title(cols[i-1])

        if i == 1:
            ax.set_ylabel(rows[0], rotation=90, size='large')

        # display reconstruction
        ax = plt.subplot(2, n, i + n)
        plt.imshow(y[i-1])
        plt.gray()
        if i == 1:
            ax.set_ylabel(rows[1], rotation=90, size='large')

    plt.show()


x = np.random.rand(10,16,16)
y = np.random.rand(10,16,16)

print(x.shape)
print(y.shape)

virtualize(x,y,5)