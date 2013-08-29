#!/bin/bash


  SVG=`ls -t i/*.svg | head -1`
  TMPDIR=.

# -------------------------------------------------------------- #
  # FORTH-AND-BACK CONVERTING 
  # TO PREVENT GEOMERATIVE ERRORS

  SRCSVG=$SVG

  inkscape --export-pdf=${SRCSVG%%.*}.pdf $SRCSVG
  pdf2ps ${SRCSVG%%.*}.pdf ${SRCSVG%%.*}.ps
  ps2pdf ${SRCSVG%%.*}.ps ${SRCSVG%%.*}.pdf
  pdf2svg ${SRCSVG%%.*}.pdf ${SRCSVG%%.*}_CONFORM.svg

  rm ${SRCSVG%%.*}.ps ${SRCSVG%%.*}.pdf

  # REMOVE PATH CLOSURE = "Z M" (CAUSED PROBLEM WITH GEOMERATIVE)
  sed -i 's/Z M [^"]*"/"/g' ${SRCSVG%%.*}_CONFORM.svg

  SVG4HPGLLINES=i/`basename ${SRCSVG%%.*}_CONFORM.svg`
  mv ${SRCSVG%%.*}_CONFORM.svg $SVG4HPGLLINES
# -------------------------------------------------------------- #


 # -------------------------------------------------------------------------- #
 # START HPGL FILE
 # -------------------------------------------------------------------------- #
 
   HPGL=${SVG%%.*}.hpgl
 
   echo "IN;"                  >  $HPGL
   # http://www.isoplotec.co.jp/HPGL/eHPGL.htm
   # IP p1x,p1y,p2x,p2y;
   echo "IP0,0,16158,11040;"   >> $HPGL
   # http://www.isoplotec.co.jp/HPGL/eHPGL.htm
   # SC xmin,xmax,ymin,ymax;
   echo "SC1488,0,0,1052;"     >> $HPGL
   echo "SP1;"                 >> $HPGL
   echo "VS1;"                >> $HPGL


   echo $SVG4HPGLLINES > svg.i

   SKETCHNAME=hpgllines_A3_01
 
   APPDIR=$(dirname "$0")
   LIBDIR=$APPDIR/src/$SKETCHNAME/application.linux/lib
   SKETCH=$LIBDIR/$SKETCHNAME.jar
 
   CORE=$LIBDIR/core.jar
   GMRTV=$LIBDIR/geomerative.jar
   BTK=$LIBDIR/batikfont.jar
 
   LIBS=$SKETCH:$CORE:$GMRTV:$BTK
 
   java  -Djava.library.path="$APPDIR" \
         -cp "$LIBS" \
         $SKETCHNAME 
 
   rm svg.i
 
 # -------------------------------------------------------------------------- #
   #echo "SP1;"   >> $HPGL
   cat hpgl.hpgl >> $HPGL

# # RANDOMIZE LINES (PREVENT FLOATING COLOR) 
#   cat hpgl.hpgl | \
#   sed 's/PU;/PU;\n/g' | \
#   sed '/./{H;d;};x;s/\n/={NL}=/g' | \
#   shuf | sed '1s/={NL}=//;s/={NL}=/\n/g'     >> $HPGL

   echo "SP0;"                                >> $HPGL
 # -------------------------------------------------------------------------- #

  # REPLACE PD WITH PD AND A RANDOM SPEED

    COUNT=1
 
    for PD in `grep -n PD $HPGL`
     do
        LINENUMBER=`echo $PD | cut -d ":" -f 1 `
        echo $LINENUMBER
 
        VS=$((RANDOM%41+1))
        VS=$COUNT 

        echo $VS
        sed -i "${LINENUMBER}s/PD/&;VS${VS}/g" $HPGL
 
        COUNT=`expr $COUNT + 2`

    done



 # CLEAN up
 # -------------------------------------------------------------------------- #
 # DEBUG  
 #cp $SVG4HPGLLINES `basename $SVG4HPGLLINES` 
 rm hpgl.hpgl ${SVG%%.*}_* 




exit 0;




