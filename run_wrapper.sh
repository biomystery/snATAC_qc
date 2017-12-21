#!/bin/bash

# wrapper to run the script
export PATH="$PATH:/home/zhc268/data/software/scATAC/scATAC/bin/"
#lanes_log="/home/zhc268/data/logs/run_20171221_demultiplex_snATAC.txt"
lanes=(`cat $lanes_log`)

cur_lane=${lanes[PBS_ARRAYID]}

#fastqdir="/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/"
outdir="${fastqdir}${cur_lane}"
mkdir -p $outdir

debarcode.py --i1 $fastqdir${cur_lane}_I1.fastq.gz --i2 $fastqdir${cur_lane}_I2.fastq.gz --r1 $fastqdir${cur_lane}_R1.fastq.gz  --r2 $fastqdir${cur_lane}_R2.fastq.gz --barcode /home/zhc268/data/software/snATAC_qc/barcodes/barcodes.txt -o $outdir
