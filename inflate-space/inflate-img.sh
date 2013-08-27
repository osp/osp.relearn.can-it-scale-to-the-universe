#!/bin/bash


 IIMG=circle.xpm
 OIMG=test.xpm

 IMGWIDTH=100


  cp $IIMG $OIMG

# REPLACE SPACES WITH PLACEHOLDER
  sed -i "/^.\{$IMGWIDTH\}/s/ /X/g" $OIMG

 
# ADD A SPACE AFTER EACH CHARACTER
# (=REPLACE ALL CHARACTERS WITH ITSELF AND A SPACE)
  sed -i "/^.\{$IMGWIDTH\}/s/./& /g" $OIMG


# REPLACE PLACEHOLDER WITH SPACES AGAIN
  sed -i "/^.\{$IMGWIDTH\}/s/X/ /g" $OIMG





exit 0;
