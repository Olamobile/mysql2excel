#!/usr/bin/env python3

"""
  Translate mysql dump to an excel file:

  Input: a folder with the output of a mysqldump, e.g.:
  	mysqldump -u root -p --where="1 limit 10" database --tab=./tsv

  Dependencies: 
	  sudo pip3 install XlsxWriter

  (c) 2015, Olamobile s.a.r.l  

"""

import os
import xlsxwriter
import logging
import re
import json
import argparse


# dealing with CLI arguments

parser = argparse.ArgumentParser(
    description="Converts mysql dump in tsv format into an Excel book (with column names)",
    epilog='Example of obtaining mysql dump in the expected format:\n\t\tmysqldump -u mysqluser -p --where="1 limit 10" database --tab=./tsv'
    )
parser.add_argument("dumpdir", help="a directory containg mysql dump files (mysqldump ... --tab=dumpdir)")
parser.add_argument("-o", "--out", metavar="file.xlsx", help="excel book filename", type=str, default="./dump.xlsx")
parser.add_argument('--verbose', '-v', help="say what it is doing", action='count', default=0)
args = parser.parse_args()

# Set up logger
log = logging.getLogger(__file__)
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
level = logging.ERROR
if args.verbose == 1:
    level = logging.INFO
elif args.verbose > 1:
    level = logging.DEBUG
logging.basicConfig(format= FORMAT, level=level)


if not os.path.isdir(args.dumpdir):
    log.error("%s is not a directory. Aborting", args.dumpdir)
    exit(3)

INPUT = args.dumpdir
OUTPUT = args.out




rex_field = re.compile("\s*`(.*?)`.*")

book = xlsxwriter.Workbook(OUTPUT)
bold = book.add_format({'bold': True}) 

for fn in os.listdir(INPUT):
    if fn.endswith(".sql"):
        log.info(" --> Processing: %s", fn)
        f = open(os.path.join(INPUT, fn))
        # ignore till CREATE TABLE
        for line in f: 
            if line.startswith("CREATE TABLE"):
                break
        # reading all lines starting with two spaces and `    
        # as we assume only those contain column names
        columns = []
        for line in f: 
            if line.startswith("  `"):
                fieldnames = rex_field.search(line).groups()
                if fieldnames: 
                    columns.append(fieldnames[0])
                else:
                   log.warning("Fieldname was considered empty?! ", str(fieldnames))
            else:
                break
        # now we got all columns
        f.close()
        log.debug("Columns: %s", json.dumps(columns))
        
        basename = fn[:-len('.sql')]
        
        # create a new sheet
        # need to cut the name, 31 symbol max
        sheet = book.add_worksheet(basename[:31])

        sheet.write_row('A1', columns, bold)
        
        #reading the corresponding .txt file:
        txtfn = basename + ".txt"
        f = open(os.path.join(INPUT, txtfn))
        log.info("Reading %s file ", f)

        irow = 2
        for line in f: 
            # dealing with multiline values (ending with \)
            l = line
            while l.endswith("\\\n"): 
                l = f.readline()
                line += l
                
            row = line.split('\t')
            sheet.write_row('A%d'%irow, row)
            irow+=1
          
        f.close()

    else:
        log.info("Ignoring %s", fn)

book.close()

log.info("Output is written to %s", OUTPUT)
