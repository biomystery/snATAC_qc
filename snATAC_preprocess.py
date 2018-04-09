#!/usr/bin/env python
import gzip
import bz2
import sys
import collections
import os
import operator
import os.path
import optparse

def min_dist(s, sl):
    """ return the string with min edit distance """
    ss = sl[:]
    if len(s) == 0: sys.exit("error(min_dist): inquiry string has length 0")
    if len(ss) == 0: sys.exit("error(min_dist): inquiry string list has 0 elements")
    if ([len(s) == len(sj) for sj in ss].count(False) > 0): sys.exit("error(min_dist): different string length")
    dists = [[a == b for (a,b) in zip(s, sj)].count(False) for sj in ss]
    min_value = min(dists)
    min_index = dists.index(min(dists))
    min_s = ss[min_index]

    # find the 2nd min element in the list
    del dists[min_index]
    del ss[min_index]

    min_value2 = min(dists)
    min_index2 = dists.index(min(dists))
    min_s2 = ss[min_index2]
    return (min_s, min_value, min_s2, min_value2)

def correct_single_barcode(b_in, key_in, b_lib,max_mm):
    """ correct single barcode b_in based on b_lib """

    all_matches = {}
     # m,num_mm,m2,mum_mm2; for all samples, do a compare
    all_matches = {k:{'match':min_dist(b_in, v)} for k,v in b_lib.iteritems()} #k: sample, v: barcodes
    
    for k,v in all_matches.iteritems(): # check if barcode in library
        #print v['match']
        all_matches[k]['is_found'] = (v['match'][1] <= max_mm and abs(v['match'][3] -v['match'][1]) > 1)

    if key_in in ['r5','r7']:
        match = all_matches[all_matches.keys()[0]] # just first sample 
        if match['is_found']:
            return  match['match'][0],"" # return corrected 
        else:
            return b_in,"" # not in library  
    else:  # need to find which sample  
        s_out  = [s for s,m in all_matches.iteritems() if m['is_found']]
        if len(s_out) >=1 :
            all_dist = [all_matches[s]['match'][1] for s in s_out]
            imin=[i for i,v in enumerate(all_dist) if v ==min(all_dist)]
            if(len(imin)>1):
                return b_in,"unknown"
            else:
                return all_matches[s_out[imin[0]]]['match'][0],s_out[imin[0]]
        else:
            return b_in,"unknown"



def correct_barcodes(input_barcode_dic_,barcode_lib_dic_,max_mm_):
    """
    correct barcode & get sample id for this read  
    """
    corrected_barcode_dic={}
    r_id_init = [] 

    for k,b in input_barcode_dic_.iteritems():
        # k is : r7, i7, i5, r5 (order not sure)
        
        b_lib_sub = {s:v[k] for s,v in barcode_lib_dic_.iteritems()}
        b_c, r_id = correct_single_barcode(b,k,b_lib_sub,max_mm_)
        corrected_barcode_dic[k] = b_c
        r_id_init.append(r_id)

    r_id = set(filter(None,r_id_init))
    
    if len(r_id)>1 or ("unknown" in r_id):
        return corrected_barcode_dic, "unknown"
    else:
        return corrected_barcode_dic, list(r_id)[0]


def check_barcode(barcode_file,samples):
    """
    check barcdes on the barcode file, if everything ok, return:
     - a nested dic d['sample1']['p1'] 
     - input:
         barcode_file 
         - : r7,i7,i5,r5 (set1) and repeated (use 8 Ns if exceeded max number of barcodes)
         samples: from -s1 and -s2
    """
    
    barcode_dic = {}
    barcode_ord = ["r7","i7","i5","r5"]
    
    with open(barcode_file, "r") as fin:
        l = [row.strip("\n").split("\t") for row in fin.readlines()] # keep empty , and 2d list

    barcode_len =[]
    iii =  xrange(0, len(l), 4) # 
    
    for i,s in enumerate(samples):
        barcode_dic[s] = {}
        for ii,vi in enumerate(barcode_ord):
            barcode_dic[s][vi] = filter(None,[r[ii+iii[i]] for r in l])
            barcode_len.append(map(len,barcode_dic[s][vi]))

    if [len(set(bl)) == 1 for bl in barcode_len].count(False) > 0:
        sys.exit("barcode index has to be of the same length")

    return barcode_dic

def check_input_file(input_f):
    """check input file and return file handle"""
    if not os.path.isfile(input_f): exit("error: \'%s\' not exist" % input_f)

    # check file type & open file
    if input_f.endswith('.gz'):
        fi1 = gzip.open(input_f, 'rb')
    elif input_f.endswith('.bz2'):
        fi1 = bz2.BZ2File(input_f, 'r')
    elif input_f.endswith('.fastq'):
        fi1 = open(input_f, 'r')
    elif input_f.endswith('.fq'):
        fi1 = open(input_f, 'r')

    return fi1

