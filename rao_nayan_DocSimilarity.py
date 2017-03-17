import sys
import string
import re
import json
import itertools
import collections
import glob
import os
import itertools
from decimal import *


document = str(sys.argv[1])
path = document + '/*.txt'

k = int(sys.argv[2])

sh_type = sys.argv[3].lower()

hashes = int(sys.argv[4])
treshold = float(sys.argv[5])
worddic={}
textdic={}
un = set()
matrixbuild = set()


if sh_type == 'word':
	#read every .txt file from the directory
	for filename in glob.glob(path):
		
		li = [i.strip().split() for i in open(filename).readlines()]
		k = int(sys.argv[2])
		worddic[filename]={}
		#create k shingles
		for j in range(0,len(li[0])-k+1):
			word = ''.join(li[0][j:k])
			k +=1
			if word in worddic[filename]:
				worddic[filename][word]+=1
			else:
				worddic[filename][word]=1
	#generate all possible pais		
	for key in sorted(worddic):
		print "No of Shingles in File %s : %d" %(key,len(worddic[key]))
	#find jaccard similarity between pairs
	cout =0	
	for pair in itertools.combinations(sorted(worddic.keys()),2):
		cout+=1
		print "Jaccard Similarity between %s and %s :%.14f"%(pair[0],pair[1],Decimal(len(set(worddic[pair[0]]).intersection(set(worddic[pair[1]]))))/Decimal(len(set(worddic[pair[0]]).union(set(worddic[pair[1]])))))
		#print Decimal(len(set(worddic[pair[0]]).intersection(set(worddic[pair[1]]))))
		#print Decimal(len(set(worddic[pair[0]]).union(set(worddic[pair[1]]))))		
	similardocs = [[]  for i in range(cout)]
	for key in worddic:
		un = un.union(set(worddic[key]))
	
	#print len(un)
	#initialize multidimensional list
	dlist = [[]  for i in range(len(worddic))]
	count =0
	#each list[count] holds 0's and 1's for each text in the sorted order respectively
	for key in sorted(worddic):
		for word in sorted(un):
			if word in set(worddic[key]):
				dlist[count].append(1)
			else:
				dlist[count].append(0)
		count+=1		
	tlist = zip(*dlist)
	#print dlist[0]
	#print len(set(un))
	mlist = [[99999]*len(worddic)  for i in range(hashes)]
	mhashlist = [[]  for i in range(hashes)]
	i=1
	#for r in range(30):
	#	for c in range(len(tlist[0])):
	#		if tlist[r][c]==1:
	#			if (i*r+1)%len(un) < mlist[i-1][c]:
	#				mlist[i-1][c] = (i*r+1)%len(un)		
	#	i+=1
	a =0
	for i in range(hashes):
		row =0
		a +=1
		while row < len(un):
			mhashlist[i].append((a*row+1)%len(un))
			row +=1
	print"    "
	#print mlist
	#print len(mhashlist[0])
	tmhashlist = zip(*mhashlist)
	#print len(tmhashlist[0])
	#print tmhashlist[2]		
	

	for r in range(len(tlist)):
		for c in range(len(tlist[0])):
			if tlist[r][c]==1:
				for i in range(0,hashes):
					if mlist[i][c]>tmhashlist[r][i]:
						mlist[i][c]=tmhashlist[r][i]
	mtlist = zip(*mlist)
	#print mlist
	#print mtlist
	print "Min-Hash Signature for the Documents"
	t=0
	for key in sorted(worddic):
		print "%s : %s"%(key,list(mtlist[t]))
		t+=1

	pairlist=[]
	
	tot=0	
	for i in range(len(worddic)):
		pairlist.append(i)	
	for pairs in itertools.combinations(pairlist,2):
		
		total =0
		for k in range(len(mtlist[0])):
			if mtlist[pairs[0]][k]==mtlist[pairs[1]][k]:
				total+=1
		#print Decimal(total/hashes)		
		print "Jaccard Similarity between %s and %s :%.14f"%(sorted(worddic.keys())[pairs[0]],sorted(worddic.keys())[pairs[1]],(Decimal(total)/Decimal(hashes)))		
		#pairlist[tot].append(sorted(worddic.keys())[pairs[0]],sorted(worddic.keys())[pairs[1]],(Decimal(total)/Decimal(hashes)))
		if Decimal(total)/Decimal(hashes) > treshold:
			similardocs[tot].append(sorted(worddic.keys())[pairs[0]])
			similardocs[tot].append(sorted(worddic.keys())[pairs[1]])
			tot+=1
	print "   "
	print "   "
	print "Candidate pairs obtained using LSH"		
	for key in similardocs:
		if len(key)>0:
			print tuple(key)	


