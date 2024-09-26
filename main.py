import time
import PIL.ImageShow
import tkinter as tk
import customtkinter as ctk
import os
from os import walk
from PIL import Image, ImageDraw
import configparser
from datetime import datetime
import numpy as np
from widgets import Widgets
from area_manager import AreaManager
import threading


def slider_update(slider, slider_name, label):
    edit = False
    value = slider.get()
    if slider_name == 'red':
        label.configure(text=int(value))
        edit = True
    if slider_name == 'green':
        label.configure(text=int(value))
        edit = True
    if slider_name == 'blue':
        label.configure(text=int(value))
        edit = True
    if slider_name == 'tolerance':
        label.configure(text=int(value))
        edit = True
    if slider_name == 'all_slider':
        label.configure(text=int(value))
        edit = True

    if slider_name == 'width':
        value = area_manager.change_size(int(value), slider_name)
        slider.set(int(value))
    if slider_name == 'height':
        value = area_manager.change_size(int(value), slider_name)
        slider.set(int(value))

    if edit:
        main.edit_image(main.selected_image, save=False)
    else:
        area_manager.draw_areas()
    return


def change_slider_value(number):
    if number == 0 or number == 1:
        slider = area_manager.selected_area['b_slider']
        label = area_manager.selected_area['b_label']
        value = slider.get()
        if number == 0:
            value = int(value - 1)
        else:
            value = int(value + 1)

    if number == 2 or number == 3:
        slider = area_manager.selected_area['g_slider']
        label = area_manager.selected_area['g_label']
        value = slider.get()
        if number == 2:
            value = int(value - 1)
        else:
            value = int(value + 1)

    if number == 4 or number == 5:
        slider = area_manager.selected_area['r_slider']
        label = area_manager.selected_area['r_label']
        value = slider.get()
        if number == 4:
            value = int(value - 1)
        else:
            value = int(value + 1)

    if number == 10 or number == 11:
        slider = area_manager.selected_area['all_slider']
        label = area_manager.selected_area['all_label']
        value = slider.get()
        if number == 10:
            value = int(value - 1)
        else:
            value = int(value + 1)

    if number == 12 or number == 13:
        slider = area_manager.selected_area['t_slider']
        label = area_manager.selected_area['t_label']
        value = slider.get()
        if number == 12:
            value = int(value - 1)
        else:
            value = int(value + 1)

    if value < 0:
        value = int(0)
    elif value > 255:
        value = int(255)

    slider.set(value)
    label.configure(text=str(value))

    main.edit_image(main.selected_image, save=False)
    return


def changes_default_image():
    main.display_default_image = not main.display_default_image

    if not main.display_default_image:
        area_manager.image = main.edited_image

    else:
        area_manager.image = main.selected_image
    area_manager.draw_areas()

    return


def advanced_colors():
    event = area_manager.event_mem
    area_manager.selected_area['advanced_colors_on'] = not area_manager.selected_area['advanced_colors_on']
    area_manager.select_area(event)

    main.edit_image(main.selected_image, save=False)
    return


def change_color_side():
    area_manager.selected_area['default_side'] = not area_manager.selected_area['default_side']

    slider = area_manager.selected_area['r_slider']
    change_slider_color_side(slider, color='red')

    slider = area_manager.selected_area['g_slider']
    change_slider_color_side(slider, color='green')

    slider = area_manager.selected_area['b_slider']
    change_slider_color_side(slider, color='blue')

    slider = area_manager.selected_area['all_slider']
    change_slider_color_side(slider, color='lightblue')

    main.edit_image(main.selected_image, save=False)
    return


def change_slider_color_side(slider, color):
    if not area_manager.selected_area['default_side']:
        fg_color = '#AAB0AB'
        progress_color = color
    else:
        fg_color = color
        progress_color = '#AAB0AB'
    slider.configure(fg_color=fg_color,
                     progress_color=progress_color)

    return


