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
# directory = 'D:\\Mallory_mda\\'
# directory_output = 'D:\\Mallory_mda\\'
directory = '/media/genzel/TOSHIBA EXT/Mallory_mda'
directory_output = '/media/genzel/TOSHIBA EXT/Mallory_mda/'


recording = se.MdaRecordingExtractor(directory,raw_fname='raw.mda',params_fname='params.json',geom_fname='geom.csv')

recording_f = st.bandpass_filter(recording, freq_min=300, freq_max=6000)
w = sw.plot_timeseries(recording_f)
recording_cmr = st.common_reference(recording_f, reference='global', operator='median')
w = sw.plot_timeseries(recording_cmr)

#%%
recording_saved = recording_f.save(folder=directory_output+"/preprocessed", progress_bar=True, 
                                     n_jobs=4, total_memory="200M")
#%% Generate tetrode
recording_saved = si.load_extractor(directory_output+"/preprocessed")
from probeinterface import generate_tetrode, ProbeGroup

probegroup = ProbeGroup()
for i in range(1):
    tetrode = generate_tetrode()
    tetrode.set_device_channel_indices(np.arange(4) + i * 4)
    probegroup.add_probe(tetrode)
    
recording_4_tetrodes = recording_saved.set_probegroup(probegroup, group_mode='by_probe')

# get group
print(recording_4_tetrodes.get_channel_groups())
# similar to this
print(recording_4_tetrodes.get_property('group'))
#%%
#%% tridesclous 

print(ss.installed_sorters())
default_TDC_params = ss.TridesclousSorter.default_params()
print(default_TDC_params)
# tridesclous spike sorting
default_TDC_params['detect_threshold'] = 5

# parameters set by params dictionary
sorting_TDC_5 = ss.run_tridesclous(recording=recording_f, output_folder=directory_output+'/tmp_TDC_5',
                                   **default_TDC_params, )
we_all = si.extract_waveforms(recording_f, sorting_TDC_5, folder=directory_output+"/wf_TDC_all", 
                                  max_spikes_per_unit=None, progress_bar=True)
export_to_phy(we_all, output_folder=directory_output+'/phy_TDC',
              progress_bar=True, total_memory='100M')
#%%ironclust
ss.IronClustSorter.set_ironclust_path('./ironclust')
ss.IronClustSorter.ironclust_path
ss.installed_sorters()
# run spike sorting by group
sorting_IC = ss.run_ironclust(recording_f, 
                              output_folder= directory_output + '/results_IC',
                              verbose=True)
print(f'IronClust found {len(sorting_IC.get_unit_ids())} units')
print(f'Ironclust unit ids: {sorting_IC.get_unit_ids()}')
print(f'Spike train of a unit: {sorting_IC.get_unit_spike_train(13)}')
w_rs = sw.plot_rasters(sorting_IC)

we_all = si.extract_waveforms(recording_f, sorting_IC, folder=directory_output+"/wf_IC_all", 
                                  max_spikes_per_unit=None, progress_bar=True)

export_to_phy(we_all, output_folder=directory_output+'/phy_IC',
                 progress_bar=True, total_memory='100M')

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
we = si.extract_waveforms(recording_f, sorting_MS, folder=directory_output+"/wf_MS", progress_bar=True,
                              n_jobs=1, total_memory="500M", overwrite=True)
print(we)
waveforms0 = we.get_waveforms(unit_id=1)
print(f"Waveforms shape: {waveforms0.shape}")
template0 = we.get_template(unit_id=1)
print(f"Template shape: {template0.shape}")
all_templates = we.get_all_templates()
print(f"All templates shape: {all_templates.shape}")
w = sw.plot_unit_waveforms(we, unit_ids=[1])
w = sw.plot_unit_templates(we, unit_ids=[1])
w = sw.plot_unit_probe_map(we, unit_ids=[1])
w = sw.plot_unit_summary(we, unit_id=1)
for unit in sorting_MS.get_unit_ids():
    waveforms = we.get_waveforms(unit_id=unit)
    spiketrain = sorting_MS.get_unit_spike_train(unit)
    print(f"Unit {unit} - num waveforms: {waveforms.shape[0]} - num spikes: {len(spiketrain)}")
we_all = si.extract_waveforms(recording_f, sorting_MS, folder=directory_output+"/wf_MS_all", 
                                  max_spikes_per_unit=None, progress_bar=True)
for unit in sorting_MS.get_unit_ids():
    waveforms = we_all.get_waveforms(unit_id=unit)
    spiketrain = sorting_MS.get_unit_spike_train(unit)
    print(f"Unit {unit} - num waveforms: {waveforms.shape[0]} - num spikes: {len(spiketrain)}")

export_to_phy(we_all, output_folder=directory_output+'/phy_MS',
                  progress_bar=True, total_memory='100M')