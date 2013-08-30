autotrace -background-color=FFFFFF \
          -color-count 2 \
          -centerline \
          -remove-adjacent-corners \
          -corner-threshold 132 \
          -corner-always-threshold 180 \
          -error-threshold -100 \
          -output-file=$2 \
          $1
#           
# autotrace -background-color=FFFFFF \
#           -color-count 2 \
#           -centerline \
#           -output-file=$2 \
#           $1
#           
# autotrace -background-color=FF0000 \
#           -color-count 2 \
#           -remove-adjacent-corners \
#           -corner-threshold 132 \
#           -corner-always-threshold 180 \
#           -filter-iterations 10 \
#           -corner-threshold 120 \
#           -output-file=$2\
#            $1