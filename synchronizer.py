import os
import simpleaudio as sa
from scipy.io import wavfile
import numpy as np
import pandas as pd
import datetime as dt
import cv2
from copy import deepcopy 
from typing import List
from moviepy.editor import * 
from data_handler import SessionData

from synchronizer_utils import (
    get_time_from_str,
    append_frame,
    clean_log,
    closest_value,
    get_fps
)

class Synchronizer():

    def __init__(self, fps = 30 ) -> None:
        self.fps = fps
    
    def resample_frames(self, state_file, from_frame):

        assert(from_frame == state_file['frame_index'].values[from_frame])
        start_frame = state_file['frame_index'].values[from_frame]
        start_time = get_time_from_str(state_file['time'].values[from_frame])
        frame_to_keep = []
        
        current_s = 1
        for frame_idx, time  in zip(state_file['frame_index'].values[start_frame:],state_file['time'].values[start_frame:]):
            if get_time_from_str(time)  > (start_time + dt.timedelta(0,current_s)) :
                
                append_frame(frame_to_keep, np.linspace(start_frame,frame_idx-1,self.fps,endpoint=True,dtype=int))
                start_frame = frame_idx
                current_s += 1
        return frame_to_keep
    
    def resample_state_file(self,state_file,save_location,frame_to_keep):
        new_frame = 0
        l = []
        for idx in frame_to_keep : 
            l.append([new_frame] + state_file.iloc[idx].to_list()) 
            new_frame += 1
        old_col_names = state_file.columns
        col_names = ['frame_index'] + list(map(lambda x: x.replace('frame_index', 'old_frame_index'), old_col_names))
        pd_tmp = pd.DataFrame(l,columns=col_names)
        pd_tmp.to_csv(save_location,index=False,sep = ';')
    
    def resample_log(self,state_file_location,log_location,log_save_location):
        state_file = pd.read_csv(state_file_location, delimiter=';')
        time_array = state_file['time'].values
        get_frame = lambda x: state_file['frame_index'].iloc[closest_value(x,time_array)]
        if log_location is None:
            pass
        else:
            log_file = pd.read_csv(log_location, delimiter=';')
            log_file['frame'] = log_file['time'].apply(get_frame)
            log_file.to_csv(log_save_location,index=False,sep = ';')

    def resample_video(self, video_path,video_save_path,frame_to_include):

        frame_as_dict = {}
        for i in frame_to_include:
            if str(i) in frame_as_dict.keys():
                frame_as_dict[str(i)] += 1
            else:
                frame_as_dict[str(i)] = 1
        
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if video_path.split('.')[-1] == 'mp4':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        else: 
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        out = cv2.VideoWriter(video_save_path,fourcc, self.fps, (width,height))

        i = -1 
        while(cap.isOpened()):
            ret, frame = cap.read()
            i += 1
            if i%1000==0:
                print('step : ',i,'/',length,'')
            if i in frame_to_include:
                for _ in range(frame_as_dict[str(i)]):
                    out.write(frame)
            if ret==False:
                break
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def resample_audio(self, audio_path, audio_save_path, begining_pos,frame_to_include):
        nb_frame = len(frame_to_include)
        samplerate, data = wavfile.read(audio_path)
        audio_duration = int(nb_frame*(1/self.fps)*samplerate)
        data = data[begining_pos:begining_pos+audio_duration]
        wavfile.write(audio_save_path, samplerate, data)

    def __call__(self, session : SessionData) -> SessionData:

        if not session.is_ready_to_sync(): 
            return None
        
        session_sync = deepcopy(session)
        session_sync.set_session_location_path(session_sync.session_location_path+'_sync')
        session_sync.create_folder()

        state_file_main = session.load_state_file('main')
        state_file_side = session.load_state_file('side_view')
        frame_to_keep = self.resample_frames(
            state_file = state_file_main,
            from_frame = session.modalities['video']['start_frame_main_rgb']
        )
        # resample the main video and state file
        self.resample_video(
            video_path = session.get_path('video','main_rgb'),
            video_save_path = session_sync.get_path('video','main_rgb'),
            frame_to_include = frame_to_keep
        )
        self.resample_video(
            video_path = session.get_path('video','main_depth'),
            video_save_path = session_sync.get_path('video','main_depth'),
            frame_to_include = frame_to_keep
        )
        self.resample_audio(
            audio_path = session.get_path('audio'),
            audio_save_path = session_sync.get_path('audio'),
            begining_pos = session.get_audio_start(),
            frame_to_include = frame_to_keep
        )
        # make sur to resample the state file before resampling the log because
        # the frame number is different 
        self.resample_state_file(
            state_file = state_file_main,
            save_location = session_sync.get_path('video','main_state_file'),
            frame_to_keep = frame_to_keep 
        )
        self.resample_log(
            state_file_location = session_sync.get_path('video','main_state_file'),
            log_location = session.get_path('log'),
            log_save_location = session_sync.get_path('log'),
        )

        # resample the side view video and state file
        self.resample_video(
            video_path = session.get_path('video','side_view_rgb'),
            video_save_path = session_sync.get_path('video','side_view_rgb'),
            frame_to_include = frame_to_keep
        )
        self.resample_video(
            video_path = session.get_path('video','side_view_depth'),
            video_save_path = session_sync.get_path('video','side_view_depth'),
            frame_to_include = frame_to_keep
        )
        self.resample_state_file(
            state_file = state_file_main,
            save_location = session_sync.get_path('video','side_view_state_file'),
            frame_to_keep = frame_to_keep 
        )
        

