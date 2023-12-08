import argparse
import time
import numpy as np
from tabulate import tabulate
from math import sqrt
import pdb


##### I THINK THE IDEA OF THE CODE IS OK BUT IT STILL HAS SOME ERRORS SO IT DOESNT RUN, IM STILL TRYING TO CORRECT THEM

def shiftRegister(C, N, init):
	out = []
	current = init
	while len(out) < N:
		#print("CURRENT: ", current)
		#breakpoint()
		add = 0
		for ix,i in enumerate(C):
			add += i*init[i]
		current.append(add%2)
		out.append(current[0])
		current.pop(0)
	return out

def calculateHamming(u,z):
	hamm = 0
	for ix,i in enumerate(u):
		if u == int(z[ix]):
			hamm += 1
	return hamm

def calculatePStar(hamm, N):
	return 1 - (hamm/N)

def findKeyLFSR(C,N,stream):
	L = len(C)
	p_star = []
	for i in range(0,2**L):
		init = [int(x) for x in str(bin(i))[2:]]
		while len(init) < L:
			init.insert(0,0)
		breakpoint()
		u = shiftRegister(C,N,init)
		breakpoint()
		p_star.append(calculateHamming(u,stream))

		print(p_star)
	return p_star.index(max(p_star))


def findKey(stream, showSteps):
	N = len(stream)
	key = []
	C1 = [1,1,0,1,0,1,1,0,0,1,1,0,1]
	key.append(bin(findKeyLFSR(C1,N,stream)))
	print("Broke L1! Key: ", key[-1])
	C2 = [0,1,0,1,0,1,1,0,0,1,1,0,1,0,1]
	key.append(bin(findKeyLFSR(C2,N,stream)))
	print("Broke L2! Key: ", key[-1])
	c3 = [0,1,0,1,1,0,0,1,0,1,0,0,1,0,0,1,1]
	key.append(bin(findKeyLFSR(C3,N,stream)))
	print("Broke L3! Key: ", key[-1])


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
	
	#print("Looking for the key of = " + stream)

	print("The key is: ", findKey(stream, showSteps))
