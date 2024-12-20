#File: parse_file_output_trust.py
#Purpose: This file includes code to parse output files from running the script
#run_program_sc.sh to get starting trust values and subsequent average updated
#trust values. Usage: python parse_file_output_trust.py <file_name>

import math
import sys

def parse_and_compute_statistics(file_name):
    """
    This function parses the output file to aggregate all statistics printed, 
    then computes averages and standard deviation.
    """
    starting_trust_dict = {
        0.25: [],
        0.5: [],
        0.75: []
    }

    with open(file_name, 'r') as file:
        current_starting_trust = None

        for line in file:
            line = line.strip()
            if line.startswith("Starting Trust Value:"):
                current_starting_trust = float(line.split(":")[1].strip())
            elif line.startswith("Updated Trust Value:"):
                updated_trust = float(line.split(":")[1].strip())
                if current_starting_trust in starting_trust_dict:
                    starting_trust_dict[current_starting_trust].append(updated_trust)

    def compute_stats(values):
        """
        This function computes averages of values.
        """
        if not values:
            return 0.0, 0.0
        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        stddev = math.sqrt(variance)
        return avg, stddev

    for trust_value, updated_values in starting_trust_dict.items():
        avg_updated_trust, stddev_updated_trust = compute_stats(updated_values)
        print(f"Starting Trust Value: {trust_value:.2f}")
        print(f"  Average Updated Trust Value: {avg_updated_trust:.2f}")
        print(f"  Standard Deviation: {stddev_updated_trust:.2f}")
        print(f"  Total Runs: {len(updated_values)}")
        print()

if len(sys.argv) != 2:
    print("Usage: python script_name.py <file_name>")
    sys.exit(1)

file_name = sys.argv[1]
parse_and_compute_statistics(file_name)