def clear_borders():
    area_manager.hide_borders = not area_manager.hide_borders
    if area_manager.hide_borders:
        widgets.buttons[5].configure(fg_color='#1F6AA5')
    else:
        widgets.buttons[5].configure(fg_color='white')

    area_manager.forgot_areas()
    area_manager.draw_areas()
    return


def enable_sliders(area, x, y):
    area["t_slider"].place(x=x + 280, y=y - 30)
    area["t_label"].place(x=x + 380, y=y - 60)
    area["t_slider"].configure(state='normal')

    # plus / minus buttons for tolerance
    for i in range(2):
        k = 16 + i * 2
        j = i + 8
        enable_buttons(k, j)

    # show sliders if advanced colors
    if area["advanced_colors_on"]:
        area['advanced_colors'].select()

        area["r_slider"].place(x=x, y=y - 60)
        area["g_slider"].place(x=x, y=y - 30)
        area["b_slider"].place(x=x, y=y)

        area["r_label"].place(x=x + 225, y=y - 66)
        area["g_label"].place(x=x + 225, y=y - 36)
        area["b_label"].place(x=x + 225, y=y - 6)

        area["r_slider"].configure(state='normal')
        area["g_slider"].configure(state='normal')
        area["b_slider"].configure(state='normal')

        # plus / minus buttons
        for i in range(6):
            k = i * 2
            j = i
            enable_buttons(k, j)

    else:
        area['advanced_colors'].deselect()
        area["all_label"].place(x=x + 225, y=y - 36)
        area["all_slider"].place(x=x, y=y - 30)
        area["all_slider"].configure(state='normal')

        # plus / minus buttons for all slider
        for i in range(2):
            k = 12 + i * 2
            j = i + 6
            enable_buttons(k, j)

    return


def enable_buttons(k, j):
    x1 = widgets.plus_minus_location[k]
    y1 = widgets.plus_minus_location[k + 1]
    widgets.plus_minus_buttons[j].place(x=x1, y=y1)
    widgets.plus_minus_buttons[j].configure(state='normal')

    return


def clear_pixels_function(amount, image, color):
    width = image.width
    height = image.height

    if amount == 'None':
        return

    pixels = image.load()
    amount = int(amount)
    for i in range(width):
        for k in range(height):
            count = 0
            if i != 0 and k != 0 and i + 1 != width and k + 1 != height:
                if (k + 1) % 3 == 0 and (i + 1) % 3 == 0:
                    if pixels[i + 1, k] != color:
                        count += 1
                    if pixels[i - 1, k] != color:
                        count += 1
                    if pixels[i, k + 1] != color:
                        count += 1
                    if pixels[i, k - 1] != color:
                        count += 1
                    if pixels[i + 1, k + 1] != color:
                        count += 1
                    if pixels[i - 1, k - 1] != color:
                        count += 1
                    if pixels[i - 1, k + 1] != color:
                        count += 1
                    if pixels[i + 1, k - 1] != color:
                        count += 1

                    if count < amount:
                        pixels[i, k] = color
                        pixels[i + 1, k] = color
                        pixels[i - 1, k] = color
                        pixels[i, k + 1] = color
                        pixels[i, k - 1] = color
                        pixels[i + 1, k + 1] = color
                        pixels[i - 1, k - 1] = color
                        pixels[i - 1, k + 1] = color
                        pixels[i + 1, k - 1] = color

    return


def log_save_data(image, edit_time, name):
    y_ratio = image.height / main.selected_image.height
    x_ratio = image.width / main.selected_image.width

    file_path = f'{name}_{edit_time}.log'
    with open(f'Pictures/logs/{file_path}', 'w') as file:
        for i, area in enumerate(area_manager.areas):
            file.write(f'Area {i + 1}')

            file.write("\n")
            file.write("x1 = ")
            file.write(str(area['area']))

            file.write("\n")
            file.write("RGBt = ")
            file.write(str(area['r_slider'].get()))
            file.write(" : ")
            file.write(str(area['g_slider'].get()))
            file.write(" : ")
            file.write(str(area['b_slider'].get()))
            file.write(" : ")
            file.write(str(area['t_slider'].get()))
            file.write("\n")

    return


