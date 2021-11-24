from ahk import AHK
from random import shuffle
import os
import cv2
import ctypes
import winsound

from imageHandler import *

def line_coords_generator(image):
    image_line_coords = []
    for iterator, line in enumerate(image):
        temp_line_coords = []
        line_start = 0
        is_anterior_black = False
        for i in range(len(line)):
            if is_anterior_black:
                if line[i] == 0:
                    is_anterior_black = True

                else:
                    temp_line_coords.append([line_start, i])
                    is_anterior_black = False
            else:
                if line[i] == 0:
                    line_start = i
                    is_anterior_black = True
                else:
                    is_anterior_black = False

        image_line_coords.append([iterator, temp_line_coords.copy()])

    return image_line_coords


def generate_ahk(image, line_step=1, shuffled = False):
    ahk = AHK()
    init_y, init_x  = ahk.get_mouse_position()



    image_order = [i for i in range(0, len(image), line_step)]
    if shuffled:
        shuffle(image_order)

    content = f"ListLines Off\nProcess, Priority, , A\nSetBatchLines, -1\nSetDefaultMouseSpeed, 0\nSetKeyDelay, 1\nSetMouseDelay, 1\n#SingleInstance Force\nf3::\nPause\nsuspend\nreturn\nf4::ExitApp\nf2::\n"
    content += "Click, Up\n"
    for i in image_order:
        for trace in image[i][1]:
            content += f"MouseMove, {init_y + trace[0]}, {init_x + image[i][0]}, 0\n"
            content += "Click, Down\n"
            content += f"MouseMove, {init_y + trace[1]}, {init_x + image[i][0]}, 0\n"
            content += "Click, Up\n"

    content += "ExitApp\n"
    
    with open("desenho.ahk", "w") as f:
        f.write(content)
            
def generate_contours_ahk(image_traces, position_skip = 1):
    ahk = AHK()

    # image_traces = np.array(sorted(image_traces, key=len, reverse=True))
    image_traces = sorted(image_traces, key=len, reverse=True)

    init_y, init_x  = ahk.get_mouse_position()
    content = f"ListLines Off\nProcess, Priority, , A\nSetBatchLines, -1\nSetDefaultMouseSpeed, 0\nSetKeyDelay, 1\nSetMouseDelay, 1\n#SingleInstance Force\nf3::\nPause\nsuspend\nreturn\nf4::ExitApp\nf2::\n"

    for trace in image_traces:
        content += f"MouseMove, {init_y + trace[0][0][0]}, {init_x + trace[0][0][1]}, 0\n"
        content += "Click, Down\n"
        for position in range(0, len(trace), position_skip):
            content += f"MouseMove, {init_y + trace[position][0][0]}, {init_x + trace[position][0][1]}, 0\n"
        content += "Click, Up\n"

    content += "ExitApp\n"
    
    with open("desenho.ahk", "w") as f:
        f.write(content)



image = resizeCalc(get_from_clipboard(), (600,800))

desenho_cagado = True

if desenho_cagado:
    canny, image_contours = make_contours(image)
    generate_contours_ahk(image_contours, position_skip=1)
else:
    image = make_threshold(image)
    generate_ahk(line_coords_generator(image), line_step=2, shuffled=True)




ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
winsound.Beep(1000, 300)
winsound.Beep(1500, 300)
os.system("desenho.ahk")
winsound.Beep(1500, 300)
winsound.Beep(1000, 300)