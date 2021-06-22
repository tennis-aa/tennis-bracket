from random import random
import math

def generateMonkeys(players,n):
    # helper variables
    bracketSize = len(players)
    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
        raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)
    
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))

    # generate random brackets
    monkeys = {}
    for k in range(n):
        bracket = []
        for i in range(int(bracketSize/2)):
            if players[2*i]=="Bye":
                bracket.append(players[2*i+1])
            elif players[2*i+1]=="Bye":
                bracket.append(players[2*i])
            elif random() < 0.5:
                bracket.append(players[2*i])
            else:
                bracket.append(players[2*i+1])
        
        for j in range(1,rounds):
            for i in range(int(bracketSize/(2**(j+1)))):
                if random()<0.5:
                    bracket.append(bracket[counter[j]-bracketSize+2*i])
                else:
                    bracket.append(bracket[counter[j]-bracketSize+2*i+1])
        monkeys["monkey"+str(k)] = bracket

    return monkeys


def generateBots(players,elo,n):
    # helper variables
    bracketSize = len(players)
    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
        raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)
    
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))

    # generate brackets based on probabilities from elo
    bots = {}
    for k in range(n):
        bracket = []
        bracket_elo = []
        for i in range(int(bracketSize/2)):
            if players[2*i]=="Bye":
                bracket.append(players[2*i+1])
                bracket_elo.apend(elo[2*i+1])
                continue
            elif players[2*i+1]=="Bye":
                bracket.append(players[2*i])
                bracket_elo.append(elo[2*i])
                continue
            
            Q1 = 10**(elo[2*i]/400)
            Q2 = 10**(elo[2*i+1]/400)
            probability = Q1/(Q1+Q2)
            if random() < probability:
                bracket.append(players[2*i])
                bracket_elo.append(elo[2*i])
            else:
                bracket.append(players[2*i+1])
                bracket_elo.append(elo[2*i+1])
        
        for j in range(1,rounds):
            for i in range(int(bracketSize/(2**(j+1)))):
                Q1 = 10**(bracket_elo[counter[j]-bracketSize+2*i]/400)
                Q2 = 10**(bracket_elo[counter[j]-bracketSize+2*i+1]/400)
                probability = Q1/(Q1+Q2)
                if random() < probability:
                    bracket.append(bracket[counter[j]-bracketSize+2*i])
                    bracket_elo.append(bracket_elo[counter[j]-bracketSize+2*i])
                else:
                    bracket.append(bracket[counter[j]-bracketSize+2*i+1])
                    bracket_elo.append(bracket_elo[counter[j]-bracketSize+2*i+1])
        bots["bot"+str(k)] = bracket

    return bots

def generateElo(players,elo):
    # helper variables
    bracketSize = len(players)
    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
        raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)
    
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))

    # generate brackets based on probabilities from elo
    bracket = []
    bracket_elo = []
    for i in range(int(bracketSize/2)):
        if players[2*i]=="Bye":
            bracket.append(players[2*i+1])
            bracket_elo.append(elo[2*i+1])
            continue
        elif players[2*i+1]=="Bye":
            bracket.append(players[2*i])
            bracket_elo.append(elo[2*i])
            continue
        
        if elo[2*i]>elo[2*i+1]:
            bracket.append(players[2*i])
            bracket_elo.append(elo[2*i])
        else:
            bracket.append(players[2*i+1])
            bracket_elo.append(elo[2*i+1])
    
    for j in range(1,rounds):
        for i in range(int(bracketSize/(2**(j+1)))):
            if bracket_elo[counter[j]-bracketSize+2*i]>bracket_elo[counter[j]-bracketSize+2*i+1]:
                bracket.append(bracket[counter[j]-bracketSize+2*i])
                bracket_elo.append(bracket_elo[counter[j]-bracketSize+2*i])
            else:
                bracket.append(bracket[counter[j]-bracketSize+2*i+1])
                bracket_elo.append(bracket_elo[counter[j]-bracketSize+2*i+1])
    Elo = {}
    Elo["Elo"] = bracket

    return Elo
