import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
import scipy.constants as cnst
from matplotlib.lines import Line2D

# import array

#initial condition
n = 2 #second order reaction
T = 300+273.15 #K
Rcons = cnst.R #m3⋅Pa/K⋅mol
P = 400000 #Pa
A = 6.6486 #m6/mol g s
E = 61324 #J/mol
rho_bed = 1.2 * 10**6 #g/m3
poro = 0.45 #  porosity
rho_cat = rho_bed/(1-poro) #catalyst density
Cab0 = np.array([P/(Rcons*T)]) #mol/m3 #To use solve_ivp, even with 1 ode, need to convert to array.
De = 2.66*(10**(-8)) #m2/s
conv = 0.7 #70% conversion
U = 10 #m/s superficial vel
want_conv = 70 #required conversion
maxbed = 10 #Bed Plot range 
R = (6/1000)*(1/2) #m

#For solve_IVP
steps = 1000 # 1000000
z_array = np.array([0,maxbed]) # solve_ivp use array even if only 1 value
z = np.linspace(0, maxbed,steps)

def diffHP2(z_array,Cab,Rnew,Tnew,args=(rho_cat, n, Cab0)):
    Cas = Cab
    ka = A*math.exp(-E/(Rcons*Tnew))
    thiele = Rnew*((ka*rho_cat*Cas/De)**0.5) #Thiele modulus
    Eff_fac = ((2/(n+1))**(1/2))*(3/thiele) #effectiveness factor eta
    omega = Eff_fac #high fluid velocity, overall eff approach internal eff
    dCabdz = -omega*ka*rho_bed*(Cab**2)/U
    return dCabdz

bed_length_list_list = []
R_list = []
ka_list =[]
for j in [0.0003, 0.001, 0.003, 0.006, 0.01]:
    # Reset everytime new Rnew value
    Cab_list = []
    thiele_list = []
    T_list = []
    Rnew = j
    R_list.append(Rnew)
    for i in range(400,700,1): 
        Tnew = i
        Cab_ode = solve_ivp(diffHP2,z_array,Cab0,t_eval=(np.linspace(0,maxbed,steps)),args=(Rnew,Tnew,))
        Cab = Cab_ode.y #Take the result from "y" key
        Cab_list.append(Cab)
        T_list.append(Tnew)
# Squeeze to make into neat array
    Cab_array = np.squeeze(Cab_list).T #transpose to rotate the plot

    thiele_array = np.squeeze(thiele_list).T #transpose
    conversion_array = (1-(Cab_array/Cab0.item()))*100
# List of bed length that achieve 70% conv
    bed_length_list = []
    Cab_out_list = []
    for i in range(0,Cab_array.shape[1],1):  #count number of array, find bed length
        bed_length_list.append(np.interp(want_conv,conversion_array[:,i],z))
    bed_length_list_list.append(bed_length_list)
bed_length_array = np.squeeze(bed_length_list_list).T
check_T = np.interp(T,T_list,bed_length_array[:,2])

plt.figure(figsize=(8,8))
plt.plot(T_list,bed_length_array[:,:],color='black')
plt.title('Required bed length to reach 70% conversion \n as a function of temperature')
plt.ylim(0, maxbed)
plt.xlim(400, max(T_list)+1)
plt.yticks(np.arange(0,max(bed_length_list)+1,1))
plt.xlabel('Temperature ($^\circ C$)')
plt.ylabel('Bed length (m)')
plt.axvline(x=T,linestyle=":",linewidth=3,color="red")
plt.axhline(y=check_T,linestyle="--",linewidth=3,color="blue")
custom_lines = [Line2D([0], [0], color='red', lw=2.5,linestyle=':'),
                Line2D([0], [0], color='blue', lw=2.5,linestyle='--')]
plt.legend(custom_lines, ['$T=573 ^\circ C$','Required bed length for \n given $T$ and $R$'], loc="upper right",fontsize=9)
plt.grid()
plt.show()