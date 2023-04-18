
import os
from scipy.io import wavfile
import pandas as pd
from copy import deepcopy 
from typing import List
from moviepy.editor import * 
import shutil
from synchronizer_utils import (
    clean_log,
    get_fps
)

class SessionData():

    def __init__(self, session_location_path) -> None:

        self.session_location_path = session_location_path
        self.modalities = { k : {} for k in ['audio','video','log']}

        self.init_path()

    def init_path(self):
        self.init_audio_path()
        self.init_video_path()
        self.init_log_path()

    def init_audio_path(self):
        count = 0
        for l in os.listdir(os.path.join(self.session_location_path,'audio')): 
            if (l.split('.')[-1] == 'wav') and (l.startswith('Audio')) :
                self.modalities['audio']['name_file'] = l
                count +=1
        assert(count == 1)
    
    def init_video_path(self):
        self.modalities['video']['name_file_main_rgb'] = os.path.join( 'D415_main','rgb.mp4')
        self.modalities['video']['name_file_main_depth'] = os.path.join( 'D415_main','depth.avi')
        self.modalities['video']['name_file_main_state_file'] = os.path.join('D415_main','state_final.txt')
        self.modalities['video']['name_file_side_view_rgb'] = os.path.join('D415_side_view','rgb.mp4')
        self.modalities['video']['name_file_side_view_depth'] = os.path.join('D415_side_view','depth.avi')
        self.modalities['video']['name_file_side_view_state_file'] = os.path.join('D415_side_view','state.txt')
    
    def init_log_path(self):
        count = 0
        for l in os.listdir(os.path.join(self.session_location_path,'log')):
            if (l.split('.')[-1] == 'txt') and (l.startswith('participant_')):
                self.modalities['log']['name_file'] = l
                count +=1
            if (l.split('.')[-1] == 'txt') and (l.startswith('clean_log')):
                self.modalities['log']['name_file'] = l
                return
        assert(count <= 1)
        if count == 0:
            self.modalities['log']['name_file'] = None
        else:
            clean_log(os.path.join(self.session_location_path,'log',self.modalities['log']['name_file']),
                    os.path.join(self.session_location_path,'log','clean_log.txt'))
            self.modalities['log']['name_file'] = 'clean_log.txt'

    def get_path(self, modality, file_name = ''):
        if modality in ['audio','log']:
            assert file_name == ''
        elif modality == 'video':
            assert file_name in ['main_rgb','main_depth','main_state_file','side_view_rgb','side_view_depth','side_view_state_file']
        else :
            print('Modality not found')
            return None
        name = 'name_file' if file_name == '' else 'name_file'+'_'+file_name
        if self.modalities[modality][name] is None: 
            return None
        else:
            if modality == 'video':
                return os.path.join(self.session_location_path, self.modalities[modality][name])
            else:
                return os.path.join(self.session_location_path, modality, self.modalities[modality][name])
    
    def set_session_location_path(self, session_location_path):
        self.session_location_path = session_location_path
        
    def set_audio_start(self, beep_time : float):
        """ Define when the beep sound in audio file
        """
        samplerate, _ = wavfile.read(self.get_path('audio'))
        start_pos = int(samplerate*beep_time)
        self.modalities['audio']['start_audio'] = start_pos

    def get_audio_start(self):
        return self.modalities['audio']['start_audio']
    
    def set_video_start(self, frame_light : int):
        """ Define when the light appear on the main rbg video (same beep)
        """
        self.modalities['video']['start_frame_main_rgb'] = frame_light
    
    def get_video_start(self):
        return self.modalities['video']['start_frame_main_rgb']

    def get_video_fps(self, camera_id):
        state_file = self.load_state_file(camera_id)
        fps = get_fps(state_file)
        return fps
    
    def create_folder(self) -> None :
        for mod in ['audio', 'video', 'log']:
            if mod == 'video':
                os.makedirs(os.path.join( self.session_location_path,'D415_main'),exist_ok=True)
                os.makedirs(os.path.join( self.session_location_path,'D415_side_view'),exist_ok=True)
            else:
                os.makedirs(os.path.join(self.session_location_path,mod),exist_ok=True)
    
    def is_ready_to_sync(self) -> bool :
        audio = 'start_audio' in self.modalities['audio'].keys()
        video = 'start_frame_main_rgb' in self.modalities['video'].keys()
        if audio and video: 
            return True
        else :
            return False
    
    def load_state_file(self, camera_id): 
        # Need to update in case the state file change
        assert camera_id in ['main','side_view'], 'camera_id should be main or side_view'

        path = self.get_path('video', camera_id+'_state_file')
        #path = path.replace('state.txt','final_state.txt') if is_final else path
        if not os.path.exists(path):
            print('State file not found') 
            return None
        state_file = pd.read_csv(path, delimiter=';', )
        #state_file.columns = ["frames", "col_1", "col_2", "time"]
        return state_file
    
    def load_log_file(self): 
        # Need to update in case the state file change
        path = self.get_path('log')
        print(path)
        if path is None:
            return None
        log_file = pd.read_csv(path, delimiter=';')
        return log_file


