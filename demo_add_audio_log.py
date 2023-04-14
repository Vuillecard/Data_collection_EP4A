import argparse
from data_handler import add_audio_and_log

def main(args):
    # add audio and log to the session folder
    add_audio_and_log(
        global_path = args.global_path,
        room = args.room,
        day = args.day,
        participant = args.participant
    )

# main 
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
    
    args = ap.parse_args()
    main(args)