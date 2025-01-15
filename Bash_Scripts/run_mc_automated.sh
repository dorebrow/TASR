#!/bin/bash

NUMBER_OF_ITERATIONS=100
NETWORK_PATHS=("TNTP_Networks/SiouxFalls" "TNTP_Networks/ChicagoSketch" "TNTP_Networks/Anaheim" "TNTP_Networks/Austin")
ALGORITHMS=("TASR" "CC" "LLF" "SCALE" "ASCALE" "ALOOF")
DEMANDS=("low" "med" "high")

declare -A NETWORK_PREFIXES
NETWORK_PREFIXES["TNTP_Networks/SiouxFalls"]="sf"
NETWORK_PREFIXES["TNTP_Networks/ChicagoSketch"]="cs"
NETWORK_PREFIXES["TNTP_Networks/Anaheim"]="ana"
NETWORK_PREFIXES["TNTP_Networks/Austin"]="aus"

for NETWORK_PATH in "${NETWORK_PATHS[@]}"; do
    PREFIX="${NETWORK_PREFIXES[$NETWORK_PATH]}"
    for ALG in "${ALGORITHMS[@]}"; do
        for TOTAL_DEMAND in "${DEMANDS[@]}"; do
            OUTPUT_FILE="Results_Files/${PREFIX}_mc_${TOTAL_DEMAND}_${ALG}.txt"
            
            > "$OUTPUT_FILE"

            for ((i=1; i<=NUMBER_OF_ITERATIONS; i++)); do
                echo "Run #$i for NETWORK=$PREFIX, ALG=$ALG, DEMAND=$TOTAL_DEMAND"
                echo "Run #$i" >> "$OUTPUT_FILE"

                runtime=$(python -c "
                import time, subprocess
                start = time.time()
                subprocess.run(['python', 'main.py', '$NETWORK_PATH', '$TOTAL_DEMAND', '$ALG'], stdout=open('$OUTPUT_FILE', 'a'))
                end = time.time()
                print(round(end - start, 5))
                                ")

                echo "Runtime: $runtime seconds" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            done
        done
    done
done
