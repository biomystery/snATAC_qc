snATAC_preprocess: 
============================================================
A tool for demultiplex and encode barcode for snATAC. 

# Usage 

``` shell
snATAC_preprocess.py --help
```

``` shell
Usage: snATAC_preprocess.py [-h] [-a I1.fastq] [-b I2.fastq] [-c R1.fastq] [-d R2.fastq]

Decomplex single-cell ATAC-seq barcode allowing mismatch.

Options:
  -h, --help            show this help message and exit
  -a I1, --i1=I1        I1.fastq.gz
  -b I2, --i2=I2        I2.fastq.gz
  -c R1, --r1=R1        R1.fastq.gz
  -d R2, --r2=R2        R2.fastq.gz
  -m S1, --s1=S1        Sample 1 using barcode set1
  -n S2, --s2=S2        Sample 2 using barcode set2
  -x XMISMATCH, --xmismatch=XMISMATCH
                        max allowed mismatch (default 2).
  -l BARCODES, --barcode=BARCODES
                        a single barcode library text file.
  -o OUTDIR, --outdir=OUTDIR
                        output dir.
  --version=VERSION     
```

# Two rounds of multiplexing

Libraries are sequenced paired end. Each sequencing read is assigned to 4 barcodes on 2 Index reads.
The index reads are `43 (Index 1)` and `37 (Index 2)` reads long. 

Two rounds: 
1. During tagmentation (Tn5 treatment) `p/r` barcodes are integrated
2. During PCR, `i` barcodes are integrated 

PCR after FACS Positions for the barcodes are: p/r7 i7 i5 p/r5
- p/r7 1-8 (Index read 1)
- i7 36-43 (Index read 1)
- i5 1-8 (Index read 2)
- p/r5 30-37 (Index read 2)

