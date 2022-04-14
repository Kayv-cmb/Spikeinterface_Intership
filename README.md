# Spikeinterface
## Installation of Spikeinterface

Create a new environment, Python need to be >=3.7

```
conda create --name environmnent
```
Activate you envinronment  
If you want to use spyder
```
conda install spyder=5
```
for spikeinterface installation
```
pip install spikeinterface[full]==0.93
```
for phy
```
pip install phy==2.0b1
```
For Mountainsor4 in spikeinterface
```
pip install mountainsort4
```
## Installation of Mountainsort

Create a new environment Python need to be be 3.6

```
conda create --name environmnentMS4 python=3.6
```
If you want to use spyder
```
conda install spyder=5
```
The install mountainsort package
```
conda install -c flatiron -c conda-forge mountainlab mountainlab_pytools ml_ephys ml_ms3 ml_ms4alg ml_pyms
```
## Potential Errors during installation/running

If you run into the error 
```
ImportError: cannot import name 'Selector' from 'phylib.io.array' (/home/genzel/anaconda3/envs/environmnent/lib/python3.9/site-packages/phylib/io/array.py)
```
### Solution
Go to https://github.com/cortex-lab/phy
Downloads the master and replace the phy file in /home/genzel/anaconda3/envs/environmnent/lib/python3.9/site-packages by the phy file in the master
