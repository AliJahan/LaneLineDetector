
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import statistics
import cv2
import math


class ImageOperations(object):
    # def __init__(self,nb_frame):
        # self.nb_frame_ = nb_frame

    def read_image(self, file_name):
        """ Reads image from the file"""
        return mpimg.imread(file_name)
    def grayscale(self, img):
        """Applies the Grayscale transform
        This will return an image with only one color channel
        but NOTE: to see the returned image as grayscale
        (assuming your grayscaled image is called 'gray')
        you should call plt.imshow(gray, cmap='gray')"""
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Or use BGR2GRAY if you read an image with cv2.imread()
        # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    def imshow(self, image, print_info=False, gray=False):
        """Shows an image as regular or gray, prints its info"""
        if print_info:
            print('This image is:', type(image), 'with dimensions:', image.shape)

        if gray:
            plt.imshow(image, cmap='gray')
        else:
            plt.imshow(image)
            
    def canny(self, img, low_threshold, high_threshold):
        """Applies the Canny transform"""
        return cv2.Canny(img, low_threshold, high_threshold)

    def gaussian_blur(self, img, kernel_size):
        """Applies a Gaussian Noise kernel"""
        return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

    def region_of_interest(self, img, vertices):
        """
        Applies an image mask.
        
        Only keeps the region of the image defined by the polygon
        formed from `vertices`. The rest of the image is set to black.
        `vertices` should be a numpy array of integer points.
        """
        #defining a blank mask to start with
        mask = np.zeros_like(img)   
        
        #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(img.shape) > 2:
            channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255
            
        #filling pixels inside the polygon defined by "vertices" with the fill color    
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        
        #returning the image only where mask pixels are nonzero
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def draw_lines(self, img, lines, color=[255, 0, 0], thickness=2):
        """
        NOTE: this is the function you might want to use as a starting point once you want to 
        average/extrapolate the line segments you detect to map out the full
        extent of the lane (going from the result shown in raw-lines-example.mp4
        to that shown in P1_example.mp4).  
        
        Think about things like separating line segments by their 
        slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
        line vs. the right line.  Then, you can average the position of each of 
        the lines and extrapolate to the top and bottom of the lane.
        
        This function draws `lines` with `color` and `thickness`.    
        Lines are drawn on the image inplace (mutates the image).
        If you want to make the lines semi-transparent, think about combining
        this function with the weighted_img() function below
        """
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)

    def hough_lines(self, img, rho, theta, threshold, min_line_len, max_line_gap):

        """
        `img` should be the output of a Canny transform.
            
        Returns an image with hough lines drawn.
        """
        lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
        line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        draw_lines(line_img, lines)
        return line_img

    def weighted_img(self, img, initial_img, alpha=0.8, beta=1.0, gamma=0.0):
        # """
        # `img` is the output of the hough_lines(), An image with lines drawn on it.
        # Should be a blank image (all black) with lines drawn on it.
        # `initial_img` should be the image before any processing.
        # The result image is computed as follows:
        # initial_img * α + img * β + γ
        # NOTE: initial_img and img must be the same shape!
        # """
        return cv2.addWeighted(initial_img, alpha, img, beta, gamma)
    
    def point_vs_line_loc(self, lp_x1, lp_y1, lp_x2, lp_y2, p_x, p_y):
        v1 = (lp_x2-lp_x1, lp_y2-lp_y1)     # Vector 1
        v2 = (p_x-lp_x1, p_y-lp_y1)             # Vector 2
        cross_product = v1[0]*v2[1] - v1[1]*v2[0]
        if cross_product >= 0:
            return "cc_side"
        else:
            return "c_side"
        
    # @staticmethod
    def process_image(self, image):
        # if self.nb_frame_ == 0:
        cv2.imwrite('test_images/challenge.jpg', image)
        # print(image.shape)
        gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # print(gray.shape)
        # Define a kernel size and apply Gaussian smoothing
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

        # Define our parameters for Canny and apply
        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

        # Next we'll create a masked edges image using cv2.fillPoly()
        mask = np.zeros_like(edges)   
        ignore_mask_color = 255   

        # This time we are defining a four sided polygon to mask
        imshape = image.shape
        vertices = np.array([[(0,imshape[0]),(0, 0), (imshape[1], 0), (imshape[1],imshape[0])]], dtype=np.int32)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(edges, mask)

        # Define the Hough transform parameters
        # Make a blank the same size as our image to draw on
        rho = 1 # distance resolution in pixels of the Hough grid
        theta = np.pi/180 # angular resolution in radians of the Hough grid
        threshold = 1     # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 7 #minimum number of pixels making up a line
        max_line_gap = 1    # maximum gap in pixels between connectable line segments
        line_image = np.copy(image)*0 # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                                    min_line_length, max_line_gap)

        length = image.shape[0]
        length = image.shape[0]
        buttom_left = (30, 600)
        top_left = (445, 320)
        top_right = (520, 320)
        buttom_right = (1000, 600)
        # Iterate over the output "lines" and draw lines on a blank image
        neg_slope = []
        pos_slope = []
        pos_slopes = []
        neg_slopes= []
        for line in lines:
            for x1,y1,x2,y2 in line:
                right_of_left_border = self.point_vs_line_loc(buttom_left[0],buttom_left[1],top_left[0],top_left[1], x1,y1) == "cc_side" and self.point_vs_line_loc(buttom_left[0],buttom_left[1],top_left[0],top_left[1], x2,y2) == "cc_side" 
                left_of_right_border = self.point_vs_line_loc(buttom_right[0],buttom_right[1],top_right[0],top_right[1], x1,y1) == "c_side" and self.point_vs_line_loc(buttom_right[0],buttom_right[1],top_right[0],top_right[1], x2,y2) == "c_side"
                below_upper_border = self.point_vs_line_loc(top_right[0],top_right[1],top_left[0],top_left[1], x1,y1) == "c_side" and self.point_vs_line_loc(top_right[0],top_right[1],top_left[0],top_left[1], x2,y2) == "c_side" 
                if right_of_left_border and left_of_right_border and below_upper_border:
                    slope = (y2-y1)/(x2-x1)
                    if slope>0:
                        neg_slope.append((x1,y1))
                        neg_slope.append((x2,y2))
                        neg_slopes.append(((y2-y1)/(x2-x1)))
                    else:
                        pos_slope.append((x1,y1))
                        pos_slope.append((x2,y2))
                        pos_slopes.append(((y2-y1)/(x2-x1)))
        neg_median = statistics.median(neg_slopes)
        pos_median = statistics.median(pos_slopes)
        threshold = .2

        tmp = []
        for i in range(0,len(neg_slope),2):
            slope = (neg_slope[i+1][1]-neg_slope[i][1])/(neg_slope[i+1][0]-neg_slope[i][0])
            if abs(slope-neg_median) < threshold:
                tmp.append(neg_slope[i])
                tmp.append(neg_slope[i+1])

        neg_slope = tmp
        tmp = []
        for i in range(0,len(pos_slope),2):
            slope = (pos_slope[i+1][1]-pos_slope[i][1])/(pos_slope[i+1][0]-pos_slope[i][0])
            if abs(slope-pos_median) < threshold:
                tmp.append(pos_slope[i])
                tmp.append(pos_slope[i+1])
        pos_slope = tmp
        # for i in range(0,len(neg_slope),2):
        #     cv2.line(line_image,neg_slope[i],neg_slope[i+1],(0,255,0),5)
        # for i in range(0,len(pos_slope),2):
        #     cv2.line(line_image,pos_slope[i],pos_slope[i+1],(0,0,255),5)
        # print(len(neg_slope))
        
        [vx,vy,x,y] = cv2.fitLine(np.array(neg_slope, dtype=np.int32), cv2.DIST_L2,0,0.01,0.01)
        lefty = int(((top_right[0]-x)*vy/vx) + (y))
        righty = int(((buttom_right[0]-x)*vy/vx)+(y))
        cv2.line(image,(buttom_right[0],righty),(top_right[0],lefty),(0,0,255), 4)
 
        [vx,vy,x,y] = cv2.fitLine(np.array(pos_slope, dtype=np.int32), cv2.DIST_L2,0,0.01,0.01)
        lefty = int(((top_left[0]-x)*vy/vx) + (y))
        righty = int(((buttom_left[0]-x)*vy/vx)+(y))
        cv2.line(image,(buttom_left[0],righty),(top_left[0],lefty),(0,0,255),4)
        
        # Create a "color" binary image to combine with line image
        # color_edges = np.dstack((image[:,:,0],image[:,:,1],image[:,:,2])) 
        color_edges = np.dstack((edges, edges, edges)) 
        # Draw the lines on the edge image
        lines_edges = cv2.addWeighted(color_edges, 1, line_image, .5, 0) #,(515, 310), (980, 600)
        cv2.polylines(lines_edges, np.array([[top_left,top_right]], dtype=np.int32),False,(255,255,0) )
        cv2.polylines(lines_edges, np.array([[top_right,buttom_right]], dtype=np.int32),False,(255,255,0) )
        cv2.polylines(lines_edges, np.array([[top_left,buttom_left]], dtype=np.int32),False,(255,255,0) )
        
        return lines_edges

# n_frame = 0
def wrapped_process_image(image):
    # print("s")
    d = ImageOperations()
    # n_frame += 1
    return d.process_image(image)
