# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 10:22:17 2022

@author: kayva
"""

import os
import spikeinterface as si
import spikeinterface.extractors as se 
import spikeinterface.toolkit as st
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw
  
import tempfile

os.environ['TEMPDIR'] = tempfile.gettempdir()
import matplotlib.pyplot as plt
import numpy as np
 
from spikeinterface.exporters import export_to_phy

#%%

directory = './'
directory_output = './'


recording = se.MdaRecordingExtractor(directory,raw_fname='raw.mda',params_fname='params.json',geom_fname='geom.csv')

recording_f = st.bandpass_filter(recording, freq_min=300, freq_max=6000)
w = sw.plot_timeseries(recording_f)
recording_cmr = st.common_reference(recording_f, reference='global', operator='median')
w = sw.plot_timeseries(recording_cmr)

#%%
recording_saved = recording_f.save(folder=directory_output+"/preprocessed", progress_bar=True, 
                                     n_jobs=4, total_memory="200M")
#%% if recording already  saved
recording_saved = si.load_extractor(directory_output+"/preprocessed")

#%% Mountainsorted 

ss.installed_sorters()
default_MS = ss.Mountainsort4Sorter.default_params()
print(default_MS)
# run spike sorting on entire recording
sorting_MS = ss.run_mountainsort4(recording_saved, output_folder=directory_output+'/results_MS', verbose=True, **default_MS,)

#%% Klusta
ss.installed_sorters()

# run spike sorting on entire recording
sorting_KS = ss.run_klusta(recording_4_tetrodes, output_folder=directory_output+'/results_KS', verbose=True)
print('Found', len(sorting_KS.get_unit_ids()), 'units')

#%% Waveform Extraction

we_all = si.extract_waveforms(recording_f, sorting_MS, folder=directory_output+"/wf_MS_all", 
                                  max_spikes_per_unit=None, progress_bar=True)
export_to_phy(we_all, output_folder=directory_output+'/phy_MS',
                  progress_bar=True, total_memory='100M')
