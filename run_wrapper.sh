#!/bin/bash

# wrapper to run the script
export PATH="$PATH:/home/zhc268/data/software/snATAC_qc/"
#lanes_log="/home/zhc268/data/logs/run_20171221_demultiplex_snATAC.txt"
lanes=(`cat $lanes_log`)

cur_lane=${lanes[PBS_ARRAYID]}

#fastqdir="/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/"
outdir="${fastqdir}${cur_lane}"
mkdir -p $outdir

debarcode.py --i1 $fastqdir${cur_lane}_I1_001.fastq.gz --i2 $fastqdir${cur_lane}_I2_001.fastq.gz --r1 $fastqdir${cur_lane}_R1_001.fastq.gz  --r2 $fastqdir${cur_lane}_R2_001.fastq.gz --barcode /home/zhc268/data/software/snATAC_qc/barcodes/barcodes.txt -o $outdir
