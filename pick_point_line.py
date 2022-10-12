import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# x, y, c, s = rand(4, 100)

CV_file = 'data/CV and EIS/Sample 1(500C3h)/CV_V3_0to1.2V.txt'
df=pd.read_table(CV_file, skiprows=1, sep='\t', header=None, usecols=[0,1])
df = np.array(df)
volt = df[:,0]
current = df[:,1]

x = volt
y = current

def onpick(event):
    ind = event.ind
    volt = np.take(x, ind)[0]
    current = np.take(y, ind)[0]
    print('volt',volt,'current',current)
    return volt, current
    
fig, ax = plt.subplots()
col = ax.plot(x, y, picker=1)
fig.canvas.mpl_connect('pick_event', onpick)



