'''
Lane Detection algorithm based on Hough transform.
'''
import numpy as np
import cv2

class LaneDetection():
    '''The LaneDetection object contains processed frame with lines.'''
    def __init__(self, frame):
        self.frame = frame
        self.height, self.width, self.channels = frame.shape
        self.lane_detection()

    def lane_detection(self):
        '''
        Calling image preprocessing, processing and postprocessing
        :return: postprocessed frame
        '''
        preprocessed_frame, height_shift = self.frame_preprocessing(self.frame)
        roi_edges = self.canny_edge_detection(preprocessed_frame)
        lines = cv2.HoughLinesP(roi_edges, 1, np.pi / 180, 127, minLineLength=10, maxLineGap=250)
        for line in lines:
            x_1, y_1, x_2, y_2 = line[0]
            cv2.line(self.frame, (x_1, y_1 + height_shift),
                     (x_2, y_2 + height_shift), (0, 255, 0), 2)

        postprocessed_frame = self.frame_postprocessing(frame=self.frame,
                                                        processed_frame=roi_edges, scale=0.7)
        return postprocessed_frame

    def frame_preprocessing(self, frame):
        '''
        Frame preprocessing. Selecting ROI (Region of Interest), grayscaling and smoothing.
        :param frame: original video frame
        :return: preprocessed frame, ROI's shift
        '''
        height_shift = int(self.height / 2)
        roi_frame = frame[height_shift:self.height, 0:self.width]
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 2)
        return blur, height_shift

    @staticmethod
    def canny_edge_detection(frame, sigma=0.33):
        '''
        Canny edge detection with automatic threshold values.
        :param frame: preprocessed frame
        :param sigma: threshold width range
        :return: frame's edges
        '''
        median = np.median(frame)
        thresh_low = int(max(0, (1.0 - sigma) * median))
        thresh_up = int(min(255, (1.0 + sigma) * median))
        edges = cv2.Canny(frame, thresh_low, thresh_up)
        print(median, thresh_low, thresh_up)
        return edges

    def frame_postprocessing(self, frame, processed_frame, scale=1.0):
        '''
        Merging original and processed frame for better comparison.
        :param frame: original video frame
        :param processed_frame: processed frame
        :param scale: frame scale factor
        :return: postprocessed frame
        '''
        height_m = int(self.height * scale)
        width_m = int(self.width * scale * 2)
        blank_frame = np.zeros((int(self.height / 2), self.width, 3), np.uint8)
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2RGB)
        merged_frames = np.concatenate((blank_frame, processed_frame_rgb), axis=0)
        merged_frames = np.concatenate((frame, merged_frames), axis=1)
        resized_frame = cv2.resize(merged_frames, (width_m, height_m))
        return resized_frame
