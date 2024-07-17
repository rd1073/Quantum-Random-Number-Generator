from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.compiler import assemble
from qiskit.visualization import plot_bloch_multivector, plot_state_city, state_drawer
from qiskit_aer import Aer, AerSimulator
import matplotlib.pyplot as plt
import numpy as np

print("All libraries imported successfully!")

def real_map(n, start1, stop1, start2, stop2):
    # Map n from range start1-stop1 to start2-stop2
    return start2 + (stop2 - start2) * ((n - start1) / (stop1 - start1))

def QRandom(a, b, qubits):
    q = QuantumRegister(qubits, 'q')
    circ = QuantumCircuit(q)
    c0 = ClassicalRegister(qubits, 'c0')
    circ.add_register(c0)

    for i in range(qubits):
        circ.h(q[i])

    for i in range(qubits):
        circ.measure(q[i], c0[i])
    
    simulator = AerSimulator()

    backend = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(circ, simulator)

    job = simulator.run(transpiled_circuit)
    result = job.result()
    
    counts = result.get_counts(circ)

    # Calculate output based on measurement results
    total_counts = sum(counts.values())
    weighted_sum = sum(int(state, 2) * counts[state] for state in counts.keys())
    avg_value = weighted_sum / total_counts

    y = real_map(avg_value, 0, 2**qubits - 1, a, b)

    return y

qubits=6
x = []
for i in range(100):
    x.append(QRandom(0, 100, qubits))
    print(f"{i}: {x[-1]}")  # Print the last generated random number in the list x

plt.plot(x)
plt.xlabel('Iteration')
plt.ylabel('Random Number')
plt.title('Random Numbers Generated')
plt.show()


 