#!/bin/bash


# bin_dir 
export PATH="$PATH:/home/zhc268/data/software/scATAC/scATAC/bin/"


# fastq_dir & fastqs 

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


# fastqc

for l in ${l1_fastq[@]}; do echo $l; fastqc -t 2 -o $libqc_dir $l; done
for l in ${l2_fastq[@]}; do echo $l; fastqc -t 2 -o $libqc_dir $l; done

# fastq_screen

for l in $



