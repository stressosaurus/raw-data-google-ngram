#!/usr/bin/env python3

##!/home/[username]/miniconda3/bin/python

### Computes 
### 1. the rscore matrix - raw scores,
### 3. the pscore matrix - probability scores,
### 4. the zscore matrix - normalized score
### of the filtered google ngram data.
## Alex John Quijano
## Created: 3/17/2018

import pandas as pd
import numpy as np
import sys
import os
import re

# string to boolean
def str2bool(v):
  return v.lower() in ("yes", "true", "1")

# ngram parameters
n = sys.argv[1]
l = sys.argv[2]
ignore_case = str2bool(sys.argv[3])
restriction = str2bool(sys.argv[4])
annotation = str2bool(sys.argv[5])

# generate rscore matrix with some restriction
def generate_rscore(l,ignore_case,restriction,annotation,gram_specific=[]):
	
	# Data directory
	data_path = n+'gram-filtered/googlebooks-'+l+'-all-'+n+'gram-20120701.filtered'
	
	# Read file
	grams_all = []
	years_all = []
	rscore_all = []
	file = open(data_path)
	for line in file:
		l1 = line.replace('\n','')
		line = re.split('\t',l1)
		
		# gram specific ngrams
		if len(gram_specific) != 0:
			match = 0
			gram_check = line[0].lower()
			gram_check = re.split('\s',gram_check)
			for gc in gram_check:
				if gc in gram_specific:
					match = 1
		else:
			match = 1
			
		if match == 1:
			grams_all.append(str(line[0]))
			years_all.append(int(line[1]))
			rscore_all.append(int(line[2]))
			
	year_max = np.max(years_all)
	year_min = np.min(years_all)
	year_length = (year_max - year_min) + 1
	
	# the rscore matrix - unrestricted
	rscore = {}
	for i, j in enumerate(grams_all):
		
		# ignore cases
		if ignore_case == True:
			try:
				gram = j.split('_')
				gram = gram[0].lower()+'_'+gram[1]
			except:
				gram = j.lower()
		elif ignore_case == False:
			gram = j
			
		try:
			rscore[gram][years_all[i]] = rscore[gram][years_all[i]] + rscore_all[i]
		except:
			try:
				rscore[gram][years_all[i]] = rscore_all[i]
			except:
				rscore[gram] = {}
				rscore[gram][years_all[i]] = rscore_all[i]
				
	# restriction and annotation
	rscore_pos = {}
	pos_vector = {}
	for i in rscore.keys():
		years = rscore[i].keys()
		# restriction
		if restriction == True:
			years_lim = year_length
		elif restriction == False:
			years_lim = 1
			
		if len(years) >= years_lim:
			annotation_code = re.search(r'\_.+',i)
			if annotation_code != None:
				an = annotation_code.group(0).replace('_','')
				if an not in ['NOUN','VERB','ADJ','ADV','PRON','DET','ADP','NUM','CONJ','PRT']:
					an = 'O'
			else:
				an = ''
				
			if annotation == False:
				gram = re.sub(r'\_.+','',i)
				try:
					pos_vector[gram].append(an)
				except:
					pos_vector[gram] = [an]
			elif annotation == True:
				gram = i
				pos_vector[gram] = an
			
			for j in years:
				try:
					rscore_pos[gram][j] = rscore_pos[gram][j] + rscore[i][j]
				except:
					try:
						rscore_pos[gram][j] = rscore[i][j]
					except:
						rscore_pos[gram] = {}
						rscore_pos[gram][j] = rscore[i][j]
					
	rscore_matrix = pd.DataFrame.from_dict(rscore_pos,orient='index').fillna(0).astype('float64')
	
	return rscore_matrix, pos_vector

# generate pscore matrix
def generate_pscore(rscore_matrix):
	
	return np.divide(rscore_matrix,np.sum(rscore_matrix,axis=0))

# generate zscore matrix
def generate_zscore(pscore_matrix):
	
	a = pscore_matrix.T - np.mean(pscore_matrix.T,axis=0)
	b = np.std(pscore_matrix.T,axis=0)
	
	return np.divide(a,b).T
	
# create directory
directory_0 = n+'gram-normalized/'
try:
	os.makedirs(directory_0)
except FileExistsError:
	pass

# generate all matrices
def generate_matrices(language):
	if n == '1':
		try:
			specific_fileName = sys.argv[6]
		except:
			specific_fileName = ''
		if specific_fileName != 'all':
			specific_fileName = 'all'
		rscore, pos_annotation = generate_rscore(language,ignore_case,restriction,annotation)
	elif n != '1':
		specific_fileName = sys.argv[6]
		if specific_fileName != 'all':
			specific_fileName = 'all'
		gram_specific = []
		try:
			file = open(specific_fileName,'r')
			for line in file:
				gram_specific.append(line.replace('\n',''))
		except FileNotFoundError:
			pass
		rscore, pos_annotation = generate_rscore(language,ignore_case,restriction,annotation,gram_specific=gram_specific)
		specific_fileName = '-'+specific_fileName
	
	pscore = generate_pscore(rscore)
	try:
		zscore = generate_zscore(pscore)
	except:
		zscore = None
	
	directory_1 = directory_0+language+'/'
	try:
		os.makedirs(directory_1)
	except FileExistsError:
		pass
	
	rscore.to_pickle(directory_1+'googlebooks-'+language+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.rscore.pkl',compression='gzip')
	pscore.to_pickle(directory_1+'googlebooks-'+language+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pscore.pkl',compression='gzip')
	try:
		zscore.to_pickle(directory_1+'googlebooks-'+language+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.zscore.pkl',compression='gzip')
	except:
		pass
	np.save(directory_1+'googlebooks-'+language+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pos.npy',pos_annotation)

	print('normalization complete for '+'googlebooks-'+language+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pkl')

generate_matrices(l)