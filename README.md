# Data_collection_EP4A

### Installation

```
conda create -n data_ep4a python==3.7.15
conda activate data_ep4a
```

install libraries

```
pip install moviepy
conda install scipy
pip install opencv-python
```
### file structure for now 

├──  session_01
    
    ├── audio 

        └── audio_file_01.wav 

    ├── log 

        └── original_log_file.txt

    └── video

        ├── D415_main

            ├── depth.avi

            ├── rgb.mp4

            └── state_final.txt

        └── D415_side_view

            ├── depth.avi

            ├── rgb.mp4

            └── state.txt

├── session_02

└── ...