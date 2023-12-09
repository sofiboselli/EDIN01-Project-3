import argparse
from time import time

def shiftRegister(C, N, init):
	# C is a list of the coefficients of the LFSR
	# N is the number of output desired
	# init is a list of the initial state of the LFSR
	out = []
	current = init.copy()
	while len(out) < N:
		add = 0
		for coeff_id,coeff in enumerate(C):
			add += coeff*current[coeff_id]
		current.append(add%2)
		out.append(current[0])
		current.pop(0)
	return out

def calculateHamming(u,z):
	# u and z are two vectors of the same size
	hamm = 0
	for coor_id,coor in enumerate(u):
		if coor != z[coor_id]:
			hamm += 1
	return hamm

def calculatePStar(u,z,N):
	# u and z are two vectors of the same size
	# N is the size of u and z
	hamm = calculateHamming(u,z)
	pStar = 1 - (hamm/N)
	return pStar

def findKeyLFSR(C,N,stream):
	# C is a list of the coefficient of the LFSR
	# N is the number of output desired
	# stream is the output stream that we use to compute correlation
	L = len(C)
	p_star = []
	for i in range(1,2**L):
		init = [int(x) for x in str(bin(i))[2:]]
		while len(init) < L:
			init.insert(0,0)
		u = shiftRegister(C,N,init)
		p_star.append(calculatePStar(u,stream,N))
	bestKeyIndex = p_star.index(max(p_star))
	bestKeyInt = bestKeyIndex + 1
	return bestKeyInt

def formatKey(L,key):
	# L is the length of the key
	# key is the integer number coresponding to the binary key
	key = [int(x) for x in str(bin(key))[2:]]
	while len(key) < L:
		key.insert(0,0)
	return key


def checkKey(C1,C2,C3,keys,N,stream):
	# C1 is a list of the coefficients of LFSR 1
	# C2 is a list of the coefficients of LFSR 2
	# C3 is a list of the coefficients of LFSR 3
	# keys is a list of the 3 intial states of LFSR 1, 2 & 3
	# N is the length of the output stream
	# stream is the output stream
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
			break
	return correct, z



def findKey(stream, showSteps):
	N = len(stream)
	keys = []

	# LSFR 1
	C1 = [1,0,1,1,0,0,1,1,0,1,0,1,1]
	beginDate1 = time()
	key1 = formatKey(len(C1),findKeyLFSR(C1,N,stream)) 
	endDate1 = time()
	keys.append(key1)
	print("Broke L1! \nKey: ", key1, "\nTime required for L1: ", endDate1-beginDate1)

	# LSFR 2
	C2 = [1,0,1,0,1,1,0,0,1,1,0,1,0,1,0]
	beginDate2 = time()
	key2 = formatKey(len(C2),findKeyLFSR(C2,N,stream)) 
	endDate2 = time()
	keys.append(key2)
	print("Broke L2! \nKey: ", key2, "\nTime required for L2: ", endDate2-beginDate2)

	# LSFR 3
	C3 = [1,1,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0]
	beginDate3 = time()
	key3 = formatKey(len(C3),findKeyLFSR(C3,N,stream)) 
	endDate3 = time()
	keys.append(key3)
	print("Broke L3! \nKey: ", key3, "\nTime required for L3: ", endDate3-beginDate3)
	print("Total time required: ", endDate1-beginDate1+endDate2-beginDate2+endDate3-beginDate3)

	print("Checking if correct:")
	correct,z = checkKey(C1,C2,C3,keys,N,stream)
	print("The key is correct? ", correct)

	return correct, keys



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
