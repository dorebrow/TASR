#!/bin/bash

#Change to desired values
NUMBER_OF_ITERATIONS=100
NETWORK_PATH="TNTP_Networks/SiouxFalls" #"TNTP_Networks/SiouxFalls" #"TNTP_Networks/ChicagoSketch" #"TNTP_Networks/Anaheim"
TOTAL_DEMAND="HIGH"
COMMODITY="(23, 24)" #Pigou: "(1, 3)" Chicago Sketch: "(359, 124)" Sioux Falls: "(23, 24)" Anaheim: "(34, 37)" Austin "(1877, 1902)"
ALG="ALOOF" #CC, TASR, LLF, SCALE, ASCALE, ALOOF

#Change output file to reflect above as desired
OUTPUT_FILE="Results_Files/sf_sc_high_aloof.txt"

> "$OUTPUT_FILE"

#Change the upper bound on the loop to the desired number of runs
for ((i=1; i<=NUMBER_OF_ITERATIONS; i++)); do
    echo "Run #$i"
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
