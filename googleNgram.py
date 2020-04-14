### Google Ngram Data Tools
## Alex John Quijano
## Created: 9/13/2017

import os
import re
import sys
import math
import errno
import numpy as np
import pandas as pd
import subprocess as sb

# Read Google ngram data
def read(n,l,ignore_case=True,restriction=True,annotation=False,specific_fileName='all'):

	try:
		# raw data (in of directory)
		directory_A = '/google-ngram/'+n+'gram-normalized/'+l+'/'
		directory_0 = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+directory_A
		rscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.rscore.pkl',compression='gzip')
		pscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pscore.pkl',compression='gzip')
		try:
			zscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.zscore.pkl',compression='gzip')
		except:
			zscore = None
		pos_annotation = np.load(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pos.npy',allow_pickle=True).item()
		
		return {'rscore':rscore,'pscore':pscore,'zscore':zscore,'pos':pos_annotation}

	except FileNotFoundError:
		try:
			# raw data (out of directory)
			directory_A = '/raw-data/google-ngram/'+n+'gram-normalized/'+l+'/'
			directory_0 = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+directory_A
			rscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.rscore.pkl',compression='gzip')
			pscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pscore.pkl',compression='gzip')
			try:
				zscore = pd.read_pickle(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.zscore.pkl',compression='gzip')
			except:
				zscore = None
			pos_annotation = np.load(directory_0+'googlebooks-'+l+'-all-'+n+'gram-20120701.filtered.'+'I'+str(ignore_case)+'R'+str(restriction)+'A'+str(annotation)+'.'+specific_fileName+'.pos.npy',allow_pickle=True).item()
			
			return {'rscore':rscore,'pscore':pscore,'zscore':zscore,'pos':pos_annotation}
	
		except FileNotFoundError:
			print('Error: The computed-data directory can not be found of '+n+'gram dataset for '+l+' with specified parameters does not exist anywhere.')
			print('TRY: Use the bash script below to download and process the Google Ngram data according to your specified parameters or see Section 2 of the INSTRUCTIONS file.')
			print()
			print('%%bash')
			print('./downloadAndFilter.ngram.sh '+n+' '+l+' 1900 2008 1 1')
			print('./normalize.ngram.py '+n+' '+l+' '+str(ignore_case)+' '+str(restriction)+' '+str(annotation)+' '+specific_fileName)
			try:
				sys.exit()
			except SystemExit:
				sys.exit

# get word set from a file
def get_subset(DataFrame,file_path):

	# defined stop words
	ngrams = []
	try:
		file = open(file_path,encoding='utf-8')
	except FileNotFoundError:
		print('The file')
		
	for f in file:
		ngrams.append(f.replace('\n',''))
		
	df_ngrams = DataFrame.index
	df_ngrams_chosen = []
	for i in df_ngrams:
		i_split = i.split(' ')
		for j in i_split:
			if j in ngrams:
				df_ngrams_chosen.append(i)
				
	out = DataFrame.reindex(np.array(df_ngrams_chosen)).dropna(axis='index')
	
	print('Number of input words: '+str(len(ngrams)))
	print('Number of valid words: '+str(out.shape[0]))
		
	return out
