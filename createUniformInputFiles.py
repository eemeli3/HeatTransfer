import os
import sys
import numpy as np

def saveMatrix(filepath, Tinitial, separator):
    with open(filepath+'Tinitial.csv', 'w') as file:
        for j in range(Tinitial.shape[0]):
            for i in range(Tinitial.shape[1]):
                value = str(Tinitial[i,j])
                if (separator == ';'):
                    value = value.replace('.',',')
                if (i == Tinitial.shape[1]-1):
                    if (j != Tinitial.shape[1]-1):
                        file.write(value+'\n')
                    else:
                        file.write(value)
                else:
                    file.write(value+separator)

def createUniformInitial(filepath):
    while (True):
        T = input('Enter initial temperature: ')
        try:
            T = float(T.replace(',','.'))
            break
        except:
            print("Initial temperature needs to be a number.\n")
    try:
        with open(filepath+'/Constants.txt', 'r') as file:
            for line in file:
                line = line.replace(" ","")
                line = line.split("=")
                line[1] = line[1].rstrip('\n')
                if (line[0] == 'ni'):
                    ni = int(line[1])
                elif (line[0] == 'nj'):
                    nj = int(line[1])
            if (not('ni' in locals() and 'nj' in locals())):
                print('The "Constants.txt" file does not have "ni" and "nj" variables. Initial temperature file could not be created.\n')
                return
        print('ni and nj were created')
        Tinitial = T*np.ones((nj, ni))
        while (True):
            separator = input('Are numbers written in finnish or english system? Enter "exit" to exit: ')
            if (separator == 'finnish' or separator == 'english'):
                if (separator =='finnish'):
                    separator = ';'
                else:
                    separator = ','
                saveMatrix(filepath, Tinitial, separator)
                return
            elif (separator == 'exit'):
                return
            else:
                print('Only "finnish" and "english" are allowed.\n')
    except:
        print('The file "Constants.txt" does not exist or contains errors.\n')