from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.monitor import job_monitor, backend_overview
nqubits = 3
circuit = QuantumCircuit(nqubits, nqubits)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0, 1, 2], [0,1, 2])
#circuit.draw(output = 'mpl')


simulator = Aer.get_backend('qasm_simulator')
sim_result = execute(circuit, backend = simulator, shots = 1024).result()
from qiskit.visualization import plot_histogram

plot_histogram(sim_result.get_counts(circuit))



IBMQ.load_account()

provider = IBMQ.get_provider(hub = 'ibm-q')
backend_overview()

backend_name = input("Which backend do you want to use: ")
device = provider.get_backend(backend_name)

job = execute(circuit, backend = device, shots = 1024)

#print(job.job_id())

job_monitor(job)

device_result = job.result()

plot_histogram(device_result.get_counts(circuit))

from qiskit.ignis.mitigation.measurement import (complete_meas_cal, CompleteMeasFitter)
cal_circuits, state_labels = complete_meas_cal(qr = circuit.qregs[0], circlabel = 'measerrormistigationcal')
#print(state_labels)
cal_circuits[2].draw(output = 'mpl')

cal_job = execute(cal_circuits,
                backend = device,
                shots = 1024,
                optimization_level = 0
                )

#print(cal_job.job_id())
job_monitor(cal_job)
cal_results = cal_job.result()

plot_histogram(
cal_results.get_counts(cal_circuits[3])
)


meas_fitter = CompleteMeasFitter(cal_results, state_labels)
meas_fitter.plot_calibration()


meas_filter = meas_fitter.filter
mitigated_result = meas_filter.apply(device_result)

device_counts = device_result.get_counts(circuit)
mitigated_counts = mitigated_result.get_counts(circuit)
plot_histogram([device_counts, mitigated_counts], legend = ['device, noisy', 'device, mitigated'])



plt.show()
