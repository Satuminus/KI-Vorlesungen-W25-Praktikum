## Aufgabe 1

### Vorwärtslauf

Mit
$$
A^{[0]} = X
$$

für jede Schicht $l \in \{1,2,3\}$:
$$
Z^{[l]} = W^{[l]}A^{[l-1]} + b^{[l]}, \qquad
A^{[l]} = \sigma(Z^{[l]}), \qquad
\sigma(z)=\frac{1}{1+e^{-z}}
$$

---

### Rückwärtslauf

Ableitung der Sigmoid-Funktion:
$$
\sigma'(z)=\sigma(z)(1-\sigma(z))
$$

Allgemein gilt:
$$
dZ^{[l]} = dA^{[l]} \odot \sigma'(Z^{[l]}), \qquad
dA^{[l-1]} = (W^{[l]})^T dZ^{[l]}
$$

Für die erste versteckte Schicht ergibt sich:
$$
dZ^{[1]} =
\Bigl((W^{[2]})^T
\bigl(((W^{[3]})^T dZ^{[3]})
\odot (A^{[2]} \odot (1-A^{[2]}))\bigr)\Bigr)
\odot (A^{[1]} \odot (1-A^{[1]}))
$$

---

### Gradienten und Update

Für $m$ Trainingsbeispiele:
$$
dW^{[1]} = \frac{1}{m} dZ^{[1]} (A^{[0]})^T, \qquad
db^{[1]} = \frac{1}{m} \sum_{i=1}^m dZ^{[1](i)}
$$

Gradientenabstieg:
$$
W^{[1]} \leftarrow W^{[1]} - \alpha dW^{[1]}, \qquad
b^{[1]} \leftarrow b^{[1]} - \alpha db^{[1]}
$$

---

## Aufgabe 2

### Forward Pass

Hidden-Neuron:
$$
z_1 = -1\cdot 0 + 1 = 1, \qquad
a_1 = \sigma(1) \approx 0.73106
$$

Output-Neuron:
$$
z_2 = 1\cdot 0.73106 + 2\cdot 0 - 2 = -1.26894, \qquad
y = \sigma(z_2) \approx 0.21944
$$

---

### Fehler

Quadratischer Fehler:
$$
E = \frac{1}{2}(y - y_T)^2
= \frac{1}{2}(0.21944 - 0.5)^2
\approx 0.03936
$$

---

### Backpropagation

Output-Schicht:
$$
\delta_2 = (y - y_T)\, y(1 - y) \approx -0.04806
$$

Partielle Ableitungen:
$$
\frac{\partial E}{\partial w_{1\to2}} = \delta_2 a_1 \approx -0.03513
$$
$$
\frac{\partial E}{\partial w_{x\to2}} = \delta_2 x = 0
$$
$$
\frac{\partial E}{\partial b_2} = \delta_2 \approx -0.04806
$$

Hidden-Schicht:
$$
\delta_1 = w_{1\to2}\delta_2 a_1(1-a_1) \approx -0.00945
$$

Partielle Ableitungen:
$$
\frac{\partial E}{\partial w_{x\to1}} = \delta_1 x = 0
$$
$$
\frac{\partial E}{\partial b_1} = \delta_1 \approx -0.00945
$$

---

### Gewichtsupdates ($\alpha = 0.01$)

Update-Regel:
$$
w^{neu} = w - \alpha \frac{\partial E}{\partial w}, \qquad
b^{neu} = b - \alpha \frac{\partial E}{\partial b}
$$

Ergebnisse:
$$
\begin{aligned}
w_{1\to2}^{neu} &\approx 1.00035 \\
w_{x\to2}^{neu} &= 2 \\
b_2^{neu} &\approx -1.99952 \\
w_{x\to1}^{neu} &= -1 \\
b_1^{neu} &\approx 1.00009
\end{aligned}
$$

---

## Aufgabe 3: MLP und Backpropagation

### Modell (Forward Propagation)

Hidden Layer:
$$
z^{[1]} = W^{[1]}x + b^{[1]}, \qquad
a^{[1]}=\mathrm{ReLU}(z^{[1]})
$$

Output Layer:
$$
z^{[2]} = W^{[2]}a^{[1]} + b^{[2]}, \qquad
\hat y=\sigma(z^{[2]})
$$

Aktivierungen:
$$
\mathrm{ReLU}(z)=\max(0,z),\qquad
\mathrm{ReLU}'(z)=
\begin{cases}
1,& z>0\\
0,& z\le 0
\end{cases}
$$
$$
\sigma(z)=\frac{1}{1+e^{-z}}
$$

---

### Loss

Für den Iris-Datensatz (3 Klassen) wird das Label one-hot kodiert $y\in\{0,1\}^K$ mit $K=3$.  
Mit Sigmoid-Ausgängen ergibt sich die Summe binärer Cross-Entropies:

$$
\mathcal L = -\sum_{k=1}^K \Big[y_k\log(\hat y_k)+(1-y_k)\log(1-\hat y_k)\Big]
$$

Für Sigmoid + Cross-Entropy gilt:
$$
\delta^{[2]}=\frac{\partial\mathcal L}{\partial z^{[2]}}=\hat y - y
$$

---

### Backpropagation und Update

Hidden-Delta:
$$
\delta^{[1]} = (W^{[2]})^T\delta^{[2]} \odot \mathrm{ReLU}'(z^{[1]})
$$

Gradienten:
$$
\frac{\partial \mathcal L}{\partial W^{[2]}}=\delta^{[2]}(a^{[1]})^T,\qquad
\frac{\partial \mathcal L}{\partial b^{[2]}}=\delta^{
