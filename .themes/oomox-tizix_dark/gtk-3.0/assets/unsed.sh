#!/bin/sh
sed -i \
         -e 's/rgb(0%,0%,0%)/#1d2324/g' \
         -e 's/rgb(100%,100%,100%)/#dcdcdc/g' \
    -e 's/rgb(50%,0%,0%)/#1d2324/g' \
     -e 's/rgb(0%,50%,0%)/#126d7a/g' \
 -e 's/rgb(0%,50.196078%,0%)/#126d7a/g' \
     -e 's/rgb(50%,0%,50%)/#272f30/g' \
 -e 's/rgb(50.196078%,0%,50.196078%)/#272f30/g' \
     -e 's/rgb(0%,0%,50%)/#dcdcdc/g' \
	"$@"
