# lss
---
 List all file sequences in a directory. Uses C style printf formatting to show counting number of sequences.

 The command accepts one optional argument> -p for directory path or file.

 The goal is to find sequences of files that can be concatenated together.
 The file name could be anything, the sequence number padding could be any length.

## Purpose of this tool

  Identifying the collection of files and the count of sequencing files inside specified directory.
  It will not look for directory folders.


## Steps
1. List all files inside a directory.

2. Sort the files right.

4. Find the incrementing digit and format that digit: %d, %3d ...

5. Find out the ranges of the sequencing files.

6. Print the output in the command prompt.

## The lss arguments
```
usage: lss.py [-h] [-p PATH] [-v VERBOSITY] [FILENAME]

Process some files.

positional arguments:
  FILENAME      glob file name search.

optional arguments:
  -h, --help    show this help message and exit
  -p PATH       Optionally specify a directory or a file path.
  -v VERBOSITY  Specify verbosity. Options: 0, 1, 2.
```

## Desired output
```
> lss

> (length of sequence) file01_%04d.jpg    (start frame number) - (end frame number), (start frame number) - (end frame number)
```

### Example:
```
> lss

> 10 file01_%04d.png

> 3 file02_%04d.png

> 67 V2-0001_ATK2250_comp_v0060_%04d.png  0001-0059 0060-0067
```

### Example Commands:
first argument of the tool initiates a glob search for all files, otherwise if nothing is given, it will look in the current working directory.
the tool accepts one optional command "lss -p" this can either be a directory or a path name.
```
lss
lss *
lss \sequence_03\image-0003.png
lss \sequence_03\image-*
lss \sequence_03\*
lss -p D:\Work\Python\lss\testdirectories\sequence_03
lss -p D:\Work\Python\lss\testdirectories\sequence_03\image-0005.png
```

### Important information:

  1. This tool does not check the validity of the files. Like corrupted files, empty image sequences, etc.

  2. This tool does not check if there are multiple copies of identical contents of the files.

  3. This tool only checks for sequence increments of 1.

  4. This tool will not display folders inside the directory.

  5. This tool has only been tested on Python 2.7
