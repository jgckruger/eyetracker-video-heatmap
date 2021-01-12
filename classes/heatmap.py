import os
import pandas as pd
from cv2 import cv2

class HeatMap:

    def __init__(self, base_video, base_input, framerate):
        self.base_video = base_video
        self.base_input = base_input
        self.framerate = framerate
        self.list_point = []
        self.create_point_list()

    def create_point_list(self):
        if os.path.isdir(self.base_input):
            ## TODO Handle multiple inputs
            pass
        _, extension = os.path.splitext(self.base_input)
        if extension == ".json":
            df = pd.read_json(self.base_input)
        elif extension == ".csv":
            df = pd.read_csv(self.base_input, delimiter = ",")
        else:
            raise Exception("File Format Not Supported")

        df = df[["GazeX","GazeY","FrameNr"]]
        df['Timestamp'] = (df['FrameNr']*1/self.framerate).astype(int) * 100
        df = df.drop(["FrameNr"],axis=1)
        records = df.to_records(index=False)
        self.list_point = list(records)

    def generate_heatmap(self):
        ## TODO Get code from jupyter here
        pass

    def generate_output_video(self, output_name = "output.avi"):
        cap = cv2.VideoCapture(self.base_video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps =  cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(output_name, 20, fps, (height,  width))
        count = 0
        while cap.isOpened():
            _,frame = cap.read()
            heat_mask = cv2.flip(frame , 0)
            new_img = cv2.addWeighted(frame, 1, heat_mask, 0.2, 0)
            out.write(new_img)
            count = count + 1
        cap.release()
        out.release()