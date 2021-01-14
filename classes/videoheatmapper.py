import cv2
import numpy as np
from collections import defaultdict

class VideoHeatmapper:
    def __init__(self, img_heatmapper):
        self.img_heatmapper = img_heatmapper

    def heatmap_on_video_path(self, video_path, points, heat_fps=25, keep_heat=True, heat_decay_s=None):
        video = cv2.VideoCapture(video_path)
        return self.heatmap_on_video(video, points, heat_fps, keep_heat, heat_decay_s)

    def heatmap_on_video(self, base_video, points, heat_fps, keep_heat, heat_decay_s):
        width  = int(base_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(base_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = base_video.get(cv2.CAP_PROP_FPS)
        frame_points = self._frame_points(
            points,
            fps=heat_fps or fps,
            keep_heat=keep_heat,
            heat_decay_s=heat_decay_s
        )
        heatmap_frames = self._heatmap_frames(width, height, frame_points)
        
        new_video_frames = []
        count = 0
        total_frames = self._get_number_of_frames(base_video)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4',fourcc, fps, (width,height))
        
        while base_video.isOpened():
            ret,frame = base_video.read()
            count += 1
            print(str(int(count*100/total_frames)) + "/" + str(total_frames*100/total_frames))
            if count > total_frames:
                break
            try:
                heat_frame = next(heatmap_frames)
                # TODO: correctly merge the RGBA and RGB frames
                # TODO: merge audio
                heat_mask = self._rgba2rgb(heat_frame[1])
                # frame=cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
                new_img = cv2.addWeighted(frame, 0.5, heat_mask, 0.2, 0)
                new_video_frames.append(new_img)
                out.write(new_img)
            except StopIteration as e:
                new_video_frames.append(frame)
                out.write(frame)

        base_video.release()
        out.release()


        # TODO: GENERATE VIDEO FILE
        return new_video_frames


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
    def _get_number_of_frames(video_capture):
        if cv2.__version__.startswith("4."): # OpenCV 3+
            return int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        return int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

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