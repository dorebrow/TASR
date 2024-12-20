from tasr_implementation import run_sc_tasr, run_mc_tasr
from llf_implementation import run_sc_llf, run_mc_llf
from scale_implementation import run_sc_scale, run_mc_scale
from aloof_implementation import run_sc_aloof, run_mc_aloof
from ascale_implementation import run_sc_ascale, run_mc_ascale
from cc_implementation import run_sc_cc, run_mc_cc
import sys

if len(sys.argv) > 4:  #Single commodity version should be run
    GRAPH = sys.argv[1] #Graph file location
    TOTAL_DEMAND = sys.argv[2] #Choose LOW, MED, or HIGH
    SINGLE_COMMODITY = tuple(map(int, sys.argv[3].strip('()').split(','))) #Input in string format. Ex: "(23, 24)"
    SC = True
    ALG = sys.argv[4] #Model to be run: TASR, LLF, SCALE, or ASCALE
else:
    GRAPH = sys.argv[1] #Graph file location
    TOTAL_DEMAND = sys.argv[2] #Choose LOW, MED, or HIGH
    SC = False
    ALG = sys.argv[3] #Model to be run: TASR, LLF, SCALE, or ASCALE

def main():
    # If a specific single commodity has been entered
    if SC == True:
        if ALG == "TASR" or ALG == "tasr":
            run_sc_tasr(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        elif ALG == "LLF" or ALG == 'llf':
            run_sc_llf(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        elif ALG == "scale" or ALG == "Scale" or ALG == "SCALE":
            run_sc_scale(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        elif ALG == "aloof" or ALG == "Aloof" or ALG == "ALOOF":
            run_sc_aloof(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        elif ALG == "ascale" or ALG == "Ascale" or ALG == "ASCALE":
            run_sc_ascale(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        elif ALG == "cc" or ALG == "CC":
            run_sc_cc(GRAPH, SINGLE_COMMODITY, TOTAL_DEMAND)
        else:
            print("Please try to run a valid algorithm: TASR, LLF, Scale, ASCALE, or Aloof")
    else:
        if ALG == "TASR" or ALG == "tasr":
            run_mc_tasr(GRAPH, TOTAL_DEMAND)
        elif ALG == "LLF" or ALG == "llf":
            run_mc_llf(GRAPH, TOTAL_DEMAND)
        elif ALG == "scale" or ALG == "Scale" or ALG == "SCALE":
            run_mc_scale(GRAPH, TOTAL_DEMAND)
        elif ALG == "aloof" or ALG == "Aloof" or ALG == "ALOOF":
            run_mc_aloof(GRAPH, TOTAL_DEMAND)
        elif ALG == "ascale" or ALG == "Ascale" or ALG == "ASCALE":
            run_mc_ascale(GRAPH, TOTAL_DEMAND)
        elif ALG == "cc" or ALG == "CC":
            run_mc_cc(GRAPH, TOTAL_DEMAND)
        else:
            print("Please try to run a valid algorithm: TASR, LLF, Scale, ASCALE, or Aloof")


if __name__ == '__main__':
    main()