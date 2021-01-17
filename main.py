from classes.videoheatmapper import VideoHeatmapper
from classes.heatmapper import Heatmapper
import pandas as pd
import cv2


video_path = 'example/video_input/Estimulo Hibrido Cogni.mp4'
text_path = 'example/text_input/etr_1592956701406.csv'
output_path = 'example/video_input/heatmap.mp4'

df = pd.read_csv(text_path)
df = df[['GazeX','GazeY','time']]
df = df[df['time'] != 0]
df['timestamp'] = (df['time'] - df['time'].min())#/1000
df.drop(['time'],axis=1, inplace=True)
records = df.to_records(index=False)
points = list(records)

img_heatmapper = Heatmapper(colours='default', point_strength=0.9, point_diameter=150, opacity=0.7)
video_heatmapper = VideoHeatmapper(img_heatmapper)
video = video_heatmapper.heatmap_on_video_path(video_path, output_path, points, keep_heat=True, heat_decay_s=5)

