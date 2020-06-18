'''
Simple lane detection algorithm.
To use type "python3 main.py path_fo_video_file".
'''
import time
import sys
import cv2
from lane_detection import LaneDetection

def sync_fps(time_start, fps):
    '''
    Sleeping function. Wait until reach desired frame rate.
    :param time_start: last frame timestamp
    :return:
    '''
    time_difference = time.time() - time_start
    if time_difference < 1.0 / (fps):
        time.sleep(1.0 / (fps) - time_difference)

def main():
    '''
    Video streaming.
    Press 'q' to exit and 'w' to pause video.
    :return:
    '''
    if len(sys.argv) > 1:
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture('videos/road01.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    while cap.isOpened():
        time_start = time.time()
        _, frame = cap.read()
        frame = LaneDetection(frame).lane_detection()
        cv2.imshow("Lane Detection", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('w'):
            cv2.waitKey(-1)
        sync_fps(time_start, fps)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
