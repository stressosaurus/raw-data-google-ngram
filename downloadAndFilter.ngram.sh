#!/bin/bash

### Download and Filter Google ngram data (Version 20120701 "v2")
## Alex John Quijano
## Created: 2/12/2017
## Updated: 5/28/2017

# Arguments
n=$1
language=$2
yearLowerBound=$3
yearUpperBound=$4
wordCountLowerBound=$5
bookCountLowerBound=$6

# Arrays
# Alphabet
g[0]=a g[1]=b g[2]=c g[3]=d g[4]=e g[5]=f g[6]=g g[7]=h g[8]=i g[9]=j
g[10]=k g[11]=l g[12]=m g[13]=n g[14]=o g[15]=p g[16]=q g[17]=r g[18]=s g[19]=t
g[20]=u g[21]=v g[22]=w g[23]=x g[24]=y g[25]=z

# numerals
#g[26]=0 g[27]=1 g[28]=2 g[29]=3 g[30]=4 g[31]=5 g[32]=6 g[33]=7 g[34]=8 g[35]=9 g[36]=punctuation

# downloader and filter function
function df {
	alpha=$1
	beta=$2

	# downloader
	if [ -e ${n}gram-raw/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta} ]
	then
		:
	else
		wget -q http://storage.googleapis.com/books/ngrams/books/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.gz

		# Extract tgz files and place in designated folder
		if [ -e googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.gz ]
		then
			gzip -d googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.gz
			mv googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta} ${n}gram-raw/${language}

			echo "googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}"
		fi
	fi
	
	# filter
	if [ -e ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered ]
	then
		:
	else
		if [ -e ${n}gram-raw/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta} ]
		then
			if [ ${n} -eq 1 ]
			then
				# 1st filter (year lower bound)
				awk -v var="$yearLowerBound" '$2 >= var' ${n}gram-raw/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta} > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0

				# 2nd filter (year upper bound)
				awk -v var="$yearUpperBound" '$2 <= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1

				# 3rd filter (word count lower bound)
				awk -v var="$wordCountLowerBound" '$3 >= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2

				# 4th filter (book count lower bound)
				awk -v var="$bookCountLowerBound" '$4 >= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered

				# Remove extra files
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2
			elif [ ${n} -ge 2 ]
			then
				# 1st filter (year lower bound)
				awk -v var="$yearLowerBound" '$3 >= var' ${n}gram-raw/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta} > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0

				# 2nd filter (year upper bound)
				awk -v var="$yearUpperBound" '$3 <= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1

				# 3rd filter (word count lower bound)
				awk -v var="$wordCountLowerBound" '$4 >= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2

				# 4th filter (book count lower bound)
				awk -v var="$bookCountLowerBound" '$5 >= var' ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2 > ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered

				# Remove extra files
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered0
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered1
				rm ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered2
			fi

			echo "googlebooks-${language}-all-${n}gram-20120701-${alpha}${beta}.filtered"
		fi
	fi
}

# download and filter loop
mkdir -p ${n}gram-raw/${language}
mkdir -p ${n}gram-filtered/${language}

if [ ${n} -eq 1 ]
then
	for i in "${g[@]}";
	do
		df ${i} ""
	done
elif [ ${n} -ge 2 ]
then
	# Extension (if n >= 2)
	g[26]="_"
	for i in "${g[@]}";
	do
		for j in "${g[@]}";
		do
			df ${i} ${j}
		done
	done
fi

# record raw data information and delete raw data
wc -lc ${n}gram-raw/${language}/googlebooks-${language}-all-${n}gram-20120701-* > ${n}gram-raw/googlebooks-${language}-all-${n}gram-20120701.info
rm -rf ${n}gram-raw/${language}

# concatenate filtered files
cat ${n}gram-filtered/${language}/googlebooks-${language}-all-${n}gram-20120701-*.filtered > ${n}gram-filtered/googlebooks-${language}-all-${n}gram-20120701.filtered
wc -lc ${n}gram-filtered/googlebooks-${language}-all-${n}gram-20120701.filtered > ${n}gram-filtered/googlebooks-${language}-all-${n}gram-20120701.filtered.info
echo "n:$1 language:$language yearLowerBound:$yearLowerBound yearUpperBound:$yearUpperBound wordCountLowerBound:$wordCountLowerBound bookCountLowerBound:$bookCountLowerBound" >> ${n}gram-filtered/googlebooks-${language}-all-${n}gram-20120701.filtered.info
rm -rf ${n}gram-filtered/${language}

echo ""
echo "googlebooks-${language}-all-${n}gram-20120701 download and filter is finished!"