def parse_fastq(f):
    """parse every 4 lines of fastq file opened with f handle"""
    name = f.readline().strip()[1:]
    read = f.readline().strip()
    plus = f.readline().strip()
    qual = f.readline().strip()

    return [name,read,plus,qual]
    

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-a I1.fastq] [-b I2.fastq] [-c R1.fastq] [-d R2.fastq]',
                                   description='Decomplex single-cell ATAC-seq barcode allowing mismatch.')
    parser.add_option('-a','--i1',
                      dest="I1",
                      help='I1.fastq.gz'
                      )

    parser.add_option('-b','--i2',
                      dest='I2',
                      help='I2.fastq.gz'
                      )

    parser.add_option('-c','--r1',
                      dest='R1',
                      help='R1.fastq.gz'
                      )

    parser.add_option('-d','--r2',
                      dest='R2',
                      help='R2.fastq.gz'
                      )

    parser.add_option('-m','--s1',
                      dest='S1',
                      help='Sample 1 using barcode set1'
                      )

    parser.add_option('-n','--s2',
                      dest='S2',
                      help='Sample 2 using barcode set2'
                      )

    parser.add_option('-x','--xmismatch',
                      dest="xmismatch",
                      default = 2,
                      type=int,
                      help='max allowed mismatch (default 2).'
                      )

    parser.add_option('-l','--barcode',
                      dest="barcodes", 
                      help='a single barcode library text file.'
                      )

    parser.add_option('-o','--outdir',
                      dest="outdir", 
                      help='output dir.'
                      )

    parser.add_option('--version',
                      dest="version",
                      default=1.0,
                      type="float",
                      )

    args = parser.parse_args()[0]
    max_mm = int(args.xmismatch)
    out_dir = args.outdir
    samples=[args.S1, args.S2]
    
    # check barcode list
    barcode_lib_dic = check_barcode(args.barcodes,samples)
    
    # open input files; regular dic
    infiles_dic = {k:check_input_file(v) for k,v in {"I1":args.I1,"I2":args.I2,"R1":args.R1,"R2":args.R2}.iteritems()}

    # open output files: nested dic 
    outfiles_dic = {k: {"R1":gzip.open(out_dir +"/" + k +"_R1.fastq.gz" , "wb"), "R2":gzip.open(out_dir+"/" + k +"_R2.fastq.gz","wb")} for k in barcode_lib_dic.keys()}
    outfiles_dic["unknown"]={"R1":gzip.open(out_dir+"/"+ "undetermined_R1.fastq.gz","wb"),"R2":gzip.open(out_dir +"/"+ "undetermined_R2.fastq.gz","wb")}
        
    while True:

        cur_read = {k:parse_fastq(f)  for k,f in infiles_dic.iteritems()} # key: I1, I2, R1, R2

        # check all read name

        if "" in cur_read['I1']: break
        
        cur_read_name =set([v[0].split()[0] for k,v in cur_read.iteritems()])
        if "" in cur_read_name: break         
        if len(cur_read_name)>1: sys.exit("error(main): read name not matched")        

        # get current barcode before correction
        cur_barcode_lib_dic = {"r7":cur_read['I1'][1][:8],"i7":cur_read['I1'][1][-8:],"i5": cur_read['I2'][1][:8],"r5": cur_read['I2'][1][-8:]}

        # correct barcode & get sample id for this read  
        cur_barcode_c,read_id = correct_barcodes(cur_barcode_lib_dic,barcode_lib_dic,max_mm)
        
        # concorate barcodes
        cur_barcode = cur_barcode_c["r7"] + cur_barcode_c["i7"] + cur_barcode_c["i5"] +cur_barcode_c["r5"]

        #if cur_barcode.count('N') >= 12: read_id="unknown" 

        # demultiplex r1 & r2 (split to sample1_R1.fastq.gz, sample2_R1.fastq.gz, undetermined_R1.fastq.gz, undetermined_R2.fastq.gz)
        # write to output files
        outfiles_dic[read_id]["R1"].write('@' + cur_barcode + ':' + cur_read['R1'][0] +"\n")
        outfiles_dic[read_id]["R2"].write('@' + cur_barcode + ':' + cur_read['R2'][0] +"\n")

        
        outfiles_dic[read_id]["R1"].write( cur_read["R1"][1] + "\n")
        outfiles_dic[read_id]["R2"].write( cur_read["R2"][1] + "\n")
        
        outfiles_dic[read_id]["R1"].write( '+' + "\n")
        outfiles_dic[read_id]["R2"].write( '+' + "\n")

        outfiles_dic[read_id]["R1"].write( cur_read["R1"][3]+ "\n")
        outfiles_dic[read_id]["R2"].write( cur_read["R2"][3]+ "\n")


    # close all files
    for f in infiles_dic.values(): f.close();
    for f in outfiles_dic.values(): f["R1"].close(); f["R2"].close();
    
if __name__ == '__main__':
    main()
