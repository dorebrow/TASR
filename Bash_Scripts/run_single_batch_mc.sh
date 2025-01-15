#!/bin/bash

#Rplace with desired values
NUMBER_OF_ITERATIONS=100
NETWORK_PATH="TNTP_Networks/ChicagoSketch"
TOTAL_DEMAND="'LOW'"
OUTPUT_FILE="Results_Files/cs_mc_low_tasr.txt"
ALG="TASR"

> "$OUTPUT_FILE"

#Change the upper bound on loop to desired number of runs
for ((i=1; i<=NUMBER_OF_ITERATIONS; i++)); do
    echo "Run #$i"
    echo "Run #$i" >> "$OUTPUT_FILE"
    
    runtime=$(python -c "
    import time, subprocess
    start = time.time()
    subprocess.run(['python', 'main.py', '$NETWORK_PATH', str($TOTAL_DEMAND), '$ALG'], stdout=open('$OUTPUT_FILE', 'a'))
    end = time.time()
    print(round(end - start, 5))
        ")

    echo "Run #$i completed in $runtime seconds"
    echo "Runtime: $runtime seconds" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE" 
done