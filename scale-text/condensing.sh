#!/bin/bash

 SRCTXT=src.txt

 for WORD in `cat $SRCTXT`
  do
      FIRSTCHAR=`echo $WORD | \
                 cut -c 1`

      LASTCHAR=`echo $WORD | \
                cut -c 2- | \
                rev | cut -c 1 | rev`

      INBETWEEN=`echo $WORD | cut -c 2-`

   # ---------------------------------------------------------- #
   # EXCEPTION FOR INTERPUNCTUATION
   # ---------------------------------------------------------- #

       if [ `echo $LASTCHAR | tr -d [a-z] | wc -c` -gt 1 ]
       then
             LASTCHAR=`echo $WORD | \
                       cut -c 2- | \
                       rev | cut -c 1-2 | rev`

             INBETWEEN=`echo $INBETWEEN | \
                        rev | cut -c 3- | rev`
       else
             INBETWEEN=`echo $INBETWEEN | rev | cut -c 2- | rev`
       fi
   # ---------------------------------------------------------- #


      IBLENGTH=`echo $INBETWEEN | wc -c`

      if [ $IBLENGTH -gt 6 ]; then

      SELECT=`expr $IBLENGTH \/ 2`

      else

      SELECT=$IBLENGTH

      fi
 
       INBETWEEN=`echo $INBETWEEN | \
                  sed 's/./&\n/g' | \
                  sed 'n;d;' | \
                  sed ':a;N;$!ba;s/\n//g'`

      WORD=${FIRSTCHAR}${INBETWEEN}${LASTCHAR}

      TEXT=${TEXT}" "${WORD}
 done

 echo $TEXT | \
 fold -s -60 | \
 tee ${0%.*}.txt

exit 0;
