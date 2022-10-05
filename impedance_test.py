from impedance import preprocessing
from impedance.models.circuits import CustomCircuit
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist


eis_file = 'data/Group 3/EIS_V3_65ml_e4.par'

frequencies, z = preprocessing.readVersaStudio(eis_file)

# # keep only the impedance data in the first quandrant
frequencies, z = preprocessing.ignoreBelowX(frequencies, z)

# circuit = 'R0-p(R1-Wo0,C0)-Wo1'
# circuit = 'R0-p(R1-Wo0,C0)-Wo1'
# circuit = 'R0-p(R1,C0)'
circuit2 = 'R0-p(R1-Wo0,CPE0)-Wo1'
# circuit2 = 'R0-p(R1,C0)-Wo1'
initial_guess = [1.483e+00, 1.9e-01, 5.70e+02, 3.79e+04, 3.63e-04, 1, 5.34e+02, 3.17e+04]
# initial_guess = [1.5e+00, 2e-01, 3e-02]

circuit = CustomCircuit(circuit2, initial_guess=initial_guess)

circuit.fit(frequencies, z)

z_fit = circuit.predict(frequencies)

fig, ax = plt.subplots(figsize=(10,10))
# plt.xlim(left=0,right=np.ceil(max(z.real)*0.1)/0.1)
# plt.ylim(top=np.ceil(max(np.abs(z.imag))*0.1)/0.1)
plot_nyquist(ax, z,fmt='o')
plot_nyquist(ax, z_fit, fmt='-')

plt.legend(['Data', 'Fit'])
plt.show()

print(circuit)