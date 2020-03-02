import cv2
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
output_vids_path = "test_videos_output/"

class LineDetector:
    def __init__(self, video=None):
        if video == None:
            self.video_mode = False
        else:
            self.video_ = video
            self.video_mode = True
        
        self.left_lines_  = deque(maxlen=500)
        self.right_lines_ = deque(maxlen=500)

    def show_images(self, images, cmap=None):
        cols = 2
        rows = (len(images)+1)//cols
        
        plt.figure(figsize=(10, 11))
        for i, image in enumerate(images):
            plt.subplot(rows, cols, i+1)
            # use gray scale color map if there is only one channel
            cmap = 'gray' if len(image.shape)==2 else cmap
            plt.imshow(image, cmap=cmap)
            plt.xticks([])
            plt.yticks([])
        plt.tight_layout(pad=0, h_pad=0, w_pad=0)
        plt.show()

    def convert_gray_scale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def convert_hls(self, image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

    def select_white_yellow(self, image):
        converted = self.convert_hls(image)
        # white color mask
        lower = np.uint8([0, 200, 0])
        upper = np.uint8([255, 255, 255])
        white_mask = cv2.inRange(converted, lower, upper)
        # yellow color mask
        lower = np.uint8([10, 0, 100])
        upper = np.uint8([40, 255, 255])
        yellow_mask = cv2.inRange(converted, lower, upper)
        # combine the mask
        mask = cv2.bitwise_or(white_mask, yellow_mask)
        return cv2.bitwise_and(image, image, mask = mask)
    
    def filter_region(self, image, vertices):
        """
        Create the mask using the vertices and apply it to the input image
        """
        mask = np.zeros_like(image)
        if len(mask.shape)==2:
            cv2.fillPoly(mask, vertices, 255)
        else:
            cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
        return cv2.bitwise_and(image, mask)
    

    def select_region(self, image):
        """
        It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
        """
        # first, define the polygon by vertices
        rows, cols   = image.shape[:2]
        bottom_left  = [cols*0.1, rows*0.95]
        top_left     = [cols*0.4, rows*0.65]
        bottom_right = [cols*0.9, rows*0.95]
        top_right    = [cols*0.6, rows*0.65] 
        # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
        vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
        return self.filter_region(image, vertices)

    def apply_smoothing(self, image, kernel_size=15):
        """
        kernel_size must be postivie and odd
        """
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def detect_edges(self, image, low_threshold=50, high_threshold=150):
        return cv2.Canny(image, low_threshold, high_threshold)

    def hough_lines(self, image):
        return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)


    def average_slope_intercept(self, lines):
        left_lines    = [] # (slope, intercept)
        left_weights  = [] # (length,)
        right_lines   = [] # (slope, intercept)
        right_weights = [] # (length,)
        
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x2==x1:
                    continue # ignore a vertical line
                slope = (y2-y1)/(x2-x1)
                intercept = y1 - slope*x1
                length = np.sqrt((y2-y1)**2+(x2-x1)**2)
                if slope < 0: # y is reversed in image
                    left_lines.append((slope, intercept))
                    left_weights.append((length))
                else:
                    right_lines.append((slope, intercept))
                    right_weights.append((length))
        
        # add more weight to longer lines    
        left_lane  = np.dot(left_weights,  left_lines) /np.sum(left_weights)  if len(left_weights) >0 else None
        right_lane = np.dot(right_weights, right_lines)/np.sum(right_weights) if len(right_weights)>0 else None
        
        return left_lane, right_lane # (slope, intercept), (slope, intercept)

    def make_line_points(self, y1, y2, line):
        """
        Convert a line represented in slope and intercept into pixel points
        """
        if line is None:
            return None
        
        slope, intercept = line
        
        # make sure everything is integer as cv2.line requires it
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        y1 = int(y1)
        y2 = int(y2)
        
        return ((x1, y1), (x2, y2))

    def lane_lines(self, image, lines):
        left_lane, right_lane = self.average_slope_intercept(lines)
        
        y1 = image.shape[0] # bottom of the image
        y2 = y1*0.6         # slightly lower than the middle

        left_line  = self.make_line_points(y1, y2, left_lane)
        right_line = self.make_line_points(y1, y2, right_lane)
        
        return left_line, right_line

    def mean_line(self, line, lines):
        if line is not None:
            lines.append(line)

        if len(lines)>0:
            line = np.mean(lines, axis=0, dtype=np.int32)
            line = tuple(map(tuple, line)) # make sure it's tuples not numpy array for cv2.line to work
        return line

    def draw_lane_lines(self, image, lines, color=[255, 0, 0], thickness=10):
        # make a separate image to draw lines and combine with the orignal later
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                cv2.line(line_image, *line,  color, thickness)
        # image1 * α + image2 * β + λ
        # image1 and image2 must be the same shape.
        return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)


    def process_frame(self, image):
            white_yellow = self.select_white_yellow(image)
            gray         = self.convert_gray_scale(white_yellow)
            smooth_gray  = self.apply_smoothing(gray)
            edges        = self.detect_edges(smooth_gray)
            regions      = self.select_region(edges)
            lines        = self.hough_lines(regions)
            left_line, right_line = self.lane_lines(image, lines)
            
            left_line  = self.mean_line(left_line,  self.left_lines_)
            right_line = self.mean_line(right_line, self.right_lines_)

            return self.draw_lane_lines(image, (left_line, right_line))
    
    def process_video(self):
        if self.video_mode:
            global output_vids_path
            clip = VideoFileClip(self.video_)
            processed = clip.fl_image(self.process_frame)
            processed.write_videofile(output_vids_path + self.video_.split("/")[-1], audio=False)
        else:
            print("This object is not capable of processing video")