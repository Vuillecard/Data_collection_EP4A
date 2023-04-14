from synchronizer import Synchronizer, Viewer
from data_handler import SessionData

def main(): 
    path_session = '/Volumes/T7/dataset/EP4A_test/session_2023-01-30_16-59'

    synchroniser = Synchronizer(fps=30)
    viewer = Viewer()

    session = SessionData(path_session)
    # beep sound
    session.set_audio_start(12.419)
    session.set_video_start(205)

    #synchroniser = Synchronizer(fps=30)
    #session_sync = synchroniser(session)  

    session_sync = SessionData(path_session+'_sync')

    viewer.create_video_logs(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/video_test_main_log.mp4'
    )
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/video_test_main.mp4',
        camera_id= ['main'],
        path_rgb_log= '/Volumes/T7/dataset/EP4A_test/video_test_main_log.mp4',
        format_ffmpeg= False
    )
    
    # viewer.audio_video(
    #     session = session_sync, 
    #     path_save = '/Volumes/T7/dataset/EP4A_test/video_test_main_side.mp4',
    #     camera_id= ['main','side_view'],
    #     format_ffmpeg= False
    # )
    # viewer.audio_video(
    #     session = session_sync, 
    #     path_save = '/Volumes/T7/dataset/EP4A_test/video_test_main_side_depth.mp4',
    #     camera_id= ['main','side_view','depth'],
    #     format_ffmpeg= False
    # )

def process_new_data():
    path_session = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47'

    synchroniser = Synchronizer(fps=30)
    viewer = Viewer()
    
    session = SessionData(path_session)
    #session.set_audio_start(24.418)
    #session.set_video_start(480)

    session.set_audio_start(22.207)
    session.set_video_start(379)
    print('Curent video fps is %.2f s '%session.get_video_fps('main'))
    
    session_sync = synchroniser(session)  

    viewer.create_video_logs(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main_log.mp4'
    )
    session_sync = SessionData(path_session+'_sync')
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main.mp4',
        camera_id= ['main'],
        path_rgb_log= '/Volumes/T7/dataset/EP4A_test/video_test_main_log.mp4',
        format_ffmpeg= False
    )
    """ 
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main_side.mp4',
        camera_id= ['main','side_view'],
        format_ffmpeg= False
    )
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main_side_depth.mp4',
        camera_id= ['main','side_view','depth'],
        format_ffmpeg= False
    )"""


def process_new_data_2():
    path_session = '/Volumes/T7/dataset/EP4A_test/session_2023-01-30_17-56'

    synchroniser = Synchronizer(fps=30)
    viewer = Viewer()
    
    session = SessionData(path_session)
    session.set_audio_start(5.770)
    session.set_video_start(185)

    #session.set_audio_start(22.207)
    #session.set_video_start(379)
    print('Curent video fps is %.2f s '%session.get_video_fps('main'))
    
    #session_sync = synchroniser(session)  

    session_sync = SessionData(path_session+'_sync')
    viewer.create_video_logs(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-01-30_17-56/video_test_main_log.mp4'
    )
    session_sync = SessionData(path_session+'_sync')
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-01-30_17-56/video_test_main.mp4',
        camera_id= ['main'],
        path_rgb_log= '/Volumes/T7/dataset/EP4A_test/session_2023-01-30_17-56/video_test_main_log.mp4',
        format_ffmpeg= False
    )
    """ 
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main_side.mp4',
        camera_id= ['main','side_view'],
        format_ffmpeg= False
    )
    viewer.audio_video(
        session = session_sync, 
        path_save = '/Volumes/T7/dataset/EP4A_test/session_2023-02-09_16-47/video_test_main_side_depth.mp4',
        camera_id= ['main','side_view','depth'],
        format_ffmpeg= False
    )"""


# main 
if __name__ == '__main__':
    process_new_data_2()
