#!/bin/bash

NUMBER_OF_ITERATIONS=100
NETWORK_PATH="TNTP_Networks/Anaheim"
ALGORITHMS=("ASCALE" "ALOOF")
DEMANDS=("low")
PREFIX="ana"

for ALG in "${ALGORITHMS[@]}"; do
    for TOTAL_DEMAND in "${DEMANDS[@]}"; do
        OUTPUT_FILE="Results_Files/${PREFIX}_mc_${TOTAL_DEMAND}_${ALG}.txt"
        > "$OUTPUT_FILE" 

        for ((i=1; i<=NUMBER_OF_ITERATIONS; i++)); do
            echo "Run #$i for NETWORK=$PREFIX, ALG=$ALG, DEMAND=$TOTAL_DEMAND"
            echo "Run #$i" >> "$OUTPUT_FILE"

            runtime=$(python -c "
import time
import subprocess
start = time.time()
try:
    subprocess.run(['python', 'main.py', '$NETWORK_PATH', '$TOTAL_DEMAND', '$ALG'], stdout=open('$OUTPUT_FILE', 'a'), stderr=subprocess.STDOUT, check=True)
except subprocess.CalledProcessError as e:
    print(f'Error during execution: {e}', file=open('$OUTPUT_FILE', 'a'))
end = time.time()
print(round(end - start, 5))
            ")

            echo "Runtime: $runtime seconds" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        done
    done
done
