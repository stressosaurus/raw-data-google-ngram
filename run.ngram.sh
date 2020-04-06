#!/bin/bash

## Google ngram raw data downloader, filter, and Normalizer
## Alex John Quijano
## Created: 2/12/2017

date
uname -s -n -r -p
echo $'\n'

## Available languages
#	eng			english
#	eng-us		american english
#	eng-gb		british english
#	eng-fiction	english fiction
#	chi-sim		chinese simplified
#	fre			french
#	ger			german
#	heb			hebrew
#	ita			italian
#	rus			russian
#	spa			spanish

## Variables
n=$1
specific=$2

## Language array
l[0]=eng
l[1]=eng-us
l[2]=eng-gb
l[3]=eng-fiction
l[4]=chi-sim
l[5]=fre
l[6]=ger
l[7]=heb
l[8]=ita
l[9]=rus
l[10]=spa

## Book count array
bookCount[0]=500
bookCount[1]=500
bookCount[2]=500
bookCount[3]=200
bookCount[4]=1
bookCount[5]=200
bookCount[6]=200
bookCount[7]=10
bookCount[8]=200
bookCount[9]=200
bookCount[10]=200

if [ ${n} -eq 1 ]
then
#	index=(0 1 2 3 4 5 6 7 8 9 10)
	index=(4)
elif [ ${n} -eq 2 ]
then
	bookCount[0]=500
	bookCount[1]=500
	bookCount[2]=500
	bookCount[3]=200
#	index=(0 1 2 3)
	index=(4)
fi

# for local machine
echo '##---------------------------------------------------------------------##'

# Download and Filter raw data then normalize filtered data
for i in "${index[@]}";
do
	echo 'downloading ' ${l[$i]} '...'
	./downloadAndFilter.ngram.sh ${n} ${l[$i]} 1900 2008 1 ${bookCount[$i]}
	echo 'normalizing ' ${l[$i]} '...'
	./normalize.ngram.py ${n} ${l[$i]} True True True ${specific}
	./normalize.ngram.py ${n} ${l[$i]} True True False ${specific}
	./normalize.ngram.py ${n} ${l[$i]} True False True ${specific}
	./normalize.ngram.py ${n} ${l[$i]} True False False ${specific}
	./normalize.ngram.py ${n} ${l[$i]} False False True ${specific}
	./normalize.ngram.py ${n} ${l[$i]} False False False ${specific}
	./normalize.ngram.py ${n} ${l[$i]} False True True ${specific}
	./normalize.ngram.py ${n} ${l[$i]} False True False ${specific}
done

# for hpc
#echo '##---------------------------------------------------------------------##'

# Download and Filter raw data then normalize filtered data
#for i in "${index[@]}";
#do
#	mkdir -p 'hpc-log'
#	sbatch hpc.downloadAndFilter.ngram.sh ${n} ${l[$i]} 1900 2008 1 ${bookCount[$i]}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} True True True ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} True True False ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} True False True ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} True False False ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} False False True ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} False False False ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} False True True ${specific}
#	sbatch hpc.normalize.ngram.sh ${n} ${l[$i]} False True False ${specific}
#done
