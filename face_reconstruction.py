#!/usr/bin/env python
# -*-coding:utf-8 -*-

""" Design for face reconstruction experiments."""

__author__ = "caozhiyuan"

import pygame
from pygame.locals import *
import numpy as np
np.random.seed(1336)  # for reproducibility

import os
import argparse
import time
import sys


class Run(object):

    def __init__(self):
        super(Run, self).__init__()

        self.interval = 200
        self.stimulate = 1
        self.i = 0
        self.j = 0
        self.k = 0
        self.flag = -1
        self.num = 1
        self.start = time.time() * 1000
        self.last = self.start + 6000
        self.cross_color = [0, 255, 0]
        # self.windowSize = pygame.display.list_modes()[0]
        self.windowSize=[1024,768]
        self.HcrossStart_pos = [self.windowSize[0] / 2 -
                                self.windowSize[0] / 150, self.windowSize[1] / 2]
        self.HcrossEnd_pos = [self.windowSize[0] / 2 +
                              self.windowSize[0] / 150, self.windowSize[1] / 2]
        self.VcrossStart_pos = [self.windowSize[0] / 2,
                                self.windowSize[1] / 2 - self.windowSize[0] / 150]
        self.VcrossEnd_pos = [self.windowSize[0] / 2,
                              self.windowSize[1] / 2 + self.windowSize[0] / 150]
        self.line_width = 3
        # self.color_change= False
        # self.color = time.time()*1000 + 6000

    def do_trial(self, screen, img, background):
        # do_trial, only if interval has been 0.3 seconds since last

        now = time.time() * 1000

        if now - self.last <= self.interval:  # Display the image every interval

            screen.blit(background, [0, 0])
            screen.blit(img.convert(), [screen.get_width(
            ) / 2 - img.get_width() / 2, screen.get_height() / 2 - img.get_height() / 2])

        else:  # Display empty screen every interval
            screen.blit(background, [0, 0])

        pygame.draw.line(
            screen, self.cross_color, self.HcrossStart_pos, self.HcrossEnd_pos, self.line_width)
        pygame.draw.line(
            screen, self.cross_color, self.VcrossStart_pos, self.VcrossEnd_pos, self.line_width)
        pygame.display.flip()

        if now - self.last >= self.interval * 2 and self.stimulate % 5 != 0:  # A trial does not finish, go next loop
            self.last = now
            self.stimulate += 1

            # p = np.random.randint(1, 5)
            # if self.stimulate == p:
            #     self.cross_color = [255, 0, 0]
            #     # self.color_change = True
            # else:
            #     # self.color_change = False
            #     self.cross_color = [0, 255, 0]

        if now - self.last >= 6397:  # A trial has finished, wait 6000ms and go next trial
            if self.stimulate % 5 == 0:
                self.stimulate = 1
            else:
                self.stimulate += 1
            self.last = now
            self.i += 1

    def do_run(self, screen, background, path_list, test_index, record):

        # print 'path_list shape', path_list.shape
        # if self.i == path_list.shape[2]:
        #     self.i = 0  # An actor's all the expressions are presented
        #     self.j += 1  # Present next actor's expressions
        #     if self.j == path_list.shape[1]:
        #         self.j = 0  # A run has finished
        #         self.k += 1  # Next run
        #         if self.k == path_list.shape[0]:
        #             pygame.quit()

        if self.i == len(path_list):
            return True  # A run has finished

        global img

        now = time.time() * 1000
        if now - self.start >= 6000:
            if self.i != self.flag:
                self.flag = self.i
                img_path = path_list[self.i]

                record.write('\n')
                record.write('   %-3d  |' % self.num)
                # is test image
                if test_index[self.i] in [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]:
                    record.write('  YES   | ')
                else:
                    record.write('        | ')

                record.write(img_path)
                record.write('  %d  '%now)
                img = pygame.image.load(img_path)
                self.num += 1

            self.do_trial(screen, img, background)
        else:
            screen.blit(background, [0, 0])
            pygame.draw.line(
                screen, [0, 255, 0], self.HcrossStart_pos, self.HcrossEnd_pos, self.line_width)
            pygame.draw.line(
                screen, [0, 255, 0], self.VcrossStart_pos, self.VcrossEnd_pos, self.line_width)
            pygame.display.flip()
        return False  # A run has not finished


def generate_list(data_path):

    data_list = []
    image_list = []
    for i, image in enumerate(os.listdir(data_path)):
        data_list.append(os.path.join(data_path, image))
        if (i + 1) % nb_expressions == 0:  # An actor's nb_expressions
            image_list.append(data_list)
            data_list = []
    image_list = np.asarray(image_list)
    np.random.shuffle(image_list)  # shuffle the list

    # for actor in image_list:  # shuffle the expressions
    #     np.random.shuffle(actor)

    # if run_index == 1:
    #     # 100 actors for session 1
    #     return image_list[:nb_actors / 2].reshape(nb_runs, -1, nb_expressions)
    # elif run_index == 2:
    #     # 100 actors for session 2
    #     return image_list[-nb_actors / 2:].reshape(nb_runs, -1, nb_expressions)
    # else:
    #     raise ValueError('Invalid session index')
    #     sys.exit(1)
    return image_list