def add_point():
    area = area_manager.selected_area["area"]
    x1 = area[0][0]
    y1 = area[0][1]
    if len(area) < 5:
        x2 = area[3][0]
        y2 = area[3][1]
    else:
        lenght = len(area) - 1
        x2 = area[lenght][0]
        y2 = area[lenght][1]

    dif_x = (x2 - x1) / 2 + x1 + 10
    dif_y = (y2 - y1) / 2 + y1 + 10

    area_manager.selected_area["area"].append((dif_x, dif_y))

    # add new button to the point
    i = len(area_manager.selected_area["corner_button"])
    button = widgets.create_button(x=0,
                                   y=0,
                                   width=6,
                                   height=6,
                                   text='',
                                   command=lambda number=i: active_corner(number),
                                   hover_color='White',
                                   bg_color='transparent',
                                   fg_color='#1F6AA5',
                                   save=False)
    button.bind("<B1-Motion>", area_manager.drag_corner)
    button.bind("<ButtonRelease-1>", corner_button_place)
    button.configure(state='normal',
                     corner_radius=0,
                     border_width=0,
                     border_spacing=0)

    x = area[i][0] + 15
    y = area[i][1] + 15
    button.place(x=x, y=y, anchor='center')

    area_manager.selected_area['corner_button'].append(button)
    area_manager.draw_areas()

    return


def active_corner(number):
    area_manager.select_corner = True
    area_manager.corner_number = number
    update_button.configure(state='normal')

    # change corner color
    for i in range(len(area_manager.selected_area["corner_button"])):
        area_manager.selected_area["corner_button"][i].configure(fg_color='#1F6AA5')

    area_manager.selected_area["corner_button"][number].configure(fg_color='white')

    # enable entries
    x_entry.configure(state='normal')
    text = f'X : {str(int(area_manager.selected_area["area"][number][0]))}'
    x_entry.configure(placeholder_text=text)

    y_entry.configure(state='normal')
    text = f'Y : {str(int(area_manager.selected_area["area"][number][1]))}'
    y_entry.configure(placeholder_text=text)

    return


def corner_button_place(event):
    area_manager.dragging_corner = False

    area_manager.corner_dif_x = 0
    area_manager.corner_dif_y = 0
    for i in range(len(area_manager.selected_area["area"])):
        x = area_manager.selected_area["area"][i][0]
        y = area_manager.selected_area["area"][i][1]

        area_manager.selected_area["corner_button"][i].place(x=x + 15, y=y + 15, anchor='center')

    return


def update_entry():
    try:
        x = int(x_entry.get())
    except:
        x = ''

    try:
        y = int(y_entry.get())
    except:
        y = ''

    if x == '':
        x = area_manager.selected_area["area"][area_manager.corner_number][0]
    if y == '':
        y = area_manager.selected_area["area"][area_manager.corner_number][1]

    point = tuple((x, y))
    area_manager.selected_area["area"][area_manager.corner_number] = point
    area_manager.draw_areas()

    return


# get pictures from directory
def refresh_folder():
    # get pictures from folder
    path = "Pictures"
    _, _, files = next(os.walk(path))
    image_amount = len(files)
    image_names = next(walk(path), (None, None, []))[2]

    return image_amount, image_names


