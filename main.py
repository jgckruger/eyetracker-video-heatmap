from classes.videoheatmapper import VideoHeatmapper
from classes.heatmapper import Heatmapper
import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(
    description='Heatmap on Video.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

parser.add_argument(
    'data_in_path',
    metavar='data_in_path',
    type=str,
    help='string path to input file containing heat map data points',
)

parser.add_argument(
    'video_in_path',
    metavar='video_in_path',
    type=str,
    help='string path to input video',
)

parser.add_argument(
    'output_name',
    type=str,
    help='string name to output file ',
    default="output.mp4"
)

parser.add_argument(
    '--colours',
    metavar = "",
    type=str,
    choices=['default', 'reveal'],
    help='string name of the desired colors for the heat map. Default = Blue and Orange, Reveal = Black and White',
    default="default"
)

parser.add_argument(
    '--point_strength',
    metavar = "",
    type = float,
    help = 'float that determines the strength of the heat map point',
    default = 0.9
)

parser.add_argument(
    '--point_diameter',
    metavar = "",
    type = int,
    help = 'integer that determines the pixel size of each heat map point',
    default = 150
)

parser.add_argument(
    '--point_opacity',
    metavar = "",
    type=float,
    help='float that determines the opacity of each heat map point',
    default=0.7
)

parser.add_argument(
    '--skip_n_first_lines',
    metavar = "",
    type = int,
    nargs = 1,
    help = 'integer used to skip the first inconsistent data points from input file ',
    default = 1
)

parser.add_argument(
    '--skip_n_last_lines',
    metavar = "",
    type = int,
    help = 'integer used to skip the last inconsistent data points from input file ',
    default = 0
)

parser.add_argument(
    '--keep_heat',
    metavar = "",
    type = bool,
    help = 'boolean that dictates whether the points will fade over time. With --keep_heat=False, the output video will look like a eye-tracker rater than a heatmapper',
    default = True
)

parser.add_argument(
    '--heat_decay_s',
    metavar = "",
    type = int,
    help = 'time in seconds that dictates how long the heat map points will be on the screen',
    default = 5
)

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

df = pd.read_csv(options.data_in_path)
df.drop(df.head(options.skip_n_first_lines).index,inplace=True)
df.drop(df.tail(options.skip_n_last_lines).index,inplace=True)

df = df[['GazeX','GazeY','time']]
df = df[df['time'] != 0]
df['timestamp'] = (df['time'] - df['time'].min())#/1000
df.drop(['time'],axis=1, inplace=True)
records = df.to_records(index=False)
points = list(records)

img_heatmapper = Heatmapper(colours=options.colours, point_strength=options.point_strength, point_diameter=options.point_diameter, opacity=options.point_opacity)
video_heatmapper = VideoHeatmapper(img_heatmapper)
video = video_heatmapper.heatmap_on_video_path(options.video_in_path, options.output_name, points, keep_heat=True, heat_decay_s=5)

