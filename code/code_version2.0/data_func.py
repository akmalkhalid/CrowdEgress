
#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================
# 
# DESCRIPTION:
# This software is part of a python library to assist in developing and
# analyzing evacuation simulation results from Fire Dynamics Simulator with Evacuation (FDS+Evac).
# FDS+Evac is an open source software package developed by NIST. The source
# code is available at: https://github.com/firemodels/fds
#

# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import pygame
import pygame.draw
import numpy as np
#from agent_model_obst3 import *
from agent import *
from obst import *
#from passage import *
from math_func import *
from math import *
#from config import *
import re
import random
import csv
from ctypes import *


def readCSV_base(fileName):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    #print (dataNP)
    #print ('np.shape(dataNP)', np.shape(dataNP))
    #print ('\n')

    #print(strData[1:,1:])
    csvFile.close()
    return dataNP


def getData(fileName, strNote):
    dataFeatures = readCSV_base(fileName)

    Num_Data = len(dataFeatures)

    for i in range(Num_Data):
        if dataFeatures[i]:
            if dataFeatures[i][0]==strNote:
                IPedStart=i
                
    for j in range(IPedStart, Num_Data):
        if dataFeatures[j]==[]:
            IPedEnd=j
            break
        if j==Num_Data-1:
            IPedEnd=Num_Data

    dataOK = dataFeatures[IPedStart : IPedEnd]
    return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]
    