class Synchronizer_video_log():
    """ Synchronize the video and the log file. It do not resample the video thus do no synchronise with the audio.
    """

    def __init__(self,)->None: 
        pass 
    
    def resample_log(self,state_file_location,log_location,log_save_location):
        state_file = pd.read_csv(state_file_location, delimiter=';')
        time_array = state_file['time'].values
        get_frame = lambda x: state_file['frame_index'].iloc[closest_value(x,time_array)]
        if log_location is None: 
            pass
        else:
            log_file = pd.read_csv(log_location, delimiter=';')
            log_file['frame'] = log_file['time'].apply(get_frame)
            log_file.to_csv(log_save_location,index=False,sep = ';')


    def __call__(self, session : SessionData) -> SessionData:

        session_sync = deepcopy(session)
        session_sync.set_session_location_path(session_sync.session_location_path+'_sync')
        session_sync.create_folder()

        self.resample_log(
            state_file_location = session.get_path('video','main_state_file'),
            log_location = session.get_path('log'),
            log_save_location = session_sync.get_path('log'),
        )



class Viewer():

    def __init__( self, ) -> None:
        pass

    def audio_video( self, session: SessionData, path_save : str, camera_id: List[str],path_rgb_log : str = None, format_ffmpeg = False) -> None:
        
        if path_rgb_log: 
            path_rbg = path_rgb_log
        else:
            path_rbg = session.get_path('video','main_rgb')
        # load the audio and video
        if len(camera_id) == 1:
            if 'main' in camera_id[0]:
               videoclip = [[VideoFileClip(path_rbg)]]
            elif 'side_view' in camera_id[0]:
                videoclip = [[VideoFileClip(session.get_path('video','side_view_rgb'))]]
            else : 
                print('cannot display this camera id : ',camera_id[0])
            
        if len(camera_id) == 2:
            if (('main' in camera_id[0]) or ('main' in camera_id[1])) and \
                    (('side_view' in camera_id[0]) or ('side_view' in camera_id[1])) :
            
                videoclip = [
                    [VideoFileClip(path_rbg),
                    VideoFileClip(session.get_path('video','side_view_rgb'))]
                ]
            elif (('main' in camera_id[0]) or ('main' in camera_id[1])) and \
                    (('depth' in camera_id[0]) or ('depth' in camera_id[1])) : 
                videoclip = [
                    [VideoFileClip(path_rbg),
                    VideoFileClip(session.get_path('video','main_depth'))]
                ]
            elif (('side_view' in camera_id[0]) or ('side_view' in camera_id[1])) and \
                    (('depth' in camera_id[0]) or ('depth' in camera_id[1])) : 
                videoclip = [
                    [VideoFileClip(session.get_path('video','side_view_rgb')),
                    VideoFileClip(session.get_path('video','side_view_depth'))]
                ]
            else :
                print('cannot display this camera id : ',camera_id[0],camera_id[1])

        if len(camera_id) == 3:
            videoclip = [
                [VideoFileClip(session.get_path(path_rbg)),
                VideoFileClip(session.get_path('video','side_view_rgb'))],
                [VideoFileClip(session.get_path('video','main_depth')),
                VideoFileClip(session.get_path('video','side_view_depth'))]
            ]
        
        videoclip = clips_array(videoclip)
        audioclip = AudioFileClip(session.get_path('audio'))

        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile(path_save,codec="libx264",audio_codec="aac",fps=30)
        
        if format_ffmpeg:
            os.system('ffmpeg -i %s %s'%(path_save,path_save.replace('.mp4','_ffmpeg.mp4')))
            os.remove(path_save)
    
    # def create_video_gaze(session: SessionData, path_save):
    #     state_file = session.load_state_file('main',is_final=True)

    #     cap = cv2.VideoCapture(video_path)
    #     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #     if video_path.split('.')[-1] == 'mp4':
    #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     else: 
    #         fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
    #     out = cv2.VideoWriter(video_save_path,fourcc, self.fps, (width,height))

    #     i = -1 
    #     while(cap.isOpened()):
    #         ret, frame = cap.read()
    #         i += 1
    #         if i%1000==0:
    #             print('step : ',i,'/',length,'')
    #         if i in frame_to_include:
    #             for _ in range(frame_as_dict[str(i)]):
    #                 out.write(frame)
    #         if ret==False:
    #             break
        
    #     cap.release()
    #     out.release()
    #     cv2.destroyAllWindows()

    def create_video_logs(self,session: SessionData, path_save):

        logs = session.load_log_file()
        state_file = session.load_state_file('main')
        
        video_path = session.get_path('video','main_rgb')

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        if video_path.split('.')[-1] == 'mp4':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        else: 
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        out = cv2.VideoWriter(path_save,fourcc, fps, (width,height))

        log_frame_value = logs['frame'].values
        log_text ='No log yet'
        frame_id = -1
        print('Processing video : %s'%video_path)
        log_to_display = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret==False:
                break
            frame_id += 1
            if frame_id%1000==0:
                print('step : ',frame_id,'/',length,'')
            
            idx = np.where(log_frame_value == frame_id)
            if len(idx[0]) > 0:
                for i in idx[0]:
                    log_to_display.append(logs['log'][i])
                
            font = cv2.FONT_HERSHEY_SIMPLEX
            # print the log of the videos 
            diplay_y = 50 
            i = 1
            while 50*i < height and i < len(log_to_display):
                cv2.putText(frame, 
                            log_to_display[-i], 
                            (50, 50*i), 
                            font, 1, 
                            (0, 255, 255), 
                            2, 
                            cv2.LINE_4)
                i += 1
            
            if state_file is not None: 
                idx = np.where(state_file['frame_index'].values == frame_id)
                cv2.putText(frame, 
                            'state : %s'%state_file['gaze_state'][idx[0][0]], 
                            (width-200, 250), 
                            font, 1, 
                            (0, 255, 255), 
                            2, 
                            cv2.LINE_4)
                
                frame[:200,width-400:,:] = 0
                if state_file['gaze_state'][idx[0][0]] == 'Screen': 
                    
                    x,y = state_file['screen_point_2d'][idx[0][0]].split(',')
                    x_rescale = int((float(x)/1920)*400)
                    y_rescale = int((float(y)/1080)*200)
                
                    frame = cv2.circle(frame, (x_rescale+width-400,y_rescale), radius=4, color=(0, 0, 255), thickness=-1)

            out.write(frame)

        out.release()
        cap.release()
        cv2.destroyAllWindows()

    # def view_video_and_logs():

    # def view_main_gaze(self, session : SessionData, path_save : str): 
    #     path_gaze_video = 'todo'
    #     self.create_video_gaze(session,path_gaze_video)
    #     videoclips = [[VideoFileClip(session.get_path('video','main_rgb')),VideoClip(path_gaze_video)]]


