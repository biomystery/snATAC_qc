#!/bin/bash


# bin_dir 
export PATH="$PATH:/home/zhc268/data/software/scATAC/scATAC/bin/"

##################################################
# fastq_dir & fastqs 
##################################################
fastq_dir="/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/"
l1_fastq=(`find  $fastq_dir -name "*L001*.gz"  | sort -n`)
l2_fastq=(`find  $fastq_dir -name "*L002*.gz"  | sort -n`)

#/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/Undetermined_S0_L001_I1_001.fastq.gz
#/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/Undetermined_S0_L001_I2_001.fastq.gz
#/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/Undetermined_S0_L001_R1_001.fastq.gz
#/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/Undetermined_S0_L001_R2_001.fastq.gz


# output dir 
output_dir="/home/zhc268/others/JYH_165_JYH_166"
libqc_dir="/home/zhc268/others/JYH_165_JYH_166/libQCs"
mkdir -p $libqc_dir

##################################################
# fastqc
##################################################

for l in ${l1_fastq[@]}; do echo $l; fastqc -t 2 -o $libqc_dir $l; done
for l in ${l2_fastq[@]}; do echo $l; fastqc -t 2 -o $libqc_dir $l; done

# fastq_screen later



##################################################
# debarcode -> correct barcode ->  demultiplex
##################################################

# put barcode into the fastq name tag

# order: r7: 1-8  i7: 36-43 (I1-43)  i5:1-8 r5:30-37 (I2-37)

# p5, p7 the same between samples
# i5, I7 differ

a=`zcat Undetermined_S0_L001_I1_001.fastq.gz | grep --color -E 'CTCTCTAT' |head -n1`
echo ${#a} ; #43

zcat Undetermined_S0_L001_I1_001.fastq.gz | grep --color CTCTCTAT | head # i5 in the end

# merge barcodes
touch barcodes.txt
printf "JYH_166\tJYH_165\n" > barcodes.txt

paste p7_set1.txt i7_set1.txt i5_set1.txt p5_set1.txt p7_set2.txt i7_set2.txt i5_set2.txt p5_set2.txt >> barcodes.txt
cat -A barcodes.txt

zcat  ~/scratch/seqdata/2017_12_06_ChIP_B/R1.fastq.gz  | head -n 40000 > ./test/R1.fastq
zcat  ~/scratch/seqdata/2017_12_06_ChIP_B/R2.fastq.gz  | head -n 40000 > ./test/R2.fastq                      
zcat  ~/scratch/seqdata/2017_12_06_ChIP_B/I2.fastq.gz  | head -n 40000 > ./test/I2.fastq                      
zcat  ~/scratch/seqdata/2017_12_06_ChIP_B/I1.fastq.gz  | head -n 40000 > ./test/I1.fastq 

python ./debarcode.py --i1 ./test/I1.fastq --i2 ./test/I2.fastq --r1 ./test/R1.fastq  --r2 ./test/R2.fastq --barcode ./barcodes/barcodes.txt 

python ./debarcode.py --i1 ~/scratch/seqdata/2017_12_06_ChIP_B/I1.fastq.gz --i2 ~/scratch/seqdata/2017_12_06_ChIP_B/I2.fastq.gz --r1 ~/scratch/seqdata/2017_12_06_ChIP_B/R1.fastq.gz  --r2 ~/scratch/seqdata/2017_12_06_ChIP_B/R2.fastq.gz --barcode ./barcodes/barcodes.txt 



wc -l JYH_166_R1.fastq  #20676 JYH_166_R1.fastq
wc  -l JYH_165_R1.fastq #2268 JYH_165_R1.fastq
wc -l undetermined_R1.fastq #14056 undetermined_R1.fastq


##################################################
# add a cut file script 
##################################################

# cut each file into roughly equal file with lines that are 4 based

