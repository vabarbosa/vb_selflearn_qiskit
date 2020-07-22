from qiskit import *
import matplotlib.pyplot as plt
circuit = QuantumCircuit(3, 3)
#circuit.draw(initial_state=True, output = 'mpl')

circuit.x(0)
circuit.barrier()
#circuit.draw(output = 'mpl')

circuit.h(1)
circuit.cx(1, 2)
#circuit.draw(output = 'mpl')

circuit.cx(0, 1)
circuit.h(0)
#circuit.draw(output = 'mpl')

circuit.barrier()
circuit.measure([0, 1], [0, 1])
circuit.draw(output = 'mpl')

circuit.barrier()
circuit.cx(1, 2)
circuit.cz(0, 2)
circuit.draw(output = 'mpl')


circuit.measure(2, 2)
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots = 1024).result()
counts = result.get_counts()
from qiskit.tools.visualization import plot_histogram
plot_histogram(counts)

plt.show()
