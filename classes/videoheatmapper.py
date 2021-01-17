import cv2
import numpy as np
from collections import defaultdict
from moviepy.editor import VideoFileClip
from PIL import Image

class VideoHeatmapper:
    def __init__(self, img_heatmapper):
        self.img_heatmapper = img_heatmapper

    def heatmap_on_video_path(self, video_path, output_path, points, heat_fps=None, keep_heat=True, heat_decay_s=None):
        video = VideoFileClip(video_path)
        return self.heatmap_on_video(video, output_path, points, heat_fps, keep_heat, heat_decay_s)

    def heatmap_on_video(self, video, output_path, points, heat_fps, keep_heat, heat_decay_s):
        fps = video.fps
        width = video.w
        height = video.h
        shape = (width, height)

        frame_points = self._frame_points(
            points,
            fps=heat_fps if heat_fps is not None else int(fps),
            keep_heat=keep_heat,
            heat_decay_s=heat_decay_s
        )
        heatmap_frames = self._heatmap_frames(width, height, frame_points)
        
        new_video_frames = []
        count = 0
        total_frames = video.reader.nframes

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path,fourcc, fps, (width, height))        
        
        for frame in video.iter_frames(dtype='uint8'):
            try:
                count+=1
                print(count, total_frames)
                heat_frame = next(heatmap_frames)
                A = heat_frame[1]

                fg = Image.fromarray(heat_frame[1])
                bg = Image.fromarray(frame)

                bg.paste(fg, (0, 0), fg)

                out.write(cv2.cvtColor(np.asarray(bg), cv2.COLOR_RGBA2BGR))
            except StopIteration as e:
                out.write(cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGBA2BGR))
            
            out.release()
        
        return ret


    def _heatmap_frames(self, width, height, frame_points):
        for frame_start, points in frame_points.items():
            heatmap = self.img_heatmapper.heatmap(width, height, points)
            yield frame_start, np.array(heatmap)

    @staticmethod
    def _frame_points(pts, fps, keep_heat=False, heat_decay_s=None):
        interval = 1000 // fps
        frames = defaultdict(list)

        if not keep_heat:
            for x, y, t in pts:
                start = (t // interval) * interval
                frames[start].append((x, y))

            return frames

        pts = list(pts)
        last_interval = max(t for x, y, t in pts)

        for x, y, t in pts:
            start = (t // interval) * interval
            pt_last_interval = int(start + heat_decay_s*1000) if heat_decay_s else last_interval
            for frame_time in range(start, pt_last_interval+1, interval):
                frames[frame_time].append((x, y))

        return frames

    @staticmethod
    def _rgba2rgb( rgba, background=(255,255,255) ):
        row, col, ch = rgba.shape
        if ch == 3:
            return rgba
        assert ch == 4, 'RGBA image has 4 channels.'

        rgb = np.zeros( (row, col, 3), dtype='float32' )
        r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
        a = np.asarray( a, dtype='float32' ) / 255.0
        R, G, B = background

        rgb[:,:,0] = r * a + (1.0 - a) * R
        rgb[:,:,1] = g * a + (1.0 - a) * G
        rgb[:,:,2] = b * a + (1.0 - a) * B

        return np.asarray( rgb, dtype='uint8' )