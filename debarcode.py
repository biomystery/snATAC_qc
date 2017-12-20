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

def correct_single_barcode(b_in, b_lib):
    """ correct single barcode b_in based on b_lib """
    return b_out



def correct_barcodes(r7,i7,i5,r5,barcode_dic,fout_list):
    """
    correct all the barcode for current read and determine which sample this read belongs to (fout)
    fout_list: a list of sample file object (s1_r1.fastq) 

    eg:  cur_r7_c,cur_i7_c,cur_i5_c,cur_r5_c,fout_r1,fout_r2 = correct_barcodes(cur_r7,cur_i7,cur_i5,cur_r5,sample_file_list)
    """
    
    
    return r7_c, i7_c, i5_c, r5_c, fout  

def check_barcode(barcode_file):
    """
    check barcdes on the barcode file, if everything ok, return:
     - a nested dic d['sample1']['p1'] 
     - input: barcode_file 
         - 1st col: set names (sample names)
         - 2nd col: r7,i7,i5,r5 (set1) and repeated (use 8 Ns if exceeded max number of barcodes)
    """
    
    barcode_dic = {}
    barcode_ord = ["r7","i7","i5","r5"]
    
    with open(barcode_file, "r") as fin:
        samples = fin.readline().split() # first line define samples
        l = [row.strip("\n").split("\t") for row in f.readlines()] # keep empty , and 2d list

    barcode_len =[]
    for s in samples:
        barcode_dic[s] = {}
        for ii,vi in enumerate(barcode_ord):
            barcode_dic[s][vi] = filter(None,[r[ii] for r in l])
            barcode_len.append(map(len,barcode_dic[s][vi]))

    if [len(set(bl)) == 1 for bl in barcode_len].count(False) > 0:
        sys.exit("barcode index has to be of the same length")

    return barcode_dic

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

    parser.add_option('-x','--xmismatch',
                      dest="xmismatch",
                      default = 2,
                      type=int,
                      help='max allowed mismatch.'
                      )

    parser.add_option('-l','--barcode',
                      dest="barcodes", 
                      help='a single barcode library text file.'
                      )

    parser.add_option('--version',
                      dest="version",
                      default=1.0,
                      type="float",
                      )

    args = parser.parse_args()[0]

    fi1_name = args.I1
    fi2_name = args.I2
    fr1_name = args.R1
    fr2_name = args.R2
    max_mm = int(args.xmismatch)
    fb_name = args.barcodes
    
    
    if not os.path.isfile(fi1_name): exit("error: \'%s\' not exist" % fi1_name)
    if not os.path.isfile(fi2_name): exit("error: \'%s\' not exist" % fi2_name)
    if not os.path.isfile(fr1_name): exit("error: \'%s\' not exist" % fr1_name)
    if not os.path.isfile(fr2_name): exit("error: \'%s\' not exist" % fr2_name)
    if not os.path.isfile(fb_name): exit("error: \'%s\' not exist" % fb_name)
    
    # check file format
    if fi1_name.endswith('.gz'):
        fi1 = gzip.open(fi1_name, 'rb')
    elif fi1_name.endswith('.bz2'):
        fi1 = bz2.BZ2File(fi1_name, 'r')
    elif fi1_name.endswith('.fastq'):
        fi1 = open(fi1_name, 'r')
    elif fi1_name.endswith('.fq'):
        fi1 = open(fi1_name, 'r')

    if fi2_name.endswith('.gz'):
        fi2 = gzip.open(fi2_name, 'rb')
    elif fi2_name.endswith('.bz2'):
        fi2 = bz2.BZ2File(fi2_name, 'r')
    elif fi2_name.endswith('.fastq'):
        fi2 = open(fi2_name, 'r')
    elif fi2_name.endswith('.fq'):
        fi2 = open(fi2_name, 'r')

    if fr1_name.endswith('.gz'):
        fr1 = gzip.open(fr1_name, 'rb')
    elif fr1_name.endswith('.bz2'):
        fr1 = bz2.BZ2File(fr1_name, 'r')
    elif fr1_name.endswith('.fastq'):
        fr1 = open(fr1_name, 'r')
    elif fr1_name.endswith('.fq'):
        fr1 = open(fr1_name, 'r')

    if fr2_name.endswith('.gz'):
        fr2 = gzip.open(fr2_name, 'rb')
    elif fr2_name.endswith('.bz2'):
        fr2 = bz2.BZ2File(fr2_name, 'r')
    elif fr2_name.endswith('.fastq'):
        fr2 = open(fr2_name, 'r')
    elif fr2_name.endswith('.fq'):
        fr2 = open(fr2_name, 'r')

    # check barcode list
    barcode_dic = check_barcode(fb_name)

        
    while True:
        cur_i1_name = fi1.readline().strip()[1:]
        cur_i1_read = fi1.readline().strip()
        cur_i1_plus = fi1.readline().strip()
        cur_i1_qual = fi1.readline().strip()
    
        cur_i2_name = fi2.readline().strip()[1:]
        cur_i2_read = fi2.readline().strip()
        cur_i2_plus = fi2.readline().strip()
        cur_i2_qual = fi2.readline().strip()
    
        cur_r1_name = fr1.readline().strip()[1:]
        cur_r1_read = fr1.readline().strip()
        cur_r1_plus = fr1.readline().strip()
        cur_r1_qual = fr1.readline().strip()

        cur_r2_name = fr2.readline().strip()[1:]
        cur_r2_read = fr2.readline().strip()
        cur_r2_plus = fr2.readline().strip()
        cur_r2_qual = fr2.readline().strip()
        
        if cur_i1_name == "" or cur_i2_name == "" or cur_r1_name == "" or cur_r2_name == "": break        
        if not (cur_i1_name.split()[0] == cur_i2_name.split()[0] == cur_r1_name.split()[0] == cur_r2_name.split()[0]): sys.exit("error(main): read name not matched")        

        cur_r7 = cur_i1_read[:8]
        cur_i7 = cur_i1_read[-8:]
        cur_i5 = cur_i2_read[:8]
        cur_r5 = cur_i2_read[-8:]

        # correct barcode & get sample id for this barcode 
        cur_r7_c,cur_i7_c,cur_i5_c,cur_r5_c,fout_r1,fout_r2 = correct_barcodes(cur_r7,cur_i7,cur_i5,cur_r5)
        
        
        # concorate barcodes
        cur_barcode = cur_r7_c + cur_i7_c + cur_i5_c + cur_r5_c
        if cur_barcode.count('N') >= 12: continue

        # demultiplex r1 & r2 (split to sample1_R1.fastq.gz, sample2_R1.fastq.gz, undetermined_R1.fastq.gz, undetermined_R2.fastq.gz)
        fout_r1.write('@' + cur_barcode + ':' + cur_r1_name +"\n")
        fout_r2.write('@' + cur_barcode + ':' + cur_r2_name +"\n")
        
        fout_r1.write( cur_r1_read+ "\n")
        fout_r2.write( cur_r2_read+ "\n")
        
        fout_r1.write( '+' + "\n")
        fout_r2.write( '+' + "\n")

        fout_r1.write( cur_r1_qual + "\n")
        fout_r2.write( cur_r1_qual + "\n")         


    # close all files
    fi1.close()
    fi2.close()
    fr1.close()
    fr2.close()    

if __name__ == '__main__':
    main()
