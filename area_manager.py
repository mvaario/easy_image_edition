from PIL import Image, ImageDraw
import customtkinter as ctk


def entry_update(widgets, area, dragging_corner, corner_number):
    for entry in widgets.entry:
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.configure(placeholder_text='')

    if dragging_corner:
        x_avg = area["area"][corner_number][0]
        y_avg = area["area"][corner_number][1]
    else:
        x_avg = 0
        y_avg = 0
        for i in range(len(area["area"])):
            # calculate average position (for entry visuals)
            x_avg += area["area"][i][0]
            y_avg += area["area"][i][1]

        # add middle position to entries
        x_avg = x_avg / len(area["area"])
        y_avg = y_avg / len(area["area"])

    widgets.entry[0].configure(state='normal')
    widgets.entry[0].configure(placeholder_text=f'Y : {int(y_avg)}')

    widgets.entry[1].configure(state='normal')
    widgets.entry[1].configure(placeholder_text=f'X : {int(x_avg)}')

    if not dragging_corner:
        widgets.entry[0].configure(state='disabled')
        widgets.entry[1].configure(state='disabled')

    return


class AreaManager:
    def __init__(self, main, widgets, label, enable_sliders, enable_buttons):
        # import stuff
        self.main = main
        self.label = label
        self.widgets = widgets
        self.enable_sliders = enable_sliders
        self.enable_buttons = enable_buttons

        self.image = None

        # edited areas
        self.selected_area = None
        self.areas = []

        # corner info
        self.dragging_corner = False
        self.select_corner = False
        self.corner_number = None

        # for dragging
        self.dif_x = 0
        self.dif_y = 0
        # for corner drag
        self.corner_dif_x = 0
        self.corner_dif_y = 0

        self.hide_borders = False

        # advanced colors
        self.colors = False
        self.event_mem = None

        # image zoom
        self.zoom_x1 = 0
        self.zoom_x2 = 0
        self.zoom_y1 = 0
        self.zoom_y2 = 0

    def draw_areas(self):
        image_copy = self.image.copy()
        width = image_copy.width
        height = image_copy.height

        # create rectangle
        draw = ImageDraw.Draw(image_copy)

        # Draw all areas
        if not self.hide_borders:
            for area in self.areas:
                if area == self.selected_area:
                    color = "blue"
                    border = 3
                    # update corner buttons
                    if area != self.areas[len(self.areas) - 1]:
                        for i in range(len(area["corner_button"])):
                            if i != self.corner_number or not self.dragging_corner:
                                x = area["area"][i][0] + self.main.center
                                y = area["area"][i][1] + 15
                                area["corner_button"][i].place(x=x, y=y, anchor='center')
                else:
                    color = "lightblue"
                    border = 2

                draw.polygon(area["area"], outline=color, width=border)

        image_copy = image_copy.crop((self.zoom_x1, self.zoom_y1, self.zoom_x2, self.zoom_y2))

        image = ctk.CTkImage(image_copy,
                             size=(width, height))

        self.label.configure(image=image)

        return

    def forgot_areas(self):
        # add buttons to disable
        for i, button in enumerate(self.widgets.buttons):
            if i != 3 and i != 4 and i != 5:
                button.configure(state='disabled')

        self.widgets.combo_box[0].configure(state='disabled')

        for entry in self.widgets.entry:
            entry.configure(state='normal')
            entry.delete(0, 'end')
            entry.configure(placeholder_text='')
            entry.configure(state='disabled')

        for area in self.areas:
            for i in range(len(area["corner_button"])):
                area["corner_button"][i].place_forget()

            area['advanced_colors'].place_forget()
            area["all_label"].place_forget()
            area["all_slider"].place_forget()

            area["r_slider"].place_forget()
            area["g_slider"].place_forget()
            area["b_slider"].place_forget()
            area["t_slider"].place_forget()

            area["r_label"].place_forget()
            area["g_label"].place_forget()
            area["b_label"].place_forget()
            area["t_label"].place_forget()

            area["width_slider"].place_forget()
            area["height_slider"].place_forget()

            area["add_button"].configure(state='disabled')

            # plus / minus buttons
            for i in range(10):
                self.widgets.plus_minus_buttons[i].place_forget()

            for i in range(len(self.widgets.switches)):
                self.widgets.switches[i].place_forget()

            self.selected_area = None

        return

    def select_area(self, event):
        self.dragging_corner = False
        self.select_corner = False
        self.hide_borders = False

        self.event_mem = event
        self.dif_x = 0
        self.dif_y = 0

        self.forgot_areas()

        # get selected area
        for area in self.areas:
            n = len(area["area"])
            inside = False
            p1x, p1y = area["area"][0]
            for i in range(n + 1):
                p2x, p2y = area["area"][i % n]
                if event.y > min(p1y, p2y):
                    if event.y <= max(p1y, p2y):
                        if event.x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (event.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or event.x <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y

            if inside:
                area = area
                break

        y = self.main.height * 0.95
        x = self.main.width * 0.05

        # enable sliders and slider buttons
        self.enable_sliders(area, x, y)


        # enable rest of the buttons
        for i in range(len(self.widgets.buttons)):
            self.widgets.buttons[i].configure(state='normal')

        # enable combo box
        for i in range(len(self.widgets.combo_box)):
            self.widgets.combo_box[i].configure(state='normal')


        area['advanced_colors'].place(x=x - 55, y=y - 85)
        area['advanced_colors'].configure(state='normal')

        area["color_switch"].place(x=x + 90, y=y - 85)
        area["color_switch"].configure(state='normal')

        x += 600
        area["width_slider"].place(x=x + 320, y=y - 45)
        area["height_slider"].place(x=x + 320, y=y - 15)

        area["add_button"].place(x=x + 50, y=y - 80)

        # background size cannot be changed
        if area != self.areas[len(self.areas) - 1]:
            area["width_slider"].configure(state='normal')
            area["height_slider"].configure(state='normal')
            area["add_button"].configure(state='normal')

            # update entries
            entry_update(self.widgets, area, self.dragging_corner, self.corner_number)

            # corner buttons
            for i in range(len(area["corner_button"])):
                area["corner_button"][i].configure(state='normal',
                                                   corner_radius=0,
                                                   border_width=0,
                                                   border_spacing=0,
                                                   fg_color='#1F6AA5',
                                                   hover_color='white'
                                                   )

        else:
            # disable delete button
            self.widgets.buttons[2].configure(state='disabled')

            area["width_slider"].configure(state='disabled')
            area["height_slider"].configure(state='disabled')

            area["add_button"].configure(state='disabled')

        self.selected_area = area
        self.dif_x = event.x
        self.dif_y = event.y

        self.draw_areas()
        return

    def delete_area(self):
        self.forgot_areas()
        temp = []
        for i, area in enumerate(self.areas):
            if self.selected_area != self.areas[i]:
                temp.append(area)
            elif i + 1 == len(self.areas):
                temp.append(area)

        self.areas = temp
        self.main.edit_image(self.main.selected_image, save=False)

        return

    def drag_area(self, event):
        if self.selected_area == self.areas[len(self.areas) - 1]:
            self.drag_image(event)
            return

        # drag area
        x_movement = event.x - self.dif_x
        y_movement = event.y - self.dif_y
        self.dif_x = event.x
        self.dif_y = event.y

        # checking movement
        for i in range(len(self.selected_area["area"])):
            point = list(self.selected_area["area"][i])
            if point[0] + x_movement < 0:
                x_movement = -point[0]
            if point[1] + y_movement < 0:
                y_movement = -point[1]
            if point[0] + x_movement > self.image.width:
                x_movement = self.image.width - point[0]
            if point[1] + y_movement > self.image.height:
                y_movement = self.image.height - point[1]

        # actual movement (need to be separate since each corner is checked)
        for i in range(len(self.selected_area["area"])):
            point = list(self.selected_area["area"][i])
            point[0] += x_movement
            point[1] += y_movement

            point = tuple(point)
            self.selected_area["area"][i] = point

        # update entries
        entry_update(self.widgets, self.selected_area, self.dragging_corner, self.corner_number)

        self.update_area_sliders()
        self.draw_areas()

        return

    def drag_corner(self, event):
        self.dragging_corner = True
        for i in range(len(self.selected_area["area"])):
            if i == self.corner_number:
                x_movement = event.x - self.corner_dif_x
                y_movement = event.y - self.corner_dif_y
                self.corner_dif_x = event.x
                self.corner_dif_y = event.y

                point = list(self.selected_area["area"][i])
                if point[0] + x_movement < 0:
                    x_movement = -point[0]
                if point[1] + y_movement < 0:
                    y_movement = -point[1]
                if point[0] + x_movement > self.image.width:
                    x_movement = self.image.width - point[0]
                if point[1] + y_movement > self.image.height:
                    y_movement = self.image.height - point[1]

                point[0] += x_movement
                point[1] += y_movement
                point = tuple(point)
                self.selected_area["area"][i] = point
                self.selected_area["corner_button"][i].place_forget()

        entry_update(self.widgets,
                     self.selected_area,
                     self.dragging_corner,
                     self.corner_number)

        self.update_area_sliders()
        self.draw_areas()
        return

    def drag_image(self, event):
        # drag area
        x_movement = event.x - self.dif_x
        y_movement = event.y - self.dif_y
        self.dif_x = event.x
        self.dif_y = event.y

        self.draw_areas()
        return

    def update_area_sliders(self):
        # updated size sliders
        width_slider = self.selected_area['width_slider']
        height_slider = self.selected_area['height_slider']

        x_max = 0
        y_max = 0
        for i in range(len(self.selected_area["area"])):
            x_temp = self.selected_area["area"][i][0]
            y_temp = self.selected_area["area"][i][1]
            if x_temp > x_max:
                x_max = x_temp
            if y_temp > y_max:
                y_max = y_temp

        value = 100 / self.image.width * x_max
        width_slider.set(int(value))

        value = 100 / self.image.height * y_max
        height_slider.set(int(value))

        return

    def change_point_position_with_slider(self, value, slider_name):
        if slider_name == 'width':
            dimension = self.image.width
            coord_index = 0
        else:
            dimension = self.image.height
            coord_index = 1

        new_value = dimension * value / 100
        point = list(self.selected_area["area"][self.corner_number])
        point[coord_index] = int(new_value)
        self.selected_area["area"][self.corner_number] = tuple(point)
        value = int(100 * new_value / dimension)


        return value

    def change_size(self, value, slider_name):
        if self.select_corner:
            value = self.change_point_position_with_slider(value, slider_name)

            entry_update(self.widgets,
                         self.selected_area,
                         self.dragging_corner,
                         self.corner_number)

            return value

        if slider_name == 'width':
            dimension = self.image.width
            coord_index = 0
            points_to_update = [2, 3, 4]
        else:
            dimension = self.image.height
            coord_index = 1
            points_to_update = [4, 5, 6]

        new_value = dimension * value / 100

        # get max from other points
        minimum = 0
        for i, point in enumerate(self.selected_area["area"]):
            if i not in points_to_update and point[coord_index] > minimum:
                minimum = point[coord_index]

        # get correct points
        points = []
        for i in points_to_update:
            coord = self.selected_area["area"][i][coord_index]
            points.append((coord, i))

        points.sort()

        # calculate max and center difference
        max_dif = points[2][0] - points[0][0]
        center_dif = points[1][0] - points[0][0]

        if new_value - max_dif < minimum:
            min_coord = minimum
        else:
            min_coord = new_value - max_dif

        center_coord = min_coord + center_dif
        max_coord = min_coord + max_dif

        new_coords = {}
        new_coords[points[0][1]] = min_coord
        new_coords[points[1][1]] = center_coord
        new_coords[points[2][1]] = max_coord

        for i in new_coords:
            coords = list(self.selected_area["area"][i])
            coords[coord_index] = new_coords[i]
            self.selected_area["area"][i] = tuple(coords)

        value = int(100 * max_coord / dimension)

        entry_update(self.widgets,
                     self.selected_area,
                     self.dragging_corner,
                     self.corner_number)

        return value
