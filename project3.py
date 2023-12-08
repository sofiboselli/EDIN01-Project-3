import argparse
import time
import numpy as np
from tabulate import tabulate
from math import sqrt
import pdb

def shiftRegister(C, N, init):
	out = []
	current = init
	while len(out) < N:
		add = 0
		for ix,i in enumerate(C):
			add += i*init[ix]
		current.append(add%2)
		out.append(current[0])
		current.pop(0)
	return out

def calculateHamming(u,z):
	hamm = 0
	for ix,i in enumerate(u):
		if i == z[ix]:
			hamm += 1
	return hamm

def calculatePStar(hamm, N):
	return 1 - (hamm/N)

def findKeyLFSR(C,N,stream):
	L = len(C)
	p_star = []
	for i in range(1,2**L):
		init = [int(x) for x in str(bin(i))[2:]]
		while len(init) < L:
			init.insert(0,0)
		u = shiftRegister(C,N,init)
		p_star.append(calculateHamming(u,stream))
	return p_star.index(max(p_star))

def formatKey(L,key):
	key = [int(x) for x in str(bin(key))[2:]]
	while len(key) < L:
		key.insert(0,0)
	return key


def checkKey(C1,C2,C3,keys,N,stream):
	L1 = shiftRegister(C1, N, keys[0])
	L2 = shiftRegister(C2, N, keys[1])
	L3 = shiftRegister(C3, N, keys[2])

	z = []
	correct = True
	for i in range(N):
		if L1[i] + L2[i] + L3[i] > 1:
			z.append(1)
		else:
			z.append(0)
		if z[i] != stream[i]:
			correct = False
	print("Z: ", z)
	print("STREAM: ",stream)
	return correct, z



def findKey(stream, showSteps):
	N = len(stream)
	key = []
	C1 = [1,1,0,1,0,1,1,0,0,1,1,0,1]
	key.append(formatKey(len(C1),(findKeyLFSR(C1,N,stream))))
	print("Broke L1! Key: ", key[-1])
	C2 = [0,1,0,1,0,1,1,0,0,1,1,0,1,0,1]
	key.append(formatKey(len(C2),(findKeyLFSR(C2,N,stream))))
	print("Broke L2! Key: ", key[-1])
	C3 = [0,1,0,1,1,0,0,1,0,1,0,0,1,0,0,1,1]
	key.append(formatKey(len(C3),(findKeyLFSR(C3,N,stream))))
	print("Broke L3! Key: ", key[-1])

	print("Checking if correct:")
	correct,z = checkKey(C1,C2,C3,key,N,stream)
	print("The key is correct? ", correct)

	return correct, key



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Find the key!")
	parser.add_argument("--keystream", required=False, type=str)
	parser.add_argument("--showSteps", required=False, type=bool)
	args = parser.parse_args()
	showSteps = args.showSteps

	if args.keystream:
		stream = args.keystream
	else:
		stream = "1001000110011110011001100111000011110110101011101110000111001011010100010110000000111001011011001000011000111000111010110010101100101001111110111111000010001011110010011111111101001110101100101"
		stream = [int(x) for x in stream]

	correct, key = findKey(stream, showSteps)

	if correct:
		print("The key is: ", key)
	else:
		print("A key was found but it did not yield the same stream :(")
