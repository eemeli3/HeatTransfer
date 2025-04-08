import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def heatMap(filepath):
    t = input('Enter timestep: ')
    try:
        if os.path.exists(filepath+'\\results\T_'+str(t)+'.csv'):
            with open(filepath+'\\results\T_'+str(t)+'.csv', 'r') as file:
                if (file.readline().count(';') > 0):
                    separator = ';'
                else:
                    separator = ','
            T = []
            with open(filepath+'\\results\T_'+str(t)+'.csv', 'r') as file:
                for line in file:
                    line = line.split(separator)
                    line[-1] = line[-1].replace('\n','')
                    line = [value.replace(',','.') for value in line]
                    row = list(map(float, line))
                    T.append(row)
            T = np.array(T)
            plt.imshow(T)
            plt.show()
        else:
            print("The timestep does not exist.")
            input("Press any key to continue ...")
            sys.exit()
    except:
        print("The file ", 'T_'+str(t), 'contains errors.')
        input("Press any key to continue ...")
        sys.exit()