def RandomSampling(data_path, run_index):

    image_list = generate_list(data_path)

    image_list = image_list.reshape(
        (nb_runs, nb_actors / nb_runs, nb_expressions))

    # Randomly select 2 test images
    test_index_1 = np.random.randint(nb_actors / nb_runs)
    test_index_2 = np.random.randint(nb_actors / nb_runs)
    # Make sure that 2 test images are not same
    while test_index_1 == test_index_2:
        test_index_1 = np.random.randint(nb_actors / nb_runs)
        test_index_2 = np.random.randint(nb_actors / nb_runs)

    new_list = []
    new_index = []
    for i in xrange(nb_runs):

        run_list = image_list[i].tolist()
        run_list.append(run_list[test_index_1])
        run_list.append(run_list[test_index_2])
        run_list = np.asarray(run_list).reshape(-1)

        image_index = range(len(run_list))
        np.random.shuffle(image_index)

        # Make sure that 2 test images do not adjacent
        # while abs(image_index.index(test_index) - image_index.index(image_list.shape[1])) == 1:
        #     np.random.shuffle(image_index)

        run_list = run_list[image_index]

        new_list.append(run_list)
        new_index.append(image_index)
    return np.asarray(new_list)[run_index - 1], np.asarray(new_index)[run_index - 1]


def run_session(data_path, run_index, record):
    """For one session.
    10 runs * 88 trials(4*(18 train actors + 2 test actors*2 )=88)"""

    path_list, test_index = RandomSampling(
        data_path, run_index)

    # print path_list.shape

    try:
        pygame.init()
        # windowSize = pygame.display.list_modes()[0]
        windowSize = [1024,768]
        screen = pygame.display.set_mode(windowSize)
        background = pygame.Surface(screen.get_size())
        background.fill([128, 128, 128])

        # cross_color = [0, 255, 0]
        text_size = 40

        text_font = pygame.font.SysFont('SimHei', text_size)
        #text_font = pygame.font.Font(
           # "/Library/Fonts/Arial Unicode.ttf", text_size)

        text1_surface = text_font.render(
            u'您好，欢迎您来参加我们的实验！', True, [0, 0, 0])
        text2_surface = text_font.render(
            u'在下面的实验中，你会在屏幕中央看到一组表情图片', True, [0, 0, 0])
        text3_surface = text_font.render(
            u'请您始终注视图片中央的十字加号', True, [0, 0, 0])
        text4_surface = text_font.render(
            u'请根据表情按键：1快乐 2恐惧 3厌恶 4平静', True, [0, 0, 0])
        text5_surface = text_font.render(
            u'在实验过程中，请您保持头部不要动，谢谢您的配合！', True, [0, 0, 0])
        text6_surface = text_font.render(
            u'如果您准备好了，请按任意键', True, [0, 0, 0])

        Fullscreen = False
        running = True
        hints = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:  # Press SPACE to toggle full screen
                        Fullscreen = not Fullscreen
                        if Fullscreen:
                            screen = pygame.display.set_mode(
                                windowSize, FULLSCREEN, 32)
                            # Set the mouse invisible
                            pygame.mouse.set_visible(False)
                        else:
                            pygame.mouse.set_visible(True)
                            screen = pygame.display.set_mode(
                                windowSize, 0, 32)

                    elif event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_s and hints:  # Start
                        hints = False
                        run = Run()  # Initialize an instance
                        start_time = time.time()
                    elif event.key == K_KP1 or event.key == K_1:
                        record.write(' 1')
                    elif event.key == K_KP2 or event.key == K_2:
                        record.write(' 2')
                    elif event.key == K_KP3 or event.key == K_3:
                        record.write(' 3')
                    elif event.key == K_KP4 or event.key == K_4:
                        record.write(' 4')

            if hints:  # Display hists
                screen.blit(background, [0, 0])
                screen.blit(text1_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3])
                screen.blit(text2_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3 + text_size * 1.5])
                screen.blit(text3_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3 + text_size * 3])
                screen.blit(text4_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3 + text_size * 4.5])
                screen.blit(text5_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3 + text_size * 6])
                screen.blit(text6_surface, [screen.get_width() / 2 -
                                            text2_surface.get_width() / 2, screen.get_height() / 3 + text_size * 7.5])
                pygame.display.flip()

            if not hints:  # Do a run
                done = run.do_run(screen=screen, background=background,
                                  path_list=path_list, test_index=test_index, record=record)
                if done:
                    running = False
        print 'Done after %s seconds' % (time.time() - start_time,)
        pygame.quit()

    except Exception, e:
        raise Exception, e
    finally:
        pygame.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Face reconstruction experiments')

    # Positional arguments
    parser.add_argument('folder', help='Where to save the images')
    parser.add_argument('run_index', type=int, help='Which run')

    args = vars(parser.parse_args())

    if not os.path.exists(args['folder']):
        print 'ERROR: Folder does not exist'
        sys.exit(1)

    nb_runs = 10
    nb_trials = 44
    nb_actors = 200
    nb_expressions = 4

    record_path = os.path.join(os.path.split(args['folder'])[0],
                               'record_run_%d.txt' % args['run_index'])
    print record_path
    with open(record_path, 'w') as record:
        record.write('  No.   |  test  |\n')
        run_session(
            args['folder'],
            args['run_index'],
            record)
