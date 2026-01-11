import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_iris_csv(path: str):

    df = pd.read_csv(path, header=None)
    X = df.iloc[:, :4].to_numpy(dtype=np.float64)
    y_str = df.iloc[:, 4].astype(str).to_numpy()

    classes = np.unique(y_str)
    class_to_idx = {c: i for i, c in enumerate(classes)}
    y_idx = np.array([class_to_idx[s] for s in y_str], dtype=np.int64)

    K = len(classes)
    Y = np.zeros((len(y_idx), K), dtype=np.float64)
    Y[np.arange(len(y_idx)), y_idx] = 1.0

    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)

    return X, Y, classes

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def relu(z):
    return np.maximum(0.0, z)


def relu_grad(z):
    return (z > 0.0).astype(np.float64)

def bce_multi(y, y_hat, eps=1e-12):
  
    y_hat = np.clip(y_hat, eps, 1.0 - eps)
    return -np.sum(y * np.log(y_hat) + (1.0 - y) * np.log(1.0 - y_hat))


class MLP:
    def __init__(self, d_in: int, d_hidden: int, d_out: int, seed: int = 0):
        rng = np.random.default_rng(seed)

        self.W1 = rng.normal(0.0, np.sqrt(2.0 / d_in), size=(d_hidden, d_in))
        self.b1 = np.zeros(d_hidden)

        self.W2 = rng.normal(0.0, 0.01, size=(d_out, d_hidden))
        self.b2 = np.zeros(d_out)

    def forward(self, x):
      
        z1 = self.W1 @ x + self.b1
        a1 = relu(z1)
        z2 = self.W2 @ a1 + self.b2
        y_hat = sigmoid(z2)
        cache = (x, z1, a1, z2, y_hat)
        return y_hat, cache

    def backward(self, y, cache):
       
        x, z1, a1, z2, y_hat = cache

        delta2 = (y_hat - y) 

        dW2 = delta2[:, None] @ a1[None, :]
        db2 = delta2

        
        da1 = self.W2.T @ delta2
        delta1 = da1 * relu_grad(z1)

        dW1 = delta1[:, None] @ x[None, :]
        db1 = delta1

        return dW1, db1, dW2, db2

    def sgd_step(self, grads, lr: float):
        dW1, db1, dW2, db2 = grads
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2


def train_sgd(X, Y, hidden: int = 50, lr: float = 0.05, epochs: int = 3000, seed: int = 0):

    n, d_in = X.shape
    d_out = Y.shape[1]

    model = MLP(d_in=d_in, d_hidden=hidden, d_out=d_out, seed=seed)
    losses = []
    rng = np.random.default_rng(seed)

    for ep in range(1, epochs + 1):
        idx = rng.permutation(n)
        total_loss = 0.0

        for i in idx:
            x = X[i]
            y = Y[i]

            y_hat, cache = model.forward(x)
            total_loss += bce_multi(y, y_hat)

            grads = model.backward(y, cache)
            model.sgd_step(grads, lr)

        losses.append(total_loss / n)

        if ep % 200 == 0:
            print(f"Epoch {ep:4d} | mean loss = {losses[-1]:.6f}")

    return model, np.array(losses)


def main():
    iris_path = "./iris.csv"

    X, Y, classes = load_iris_csv(iris_path)
    print("Classes:", classes)

    model, losses = train_sgd(X, Y, hidden=50, lr=0.05, epochs=3000, seed=0)
    print("Final mean loss:", losses[-1])

    plt.figure()
    plt.plot(np.arange(1, len(losses) + 1), losses)
    plt.xlabel("Epoch")
    plt.ylabel("Training loss")
    plt.title("Iris Training Loss (MLP)")
    plt.show()


if __name__ == "__main__":
    main()