import json
import getpass
import time
from pathlib import Path

import requests
from PIL import Image
import os 
import cv2
import numpy as np
import pygame
from pygame.locals import *

import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk

from pymediainfo import MediaInfo


from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError

from video_processing import save_frames
from face_detect import crop_face
# from strotss import *

cache_file = Path("test_token.cache")
art_counter = 0

screen_height = 1080
screen_width = 1920


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code


def sign_in_get_devices():
    if cache_file.is_file():
        auth = Auth("protected-by-ring/1.0", json.loads(cache_file.read_text()), token_updated)
    else:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        auth = Auth("protected-by-ring/1.0", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()

    devices = ring.devices()
    doorbell = devices['doorbots'][0]  # this is a list but we just have 1 doorbell
    return doorbell


# def save_latest_video(doorbell, filename):
#     print("downloading most recent doorbell motion...")
#     doorbell.recording_download(doorbell.history(limit=10, kind='ding')[0]['id'], filename=filename, override=True)
#     print("Downloaded locally: ", filename)


def get_doorbell_events(doorbell):
    last_motion = doorbell.history(limit=1, kind='motion', enforce_limit=True)[0]
    last_ding = doorbell.history(limit=1, kind='ding', enforce_limit=True)[0]

    return last_ding, last_motion


def run(doorbell):
    # windowSurface = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    # os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"  # edit the x value here to control which display it is on
    # windowSurface = pygame.display.set_mode((3840, 1080), pygame.NOFRAME)  # window spans two displays

    cur_motion_id = None
    cur_ding_id = None
    while True:
        sleep = True
        last_ding, last_motion = get_doorbell_events(doorbell)
        """
        only handling one type of event now but getting two images from it
        """
        # if cur_motion_id != last_motion['id']:
        #     #close last cv2 window
        #     print('new motion event')
        #     try:
        #         doorbell.recording_download(last_motion['id'], filename='./last_motion.mp4', override=True, timeout=180)
        #
        #         cur_motion_id = last_motion['id']
        #         save_frames('./last_motion.mp4', f'./raw_images/motion/', f'{last_motion["created_at"].strftime("%H_%M_%S_%m_%d_%y")}', 5, 1)
        #         cur_motion_path = f'./raw_images/motion/{last_motion["created_at"].strftime("%H_%M_%S_%m_%d_%y")}_0.jpg'
        #         im = Image.open(cur_motion_path)
        #         #############
        #         # cv2.imwrite("content.jpg",im)
        #         # style_path = "/scene_styles/{}.jpg".format(1)
        #         # command = "python3 strotss.py content.jpg {} --weight 0.5 --output /generated_art/out_artwork{}.png --device {}".format(style_path,art_counter, 'cuda:0')
        #         # os.system(command)
        #         # try:
        #         # cv2.close()
        #         # image = cv2.imread('/generated_art/out_artwork{}.png'.format(art_counter))
        #         # resize = ResizeWithAspectRatio(image, width=screen_width)
        #         # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        #         # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        #         # cv2.imshow("window", resize)
        #         # cv2.waitKey(0)
        #         ############
        #         print('Showing motion event')
        #         im.show()
        #     except requests.exceptions.HTTPError as e:
        #         print("HTTPError when downloading")
        #     sleep = False

        if cur_ding_id != last_ding['id']:
            print('new ding event')
            try:
                doorbell.recording_download(last_ding['id'], filename='./last_ding.mp4', override=True, timeout=180)
                media_info = MediaInfo.parse('./last_ding.mp4')
                duration = int(media_info.tracks[0].duration / 1000)

                cur_ding_id = last_ding['id']
                num_frames_saved = save_frames('./last_ding.mp4', './raw_images/ding/', f'{last_ding["created_at"].strftime("%H_%M_%S_%m_%d_%y")}', 1, duration)
                cur_ding_path = f'./raw_images/ding/{last_ding["created_at"].strftime("%H_%M_%S_%m_%d_%y")}_1.jpg'
                cur_scene_path = f'./raw_images/ding/{last_ding["created_at"].strftime("%H_%M_%S_%m_%d_%y")}_{num_frames_saved-1}.jpg'
                # portrait_img = pygame.image.load(cur_ding_path)
                # scene_img = pygame.image.load(cur_scene_path)

                """
                DO style transfer here on each image, the portrait and scene image separately
                and save to accessible directory. Then specify that directory in display.py
                """
                #############
                croped = crop_face(im)
                cv2.imwrite("content.jpg",im)
                style_path = "/face_styles/{}.jpg".format(1)
                command = "python3 strotss.py content.jpg {} --weight 0.5 --output /generated_art/out_artwork{}.png --device {}".format(style_path, art_counter, 'cuda:0')
                os.system(command)
                image = cv2.imread('/generated_art/out_artwork{}.png'.format(art_counter))
                #############

                # print('Showing new images')
                # windowSurface.blit(portrait_img, (0, 0))  # Replace (0, 0) with desired coordinates
                # windowSurface.blit(scene_img, (1920, 0))  # this displays in same pygame window but since the window spans displays it will be in second display

                # pygame.display.flip()

            except requests.exceptions.HTTPError as e:
                print("HTTPError when downloading")
            sleep = False

        # events = pygame.event.get()
        # for event in events:
        #     if event.type == QUIT:
        #         pygame.quit()
        #         sys.exit()

        if sleep:
            print('no new events')
            time.sleep(5)


def main():
    doorbell = sign_in_get_devices()

    run(doorbell)
    # filename = './last_motion.mp4'
    # get_frames(filename, f'{filename[:-4]}_frames', 1, 15)  # 15 images, spaced 1 second apart
    # # if we get more than one image per ding, we could maybe do some other cool art stuff, perhaps warhol style


if __name__ == "__main__":
    main()
