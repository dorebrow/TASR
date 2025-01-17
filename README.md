# TASR: A Novel Trust-Aware Stackelberg Routing Algorithm to Mitigate Traffic Congestion

This is the implementation in code of the TASR algorithm, along with Largest-Latency First (LLF), Scale, Augmented Scale (ASCALE), and Aloof. The implementation of each algorithm is contained within its own file in the code base, which are called
```
tasr_implementation.py
cc_implementation.py
llf_implemenetation.py
scale_implementation.py
ascale_implementation.py
aloof_implementation.py
```
respectively.

# Running the Program

The file ```main.py``` stores the code for running the program. Additional implementational detais can be found there.

Arguments accepted corresponding to their respective full algorithm names are as follows:
| Argument | Algorithm Name |
| ---------| ---------------|
| TASR, tasr | Trust-Aware Selfish Routing (TASR) |
| LLF, llf | Largest-Latency First (LLF) |
| SCALE, scale, Scale | Scale |
| ASCALE, ascale, Ascale | Augmented Scale |
| ALOOF, Aloof, aloof | Aloof |

## Single-Commodity Simulations
To run a single-commodity simulation using the command line, simply use
```
python main.py "(GRAPH)" TOTAL_DEMAND "(SINGLE_COMMODITY)" ALG
```
where the arguments listed above correspond to the following values:
| Argument Name    | Value                                      |
| ---------------- | ------------------------------------------ |
| GRAPH            | Path of the pre-processed network to be simulated. E.g., "TNTP_Networks/SiouxFalls" |
| TOTAL_DEMAND     | Demand level in the single-commodity network. E.g., LOW |
| SINGLE_COMMODITY | Commodity to be used as the single-commodity, in tuple format. E.g., "(23, 24)"   |
| ALG              | Algorithm to be used. E.g., TASR |

## Multi-Commodity Simulations
To run a multi-commodity simulation using the command line, simply use
```
python main.py "(GRAPH)" TOTAL_DEMAND ALG
```
where the arguments listed above correspond to the following values:
| Argument Name    | Value                                      |
| ---------------- | ------------------------------------------ |
| GRAPH            | Path of the pre-processed network to be simulated. E.g., "TNTP_Networks/SiouxFalls" |
| TOTAL_DEMAND     | Demand level in the multi-commodity network. E.g., MED |
| ALG              | Algorithm to be used. E.g., TASR |

## Running Simulation Batches
To run batches of simulations, the bash files ```Bash_Scripts/run_single_batch_sc.sh``` and ```Bash_Scripts/run_single_batch_mc.sh``` can be used for running batches of single-commodity and multi-commodity simulations, respectively.

### Running Simulation Batches: Single-Commodity
To run batches of single-commodity simulations, in the ```Bash_Scripts/run_single_batch_sc.sh``` bash file, modify the values of NUMBER_OF_ITERATIONS, GRAPH, TOTAL_DEMAND, SINGLE-COMMODITY, ALG, and OUTPUT_FILE to your desired values at the top of the file. 

The variable NUMBER_OF_ITERATIONS controls how many simulations will be run. 

The variable OUTPUT_FILE is the file name where the results of the batch of simulations will be stored.

Note: The runtime of each simulation will also be stored in the results file.

### Running Simulation Batches: Multi-Commodity
To run batches of multi-commodity simulations, in the ```Bash_Scripts/run_single_batch_mc.sh``` bash file, modify the values of NUMBER_OF_ITERATIONS, GRAPH, TOTAL_DEMAND, ALG, and OUTPUT_FILE to your desired values at the top of the file. 

The variable NUMBER_OF_ITERATIONS controls how many simulations will be run. 

The variable OUTPUT_FILE is the file name where the results of the batch of simulations will be stored.

Note: The runtime of each simulation will also be stored in the results file.

## Automated Running of All Algorithms for a Set of Networks
Automated scripts are available to run batches of multiple individual instances of all algorithms considered (TASR, CC, LLF, Scale, ASCALE, and Aloof). To automate all single-commodity batches, use the run_sc_automated.sh bash file. To automate all multi-commodity batches, use the run_mc_automated.sh bash file.

Note: The above files by default execute a program 100 times for all combinations of the considered algorithms for low, medium, and high demand levels. These values can be changed as desired for new or different combinations of networks, demands, or numbers of runs.

## Demands
Total network demand is computed using low, medium, or high commodity demands. Please refer to the paper to see how these demand levels are chosen. The following arguments are used to indicate to the program which demand level you would like to simulate:

| Demand Level | Argument |
| ----- | ------ |
| Low | LOW |
| Medium | MED |
| High | HIGH |

