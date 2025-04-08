import numpy as np
import os
import sys


def getCSVseparator(filepath):
    try:
        with open(filepath+"/Tinitial.csv") as file:
            if (";" in file.readline()):
                separator = ";"
            else:
                separator = ","
            return separator
    except:
        print("Input file \"Tinitial.csv\" does not exist or contains errors.\n")
        input("Press any key to continue ...")
        sys.exit()

def getConstants(filepath):
    try:
        with open(filepath+"/Constants.txt") as file:
            for line in file:
                line = line.replace(" ","")
                line = line.split("=")
                line[1] = line[1].rstrip('\n')
                if (line[0] == 'H'):
                    H = float(line[1])
                elif (line[0] == 'W'):
                    W = float(line[1])
                elif (line[0] == 'ni'):
                    ni = int(line[1])
                elif (line[0] == 'nj'):
                    nj = int(line[1])
                elif (line[0] == 'k'):
                    k = float(line[1])
                elif (line[0] == 'rho'):
                    rho = float(line[1])
                elif (line[0] == 'cp'):
                    cp = float(line[1])
                elif (line[0] == 'time'):
                    time = float(line[1])
                elif (line[0] == 'nt'):
                    nt = int(line[1])
                elif (line[0] == 'record_interval'):
                    record_interval = int(line[1])
            if ('H' in locals() and 'W' in locals() and 'ni' in locals() and 'nj' in locals() and 'k' in locals() and 'rho' in locals() and 'cp' in locals() and 'time' in locals() and 'nt' in locals() and 'record_interval' in locals()):
                return (H, W, ni, nj, k, rho, cp, time, nt, record_interval)
            else:
                print("A constant is missing in \"Constants.txt\" file")
                input("Press any key to continue ...")
                sys.exit()
    except:
        print("Input file \"Constants.txt\" does not exist or contains errors.\n")
        input("Press any key to continue ...")
        sys.exit()

def getInputMatrix(filepath, ni, nj, filename):
     result = np.zeros((nj,ni))
     try:
        with open(filepath+"/"+filename) as file:
            count = 0
            for line in file:
                line = line.replace(" ","")
                if (";" in line):
                    line = line.split(";")
                else:
                    line = line.split(",")
                line[1] = line[1].rstrip('\n')
                result[count] = line
                count += 1
            if (count != nj):
                print(filename + 'is has a different number of rows than "Constants.txt".')
                input("Press any key to continue ...")
                sys.exit()
            return result
     except:
        print("Input file \"" + filename + "\" does not exist or contains errors.\n")
        input("Press any key to continue ...")
        sys.exit()

def getVariableInputMatrix(filepath, ni, nj, filename, t):
    if (os.path.exists(filepath+"/"+filename)):
        return getInputMatrix(filepath, ni, nj, filename)
    elif (os.path.exists(filepath+"/"+filename[0:-4]+"/"+filename[0:-4]+str(t)+".csv")):
        return getInputMatrix(filepath+"/"+filename[0:-4], ni, nj, filename[0:-4]+str(t)+".csv")
    else:
        print('Input file for "'+filename[0:-4]+'" is missing.')
        input("Press any key to continue ...")
        sys.exit()

def createResultsDirectory(filepath):
    if (os.path.exists(filepath+"/results")):
        try:
            files = os.listdir(filepath+"/results")
            for file in files:
                os.remove(filepath+"/results/"+file)
        except:
            print('The input file location contains a "results" folder which contains directories. Remove directories from "results" folder.')
            input("Press any key to continue ...")
            sys.exit()
    else:
        os.makedirs(filepath+"/results")

def saveState(filepath, T, t, record_interval, nt, separator):
    if (t % record_interval == 0 or t == nt):
        with open(filepath+'/results/'+'T_'+str(t)+'.csv', 'w') as file:
            for j in range(T.shape[0]):
                for i in range(T.shape[1]):
                    value = str(T[i,j])
                    if (separator == ';'):
                        value = value.replace('.',',')
                    if (i == T.shape[1]-1):
                        if (j != T.shape[1]-1):
                            file.write(value+'\n')
                        else:
                            file.write(value)
                    else:
                        file.write(value+separator)
    else:
        return

def calculate(filepath):
    separator = getCSVseparator(filepath)
    H, W, ni, nj, k, rho, cp, time, nt, record_interval = getConstants(filepath)
    Tinitial = getInputMatrix(filepath, ni, nj, "Tinitial.csv")
    createResultsDirectory(filepath)
    w = W/ni
    h = H/nj

    dt = time/nt
    dTdt = np.zeros((nj,ni))

    T = Tinitial
    saveState(filepath, T, 0, record_interval, nt, separator)
    for t in range(nt):
        TL = getVariableInputMatrix(filepath, ni, nj, "TL.csv", t)
        TR = getVariableInputMatrix(filepath, ni, nj, "TR.csv", t)
        TU = getVariableInputMatrix(filepath, ni, nj, "TU.csv", t)
        TB = getVariableInputMatrix(filepath, ni, nj, "TB.csv", t)
        S = getVariableInputMatrix(filepath, ni, nj, "S.csv", t)
        for j in range(nj):
            for i in range(ni):
                sumgradTdAdV = 0
                if (TL[j,i] == -1):
                    sumgradTdAdV += (T[j,i-1]-T[j,i])/w**2
                else:
                    sumgradTdAdV += (TL[j,i]-T[j,i])/(w**2/2)
                if (TU[j,i] == -1):
                    sumgradTdAdV += (T[j-1,i]-T[j,i])/h**2
                else:
                    sumgradTdAdV += (TR[j,i]-T[j,i])/(h**2/2)
                if (TR[j,i] == -1):
                    sumgradTdAdV += (T[j,i+1]-T[j,i])/w**2
                else:
                    sumgradTdAdV += (TR[j,i]-T[j,i])/(w**2/2)
                if (TB[j,i] == -1):
                    sumgradTdAdV += (T[j+1,i]-T[j,i])/h**2
                else:
                    sumgradTdAdV += (TB[j,i]-T[j,i])/(h**2/2)
                dTdt[j,i] = (k*sumgradTdAdV+S[j,i])/rho/cp
        T = T+dTdt*dt
        saveState(filepath, T, t+1, record_interval, nt, separator)