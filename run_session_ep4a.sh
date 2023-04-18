GLOBAL_PATH="/Volumes/TUSHI/EP4A"
ROOM=1
DAY=2
PARTICIPANT="C12"
SAVE_VIEW="/Volumes/TUSHI/res"
FRAME_SYNC=475
AUDIO_SYNC=22.633

python demo_ep4a.py --global_path ${GLOBAL_PATH} --room ${ROOM} --day ${DAY}\
            --participant ${PARTICIPANT} --save_view ${SAVE_VIEW}\
            --frame_sync ${FRAME_SYNC} --audio_sync ${AUDIO_SYNC}\
            --add_audio_log --synchronise --view
