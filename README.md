# Pytorch and Huggingface Experiments

I'm running these on WSL2 on Windows 11 with a NVidia GEForce card and drivers.

WSL2 Ubuntu has a special CUDA Toolkit install available [here](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0). This installer avoids overwriting the ```/usr/lib/wsl/lib/libcuda.so``` file setup by the NVidia GeForce driver installer.

## Scripts
* train.py and inference.py
    - straight from the PyTorch getting started. Shows how to save and load a trained model.
    
* transformerpipeline.py
    - demos the pipeline "helper" swiss army knife.

* tensors.py
    - basic tensor operations and cuda

* Microsoft phi 1.5 SML (Small Language Model) capable of non-trivial code/language one-shot results that can be run on a laptop/phone. Example run on RTX3050Ti Laptop GPU takes 8 seconds.

* Microsoft phi 2 SML (Small Language Model) capable of non-trivial code/language one-shot results that can be run on a laptop/phone. Example run on RTX3050Ti Laptop GPU takes 88 seconds.
