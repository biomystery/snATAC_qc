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
  -x XMISMATCH, --xmismatch=XMISMATCH
                        max allowed mismatch.
  -l BARCODES, --barcode=BARCODES
                        a single barcode library text file.
  -o OUTDIR, --outdir=OUTDIR
                        output dir.
  --version=VERSION     
(
```

