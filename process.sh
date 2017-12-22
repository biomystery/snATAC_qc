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


##################################################
# qsub
##################################################
qsub -q condo -N demultiplex_snATAC -l nodes=1:ppn=1 -l walltime=08:00:00 -t 0-1 -v lanes_log="/home/zhc268/data/logs/run_20171221_demultiplex_snATAC.txt",fastqdir="/home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/" ./run_wrapper.sh


# reached walltime
cd /home/zhc268/scratch/seqdata/2017_12_06_ChIP_B
zcat /home/zhc268/scratch/seqdata/2017_12_06_ChIP_B/Undetermined_S0_L001_I1_001.fastq.gz | wc -l >l1_i1_lines.txt &
zcat Undetermined_S0_L001_I2_001.fastq.gz | wc -l >l1_i2_lines.txt &
zcat Undetermined_S0_L002_I2_001.fastq.gz | wc -l >l2_i2_lines.txt 
find ./Undetermined_S0_L001 -name "*.fastq" | xargs -n1 -I {} echo  "cat {} |wc -l > {}_lines.txt &" | bash
find ./Undetermined_S0_L002 -name "*.fastq" | xargs -n1 -I {} echo  "cat {} |wc -l > {}_lines.txt &" | bash
find ./Undetermined_S0_L001/ -name "*.txt" -exec cat {} \; 
find ./Undetermined_S0_L002/ -name "*.txt" -exec cat {} \; 
cur_l1=`find ./Undetermined_S0_L001/ -name "*R1*.txt" -exec cat {} \; | awk '{s+=$1} END {print s}'`
cur_l2=`find ./Undetermined_S0_L002/ -name "*R1*.txt" -exec cat {} \; | awk '{s+=$1} END {print s}'`

l1_lines=`cat l1_i1_lines.txt`
l2_lines=`cat l2_i2_lines.txt`

remain_l1=`echo $(( $l1_lines - $cur_l1 ))`
remain_l2=`echo $(( $l2_lines - $cur_l2 ))`

# verify the read name
zcat Undetermined_S0_L001_I1_001.fastq.gz |  head  -n ${cur_l1} | tail -n16 > cur_l1_i1.fastq & 
zcat Undetermined_S0_L001_R1_001.fastq.gz |  head  -n ${cur_l1} | tail -n16 > cur_l1_r1.fastq &
cur_l1_i1=(`cat cur_l1_i1.fastq`)
cur_l1_r1=(`cat cur_l1_r1.fastq`)
# 7001113:856:HVVNVBCXY:1:2107:11894:81333 1:N:0:0
# @7001113:856:HVVNVBCXY:1:2107:11918:81350 1:N:0:0

echo  $cur_l1_r1 
cur_s1_r1=(`tail -n5  ./Undetermined_S0_L001/JYH_165_R1.fastq`)
tail -n1 ./Undetermined_S0_L001/JYH_165_R1.fastq
#7001113:856:HVVNVBCXY:1:2107:10260:79049 1:N:0:0
#@TAATGCGCGAACGGTATCCGGTAAGGCTCTGA:7001113:856:HVVNVBCXY

echo  $cur_s1_r1 | cut -d":" -f 2-
cur_s2_r1=(`tail -n5  ./Undetermined_S0_L001/JYH_166_R1.fastq`)
#7001113:856:HVVNVBCXY:1:2107:18126:81934 1:N:0:0
#@ATTCAGAAC

echo  $cur_s2_r1 | cut -d":" -f 2-                                                                                   
cur_u_r1=(`tail -n5  ./Undetermined_S0_L001/undetermined_R1.fastq`)
#7001113:856:HVVNVBCXY:1:2107:10131:81453 1:N:0:0
#@ATTACTCGGTT
echo  $cur_u_r1 | cut -d":" -f 2-                                                                                    

echo ${cur_s1_r1[@]}


##################################################
# need check the results
##################################################

