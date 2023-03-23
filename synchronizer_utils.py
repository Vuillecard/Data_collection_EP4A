from datetime import datetime
import datetime as dt
import numpy as np
import cv2 
import pandas as pd 

def get_time_from_str(time_str):
        return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')

def append_frame(L,frame_to_add):
    for frame in frame_to_add:
        L.append(frame)
    return L

def get_time(time_str):
    x = time_str.replace('[','')
    x = x.strip()
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')

def get_extra_info(log):
    x = log.split(':')
    if len(x) > 1:
        return x[1].strip()
    else:
        return None
    
def get_log(log):
    x = log.split(':')
    return x[0].strip()

def clean_log(location, save_location):
    log_file = pd.read_csv(location,delimiter=']',header=None)
    log_file.columns = ['time','log']
    log_file['time'] = log_file['time'].apply(get_time)
    log_file['extra_info'] = log_file['log'].apply(get_extra_info)
    log_file['log'] = log_file['log'].apply(get_log)
    log_file.to_csv(save_location,sep=';',header=True,index=False)

def get_timestamp(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f').timestamp()

def closest_value(value, list_time):
    
    arr = np.asarray([get_timestamp(x) for x in list_time])
    val = get_timestamp(value)
    i = (np.abs(arr - val)).argmin()
    return i

def get_fps(state_file):

    state_file['relative_time'] = state_file['time'].apply(get_time) - get_time(state_file['time'].values[0])
    # relative time between two frame: 
    diff = state_file['relative_time'].diff().apply(lambda x : x.microseconds/1000)
    moyen_frame = diff[-4:].mean()
    fps = 1000/(moyen_frame)
    return fps