def zoom_image(event):
    # no work... won't work ever
    return
    width = area_manager.image.width
    height = area_manager.image.height
    x1 = area_manager.zoom_x1
    y1 = area_manager.zoom_y1
    x2 = area_manager.zoom_x2
    y2 = area_manager.zoom_y2

    # Get mouse position
    mouse_x = event.x
    mouse_y = event.y

    # Normalize mouse position to [0, 1] range
    norm_mouse_x = (mouse_x - x1) / (x2 - x1)
    norm_mouse_y = (mouse_y - y1) / (y2 - y1)

    # Calculate zoom factor
    zoom_factor = 1.05 if event.delta < 0 else 0.95

    # Calculate new width and height based on zoom factor
    new_width = (x2 - x1) * zoom_factor
    new_height = (y2 - y1) * zoom_factor

    # Calculate new x1, y1, x2, y2 based on mouse position
    new_x1 = mouse_x - norm_mouse_x * new_width
    new_x2 = mouse_x + (1 - norm_mouse_x) * new_width
    new_y1 = mouse_y - norm_mouse_y * new_height
    new_y2 = mouse_y + (1 - norm_mouse_y) * new_height

    # Ensure new coordinates stay within image boundaries
    if new_x1 < 0:
        new_x1 = 0
        new_x2 = new_width
    if new_y1 < 0:
        new_y1 = 0
        new_y2 = new_height
    if new_x2 > width:
        new_x2 = width
        new_x1 = width - new_width
    if new_y2 > height:
        new_y2 = height
        new_y1 = height - new_height

    if new_x1 < 0:
        new_x1 = 0
    if new_y1 < 0:
        new_y1 = 0
    if new_x2 > width:
        new_x2 = width
    if new_y2 > height:
        new_y2 = height

    # Update zoom parameters if valid
    if new_x1 < new_x2 and new_y1 < new_y2:
        area_manager.zoom_x1 = new_x1
        area_manager.zoom_y1 = new_y1
        area_manager.zoom_x2 = new_x2
        area_manager.zoom_y2 = new_y2

    area_manager.selected_area = None
    area_manager.forgot_areas()

    # Redraw image
    area_manager.draw_areas()

    return


