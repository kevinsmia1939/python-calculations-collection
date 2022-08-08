import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
import scipy.constants as cnst
from matplotlib.lines import Line2D

#initial condition
n = 2 #second order reaction
T = 300+273.15 #K
Rcons = cnst.R #m3⋅Pa/K⋅mol
P = 400000 #Pa

A = 6.6486 #m6/mol g s
E = 61324 #J/mol
ka = A*math.exp(-E/(Rcons*T)) #m6/mol g s
rho_bed = 1.2 * 10**6 #g/m3
poro = 0.45 #  porosity
rho_cat = rho_bed/(1-poro) #catalyst density
Cab0 = np.array([P/(Rcons*T)]) #mol/m3 #To use solve_ivp, even with 1 ode, need to convert to array.
De = 2.66*(10**(-8)) #m2/s
conv = 0.7 #70% conversion
U = 10 #m/s superficial vel
want_conv = 70 #required conversion
maxbed = 20 #Bed Plot range 
R = (6/1000)*(1/2) #m

#For solve_IVP
steps = 5000 # 1000000
z_array = np.array([0,maxbed]) # solve_ivp use array even if only 1 value
z = np.linspace(0, maxbed,steps)

def diffHP2(z_array,Cab,Rnew,args=(ka, rho_cat, n, Cab0)):
    Cas = Cab
    thiele = Rnew*((ka*rho_cat*(Cas**(n-1))/De)**0.5) #Thiele modulus
    Eff_fac = ((2/(n+1))**(1/2))*(3/thiele) #effectiveness factor eta
    omega = Eff_fac #high fluid velocity, overall eff approach internal eff
    dCabdz = -omega*ka*rho_bed*(Cab**2)/U
    return dCabdz

# Varies R value
# Save the calculated value in array
Cab_list = []
R_list = []
thiele_list = []
# List of R that want to be test
for i in [0.0003, 0.001, 0.003, 0.006, 0.01]: 
    Rnew = i
    Cab_ode = solve_ivp(diffHP2,z_array,Cab0,t_eval=(np.linspace(0,maxbed,steps)),args=(Rnew,))
    Cab = Cab_ode.y #Take the result from "y" key
    thiele = Rnew*((ka*rho_cat*(Cab**(n-1))/De)**0.5)
    Eff_fac = (((2/(n+1))**(1/2)))*(3/thiele)
    R_list.append(Rnew)
    Cab_list.append(Cab)
    thiele_list.append(thiele)
    
# Squeeze to make into neat array
Cab_array = np.squeeze(Cab_list).T #transpose to rotate the plot
thiele_array = np.squeeze(thiele_list).T #transpose
conversion_array = (1-(Cab_array/Cab0.item()))*100
Eff_fac = (((2/(n+1))**(1/2)))*(3/thiele_array)
omega = Eff_fac

# List of bed length that achieve 70% conv
bed_length_list = []
Cab_out_list = []
for i in range(0,Cab_array.shape[1],1):  #count number of array, find bed length
    bed_length_list.append(np.interp(want_conv,conversion_array[:,i],z))
    
Cab_out_70_Rinit = np.interp(bed_length_list[1],z,Cab_array[:,1])
    
# plot
plt.figure(figsize=(8,8))
plt.rc('font', size=10)

# Create subplot
ax11 = plt.subplot()
# Create axes
ax11.plot(z,Cab_array,linestyle='dashed',color='red',label="Concentration of A")
ax11.set_xlabel('Bed length(m)')
ax11.grid()
ax11.set_ylabel('Conversion(%)')
ax11.set_ylim(0,100)
ax11.set_xticks(np.arange(0, maxbed+1, 1.0))
ax11.set_yticks(np.arange(0, 110, 10))
ax11.set_xlim(0,maxbed)

ax12 = ax11.twinx()
ax12.plot(z,conversion_array,linestyle='-',color='blue',label="Conversion of A")
ax12.set_ylabel('Concentration($mol/m^3$)')
ax12.set_ylim(0,100)
ax12.set_yticks(np.arange(0, 110, 10))

# lines
style="Simple,head_length=6,head_width=6,tail_width=1.2"
plt.axvline(x=bed_length_list[R_list.index(R)], ymax=want_conv/100,linestyle=":",linewidth=3,color="black")
plt.axhline(y=Cab_out_70_Rinit, xmin=bed_length_list[R_list.index(R)]/maxbed, xmax=1,linestyle=":",linewidth=3,color="black")
custom_lines = [Line2D([0], [0], color='red', lw=2,linestyle='--'),
                Line2D([0], [0], color='blue', lw=2, linestyle='-')]
ax11.legend(custom_lines, ['Concentration', 'Conversion'], loc="center right")
plt.show()

plt.figure(figsize=(8,8))
ax21 = plt.subplot()
ax21.plot(z,thiele_array,linestyle='dashed',color='red',label="Thiele Modulus")
ax21.set_xlabel('Bed length(m)')
ax21.set_ylabel('Thiele Modulus($\phi$)')
ax21.set_xticks(np.arange(0, maxbed+1, 1.0))
ax21.set_xlim(0,maxbed)
ax21.set_ylim(0,3500)

ax22 = ax21.twinx()
ax22.plot(z,omega,linestyle='-',color='blue',label="Overall Effectiveness")
ax22.set_ylabel('Overall Effectiveness($\Omega$)')
ax22.set_ylim(0,0.1)
ax21.grid()
custom_lines = [Line2D([0], [0], color='red', lw=2,linestyle='--'),
                Line2D([0], [0], color='blue', lw=2, linestyle='-')]
ax21.legend(custom_lines, ['Overall Effectiveness', 'Thiele Modulus'], loc="upper center")
plt.show()