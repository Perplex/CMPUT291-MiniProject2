#!/bin/bash

# Bash Script - Shardul Shah

sort -u -o terms.txt terms.txt
sort -u -o recs.txt recs.txt
sort -u -o years.txt years.txt

perl break.pl <terms.txt >terms.txt
perl break.pl <recs.txt >recs.txt
perl break.pl <years.txt >years.txt


db_load -T -t hash -f recs.txt recs.db
db_load -T -t btree -f terms.txt terms.db
db_load -T -t btree -f years.txt years.db

# Use the following command to test/show the database as terminal output. Replace db_name.db with the database name:
#db_dump -p db_name.db


