import cv2
import time

# Video variables
cap = cv2.VideoCapture('videos/road01.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

def sync_fps(time_start):
    '''
    Sleeping function. Wait until reach desired frame rate.
    :param time_start: last frame timestamp
    :return:
    '''
    timeDiff = time.time() - time_start
    if (timeDiff < 1.0 / (fps)):
        time.sleep(1.0 / (fps) - timeDiff)

def main():
    '''
    Video streaming.
    Press 'q' to exit and 'w' to pause video.
    :return:
    '''
    while (cap.isOpened()):
        time_start = time.time()
        ret, frame = cap.read()
        cv2.imshow("Lane Detection", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('w'):
            cv2.waitKey(-1)
        sync_fps(time_start)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()