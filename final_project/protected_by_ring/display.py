import pygame
from pygame.locals import *
import os
import sys
import time


def display_images():
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"  # edit the x value here to control which display it is on
    windowSurface = pygame.display.set_mode((3840, 1080), pygame.NOFRAME)  # window spans two displays

    while True:
        # adjust these to match up with model output
        latest_images = get_latest_images('/Desktop/dolly_moun/generated_art/')
        portrait_img = pygame.image.load(latest_images[0])
        scene_img = pygame.image.load(latest_images[1])

        windowSurface.blit(portrait_img, (0, 0))  # Replace (0, 0) with desired coordinates
        windowSurface.blit(scene_img, (1920, 0))  # this displays in same pygame window but since the window spans displays it will be in second display

        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        time.sleep(5)


def get_latest_images(dirpath, valid_extensions=('jpg','jpeg','png')):
    """
    Get the latest 2 image files in the given directory
    """

    # get filepaths of all files and dirs in the given dir
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    # filter out directories, no-extension, and wrong extension files
    valid_files = [f for f in valid_files if '.' in f and f.rsplit('.', 1)[-1] in valid_extensions and os.path.isfile(f)]

    if not valid_files:
        raise ValueError("No valid images in %s" % dirpath)

    images = [max(valid_files, key=os.path.getmtime)]
    valid_files.remove(images[0])
    images.append(max(valid_files, key=os.path.getmtime))

    return images


def main():
    display_images()


if __name__ == "__main__":
    main()
