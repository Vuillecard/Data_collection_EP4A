from synchronizer import Synchronizer, Viewer
from data_handler import SessionData, add_audio_and_log, session_path
import argparse
import os 

def main(args):
    # synchronise the session

    synchroniser = Synchronizer(fps=30)
    viewer = Viewer()

    path_session = session_path(
            global_path = args.global_path,
            room = args.room,
            day = args.day,
            participant = args.participant
        )
    
    if args.add_audio_log:
        add_audio_and_log(
            global_path = args.global_path,
            room = args.room,
            day = args.day,
            participant = args.participant
        )

    if args.synchronise:
        # define the data format
        session = SessionData(path_session)
        session.set_audio_start(5.770)
        session.set_video_start(185)
        print('Curent video fps is %.2f s '%session.get_video_fps('main'))
        # synnhronise the video 
        session_sync = synchroniser(session)  
        
    if args.view:
        # define the data synchronise format
        session_sync = SessionData(path_session+'_sync')
        save_dir = os.path.dirname(__file__) if args.save_view=='None' else args.save_view
        viewer.create_video_logs(
            session = session_sync, 
            path_save = os.path.join(save_dir,'video_test_main_log.mp4')
        )
        viewer.audio_video(
        session = session_sync, 
        path_save = os.path.join(save_dir,'video_main_synch.mp4'),
        camera_id= ['main'],
        path_rgb_log= os.path.join(save_dir,'video_main_log_gaze.mp4'),
        format_ffmpeg= False
    )


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-gp", "--global_path", type= str, required=True,
                    help="path to the folder containing all the data, video , audio and log")
    ap.add_argument("-r", "--room", type=int, required=True,
                    help="room number")
    ap.add_argument("-d", "--day", type=int, required=True,
                    help="day number")
    ap.add_argument("-p", "--participant", type=str, required=True,
                    help="participant number")
    ap.add_argument("-a", "--add_audio_log", action='store_true',
                    help="add audio and log to the session")
    ap.add_argument("-s", "--synchronise", action='store_true',
                    help="synchronise the session")
    ap.add_argument("-v", "--view", action='store_true',
                    help="view the synchronise session")
    ap.add_argument("--save_view", default='None', help="view location")
    
    args = ap.parse_args()
    main(args)