# Networks
Several networks in .tntp file format can be found in the ```TASR/TNTP_Networks``` folder with corresponding net and trips files. Many of these files, with no preprocessing to be easily parsed, can be found [here](https://github.com/matteobettini/Traffic-Assignment-Frank-Wolfe-2021/tree/main/tntp_networks).

## Processed Networks
Several networks have already been processed for ease of use. Processing these files consists of converting them from .tntp file format, getting all commodities in the network, and getting the paths for each commodity in the network. These networks can be found in the ```Processed_Netowrks``` folder. They are in .json format for ease of integration with Python code.

Processed networks currently include
- Austin
- Anaheim
- Barcelona
- Braess Paradox (Wheatstone) Network
- Chicago Sketch
- Eastern Massachusetts (EMA)
- Pigou
- Sioux Falls

Note that while all of the above networks have been processed, the only networks for which results are currently available are Austin, Anaheim, Chicago Sketch, Pigou (strictly single-commodity), and Sioux Falls.

### Network Abbreviations
The followinig abbreviations are commonly used throughout the project within file names to denote the specific networks considered in the simulation experiments used in the paper. 

| Network | Abbreviation |
| ----- | ------ |
| Sioux Falls | SF |
| Anaheim | ANA |
| Chicago Sketch | CS |
| Austin | AUS |
| Pigou | PIG |

### Single Commodities
The following single commodities were used in the paper for simulating the single-commodity setting. If you wish to evaluate different single commodities within any of the networks considered in the paper (Sioux Falls, Anaheim, Chicago Sketch, or Austin), make the appropriate changes in the relevant bash files for executing the program, run_sc_automated.sh or run_single_batch_sc.sh. 

| Network | Single-Commodity |
| ----- | ------ |
| Sioux Falls | (23, 24) |
| Anaheim | (34, 37) |
| Chicago Sketch | (359, 124) |
| Austin | (1877, 1902) |

### Commodity Paths
Commodity paths are processed using the ```find_paths()``` function in the ```process_network.py``` file. Specific implementational details, including function documentation, can be found in the file, but the key note is that **currently processed files consider a maximum path length of 5 edges**. If you so desire, networks can be reprocessed to get paths of a different maximum length using the following command:
```
python store_paths.py GRAPH LENGTH
```
where
GRAPH Path of the pre-processed network to be simulated (e.g., "TNTP_Networks/SiouxFalls"), and LEGNTH is an integer value denoting the maximum number of edges allowable in a path. Note that choosing large values of LENGTH will result in increased time to process a network.

Using this function creates a new .json file in the Processed_Networks folder. Note, if you want to parse a new graph that hasn't already been included in the Processed Networks folder, you must edit the store_paths.py file to include the location of the resulting .json file.

# Parsing Output
Output of results files (obtained by using one of the bash scripts in the Bash_Scipts folder) is parsed using the ```parse_file_output.py``` file in the Parsing_Output folder. To run this program, execute the following command:
```
python parse_file_output.py [result_file].txt ALG
```
where ```[result_file].txt``` is the name (or path) of the text file containing the results you wish to parse, and ```ALG``` is the algorithm used to generate those results. For example, executing the command
```
 python parse_file_output.py Results_Files/aus_sc_low_SCALE.txt SCALE
```

parses the results for running the single-commodity version of the SCALE algorithm on the Austin network for a low demand level where the SCALE algorithm was used in the simulations.

Additionally, to parse the data relating to trust, the following command can be executed:

```
parse_file_output_trust.py Results_Files/[result_file].txt
```

where ```[result_file].txt``` is the name (or path) of the text file containing the results you wish to parse. For example, executing the command

```
python parse_file_output_trust.py Results_Files/aus_sc_high_cc.txt
```

parses the results for running the single-commodity version of the CC algorithm on the Austin network for a high demand level.

# Plotting Results 
Several files for plotting the results of the single-commodity and multi-commodity experiments can be found in the Plotting_Files folder. Files in this folder are named somewhat intuitively, with python files available to plot average total travel times, runtimes, efficiency ratios, runtime ratios, and updated trust.

Note, you must manually enter the data gotten from running ```parse_file_output.py``` or ```parse_file_output_trust.py``` into the appropriate lists supplied in each of these plotting files.

## Plotting Multi-Commodity Results
Several different plotting programs are provided in the Plotting_Files/Multi-Commodity folder for plotting the following types of results: efficiency ratios (ER / er), runtime ratios (RR / rr), and serviced ratios (SR / sr). Programs are currently included for plotting these results for each of the multi-commodity networks included in the paper, Sioux Falls, Anaheim, Chicago Sketch, and Austin, and are named accordingly using each network's abbreviation. 

**Each of the files included in the subfiles of the Plotting_Files/Multi-Commodity file are those used to generate the data shown in the Multi-Commodity Results section of the paper.**

## Plotting Single-Commodity Results
Several different plotting programs are provided in the Plotting_Files/Single-Commodity folder for plotting the following types of resutls: average travel time per unit of demand (TT/tt), network congestion, efficiency ratios (ER / er), runtime ratios (RR / rr), runtimes, and trust, which are respectively stored in the following subfiles: Average_Travel_Time, Congestion, Efficiency_Ratios, Runtime_Ratios, Runtimes, and Trust. Programs are currently included for plotting these results for each or all of the single-commodity networks included in the paper, Pigou, Sioux Falls, Anaheim, Chicago Sketch, and Austin and are named accordingly using each network's abbreviation.

**Each of the files included in the subfiles of the Plotting_Files/Single-Commodity file are those used to generate the data shown in the Multi-Commodity Results section of the paper.**

# Results Data
The aggregated results for single-commodity and multi-commodity experiments are found in the Aggregated_Results_Test_Files folder. The text files in this folder contain the resulting information obtained by runnning ```parse_file_output.py``` and ```parse_file_output_trust.py``` for all experimental settings. Text files in this folder with names ending in "trust.txt" correspond to the parsed trust results. The results stored in ```sc_results_avg_tt.txt``` are obtained from executing the python programs ```Plotting_Files/Single-Commodity/Average_Travel_Time_per_Driver/plot_sc_avg_tt_per_driver_[NETWORK].py```, where [NETWORK] is the abbreviation of the network for which the average travel time (congestion) per driver is being calculated. The aggregated results for all 72 experiments of the multi-commodity setting are found in the file ```mc_results_agg.txt```.