# mysql2excel
A simple script to convert mysql dump (tsv) into an excel file (.xlsx). 
With column names.

## Motivation
Sometimes it is good to show to someone how a MySQL database look like. One can do it locally via a mysql client,
but if one needs to look into details offline, sending mysql text dumps are not handy for read. 
Moreover, not everyone will want to install any additional software (like mysql server) just to look at it. 

Here we have a small script that will generate an Excel book, each page will represent a table in a database, 
first row are its column names, the following rows are the data.

## Usage

Suppose you want to export first 25 rows of each table database `db1` into Excel format. 

1. Get mysql dump:
```
mysqldump -u mysqluser -p --where="1 limit 25" db1 --tab=./tsv
```
It will create a folder `./tsv` with files (two files per table: `.sql`, and `.txt`).
2. Run the script
```
./mysql2xlsx.py ./tsv --out db1.xlsx
```
3. 
4. Profit!

## Dependencies

Here is a couple of packages to install (debian/ubuntu style):
```
sudo apt-get install python3
sudo pip3 install XlsxWriter
```