# This function is not used in this program
def readCSV(fileName, mode='float'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    print (dataNP)
    print('np.shape(dataNP)', np.shape(dataNP))
    print('\n')

    #print(strData[1:,1:])
    csvFile.close()	
    
    if mode=='string':
        print (dataNP[1:, 1:])
        return dataNP[1:, 1:]
	
    if mode=='float':
        
        #print dataNP[1:, 1:]
        (I, J) = np.shape(dataNP)
        #print "The size of tha above matrix:", [I, J]
        #print "The effective data size:", [I-1, J-1]
        matrix = np.zeros((I, J))
        #print matrix

        for i in range(1,I):
            for j in range(1,J):
                matrix[i,j] = float(dataNP[i,j])

    print (matrix[1:, 1:])
    return matrix[1:, 1:]
    

def readFloatArray(tableFeatures, NRow, NColomn, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(tableFeatures[i+1][j+1])
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrix)
    return matrix


# The file to record the some output data of the simulation
# f = open("outData.txt", "w+")

def readAgents(FileName, debug=True, marginTitle=1, ini=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, UpperIndex = getData(FileName, '&Ped')
    Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agents = []
    for agentFeature in agentFeatures[marginTitle:]:
        agent = person()
        agent.pos = np.array([float(agentFeature[ini+0]), float(agentFeature[ini+1])])
        agent.dest= np.array([float(agentFeature[ini+2]), float(agentFeature[ini+3])])
        agent.tau = float(agentFeature[ini+4])
        agent.tpre = float(agentFeature[ini+5])
        agent.p = float(agentFeature[ini+6])
        agent.pMode = agentFeature[ini+7]
        agent.aType = agentFeature[ini+8]
        agent.interactionRange = float(agentFeature[ini+9])
        agent.ID = int(agentFeature[ini+10])
        agent.moving_tau = float(agentFeature[ini+11])
        agent.tpre_tau = float(agentFeature[ini+12])
        agent.talk_tau = float(agentFeature[ini+13])
        agent.talk_prob = float(agentFeature[ini+14])
        agent.inComp = int(agentFeature[ini+15])
        agents.append(agent)
        
    return agents


# This function addAgent() is actually not that meaningful.  We just leave it here for future optional development.  
# Because many agent features cannot be added by using the graphic user interface.
# Such as group features and door selection features.
def addAgent(agents, x_pos, y_pos):
    num = len(agents)
    agent = person()
    agent.pos = np.array([float(x_pos), float(y_pos)])
    agent.ID = int(num)
    agent.inComp = int(1)

    # add agent into the list of agents
    agents.append(agent)
    

def readWalls(FileName, debug=True, marginTitle=1, ini=1):
    #obstFeatures = readCSV(FileName, "string")
    #[Num_Obsts, Num_Features] = np.shape(obstFeatures)

    obstFeatures, lowerIndex, UpperIndex = getData(FileName, '&Wall')
    Num_Obsts=len(obstFeatures)-marginTitle

    if debug:
        print ('Number of Walls:', Num_Obsts, '\n')
        print ("Features of Walls\n", obstFeatures, "\n")
    
    walls = []
    for obstFeature in obstFeatures[marginTitle:]:
        wall = obst()
        wall.params[0]= float(obstFeature[ini+0])
        wall.params[1]= float(obstFeature[ini+1])
        wall.params[2]= float(obstFeature[ini+2])
        wall.params[3]= float(obstFeature[ini+3])
        wall.arrow = int(obstFeature[ini+4])
        wall.id = int(obstFeature[ini+5])
        wall.inComp = int(obstFeature[ini+6])
        wall.mode = obstFeature[ini+7]
        #wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
        #wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
        walls.append(wall)
        
    return walls


#This function addWall() is created for users to add wall in testGeom()
def addWall(walls, startPt, endPt, mode='line'):
    num = len(walls)
    wall = obst()
    
    if mode == 'line':
        wall.params[0]= float(startPt[0])
        wall.params[1]= float(startPt[1])
        wall.params[2]= float(endPt[0])
        wall.params[3]= float(endPt[1])
    if mode == 'rect':
        wall.params[0]= float(startPt[0])
        wall.params[1]= float(startPt[1])
        wall.params[2]= float(endPt[0])
        wall.params[3]= float(endPt[1])

    # The wall arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    wall.arrow = 0 #normalize(endPt - startPt)
    
    wall.mode = mode
    wall.id = int(num)
    wall.inComp = int(1)

    # Add wall into the list of walls
    walls.append(wall)


def readDoors(FileName, debug=True, marginTitle=1, ini=1):
    #doorFeatures = readCSV(FileName, "string")
    #[Num_Doors, Num_Features] = np.shape(doorFeatures)

    doorFeatures, lowerIndex, UpperIndex = getData(FileName, '&Door')
    Num_Doors=len(doorFeatures)-marginTitle

    if debug:
        print ('Number of Doors:', Num_Doors, '\n')
        print ('Features of Doors\n', doorFeatures, "\n")
    
    doors = []
    for doorFeature in doorFeatures[marginTitle:]:
        door = passage()
        door.params[0]= float(doorFeature[ini+0])
        door.params[1]= float(doorFeature[ini+1])
        door.params[2]= float(doorFeature[ini+2])
        door.params[3]= float(doorFeature[ini+3])
        door.arrow = int(doorFeature[ini+4])
        door.id = int(doorFeature[ini+5])
        door.inComp = int(doorFeature[ini+6])
        door.exitSign = int(doorFeature[ini+7])
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        
    return doors


#This function addDoor() is created for users to add door in testGeom()
def addDoor(doors, startPt, endPt, mode='rect'):
    num = len(doors)
    door = passage()
    
    if mode == 'rect':
        door.params[0]= float(startPt[0])
        door.params[1]= float(startPt[1])
        door.params[2]= float(endPt[0])
        door.params[3]= float(endPt[1])

    # The wall arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    door.arrow = 0 #normalize(endPt - startPt)
    
    #door.mode = mode   # door has no attribute of "mode"

    door.id = int(num)
    door.inComp = int(1)
    door.exitSign = int(0)
    door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
    
    # Add door into the list of doors
    doors.append(door)
    

#[Num_Doors, Num_DoorFeatures] = np.shape(doorFeatures)
#if np.shape(agent2doors)[0]!= Num_Agents or np.shape(agent2doors)[1]!= Num_Doors:
#    print '\nError on input data: doors or agent2doors \n'
#    print >>f, '\nError on input data: doors or agent2doors \n'


def readExits(FileName, debug=True, marginTitle=1, ini=1):
    #exitFeatures = readCSV(FileName, "string")
    #[Num_Exits, Num_Features] = np.shape(exitFeatures)

    exitFeatures, lowerIndex, UpperIndex = getData(FileName, '&Exit')
    Num_Exits=len(exitFeatures)-marginTitle

    if debug: 
        print ('Number of Exits:', Num_Exits, '\n')
        print ("Features of Exits\n", exitFeatures, "\n")
    
    exits = []
    for exitFeature in exitFeatures[marginTitle:]:
        exit = passage()
        exit.params[0]= float(exitFeature[ini+0])
        exit.params[1]= float(exitFeature[ini+1])
        exit.params[2]= float(exitFeature[ini+2])
        exit.params[3]= float(exitFeature[ini+3])
        exit.arrow = int(exitFeature[ini+4])
        exit.id = int(exitFeature[ini+5])
        exit.inComp = int(exitFeature[ini+6])
        exit.exitSign = int(exitFeature[ini+7])
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
        exits.append(exit)
        
    return exits


def readCHID(FileName):

    findHEAD=False
    for line in open(FileName):
        if re.match('&HEAD', line):
            findHEAD=True
        if  findHEAD:
            if re.search('CHID', line):
                temp1=line.split('CHID')
                line1=temp1[1]
                temp2 =  line1.split('\'')
                keyInfo = temp2[1]
                return keyInfo



def readOBST(FileName, Keyword='&OBST', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("OBSTout.txt", "w+")
    obstFeatures = []
    findOBST=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findOBST=True
        if  findOBST:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip('= ')
                #line1=temp1[1].strip('= ')
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()
                coords = re.split(r'[\s\,]+', dataXYZ)
                print(coords)
                if float(coords[4])<Zmin and float(coords[5])<Zmin:
                    continue
                if float(coords[4])>Zmax and float(coords[5])>Zmax:
                    continue
                obstFeature = []
                obstFeature.append(float(coords[0]))
                obstFeature.append(float(coords[2]))
                obstFeature.append(float(coords[1]))
                obstFeature.append(float(coords[3]))
                obstFeatures.append(obstFeature)
                findOBST=False

            if debug:
                print (line, '\n', obstFeature)
                #print >>fo, line
                #print >>fo, obstFeature

    #print >>fo, 'test\n'
    #print >>fo, 'OBST Features\n'
    #print >>fo, obstFeatures
    
    if outputFile!=None:
        with open(outputFile, mode='wb+') as obst_test_file:
            csv_writer = csv.writer(obst_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/mode'])
            index_temp=0
            for obstFeature in obstFeatures:
                csv_writer.writerow(['--', str(obstFeature[0]), str(obstFeature[1]), str(obstFeature[2]), str(obstFeature[3]), '0', str(index_temp), '1', 'rect'])
                index_temp=index_temp+1
    
    walls = []
    index = 0
    for obstFeature in obstFeatures:
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.arrow = 0
        wall.id = index
        wall.inComp = 1
        wall.mode = 'rect'
        walls.append(wall)
        index = index+1
    return walls


def readPATH(FileName, Keyword='&HOLE', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("HOLEout.txt", "w+")
    holeFeatures = []
    
    findPATH=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findPATH=True
            
        if  findPATH:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip('= ')
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()    
                coords = re.split(r'[\s\,]+', dataXYZ)
                if float(coords[4])<Zmin and float(coords[5])<Zmin:
                    continue
                if float(coords[4])>Zmax and float(coords[5])>Zmax:
                    continue
                holeFeature = []
                holeFeature.append(float(coords[0]))
                holeFeature.append(float(coords[2]))
                holeFeature.append(float(coords[1]))
                holeFeature.append(float(coords[3]))
                holeFeatures.append(holeFeature)
                findPATH=False

                if debug:
                    print (line, '\n', holeFeature)
                    #print >>fo, line
                    #print >>fo, holeFeature

    #print >>fo, 'test\n'
    #print >>fo, 'HOLE Features\n'
    #print >>fo, holeFeatures

    if outputFile!=None:
        with open(outputFile, mode='wb+') as door_test_file:
            csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
            index_temp=0
            for holeFeature in holeFeatures:
                csv_writer.writerow(['--', str(holeFeature[0]), str(holeFeature[1]), str(holeFeature[2]), str(holeFeature[3]), '0', str(index_temp), '1', '0'])
                index_temp=index_temp+1

    doors = []
    index = 0
    for holeFeature in holeFeatures:
        door = passage()
        door.params[0]= float(holeFeature[0])
        door.params[1]= float(holeFeature[1])
        door.params[2]= float(holeFeature[2])
        door.params[3]= float(holeFeature[3])
        door.arrow = 0
        door.id = index
        door.inComp = 1
        door.exitSign = 0
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        index = index+1
    return doors


# This function will be used in this program in future
def readEXIT(FileName, Keyword='&EXIT', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("EXITout.txt", "w+")
    exitFeatures = []
    findEXIT=False
    
    for line in open(FileName):
        if re.match(Keyword, line):
            findEXIT=True
            
        if findEXIT:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip('= ')
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1]
                #coords = dataXYZ.split(',')
                coords = re.split(r'[\s\,]+', dataXYZ)
                if float(coords[4])<Zmin and float(coords[5])<Zmin:
                    continue
                if float(coords[4])>Zmax and float(coords[5])>Zmax:
                    continue
                exitFeature = []
                exitFeature.append(float(coords[0]))
                exitFeature.append(float(coords[2]))
                exitFeature.append(float(coords[1]))
                exitFeature.append(float(coords[3]))
                exitFeatures.append(exitFeature)
                findEXIT=False

                if debug:
                    print (line, '\n', exitFeature)
                    #print >>fo, line
                    #print >>fo, exitFeature

    #print >>fo, 'test\n'
    #print >>fo, 'EXIT Features\n'
    #print >>fo, exitFeatures

    if outputFile:
        with open(outputFile, mode='wb+') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
            index_temp=0
            for exitFeature in exitFeatures:
                csv_writer.writerow(['--', str(exitFeature[0]), str(exitFeature[1]), str(exitFeature[2]), str(exitFeature[3]), '0', str(index_temp), '1', '0'])
                index_temp=index_temp+1

    exits = []
    index = 0
    for exitFeature in exitFeatures:
        exit = passage()
        exit.params[0]= float(exitFeature[0])
        exit.params[1]= float(exitFeature[1])
        exit.params[2]= float(exitFeature[2])
        exit.params[3]= float(exitFeature[3])
        exit.arrow = 0   #  This need to be improved
        exit.id = index
        exit.inComp = 1
        exit.exitSign = 0
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
        
        if exit.params[0]==exit.params[2]:
            exit.params[0]=exit.params[0]-0.2
            exit.params[2]=exit.params[2]+0.2
            
        if exit.params[1]==exit.params[3]:
            exit.params[1]=exit.params[1]-0.2
            exit.params[3]=exit.params[3]+0.2           
            
        exits.append(exit)
        index = index+1
    return exits


def updateDoorData(doors, outputFile):
    with open(outputFile, mode='wb+') as door_test_file:
        csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['&Door', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
        index_temp=0
        for door in doors:
            csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.id), str(door.inComp), str(door.exitSign)])
            index_temp=index_temp+1


def updateWallData(walls, outputFile):
    with open(outputFile, mode='wb+') as wall_test_file:
        csv_writer = csv.writer(wall_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['&Wall', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/mode'])
        index_temp=0
        for wall in walls:
            csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.id), str(wall.inComp), str(wall.mode)])
            index_temp=index_temp+1
            

def updateExit2Doors(exit2doors, fileName):
    (I, J) = np.shape(exit2doors)
    #print "The size of exit2door:", [I, J]
    #dataNP = np.zeros((I+1, J+1))

    dataNP=[]
    for i in range(I+1):
        row=[]
        if i==0:
            row.append('&Exit2Door')
            for j in range(1, J+1):
                row.append('DoorID'+str(j-1))
        else:
            row.append('ExitID'+str(i-1))
            for j in range(1, J+1):
                row.append(exit2doors[i-1, j-1])
            
        dataNP.append(row)

    #dataNP[1:, 1:] = exit2doors
    np.savetxt(fileName, dataNP, delimiter=',', fmt='%s')   #'2darray.csv'


if __name__ == '__main__':

    #test = readCSV("agentData2018.csv", 'string')
    doorFeatures = getData("newDataForm.csv", '&Door')
    print (doorFeatures)
    print (np.shape(doorFeatures))

    pedFeatures = getData("newDataForm.csv", '&Ped')
    print (pedFeatures)
    print (np.shape(pedFeatures))

    agents = readAgents("newDataForm.csv")
    walls = readWalls("newDataForm.csv")
    doors = readDoors("newDataForm.csv")
    exits = readExits("newDataForm.csv")
    
    print ('Length of agents:', len(agents))
    print ('Length of walls:', len(walls))

    ped2ExitFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    print (ped2ExitFeatures)
    matrix = np.zeros((len(agents), len(exits)))
    for i in range(len(agents)):
            for j in range(len(exits)):
                matrix[i,j] = float(ped2ExitFeatures[i+1][j+1])
    print ('matrix', matrix)

    Exit2DoorFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Exit2Door')
    print (Exit2DoorFeatures)
    matrix = np.zeros((len(exits), len(doors)))
    for i in range(len(exits)):
            for j in range(len(doors)):
                matrix[i,j] = float(Exit2DoorFeatures[i+1][j+1])
    print ('matrix', matrix)
    
        #for index in range(Num_Data):
        #if dataFeatures[0,index]=='&Ped':
        #    IPedStart=index
        #    while dataFeatures[0,index]!='':
        #        index=index+1
        #    IPedEnd=index

    #agentFeatures = dataFeatures[IPedStart : IPedEnd]
    #[Num_Agents, Num_Features] = np.shape(agentFeatures)

    #doors = readDoors("doorData2019.csv", True)
    #exits = readExits("doorData2018.csv", True)
    
    # Initialize Desired Interpersonal Distance
    #DFactor_Init = readCSV("D_Data2018.csv", 'float')
    #AFactor_Init = readCSV("A_Data2018.csv", 'float')
    #BFactor_Init = readCSV("B_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&groupB')
    BFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    BFactor_Init

    # Input Data Check
    #[Num_D1, Num_D2]=np.shape(DFactor_Init)
    #[Num_A1, Num_A2]=np.shape(AFactor_Init)
    #[Num_B1, Num_B2]=np.shape(BFactor_Init)

    #print >>f, np.shape(DFactor_Init), [Num_Agents, Num_Agents], '\n'

    print('\n', 'Test Output: exit2door.csv')
    exit2door=np.array([[ 1.0,  1.0,  1.0], [ 1.0,  -1.0,  -2.0], [ 1.0,  1.0,  1.0]])
    print(exit2door)
    updateExit2Doors(exit2door, 'test_exit2door.csv')

