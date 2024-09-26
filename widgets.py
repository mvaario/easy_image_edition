import customtkinter as ctk


class Widgets:

    def __init__(self, main, slider_update):
        # import stuff
        self.main = main
        self.root = main.root
        self.slider_update = slider_update

        # create list of sliders
        self.sliders = []
        self.slider_label = []

        # create list of buttons
        self.buttons = []
        self.plus_minus_buttons = []
        self.plus_minus_location = []

        # create list of switches
        self.switches = []
        self.switch_positions = []

        # combo_box
        self.combo_box = []

        self.entry = []

    # create button
    def create_button(self, x, y, width, height, text, command, hover_color, bg_color, fg_color, save):
        button = ctk.CTkButton(self.root,
                               width=width,
                               height=height,
                               text=text,
                               command=command,
                               hover_color=hover_color,
                               bg_color=bg_color,
                               state='disabled',
                               fg_color=fg_color)

        button.place(x=x, y=y)

        if save:
            self.buttons.append(button)

        return button

    # create slider
    def create_slider(self, color, width, to, slider_name):
        slider = ctk.CTkSlider(self.root,
                               from_=0,
                               to=to,
                               command=lambda name: self.slider_update(slider, slider_name, label),
                               number_of_steps=255,
                               width=width,
                               fg_color=color,
                               state='disabled',
                               bg_color='transparent',
                               border_color='transparent'
                               )

        slider.set(0)
        slider.place()

        self.sliders.append(slider)

        label = ctk.CTkLabel(self.root, text=str(0), text_color=color, font=("Arial", 15))
        label.place()

        self.slider_label.append(label)

        return slider, label

    # create switch
    def create_switch(self, x, y, command, save):
        switch = ctk.CTkSwitch(self.root,
                               switch_width=25,
                               switch_height=15,
                               command=command,
                               text='',
                               state='disabled'
                               )

        switch.place(x=x, y=y)

        if save:
            self.switches.append(switch)
            self.switch_positions.append(x)
            self.switch_positions.append(y)

        switch.place_forget()

        return switch

    def create_radio_button(self, x, y, width, height, text, command, hover_color, fg_color, save):
        button = ctk.CTkRadioButton(self.root,
                                    width=width,
                                    height=height,
                                    text=text,
                                    command=command,
                                    hover_color=hover_color,
                                    state='disabled',
                                    fg_color=fg_color,
                                    corner_radius=0,
                                    border_width_checked=3,
                                    border_width_unchecked=2,

                                    )

        button.place(x=x, y=y)
        if save:
            self.buttons.append(button)

        return button

    def create_combo_box(self, x, y):
        box = ctk.CTkComboBox(self.root,
                              font=("Arial", 15),
                              dropdown_font=("Arial", 15),
                              width=80,
                              height=25,
                              border_color='#1F6AA5',
                              command=lambda save=False: self.main.edit_image(self.main.selected_image, save=False),
                              button_color='#1F6AA5',
                              button_hover_color='#1F6AA5',
                              dropdown_hover_color='#1F6AA5',
                              values=["None", "1", "2", "3", "4", "5", "6", "7", "8"]
                              )

        box.place(x=x, y=y - 35)
        box.configure(state='disabled')
        self.combo_box.append(box)

        return

    def create_entry(self, x, y, text, save):
        entry = ctk.CTkEntry(master=self.root,
                             placeholder_text=text,
                             font=("Arial", 15),
                             width=70,
                             height=25,
                             border_width=2,
                             corner_radius=0)
        entry.place(x=x, y=y, anchor=ctk.CENTER)
        entry.configure(state='disabled')

        if save:
            self.entry.append(entry)

        return entry
