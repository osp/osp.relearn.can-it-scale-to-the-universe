#!/bin/bash


  IIMG=circle.gif
  OIMG=test.xpm

  OWIDTH=100

  IWIDTH=`identify $IIMG | \
          cut -d " " -f 3 | \
          cut -d "x" -f 1`

  convert -resize $OWIDTH -monochrome $IIMG $OIMG


# REPLACE SPACES WITH PLACEHOLDER
  sed -i "/^.\{$IWIDTH\}/s/ /X/g" $OIMG
 
# ADD A SPACE AFTER EACH CHARACTER
# (=REPLACE ALL CHARACTERS WITH ITSELF AND A SPACE)
  sed -i "/^.\{$IWIDTH\}/s/./& /g" $OIMG

# REPLACE PLACEHOLDER WITH SPACES AGAIN
  sed -i "/^.\{$IWIDTH\}/s/X/ /g" $OIMG

  INFLATEDWIDTH=`expr $IWIDTH \* 2`

# REPLACE OLD IMG WIDTH WITH NEW (FIRST INSTANCE!)
  sed -i "s/$IWIDTH/$INFLATEDWIDTH/" $OIMG



exit 0;