class DataEP4A(SessionData):

    def __init__(self, session_location_path) -> None:
        super().__init__(session_location_path)
        
    def init_video_path(self):
        self.modalities['video']['name_file_main_rgb'] = os.path.join( 'D415_main','rgb.mp4')
        self.modalities['video']['name_file_main_depth'] = os.path.join( 'D415_main','depth.avi')
        self.modalities['video']['name_file_main_state_file'] = os.path.join('D415_main','state_final.txt')
        self.modalities['video']['name_file_side_view_rgb'] = os.path.join('D415_side_view','rgb.mp4')
        self.modalities['video']['name_file_side_view_depth'] = os.path.join('D415_side_view','depth.avi')
        self.modalities['video']['name_file_side_view_state_file'] = os.path.join('D415_side_view','state.txt')
    
    def init_log_path(self):
        count = 0
        for l in os.listdir(os.path.join(self.session_location_path,'log')):
            if (l.split('.')[-1] == 'txt') and (l.startswith('participant')):
                self.modalities['log']['name_file'] = l
                count +=1
            if (l.split('.')[-1] == 'txt') and (l.startswith('clean_log')):
                self.modalities['log']['name_file'] = l
                return
        assert(count <= 1)
        if count == 0:
            self.modalities['log']['name_file'] = None
        else:
            clean_log(os.path.join(self.session_location_path,'log',self.modalities['log']['name_file']),
                    os.path.join(self.session_location_path,'log','clean_log.txt'))
            self.modalities['log']['name_file'] = 'clean_log.txt'

    def get_path(self, modality, file_name = ''):
        if modality in ['audio','log']:
            assert file_name == ''
        elif modality == 'video':
            assert file_name in ['main_rgb','main_depth','main_state_file','side_view_rgb','side_view_depth','side_view_state_file']
        else :
            print('Modality not found')
            return None
        name = 'name_file' if file_name == '' else 'name_file'+'_'+file_name
        if self.modalities[modality][name] is None: 
            return None
        else:
            return os.path.join(self.session_location_path, modality, self.modalities[modality][name])


def session_path(global_path, room, day, participant):
    path = os.path.join(global_path,'room%d'%room,'day%d'%day,'Participants',participant)
    folders = []
    for folder in os.listdir(path):
        if not folder.startswith('cal'):
            folders.append(folder)
    assert(len(folders) == 1)
    return os.path.join(path,folders[0])

def add_audio_and_log(global_path,room,day, participant):

    path_audio = os.path.join(global_path,'Audio','room%d'%room,'day_%d'%day)
    for file in os.listdir(path_audio):
        if file.endswith('%s.wav'%participant):
            path_audio = os.path.join(path_audio,file)
            break

    path_log = os.path.join(global_path,'LogFiles','room %d'%room,'Day%d'%day)
    for file in os.listdir(path_log):
        if file.startswith('participant_%s'%participant):
            path_log = os.path.join(path_log,file)
            break
    
    path_video = session_path(global_path,room,day, participant)

    os.makedirs(os.path.join(path_video,'audio'),exist_ok=True)
    os.makedirs(os.path.join(path_video,'log'),exist_ok=True)
    shutil.copy2(path_log,os.path.join(path_video,'log',path_log.split('/')[-1]))
    shutil.copy2(path_audio,os.path.join(path_video,'audio',path_audio.split('/')[-1]))
    