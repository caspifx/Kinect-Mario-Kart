import numpy as np
import cv2
import render_image
import pyautogui
import threading
import time
import Player

sdThresh = 20
font = cv2.FONT_HERSHEY_SIMPLEX
controls = [['Up', 'Left','Right'], ['w', 'a', 'd']]
number_of_players = 2

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


def capture_frame(cap):
    _, frame = cap.read()
    return render_image.slice(frame, number_of_players)


def player_initial_frames(frame1, frame2, player):

    frame1s = render_image.slice(frame1, 3)

    frame2s = render_image.slice(frame2, 3)

    player.initial_frames = [(frame1s), (frame2s)]



def main():
    cv2.namedWindow('frame')
    cap = cv2.VideoCapture(0)

    frame1 = capture_frame(cap)
    frame2 = capture_frame(cap)

    players = []
    for i in range(number_of_players):
        players.append(Player.Player(1, controls[i][0], controls[i][1], controls[i][2], 'r', 0.5))
    # capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
    i = 0
    for player in players:
        player_initial_frames(frame1[i], frame2[i], player)
        player.always_forward()
        i += 1


    # maintains fixed forward speed


    while True:
        _, frame3_all = cap.read()
        frame3s = render_image.slice(frame3_all, number_of_players)
        i = 0
        for player in players:
            frame3 = frame3s[i]
            i += 1
            frames = render_image.slice(frame3, 3)
            frame_index = 0
            # states = {'right': False, 'center': False, 'left': False}
            for frame in frames:
                frame1 = player.initial_frames[0][frame_index]
                frame2 = player.initial_frames[1][frame_index]
                rows, cols, _ = np.shape(frame)
                dist = distMap(frame1, frame)

                frame1 = frame2
                frame2 = frame

                # apply Gaussian smoothing
                mod = cv2.GaussianBlur(dist, (9, 9), 0)

                # apply thresholding
                _, thresh = cv2.threshold(mod, 100, 255, 0)

                # calculate st dev test
                _, stDev = cv2.meanStdDev(mod)

                cv2.putText(frame2, 'SPLIT', (70, 70), font, 1.5, (255, 255, 255), 1, cv2.LINE_AA)
                if stDev > sdThresh:
                    cv2.putText(frame2, 'SPLIT', (70, 70), font, 1.5, (0, 0, 100), 1, cv2.LINE_AA)
                    if frame_index == 0:
                        player.states['right'] = True
                    if frame_index == 1:
                        player.states['center'] = True
                    if frame_index == 2:
                        player.states['left'] = True
                        # TODO: Face Detection 2
                player.handle_movement()
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                frame_index += 1
            # cv2.imshow('dist', frame3)
            #     # dist = distMap(frame1, frame3)
            #     # mod = cv2.GaussianBlur(dist, (9, 9), 0)
            #     # cv2.imshow('dist', mod)
        height, width = frame3_all.shape[:2]
        width /= number_of_players
        for i in range(number_of_players):
            cv2.line(frame3_all, (int(width / 3)+ int(i*width), 0), (int(width / 3) + int(width*i), height), (0, 0, 0), 1)
            cv2.line(frame3_all, (int(width / 3)*2+ int(i*width), 0), (int(width / 3)*2+ int(i*width), height), (0, 0, 0), 1)
        if number_of_players > 1:
            cv2.line(frame3_all, (int(width), 0), (int(width), height), (0, 0, 255), 3)
        cv2.imshow('frame', frame3_all)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()