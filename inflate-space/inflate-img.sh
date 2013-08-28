#!/bin/bash


  IIMG=circle.png
  OIMG=test.xpm

  OWIDTH=100

#  IWIDTH=`identify $IIMG | \
#          cut -d " " -f 3 | \
#          cut -d "x" -f 1`

  convert -resize $OWIDTH -monochrome $IIMG $OIMG

# REPLACE SPACES WITH PLACEHOLDER
  sed -i "/^.\{$OWIDTH\}/s/ /X/g" $OIMG
 
# ADD A SPACE AFTER EACH CHARACTER
# (=REPLACE ALL CHARACTERS WITH ITSELF AND A SPACE)
  sed -i "/^.\{$OWIDTH\}/s/./& /g" $OIMG

# REPLACE PLACEHOLDER WITH SPACES AGAIN
  sed -i "/^.\{$OWIDTH\}/s/X/ /g" $OIMG

  INFLATEDWIDTH=`expr $OWIDTH \* 2`

# REPLACE OLD IMG WIDTH WITH NEW (FIRST INSTANCE!)
  sed -i "s/$OWIDTH/$INFLATEDWIDTH/" $OIMG


exit 0;
