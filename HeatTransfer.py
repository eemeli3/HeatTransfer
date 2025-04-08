import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import heatTransferCalculation
import createUniformInputFiles

def introMessage():
    msg = ('Welcome to heat transfer calculator. Commands:\n'
           '"help" for instructions\n'
           '"exit" to exit program\n'
           '"filepath" to set input/output file location\n'
           '"uni temp" to create an initial temperature file with uniform temperature\n'
           '"calculate" to do heat transfer calculation\n'
           '"heat map" to show heat map at time "t"\n')
    print(msg)

def helpMessage():
    pass

def getFilepath():
    while (True):
        filepath = input('Enter input file location. Press Enter if input location is the current working directory. Enter "exit" to return.\n')
        if (filepath == ""):
            filepath = os.getcwd()
            print('Input location is current working directory: ', filepath, '\n')
            return filepath
        elif (os.path.isdir(filepath)):
            return filepath
        elif (filepath == 'exit'):
            return ''
        else:
            print("The file path does not exist.\n")


def main():
    filepath = ''
    introMessage()
    while (True):
        command = input("Input: ")
        if (command == 'filepath'):
            filepath = getFilepath()
        elif (command == 'calculate'):
            if (filepath == ''):
                print('Input file location has not been set. Enter an input file location.\n')
                continue
            heatTransferCalculation.calculate(filepath)
        elif (command == 'help'):
            helpMessage()
        elif (command == 'uni temp'):
            createUniformInputFiles.createUniformInitial(filepath)
        elif (command == 'exit'):
            print("Press any key to continue ...")
            break
        else:
            print('Command is not valid. Enter "help" for a list of commands.\n')


main()