#File: parse_file_output_mc.py
#Purpose: This file includes code to parse output files from running the script
#run_program.sh to get starting trust values and subsequent average updated
#trust values. Usage: python parse_file_output_mc.py <file_name> <algorithm_name>

import math
import sys

'''This function parses the output file to aggregate all statistics printed, then computes averages and standard deviations.'''
def parse_and_compute_statistics(file_name, algorithm_name):
    total_runs = 0
    tstt_so_values = []
    algo_flow_values = []
    selfish_flow_values = []
    tstt_algo_values = []
    tstt_selfish_values = []
    runtime_values = []
    ultimate_tt = []

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Run #"):
                total_runs += 1
            elif line.startswith("Total System Travel Time for SO:"):
                tstt_so_values.append(float(line.split(":")[1].strip()))
            elif line.startswith(f"Total {algorithm_name} flow assigned:"):
                algo_flow_values.append(float(line.split(":")[1].strip()))
            elif line.startswith("Total selfish flow assigned:"):
                selfish_flow_values.append(float(line.split(":")[1].strip()))
            elif line.startswith(f"Total System Travel Time for {algorithm_name}:"):
                tstt_algo_values.append(float(line.split(":")[1].strip()))
            elif line.startswith("Total System Travel Time for Selfish Best Response:"):
                tstt_selfish_values.append(float(line.split(":")[1].strip()))
            elif line.startswith("Runtime:"):
                runtime_values.append(float(line.split(":")[1].strip().split()[0]))
            elif line.startswith("Total System Travel Time for All Demand:"):
                ultimate_tt.append(float(line.split(":")[1].strip()))

    '''This function computes averages and standard deviations of values.'''
    def compute_stats(values):
        if not values:
            return 0.0, 0.0
        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        stddev = math.sqrt(variance)
        return avg, stddev

    avg_tstt_so, stddev_tstt_so = compute_stats(tstt_so_values)
    avg_algo_flow, stddev_algo_flow = compute_stats(algo_flow_values)
    avg_selfish_flow, stddev_selfish_flow = compute_stats(selfish_flow_values)
    avg_tstt_algo, stddev_tstt_algo = compute_stats(tstt_algo_values)
    avg_tstt_selfish, stddev_tstt_selfish = compute_stats(tstt_selfish_values)
    avg_runtime, stddev_runtime = compute_stats(runtime_values)
    avg_ultimate_tt, stddev_ultimate_tt = compute_stats(ultimate_tt)

    print(f"Average Total System Travel Time for SO: {avg_tstt_so:.2f} ± {stddev_tstt_so:.2f}")
    print(f"Average {algorithm_name} flow assigned: {avg_algo_flow:.2f} ± {stddev_algo_flow:.2f}")
    print(f"Average selfish flow assigned: {avg_selfish_flow:.2f} ± {stddev_selfish_flow:.2f}")
    print(f"Average Total System Travel Time for {algorithm_name}: {avg_tstt_algo:.2f} ± {stddev_tstt_algo:.2f}")
    print(f"Average Total System Travel Time for Selfish Best Response: {avg_tstt_selfish:.2f} ± {stddev_tstt_selfish:.2f}")
    print(f"Average Runtime: {avg_runtime:.5f} ± {stddev_runtime:.5f} seconds")
    print(f"Average Ultimate Total System Travel Time for {algorithm_name}: {avg_ultimate_tt:.2f} ± {stddev_ultimate_tt:.2f}")

if len(sys.argv) != 3:
    print("Usage: python script_name.py <file_name> <algorithm_name>")
    sys.exit(1)

file_name = sys.argv[1]
algorithm_name = sys.argv[2]
parse_and_compute_statistics(file_name, algorithm_name)