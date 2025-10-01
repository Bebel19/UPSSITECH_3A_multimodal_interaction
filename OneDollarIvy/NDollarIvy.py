#!/usr/bin/env python
#
# $1 gesture recognizer.
# Requires pygame.
#
from dollar import Recognizer
from ivy.ivy import IvyServer
import pygame
import pickle
import time

LEFT = 1
RIGHT = 3

# Raw points for the three example gestures.
circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201), (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264), (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267), (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255), (361, 253), (375, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248), (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204), (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122), (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108), (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105), (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119), (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125), (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129), (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130), (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133), (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162), (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166), (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160), (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156), (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (371, 145), (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115), (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98), (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87), (294, 87), (293, 87), (293, 87)]

class NDollarRecognizer(IvyServer):

    def __init__(self, screen, use_custom=False, file_name=None):
        IvyServer.__init__(self, 'OneDollarIvy')
        self.name = 'OneDollarIvy'
        self.start('127.255.255.255:2010')

        self.screen = screen
        self.background = (200, 200, 200, 255)
        self.font = pygame.font.SysFont('hack', 15)
        self.fontBig = pygame.font.SysFont('hack', 25)
        self.mouseDown = False
        self.mouseButton = False
        self.positions = []

        self.all_types_string = None
        self.recognizer = Recognizer()

        self.extra_trainingPoints = []

        self.sended = False

        if use_custom and file_name is not None:
            self.useCustomTemplate(file_name)
        else:
            self.all_types_string = "Gestures: circle, square, triangle"
            self.recognizer.addTemplate('circle', circlePoints)
            self.recognizer.addTemplate('square', squarePoints)
            self.recognizer.addTemplate('triangle', trianglePoints)

        self.last_name = None
        self.last_index = -1
        self.last_accuracy = 0.0

    def useCustomTemplate(self, file_name):
        self.recognizer = Recognizer()
        with open(file_name, 'rb') as handle:
            custom_training = pickle.load(handle)
        for one_type in custom_training.keys():
            if type(custom_training[one_type][0]) == list:
                for one_data in custom_training[one_type]:
                    self.recognizer.addTemplate(one_type, one_data)
            else:
                self.recognizer.addTemplate(one_type, custom_training[one_type])

            if self.all_types_string is None:
                self.all_types_string = "Gestures: " + one_type
            else:
                self.all_types_string += "," + one_type
        print(self.all_types_string)

    def OnPaint(self, event):
        if event is not None:
            self.mouseButton = event

        if not self.positions:
            return
        (x, y, event_type) = self.positions[-1]

        if event_type == "start":
            self.sended = False

        if event_type == "stop":
            points = [(p[0], p[1]) for p in self.positions]
            if len(points) > 10:
                (index, name, score) = self.recognizer.recognize(points)
                self.last_index = index
                self.last_name = name
                self.last_accuracy = score

                if not self.sended:
                    self.send_msg('OneDollarIvy Recognized=%s Confidence=%2.2f' % (self.last_name, self.last_accuracy))
                    self.sended = True

                if self.mouseButton == RIGHT:
                    self.extra_trainingPoints.append(points)
                    print("training points saved ", len(points))
                    self.mouseButton = None

            else:
                self.last_index = -1
                self.last_name = '(Not enough points - try again!)'
                self.last_accuracy = 0.0

    def draw(self):
        dot_color = (255, 255, 255)

        for position in self.positions:
            (x, y, event_type) = position
            if event_type == "start":
                r = 5
            elif event_type == "stop":
                r = 5
            else:
                r = 2
            pygame.draw.circle(self.screen, dot_color, (x, y), r)

        self.screen.blit(self.font.render("$1_recognizer", True, (0, 0, 0)), (10, 10))
        self.screen.blit(self.font.render(self.all_types_string, True, (0, 0, 0)), (20, 30))
        self.screen.blit(self.font.render("Recognized: %s" % self.last_name, True, (0, 0, 0)), (20, 60))
        self.screen.blit(self.font.render("Gesture accuracy: %2.2f%%" % (self.last_accuracy * 100), True, (0, 0, 0)), (20, 80))

    def quit(self):
        self.stop()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('$1_Recognizer')
    icon = pygame.image.load('./data/ndollars.png')
    pygame.display.set_icon(icon)
    done = False

    NDI = NDollarRecognizer(screen, False, None)
    NDI.OnPaint(None)
    elapsed_time = 0
    
    while not done:
        screen.fill([150, 150, 150])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                NDI.mouseDown = True
                start_time = pygame.time.get_ticks()
                if elapsed_time == 0 :
                    (x, y) = pygame.mouse.get_pos()
                    NDI.positions = [(x, y, 'start')]
                    NDI.OnPaint(event.button)
                    pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEMOTION:
                if NDI.mouseDown:
                    (x, y) = pygame.mouse.get_pos()
                    NDI.positions.append((x, y, 'move'))
                    NDI.OnPaint(None)

            elif event.type == pygame.MOUSEBUTTONUP:
                NDI.mouseDown = False
                elapsed_time = (pygame.time.get_ticks() - start_time)/1000
                print(elapsed_time)
                if elapsed_time > 1:
                    (x, y) = NDI.positions[-1]
                    NDI.positions.append((x, y, 'stop'))
                    NDI.OnPaint(event.button)
                    elapsed_time = 0

        NDI.OnPaint(None)
        NDI.draw()
        pygame.display.flip()
        dt = clock.tick(100)

    pygame.quit()
    NDI.quit()

    if len(NDI.extra_trainingPoints) > 0:
        print("=======Copy below print to put as input=======", end="\n")
        for i, one_template in enumerate(NDI.extra_trainingPoints):
            print("input_{} = ".format(i), end="")
            print(one_template)

