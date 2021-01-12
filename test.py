from heatmappy import Heatmapper, VideoHeatmapper
from PIL import Image
import pandas as pd
import pandas as pd
from random import randint
from classes.heatmap import HeatMap

# TODO: get params from file
# TODO: get input from params
# TODO: remove out of bounds points
# TODO: calculate time for different frames
# TODO: add skip first lines param to Pandas
# TODO: add skip last lines param to Pandas
# TODO: merge multiple input files

## Params
TXT_IN_PATH = 'example/text_input/etr_1592956701406.csv'
# TXT_IN_PATH = 'example/text_input/etr_1592956701406.json'
IMG_IN_PATH = 'example/video_input/video_sample.mp4'
IMG_OP_PATH = 'example/video_output/out.mp4'
IMG_FRAMERATE = 30
TRK_FRAMERATE = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BITRATE = "5000k"
SKIP_N_FIRST_LINES = 0
SKIP_N_LAST_LINES = 0

## Read file
# df = pd.read_json(TXT_IN_PATH)
# df = df[["GazeX","GazeY","FrameNr"]]
# df['Timestamp'] = (df['FrameNr']*1/TRK_FRAMERATE).astype(int) * 100
# df = df.drop(["FrameNr"],axis=1)
# records = df.to_records(index=False)
# heat_points = list(records)


## Setup 
# img_heatmapper = Heatmapper()
# video_heatmapper = VideoHeatmapper(img_heatmapper)

# heatmap_video = video_heatmapper.heatmap_on_video_path(
#     video_path=IMG_IN_PATH,
#     points=heat_points
# )

# heatmap_video.write_videofile(IMG_OP_PATH, bitrate=BITRATE, fps=IMG_FRAMERATE)

hp = HeatMap(IMG_IN_PATH,TXT_IN_PATH,25)
hp.generate_output_video()