elif sh_type =='char':
	for filename in glob.glob(path):
		li = [i.strip() for i in open(filename).readlines()]
		k = int(sys.argv[2])
		textdic[filename]={}
		for j in range(0,len(li[0])-k):
			text = li[0][j:k]
			k +=1
			if text in textdic[filename]:
				textdic[filename][text]+=1
			else:
				textdic[filename][text]=1
	for key in sorted(textdic):
		print "No of Shingles in File %s : %d"%(key,len(textdic[key]))
	cout=0
	for pair in itertools.combinations(sorted(textdic.keys()),2):
		cout+=1
		print "Jaccard Similarity between %s and %s :%.14f"%(pair[0],pair[1],Decimal(len(set(textdic[pair[0]]).intersection(set(textdic[pair[1]]))))/Decimal(len(set(textdic[pair[0]]).union(set(textdic[pair[1]])))))	

	similardocs = [[]  for i in range(cout)]	
	for key in textdic:
		un = un.union(set(textdic[key]))
	
	#print len(un)
	#initialize multidimensional list
	dlist = [[]  for i in range(len(textdic))]
	count =0
	#each list[count] holds 0's and 1's for each text in the sorted order respectively
	for key in sorted(textdic):
		for word in sorted(un):
			if word in set(textdic[key]):
				dlist[count].append(1)
			else:
				dlist[count].append(0)
		count+=1		
	tlist = zip(*dlist)
	#print dlist[0]
	#print len(set(un))
	mlist = [[99999]*len(textdic)  for i in range(hashes)]
	mhashlist = [[]  for i in range(hashes)]
	i=1
	#for r in range(30):
	#	for c in range(len(tlist[0])):
	#		if tlist[r][c]==1:
	#			if (i*r+1)%len(un) < mlist[i-1][c]:
	#				mlist[i-1][c] = (i*r+1)%len(un)		
	#	i+=1
	a =0
	for i in range(hashes):
		row =0
		a +=1
		while row < len(un):
			mhashlist[i].append((a*row+1)%len(un))
			row +=1
	print"    "
	#print mlist
	#print len(mhashlist[0])
	tmhashlist = zip(*mhashlist)
	#print len(tmhashlist[0])
	#print tmhashlist[2]		
	

	for r in range(len(tlist)):
		for c in range(len(tlist[0])):
			if tlist[r][c]==1:
				for i in range(0,hashes):
					if mlist[i][c]>tmhashlist[r][i]:
						mlist[i][c]=tmhashlist[r][i]
	
	
	mtlist = zip(*mlist)

	print "Min-Hash Signature for the Documents"
	t=0
	for key in sorted(textdic):
		print "%s : %s"%(key,list(mtlist[t]))
		t+=1

	pairlist=[]
	
	tot=0	
	for i in range(len(textdic)):
		pairlist.append(i)	
	for pairs in itertools.combinations(pairlist,2):
		
		total =0
		for k in range(len(mtlist[0])):
			if mtlist[pairs[0]][k]==mtlist[pairs[1]][k]:
				total+=1
		#print Decimal(total/hashes)		
		print "Jaccard Similarity between %s and %s :%.14f"%(sorted(textdic.keys())[pairs[0]],sorted(textdic.keys())[pairs[1]],(Decimal(total)/Decimal(hashes)))
		if Decimal(total)/Decimal(hashes) > treshold:
			similardocs[tot].append(sorted(textdic.keys())[pairs[0]])
			similardocs[tot].append(sorted(textdic.keys())[pairs[1]])
			tot+=1
	print "   "
	print "   "
	print "Candidate pairs obtained using LSH"		
	for key in similardocs:
		if len(key)>0:
			print tuple(key)	

