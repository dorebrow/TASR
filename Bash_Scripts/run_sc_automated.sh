#!/bin/bash

#Change as desired
#Commodities used: Chicago Sketch: "(359, 124)" Sioux Falls: "(23, 24)" 
                #  Anaheim: "(34, 37)" Austin "(1877, 1902)"
NUMBER_OF_ITERATIONS=100
NETWORK_PATH="TNTP_Networks/Austin"
COMMODITY="(1877, 1902)"
ALGORITHMS=("TASR" "CC" "LLF" "SCALE" "ASCALE" "ALOOF")
DEMANDS=("low" "med" "high")

#Iterate through each algorithm and demand
for ALG in "${ALGORITHMS[@]}"; do
    for TOTAL_DEMAND in "${DEMANDS[@]}"; do
        OUTPUT_FILE="Results_Files/aus_sc_${TOTAL_DEMAND}_${ALG}.txt"
        
        > "$OUTPUT_FILE"

        for ((i=1; i<=NUMBER_OF_ITERATIONS; i++)); do
            echo "Run #$i for ALG=$ALG and DEMAND=$TOTAL_DEMAND"
            echo "Run #$i" >> "$OUTPUT_FILE"

            runtime=$(python -c "
import time, subprocess
start = time.time()
subprocess.run(['python', 'main.py', '$NETWORK_PATH', '$TOTAL_DEMAND', '$COMMODITY', '$ALG'], stdout=open('$OUTPUT_FILE', 'a'))
end = time.time()
print(round(end - start, 5))
            ")

            echo "Runtime: $runtime seconds" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        done
    done

done
