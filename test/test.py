#!/usr/bin/env python

from debarcode.py import *


max_mm =2

barcode_lib_dic = check_barcode("./barcodes/barcodes.txt")
barcode_lib_dic['JYH_166'].keys()
infiles_dic = {k:check_input_file(v) for k,v in {"I1":"./test/I1.fastq","I2":"./test/I2.fastq","R1":"./test/R1.fastq","R2":"./test/R2.fastq"}.iteritems()}
outfiles_dic = {k: {"R1":open(k+"_R1.fastq" , "w"), "R2":open(k+"_R2.fastq","w")} for k in barcode_lib_dic.keys()}


for i in range(40):
    cur_read = {k:parse_fastq(f)  for k,f in infiles_dic.iteritems()} # key: I1, I2, R1, R2

cur_read_name =set([v[0].split()[0] for k,v in cur_read.iteritems()])

cur_barcode_lib_dic = {"r7":cur_read['I1'][1][:8],"i7":cur_read['I1'][1][-8:],"i5": cur_read['I2'][1][:8],"r5": cur_read['I2'][1][-8:]}

cur_read
cur_barcode_lib_dic

cur_barcode_c,read_id = correct_barcodes(cur_barcode_lib_dic,barcode_lib_dic,max_mm)

b_lib_sub = {s:v[k] for s,v in barcode_lib_dic_.iteritems()}

barcode_lib_dic['JYH_165']['i5'] == barcode_lib_dic['JYH_166']['i5']

b_lib = {s:v[k] for s,v in barcode_lib_dic.iteritems()}

all_matches = {k:{'match':min_dist(b_in, v)} for k,v in b_lib.iteritems()} #k: sample, v: barcodes

