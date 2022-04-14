# Spikeinterface
## Installation of Spikeinterface



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



## Potential Errors during installation/running

If you run into the error 
```
ImportError: cannot import name 'Selector' from 'phylib.io.array' (/home/genzel/anaconda3/envs/environmnent/lib/python3.9/site-packages/phylib/io/array.py)
```
### Solution
Go to https://github.com/cortex-lab/phy
Downloads the master and replace the phy file in /home/genzel/anaconda3/envs/environmnent/lib/python3.9/site-packages by the phy file in the master
