#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:55:43 2022

@author: genzel
"""

#######################################
# imports and initialization
#######################################

# For development purposes, reload imported modules when source changes
# %load_ext autoreload
# %autoreload 2

def append_to_path(dir0): # A convenience function
    if dir0 not in sys.path:
        sys.path.append(dir0)

# standard imports
import os, sys, json
import numpy as np
from matplotlib import pyplot as plt

# mountainlab imports
from mountainlab_pytools import mlproc as mlp
from mountainlab_pytools import mdaio
import spikeforestwidgets as SFW

# imports from this repo
append_to_path(os.getcwd()+'/../../python')
from mountainsort4_1_0 import sort_dataset as ms4_sort_dataset # MountainSort spike sorting
from validate_sorting_results import validate_sorting_results # Validation processors
from synthesize_dataset import synthesize_dataset # Synthesize a test dataset


#######################################
# Initialize the pipeline object
#######################################

Pipeline=mlp.initPipeline()

# Make synthetic ephys data and create output directory
dsdir=os.getcwd()+'/'
with Pipeline:
    synthesize_dataset(dsdir,M=4,duration=600,average_snr=8)

dsdir=os.getcwd()+'/'
output_base_dir=os.getcwd()+'/output2'
if not os.path.exists(output_base_dir):
    os.mkdir(output_base_dir)
#######################################
# RUN THE PIPELINE
#######################################
#from ironclust_sort import sort_dataset as ironclust_sort_dataset

output_dir=output_base_dir+'/ms4'
with Pipeline:
    #ironclust_sort_dataset(dataset_dir=dsdir,output_dir=output_dir,adjacency_radius=-1,detect_threshold=3)
    ms4_sort_dataset(dataset_dir=dsdir,output_dir=output_dir,adjacency_radius=-1,detect_threshold=3,freq_min=300,freq_max=6000)
    A=validate_sorting_results(dataset_dir=dsdir,sorting_output_dir=output_dir,output_dir=output_dir)
    amplitudes_true=A['amplitudes_true']
    accuracies=A['accuracies']

