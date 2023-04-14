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

# Instruciton to run 

The processing is done in /demo_ep4a.py.

First you need to find the time of the beep sound in the audio file. I would suggest to view it with audacity so that you can see the bump in the audio and select the begining accuratly. 

To install audacity
'''
apt-get install audacity 
'''

Then on the main video you need to find the frame of the flash ( first frame that contain the flash) in the main video. Note: the frame number is at the top left corner. try to be as precise as possible. 

Warning in some session we miss and do it twice thus two beep sound !

You can complete the bash file in run_session_ep4a.sh and then run '''bash run_session_ep4a.sh '''
or run it directly through the terminal.

You can have a look at the parameter definition in /demo_ep4a.py.

you can first run it with --add_audio_log it should add audio and log folder and file where the video is located
then you can run it with --synchronise to sync the data it can take quite some time for 30 minutes videos 
finally you can run it with --view to see the video synchronise with audio log and gaze calibration.
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