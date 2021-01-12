import os
import pandas as pd
import numpy as np
from cv2 import cv2

class HeatMap:

    def __init__(self, base_video, base_input, framerate):
        self.base_video = base_video
        self.base_input = base_input
        self.framerate = framerate
        self.cap = cv2.VideoCapture(self.base_video)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps =  self.cap.get(cv2.CAP_PROP_FPS)
        self.list_point = list()
        self.heat_clips = list()
        self.create_point_list()
        for point in self.list_point:
            if point[0] > self.height or point[1] > self.width :
                continue
            self.heat_clips.append((point[2], self.generate_heatmap(int(point[0]),int(point[1]))))

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

        df = df[["GazeX","GazeY","time"]]
        start = df['time'].min()
        df['Frame'] = ((df.time - start)/self.fps).astype(int)
        df = df.loc[df['Frame'] <= self.frames]
        df = df.drop(["time"],axis=1)
        records = df.to_records(index=False)
        self.list_point = list(records)

    def generate_heatmap(self,x,y):
        mask_dim = (self.height, self.width, 3)
        mask = np.zeros(mask_dim, dtype=np.uint8)
        mask_size = 15
        kernel_size = 5
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_size,kernel_size))
        rng = 1
        mask[x,y] = 255
        # mask[(x-rng):(x+rng), (y-rng):(y+rng)] = 255
        mask = mask.astype(np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = 15)
        bw = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        dist = cv2.distanceTransform(bw, cv2.DIST_C, 5).astype(np.uint8)
        heat_mask = cv2.applyColorMap(dist, cv2.COLORMAP_JET)
        return heat_mask

    def get_heatmask(self,frame):
        prev_item = self.heat_clips[0]
        for item in self.heat_clips:
            if item[0] > frame:
                return prev_item[1]
            elif item[0] == frame:
                return item[1]
            else:
                prev_item = item
                continue
        return prev_item[1]

    def generate_output_video(self, output_name = "output.avi", audio = True):
        out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (self.width, self.height))
        count = 0
        while self.cap.isOpened() and count < self.frames:
            _,frame = self.cap.read()
            heat_mask = self.get_heatmask(count) ## TODO Get real Heatmap
            new_img = cv2.addWeighted(frame, 0.2, heat_mask, 0.9, 0)
            out.write(new_img)
            count = count + 1
        self.cap.release()
        out.release()