class MAIN:
    def __init__(self):
        self.root = ctk.CTk()

        self.width = 1024
        self.height = 900
        self.center = None

        self.selected_image_name = None
        self.full_image = None
        self.selected_image = None
        self.edited_image = None
        self.display_default_image = False

        self.background_color = (255, 0, 200)

    def initialize(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')

        main.width = int(config.get('System', 'width'))
        main.height = int(config.get('System', 'height'))
        full_screen = config.getboolean('System', 'full_screen')

        # System settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # app frame
        # self.root = ctk.CTk()
        self.root.update_idletasks()

        self.root.geometry(str(main.width) + 'x' + str(main.height))
        self.root.resizable(False, False)
        self.root.title("Transparent Images")

        if full_screen:
            main.width = self.root.winfo_screenwidth()
            main.height = self.root.winfo_screenheight()
            self.root.after(0, lambda: self.root.state('zoomed'))

        return

    def changes_background(self):
        if self.background_color == (0, 0, 0):
            self.background_color = (255, 0, 200)
            background_button.configure(fg_color='#FF00C8', hover_color='#FF00C8')
        elif self.background_color == (255, 0, 200):
            self.background_color = (255, 255, 255)
            background_button.configure(fg_color='#FFFFFF', hover_color='#FFFFFF')
        else:
            self.background_color = (0, 0, 0)
            background_button.configure(fg_color='#000000', hover_color='#000000')

        self.edit_image(self.selected_image, save=False)
        return

    # Create side buttons with pictures
    def image_buttons(self, image_amount, image_names):
        size = (self.height * 0.1, self.height * 0.1)
        y = - size[1]
        k = self.width - (size[0] * 2) - 30
        for i in range(image_amount):
            if i % 2 == 0:
                x = k
                y = y + size[1] + 15
            else:
                x = k + size[0] + 15

            image = ctk.CTkImage(dark_image=Image.open("Pictures/" + str(image_names[i])),
                                 size=size)

            # download button
            select = ctk.CTkButton(self.root,
                                   width=0,
                                   height=0,
                                   border_width=0,
                                   text="",
                                   command=lambda name=image_names[i]: main.select_image(name),
                                   image=image,
                                   hover_color="White",
                                   bg_color='transparent')

            select.place(x=x, y=y)

        return

    # select image
    def select_image(self, name):
        area_manager.forgot_areas()

        # clear old areas
        area_manager.areas = []
        for i in range(len(widgets.slider_label)):
            widgets.slider_label[i].configure(text=int(0))
            widgets.sliders[i].set(int(0))

        # make selected image editable
        image = Image.open("Pictures/" + str(name))
        image = image.convert("RGB")
        self.selected_image_name = name[:-4]
        self.full_image = image

        # resize image to maximum
        image_width = image.width
        image_height = image.height
        ratio = image_width / image_height

        # max image size
        max_width = self.width * 0.85
        max_height = max_width / ratio

        if max_height >= self.height * 0.80:
            height = self.height * 0.80
            width = height * ratio
        else:
            width = max_width
            height = max_height

        width = int(width)
        height = int(height)

        image = image.resize((width, height))

        # selected image
        self.selected_image = image
        self.edited_image = image
        area_manager.zoom_x1 = 0
        area_manager.zoom_y1 = 0
        area_manager.zoom_x2 = image.width
        area_manager.zoom_y2 = image.height

        area_manager.image = image

        image = ctk.CTkImage(dark_image=image,
                             size=(width, height))

        label.configure(image=image)

        self.center = max_width - width
        self.center = int(self.center / 2)
        label.place(x=self.center, y=15)

        # create default area
        self.create_area(init=True)
        return

    # create editable area
    def create_area(self, init):
        # create area
        if init:
            area = [(0, 0),
                    (0, self.selected_image.height),
                    (self.selected_image.width, self.selected_image.height),
                    (self.selected_image.width, 0)]
        else:
            area = [(0, 0),
                    (50, 0),
                    (100, 0),
                    (100, 50),
                    (100, 100),
                    (50, 100),
                    (0, 100),
                    (0, 50)]

        # allow advanced colors
        advanced_colors_switch = widgets.create_switch(x=0,
                                                       y=0,
                                                       command=advanced_colors,
                                                       save=False)

        # switch for color change
        change_color_switch = widgets.create_switch(x=0,
                                                    y=0,
                                                    command=change_color_side,
                                                    save=True)

        all_slider, all_label = widgets.create_slider(color='lightblue', width=200, to=255, slider_name="all_slider")
        r_slider, r_label = widgets.create_slider(color='red', width=200, to=255, slider_name="red")
        g_slider, g_label = widgets.create_slider(color='green', width=200, to=255, slider_name="green")
        b_slider, b_label = widgets.create_slider(color='blue', width=200, to=255, slider_name="blue")
        t_slider, t_label = widgets.create_slider(color='lightblue', width=200, to=255, slider_name="tolerance")

        width_slider, width_label = widgets.create_slider(color='gray', width=200, to=100, slider_name="width")
        height_slider, height_label = widgets.create_slider(color='gray', width=200, to=100, slider_name="height")

        # create + - buttons for sliders
        y = main.height * 0.95 + 31
        var = 225
        x = main.width * 0.05 + var - 20
        for i in range(6):
            if i % 2 == 0:
                y -= 30
                x -= var
            else:
                x += var
            button = widgets.create_button(x=x,
                                           y=y,
                                           width=15,
                                           height=15,
                                           text='',
                                           command=lambda number=i: change_slider_value(number),
                                           hover_color='White',
                                           bg_color='transparent',
                                           fg_color='#1F6AA5',
                                           save=False)

            widgets.plus_minus_buttons.append(button)
            widgets.plus_minus_location.append(x)
            widgets.plus_minus_location.append(y)
            button.place_forget()

        # create buttons for tolerance and all color sliders
        y += 31
        x -= 225
        for i in range(4):
            if i == 1:
                x += 225
            elif i == 2:
                x += 55
            elif i == 3:
                x += 225
            button = widgets.create_button(x=x,
                                           y=y,
                                           width=15,
                                           height=15,
                                           text='',
                                           command=lambda number=i + 10: change_slider_value(number),
                                           hover_color='White',
                                           bg_color='transparent',
                                           fg_color='#1F6AA5',
                                           save=False)

            widgets.plus_minus_buttons.append(button)
            widgets.plus_minus_location.append(x)
            widgets.plus_minus_location.append(y)
            button.place_forget()

        # add new area point
        add_point_button = widgets.create_button(x=x,
                                                 y=y,
                                                 width=55,
                                                 height=25,
                                                 text='add',
                                                 command=add_point,
                                                 hover_color='White',
                                                 bg_color='transparent',
                                                 fg_color='#1F6AA5',
                                                 save=False)

        add_point_button.place_forget()

        # create corner buttons
        corner_button = []
        for i in range(len(area)):
            button = widgets.create_button(x=x,
                                           y=y,
                                           width=6,
                                           height=6,
                                           text='',
                                           command=lambda number=i: active_corner(number),
                                           hover_color='White',
                                           bg_color='transparent',
                                           fg_color='#1F6AA5',
                                           save=False)
            button.bind("<B1-Motion>", area_manager.drag_corner)
            button.bind("<ButtonRelease-1>", corner_button_place)
            button.place_forget()
            corner_button.append(button)

        new_area = {
            "area": area,
            "corner_button": corner_button,

            "advanced_colors": advanced_colors_switch,
            "advanced_colors_on": False,

            "all_label": all_label,
            "r_label": r_label,
            "g_label": g_label,
            "b_label": b_label,
            "t_label": t_label,

            "all_slider": all_slider,
            "r_slider": r_slider,
            "g_slider": g_slider,
            "b_slider": b_slider,
            "t_slider": t_slider,

            "color_switch": change_color_switch,
            "default_side": True,

            "width_slider": width_slider,
            "height_slider": height_slider,

            "add_button": add_point_button
        }

        old_areas = area_manager.areas

        area_manager.areas = []
        area_manager.areas.append(new_area)
        for i in range(len(old_areas)):
            area_manager.areas.append(old_areas[i])

        area_manager.draw_areas()
        return

    def edit_image(self, image, save):
        edited_image = image.copy()
        original_image = self.selected_image.copy()

        original_image_array = np.array(original_image)
        edited_image_array = np.array(edited_image)

        selected_area = area_manager.selected_area

        # create mask for checking which pixels are already modified
        modified_mask = np.zeros(edited_image_array.shape[:2], dtype=bool)

        for i, area in enumerate(area_manager.areas):
            mask = Image.new('L', original_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.polygon(selected_area['area'], outline=1, fill=1)
            mask_array = np.array(mask)

            if area == area_manager.selected_area:
                if selected_area['advanced_colors_on']:
                    red = selected_area['r_slider'].get()
                    green = selected_area['g_slider'].get()
                    blue = selected_area['b_slider'].get()
                else:
                    red = selected_area['all_slider'].get()
                    green = selected_area['all_slider'].get()
                    blue = selected_area['all_slider'].get()

                tolerance = selected_area['t_slider'].get()

                # check edition color
                if save:
                    color = (255, 255, 255, 0)
                else:
                    color = self.background_color

                threshold = np.array([red, green, blue])
                original_image_array_init = original_image_array[:, :, :3].astype(np.int16)

                condition = (
                        (mask_array == 1) &
                        (original_image_array[:, :, :3] <= threshold).all(axis=-1) &
                        (np.abs(original_image_array_init[:, :, 0] - original_image_array_init[:, :, 1]) <= tolerance) &
                        (np.abs(original_image_array_init[:, :, 1] - original_image_array_init[:, :, 2]) <= tolerance) &
                        (np.abs(original_image_array_init[:, :, 0] - original_image_array_init[:, :, 2]) <= tolerance) &
                        ~modified_mask
                )

                # Apply color only where the condition is met and within the selected area
                original_image_array[condition] = color

                # Ensure that the areas not meeting the condition are set back to original image values
                original_image_array[(mask_array == 1) & ~condition] \
                    = original_image_array[(mask_array == 1) & ~condition]

            # Update the modified mask to include the selected area
            modified_mask[mask_array == 1] = True
            edited_image = Image.fromarray(original_image_array)

        width = edited_image.width
        height = edited_image.height
        edited_image = edited_image.resize((width, height))

        self.edited_image = edited_image
        area_manager.image = edited_image
        area_manager.draw_areas()

    # edit image
    def edit_image_original(self, image, save):
        self.display_default_image = False
        original_image = image.copy()

        # get image real size
        if save:
            y_ratio = image.height / self.selected_image.height
            x_ratio = image.width / self.selected_image.width
        else:
            y_ratio = 1
            x_ratio = 1

        # create image array where to put new data
        image_array = np.array(original_image)

        # create mask for checking which pixels are already modified
        modified_mask = np.zeros(image_array.shape[:2], dtype=bool)

        # get values from all areas
        for i, area in enumerate(area_manager.areas):
            # make mask image to check area
            mask = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.polygon(area['area'], outline=1, fill=1)
            mask_array = np.array(mask)

            # get slider data
            if area['advanced_colors_on']:
                red = area['r_slider'].get()
                green = area['g_slider'].get()
                blue = area['b_slider'].get()
            else:
                red = area['all_slider'].get()
                green = area['all_slider'].get()
                blue = area['all_slider'].get()

            tolerance = area['t_slider'].get()

            # update area ratio
            for k in range(len(area["area"])):
                point = list(area["area"][k])
                point[0] *= x_ratio
                point[1] *= y_ratio
                point = tuple(point)
                area["area"][k] = point

            # check edition color
            if save:
                color = (255, 255, 255, 0)
            else:
                color = self.background_color

            threshold = np.array([red, green, blue])

            # calculation does not work without this
            image_array_init = image_array[:, :, :3].astype(np.int16)

            if area['default_side']:
                condition = ((mask_array == 1) &
                             (image_array[:, :, :3] <= threshold).all(axis=-1) &
                             (np.abs(image_array_init[:, :, 0] - image_array_init[:, :, 1]) <= tolerance) &
                             (np.abs(image_array_init[:, :, 1] - image_array_init[:, :, 2]) <= tolerance) &
                             (np.abs(image_array_init[:, :, 0] - image_array_init[:, :, 2]) <= tolerance) &
                             ~modified_mask)

            else:
                condition = ((mask_array == 1) & (image_array >= threshold).all(axis=-1) &
                             (np.abs(image_array_init[:, :, 0] - image_array_init[:, :, 1]) <= tolerance) &
                             (np.abs(image_array_init[:, :, 1] - image_array_init[:, :, 2]) <= tolerance) &
                             (np.abs(image_array_init[:, :, 0] - image_array_init[:, :, 2]) <= tolerance) &
                             ~modified_mask)

            # update image array to color
            image_array[condition] = color

            # condition for pixel modified
            condition = (mask_array == 1)
            modified_mask[condition] = True

            # update area ratio to normal
            if save:
                for k in range(len(area["area"])):
                    point = list(area["area"][k])
                    point[0] /= x_ratio
                    point[1] /= y_ratio
                    point = tuple(point)
                    area["area"][k] = point

        if save:
            # make edited image from image array
            saved_image = Image.fromarray(image_array)

            # clear single pixels
            amount = widgets.combo_box[0].get()
            clear_pixels_function(amount, saved_image, color)

            return saved_image

        # make edited image from image array
        edited_image = Image.fromarray(image_array)

        # clear single pixels
        amount = widgets.combo_box[0].get()
        clear_pixels_function(amount, edited_image, color)

        width = edited_image.width
        height = edited_image.height
        edited_image = edited_image.resize((width, height))

        self.edited_image = edited_image
        area_manager.image = edited_image
        area_manager.draw_areas()
        return

    def save_image(self):
        area_manager.forgot_areas()
        area_manager.selected_area = None
        area_manager.draw_areas()
        self.root.update()

        image = self.full_image
        image = image.convert("RGBA")

        # edit image
        image = self.edit_image(image, save=True)
        # get time
        edit_time = datetime.now().time()
        edit_time = str(edit_time)
        edit_time = edit_time.replace(':', '-')
        edit_time = edit_time[:8]

        # get time
        name = self.selected_image_name

        # log data
        log_save_data(image, edit_time, name)

        image.save(f'./Pictures/{name}_{edit_time}.png', "PNG")
        save_button.configure(text='Saved', state='disabled')

        # refresh side pictures
        image_amount, image_names = refresh_folder()
        main.image_buttons(image_amount, image_names)

        return


if __name__ == '__main__':
    # initialize
    main = MAIN()
    widgets = Widgets(main, slider_update)

    main.initialize()
    main.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    # make label for main image
    label = ctk.CTkLabel(main.root, text="")
    label.pack()
    area_manager = AreaManager(main, widgets, label, enable_sliders, enable_buttons)

    # get images from directory
    image_amount, image_names = refresh_folder()

    # create side buttons
    main.image_buttons(image_amount, image_names)

    # default position
    y = main.height * 0.95
    x = main.width * 0.05

    x += 550
    y -= 45
    # create edit button
    edit_button = widgets.create_button(x, y,
                                        width=55,
                                        height=50,
                                        text="Edit",
                                        command=lambda save=False: main.edit_image(main.selected_image, save=False),
                                        hover_color="White",
                                        bg_color='transparent',
                                        fg_color='#1F6AA5',
                                        save=True)

    # create clear pixels
    widgets.create_combo_box(x, y)

    x += 100
    # create area button
    area_button = widgets.create_button(x=x,
                                        y=y,
                                        width=55,
                                        height=50,
                                        text='Area',
                                        command=lambda init=False: main.create_area(init),
                                        hover_color="White",
                                        bg_color='transparent',
                                        fg_color='#1F6AA5',
                                        save=True)

    # Bind mouse events to the label
    label.bind("<Button-1>", area_manager.select_area)
    label.bind("<B1-Motion>", area_manager.drag_area)
    label.bind("<MouseWheel>", zoom_image)

    y -= 35
    x += 60
    # create delete area button
    delete = widgets.create_button(x=x,
                                   y=y,
                                   width=55,
                                   height=25,
                                   text='Delete',
                                   command=area_manager.delete_area,
                                   hover_color="White",
                                   bg_color='transparent',
                                   fg_color='#1F6AA5',
                                   save=True)

    y += 35
    # create background button
    background_button = widgets.create_button(x, y,
                                              width=22,
                                              height=22,
                                              text="",
                                              command=main.changes_background,
                                              hover_color='#FF00C8',
                                              bg_color='transparent',
                                              fg_color='#FF00C8',
                                              save=True)

    y += 28
    # create default image button
    default_image = widgets.create_button(x, y,
                                          width=22,
                                          height=22,
                                          text="",
                                          command=changes_default_image,
                                          hover_color='white',
                                          bg_color='transparent',
                                          fg_color='#1F6AA5',
                                          save=True)

    x += 27
    y -= 28
    # clear area borders
    clear_borders = widgets.create_radio_button(x, y,
                                                width=22,
                                                height=22,
                                                text="",
                                                command=clear_borders,
                                                hover_color='white',
                                                fg_color='blue',
                                                save=True)

    x += 100
    # create save button
    save_button = widgets.create_button(x, y,
                                        width=55,
                                        height=50,
                                        text="Save",
                                        command=main.save_image,
                                        hover_color="White",
                                        bg_color='transparent',
                                        fg_color='#1F6AA5',
                                        save=True)

    x += 125
    y -= 20
    y_entry = widgets.create_entry(x, y, text='', save=True)
    y -= 30
    x_entry = widgets.create_entry(x, y, text='', save=True)

    x += 40
    y -= 13
    update_button = widgets.create_button(x, y,
                                          width=55,
                                          height=55,
                                          text="Update",
                                          command=update_entry,
                                          hover_color="White",
                                          bg_color='transparent',
                                          fg_color='#1F6AA5',
                                          save=True)

    # run app
    main.root.mainloop()
