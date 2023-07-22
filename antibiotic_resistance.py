import numpy as np 
import matplotlib.pyplot as plt 
import collections

class Bacterium(object):
	def __init__(self, x, y, MIC, n_mutations = 0):

		# location on lattice
		self.x = x
		self.y = y

		# minimum inhibitory concentration
		self.MIC = MIC 

		# number of mutations
		self.n_mutations = n_mutations
	


def reproduce(bacteria, pairs):

	for b in bacteria:
		
		current_MIC = b.MIC

		if np.random.random() < rep_rate:

			newx1 = (b.x + np.random.randint(0,2)) % simsize
			newy1 = (b.y + np.random.randint(-1,2)) % simsize

			p1 = (newx1,newy1)

			mutroll = np.random.uniform(0,1)

			if mutroll < p_mut:
				new_MIC = current_MIC * 10
				new_nmut = b.n_mutations + 1

			else:
				new_MIC = current_MIC
				new_nmut = b.n_mutations

			if p1 not in pairs:
				bacteria.append(Bacterium(newx1,newy1,new_MIC,new_nmut))
				pairs.append((newx1,newy1))
				
	return bacteria, pairs

def kill(bacteria, pairs, antibiotic_matrix):

	for b in bacteria:
		x = b.x
		y = b.y 
		MIC = b.MIC
		nmut = b.n_mutations

		if MIC < antibiotic_matrix[y,x]:

			bacteria.remove(b)
			pairs.remove((x,y))
			
	return bacteria,pairs






simsize  = 150
ab0      = 1    #mg/L
rep_rate = 0.025
p_mut    = 0.02

antibiotic_matrix = np.zeros((simsize, simsize))
bacteria  = []
pairs     = []
avmutlist = []
tlist     = []

# initialize ab matrix 
for x in range(simsize):
	for y in range(simsize):
		antibiotic_matrix[x,y] = ab0 * 10**((y//30)-1)


# initialize bacteria
for b in range(simsize):
	x = 0
	y = np.random.randint(0,simsize-1)

	pair = (x,y)

	if pair not in pairs:
		pairs.append(pair)
		bacteria.append(Bacterium(x, y, 0.5))
			
for t in range(500):
	bacteria,pairs = reproduce(bacteria,pairs)
	bacteria,pairs = kill(bacteria,pairs,antibiotic_matrix)
	print('time: %d, number of bacteria: %d' % (t,len(bacteria)))

bactinfo = [(b.x,b.y,b.n_mutations) for b in bacteria]
bandlist = []

for band in range(5):
	bsum = 0
	bandlist.append([])
	for x in range(band*30,(band+1)*30):
		for bact in bactinfo:
			if bact[0] == x:
				bsum += 1
				bandlist[band].append(bact[2])


	print('Number of bacteria in band: %d: %d' % (band,bsum))

for band in bandlist:
	ct = collections.Counter(band)
	print(ct)

plt.matshow(np.log10(antibiotic_matrix),fignum=0,cmap='gray_r')
plt.colorbar(label='antibiotic concentration [log mg/L]')
plt.scatter([b.x for b in bacteria],[b.y for b in bacteria],
	c=[b.n_mutations for b in bacteria], cmap='autumn', edgecolor='None', s = 10)
plt.colorbar(label = 'number of mutations')
plt.show()



