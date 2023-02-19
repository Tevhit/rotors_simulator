from tkinter import *
from simulation_manager import SimulationManager


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class Main:

    def __init__(self):

        self.uav_list = None
        self.uav_arm_button = None
        self.uav_disarm_button = None
        self.active_uav_count = 0
        self.active_uav_info = None
        self.active_uav_info_label = None
        self.triangle_formation_button = None
        self.square_formation_button = None
        self.pentagon_formation_button = None
        self.v_formation_button = None
        self.crescent_formation_button = None
        self.star_formation_button = None
        self.circle_formation_button = None
        self.saved_formation_button = None
        self.save_random_formation_button = None
        self.set_altitude_button = None
        self.sequential_landing_button = None
        # -------------------------------------------------------------------
        self.set_altitude_window = None
        self.set_altitude_entry = None
        # -------------------------------------------------------------------
        self.square_formation_window = None
        self.square_formation_entry = None
        # -------------------------------------------------------------------
        self.triangle_formation_window = None
        self.triangle_formation_entry = None
        # -------------------------------------------------------------------
        self.pentagon_formation_window = None
        self.pentagon_formation_entry = None
        # -------------------------------------------------------------------
        self.v_formation_window = None
        self.v_formation_distance_entry = None
        self.v_formation_angle_entry = None
        # -------------------------------------------------------------------
        self.crescent_formation_window = None
        self.crescent_formation_entry = None
        # -------------------------------------------------------------------
        self.star_formation_window = None
        self.star_formation_entry = None
        # -------------------------------------------------------------------
        self.circle_formation_window = None
        self.circle_formation_entry = None
        # -------------------------------------------------------------------
        self.saved_formation_window = None
        # -------------------------------------------------------------------
        self.save_random_formation_window = None
        # -------------------------------------------------------------------
        self.sequential_landing_window = None
        self.sequential_landing_entry = None
        # -------------------------------------------------------------------

        # UAV count can be parametric according to the "tevhit_swarm_example.launch" file
        self.total_uav_count = 12  # sys.argv[1]
        self.simulation_manager = SimulationManager(int(self.total_uav_count))

        # Create and show main window
        self.window = Tk()
        self.window.title("Tevhit Karsli Swarm Simulation")
        self.window.geometry('775x600')
        self.window.eval('tk::PlaceWindow . center')
        center(self.window)
        self.load_gui()
        self.window.mainloop()

    def load_gui(self):
        # Create an interactive uav list
        self.uav_list = Listbox(self.window, height=20, width=18, selectmode='multiple', font=10)
        self.uav_list.place(x=25, y=25)

        for i in range(1, int(self.total_uav_count) + 1):
            iha_name = 'firefly' + str(i)
            self.uav_list.insert(1, iha_name)

        # Each UAV can be armed and disarmed
        self.uav_arm_button = Button(self.window, text='Arm UAV', height=2, width=20,
                                     command=self.arm_auv)
        self.uav_arm_button.place(x=25, y=450)

        self.uav_disarm_button = Button(self.window, text='Disarm UAV', height=2, width=20,
                                        command=self.disarm_uav)
        self.uav_disarm_button.place(x=25, y=500)

        # All UAVs might not be armed
        self.active_uav_count = 0
        self.active_uav_info = StringVar()
        self.active_uav_info.set("Active UAV Count: 0")
        self.active_uav_info_label = Label(self.window, textvariable=self.active_uav_info)
        self.active_uav_info_label.place(x=25, y=550)

        self.triangle_formation_button = Button(self.window, text='Triangle Formation', height=2, width=25,
                                                command=self.triangle_formation)
        self.triangle_formation_button.place(x=250, y=25)

        self.square_formation_button = Button(self.window, text='Square Formation', height=2, width=25,
                                              command=self.square_formation)
        self.square_formation_button.place(x=250, y=75)

        self.pentagon_formation_button = Button(self.window, text='Pentagon Formation', height=2, width=25,
                                                command=self.pentagon_formation)
        self.pentagon_formation_button.place(x=250, y=125)

        self.v_formation_button = Button(self.window, text='V Formation', height=2, width=25,
                                         command=self.v_formation)
        self.v_formation_button.place(x=250, y=175)

        self.crescent_formation_button = Button(self.window, text='Crescent Formation', height=2, width=25,
                                                command=self.crescent_formation)
        self.crescent_formation_button.place(x=250, y=225)

        self.star_formation_button = Button(self.window, text='Star Formation', height=2, width=25,
                                            command=self.star_formation)
        self.star_formation_button.place(x=250, y=275)

        self.circle_formation_button = Button(self.window, text='Circle Formation', height=2, width=25,
                                              command=self.circle_formation)
        self.circle_formation_button.place(x=250, y=325)

        self.saved_formation_button = Button(self.window, text='Saved Formation', height=2, width=25,
                                             command=self.saved_formation)
        self.saved_formation_button.place(x=250, y=375)

        self.save_random_formation_button = Button(self.window, text='Save Random Formation', height=2, width=25,
                                                   command=self.save_random_formation)
        self.save_random_formation_button.place(x=510, y=375)

        self.set_altitude_button = Button(self.window, text='Set Altitude', height=2, width=25,
                                          command=self.set_altitude)
        self.set_altitude_button.place(x=510, y=25)

        self.sequential_landing_button = Button(self.window, text='Sequential Landing (Finish it)', height=2, width=25,
                                                command=self.sequential_landing)
        self.sequential_landing_button.place(x=510, y=175)

    def arm_auv(self):
        # Start the threads of the selected UAVs in the list

        selected_uav_list = self.uav_list.curselection()
        self.active_uav_count += len(selected_uav_list)
        self.active_uav_info.set('Total Armed UAV Count: ' + str(self.active_uav_count))

        name_of_uav_list = []
        for iha in selected_uav_list:
            self.uav_list.itemconfig(iha, {'bg': 'lightgreen'})
            name_of_uav_list.append(int(self.uav_list.get(iha).replace('firefly', '')))

        self.simulation_manager.arm_uav(name_of_uav_list)

        self.uav_list.selection_clear(0, 'end')

    def disarm_uav(self):
        # Stop the threads of the selected UAVs in the list

        selected_uav_list = self.uav_list.curselection()
        self.active_uav_count -= len(selected_uav_list)
        self.active_uav_info.set('Total Armed UAV Count: ' + str(self.active_uav_count))

        for iha in selected_uav_list:
            self.uav_list.itemconfig(iha, {'bg': 'white'})
            self.simulation_manager.disarm_uav(int(self.uav_list.get(iha).replace('firefly', '')))

        self.uav_list.selection_clear(0, 'end')

    def set_altitude(self):
        self.set_altitude_window = Tk()
        self.set_altitude_window.title('Set Altitude')
        self.set_altitude_window.geometry('500x100')
        center(self.set_altitude_window)

        set_altitude_input_label = Label(self.set_altitude_window, text="Altitude: ")
        set_altitude_input_label.place(x=25, y=25)

        self.set_altitude_entry = Entry(self.set_altitude_window)
        self.set_altitude_entry.place(x=225, y=25)

        set_altitude_okay_button = Button(self.set_altitude_window, text='Okay', command=self.publish_swarm_altitude)
        set_altitude_okay_button.place(x=225, y=50)

        self.set_altitude_window.mainloop()

    def publish_swarm_altitude(self):
        input_altitude = int(self.set_altitude_entry.get())
        self.simulation_manager.publish_mission('set_altitude', str(input_altitude))
        self.simulation_manager.set_mission_altitude(input_altitude)
        self.set_altitude_window.destroy()

    def square_formation(self):
        self.square_formation_window = Tk()
        self.square_formation_window.title('Square Formation')
        self.square_formation_window.geometry('500x100')
        center(self.square_formation_window)

        square_formation_input_label = Label(self.square_formation_window, text="Enter Distance Between UAVs: ")
        square_formation_input_label.place(x=25, y=25)

        self.square_formation_entry = Entry(self.square_formation_window)
        self.square_formation_entry.place(x=225, y=25)

        square_formation_okay_button = Button(self.square_formation_window, text='Okay',
                                              command=self.publish_square_formation)
        square_formation_okay_button.place(x=225, y=50)

        self.square_formation_window.mainloop()

    def publish_square_formation(self):
        distance_between_uav = int(self.square_formation_entry.get())
        self.simulation_manager.publish_mission("square_formation", str(distance_between_uav))
        self.square_formation_window.destroy()

    def triangle_formation(self):
        self.triangle_formation_window = Tk()
        self.triangle_formation_window.title('Triangle Formation')
        self.triangle_formation_window.geometry('500x100')
        center(self.triangle_formation_window)

        triangle_formation_input_label = Label(self.triangle_formation_window, text="Enter Distance Between UAVs: ")
        triangle_formation_input_label.place(x=25, y=25)

        self.triangle_formation_entry = Entry(self.triangle_formation_window)
        self.triangle_formation_entry.place(x=225, y=25)

        triangle_formation_okay_button = Button(self.triangle_formation_window, text='Okay',
                                                command=self.publish_triangle_formation)
        triangle_formation_okay_button.place(x=225, y=50)

        self.triangle_formation_window.mainloop()

    def publish_triangle_formation(self):
        distance_between_uav = int(self.triangle_formation_entry.get())
        self.simulation_manager.publish_mission("triangle_formation", str(distance_between_uav))
        self.triangle_formation_window.destroy()

    def pentagon_formation(self):
        self.pentagon_formation_window = Tk()
        self.pentagon_formation_window.title('Pentagon Formation')
        self.pentagon_formation_window.geometry('500x100')
        center(self.pentagon_formation_window)

        pentagon_formation_input_label = Label(self.pentagon_formation_window, text="Enter Distance Between UAVs: ")
        pentagon_formation_input_label.place(x=25, y=25)

        self.pentagon_formation_entry = Entry(self.pentagon_formation_window)
        self.pentagon_formation_entry.place(x=225, y=25)

        pentagon_formation_okay_button = Button(self.pentagon_formation_window, text='Okay',
                                                command=self.publish_pentagon_formation)
        pentagon_formation_okay_button.place(x=225, y=50)

        self.pentagon_formation_window.mainloop()

    def publish_pentagon_formation(self):
        distance_between_uav = int(self.pentagon_formation_entry.get())
        self.simulation_manager.publish_mission('pentagon_formation', str(distance_between_uav))
        self.pentagon_formation_window.destroy()

    def v_formation(self):
        self.v_formation_window = Tk()
        self.v_formation_window.title('V Formation')
        self.v_formation_window.geometry('500x125')
        center(self.v_formation_window)

        v_formation_distance_input_label = Label(self.v_formation_window, text="Enter Distance Between UAVs: ")
        v_formation_distance_input_label.place(x=25, y=25)

        self.v_formation_distance_entry = Entry(self.v_formation_window)
        self.v_formation_distance_entry.place(x=225, y=25)

        v_formation_angle_input_label = Label(self.v_formation_window, text="Enter angle of V: ")
        v_formation_angle_input_label.place(x=25, y=50)

        self.v_formation_angle_entry = Entry(self.v_formation_window)
        self.v_formation_angle_entry.place(x=225, y=50)

        v_formation_okay_button = Button(self.v_formation_window, text='Okay', command=self.publish_v_formation)
        v_formation_okay_button.place(x=225, y=75)

        self.v_formation_window.mainloop()

    def publish_v_formation(self):
        distance_between_uav = int(self.v_formation_distance_entry.get())
        angle_of_v = int(self.v_formation_angle_entry.get())
        self.simulation_manager.publish_mission('v_formation', str(distance_between_uav) + ' ' + str(angle_of_v))
        self.v_formation_window.destroy()

    def crescent_formation(self):
        self.crescent_formation_window = Tk()
        self.crescent_formation_window.title('Crescent Formation')
        self.crescent_formation_window.geometry('500x100')
        center(self.crescent_formation_window)

        crescent_formation_input_label = Label(self.crescent_formation_window, text="Enter Radius of Crescent: ")
        crescent_formation_input_label.place(x=25, y=25)

        self.crescent_formation_entry = Entry(self.crescent_formation_window)
        self.crescent_formation_entry.place(x=225, y=25)

        crescent_formation_okay_button = Button(self.crescent_formation_window, text='Okay',
                                                command=self.publish_crescent_formation)
        crescent_formation_okay_button.place(x=225, y=50)

        self.crescent_formation_window.mainloop()

    def publish_crescent_formation(self):
        radius = int(self.crescent_formation_entry.get())
        self.simulation_manager.publish_mission('crescent_formation', str(radius))
        self.crescent_formation_window.destroy()

    def star_formation(self):
        self.star_formation_window = Tk()
        self.star_formation_window.title('Star Formation')
        self.star_formation_window.geometry('500x100')
        center(self.star_formation_window)

        star_formation_input_label = Label(self.star_formation_window, text="Enter Distance Between UAVs: ")
        star_formation_input_label.place(x=25, y=25)

        self.star_formation_entry = Entry(self.star_formation_window)
        self.star_formation_entry.place(x=225, y=25)

        star_formation_okay_button = Button(self.star_formation_window, text='Okay',
                                            command=self.publish_star_formation)
        star_formation_okay_button.place(x=225, y=50)

        self.star_formation_window.mainloop()

    def publish_star_formation(self):
        distance_between_uav = int(self.star_formation_entry.get())
        self.simulation_manager.publish_mission('star_formation', str(distance_between_uav))
        self.star_formation_window.destroy()

    def circle_formation(self):
        self.circle_formation_window = Tk()
        self.circle_formation_window.title('Circle Formation')
        self.circle_formation_window.geometry('500x100')
        center(self.circle_formation_window)

        circle_formation_input_label = Label(self.circle_formation_window, text="Enter Radius of Circle: ")
        circle_formation_input_label.place(x=25, y=25)

        self.circle_formation_entry = Entry(self.circle_formation_window)
        self.circle_formation_entry.place(x=225, y=25)

        circle_formation_okay_button = Button(self.circle_formation_window, text='Okay',
                                              command=self.publish_circle_formation)
        circle_formation_okay_button.place(x=225, y=50)

        self.circle_formation_window.mainloop()

    def publish_circle_formation(self):
        radius = int(self.circle_formation_entry.get())
        self.simulation_manager.publish_mission('circle_formation', str(radius))
        self.circle_formation_window.destroy()

    def saved_formation(self):
        self.saved_formation_window = Tk()
        self.saved_formation_window.title('Saved Formation')
        self.saved_formation_window.geometry('350x125')
        center(self.saved_formation_window)

        saved_formation_question_label = Label(self.saved_formation_window, text="Run Saved Formation?")
        saved_formation_question_label.place(x=25, y=25)

        saved_formation_okay_button = Button(self.saved_formation_window, text='Okay',
                                             command=self.publish_saved_formation)
        saved_formation_okay_button.place(x=150, y=75)

        self.saved_formation_window.mainloop()

    def publish_saved_formation(self):
        self.simulation_manager.publish_mission('saved_formation')
        self.saved_formation_window.destroy()

    def save_random_formation(self):
        self.save_random_formation_window = Tk()
        self.save_random_formation_window.title('Save Random Formation')
        self.save_random_formation_window.geometry('350x125')
        center(self.save_random_formation_window)

        save_random_formation_question_label = Label(self.save_random_formation_window,
                                                     text="Save Random Formation?")
        save_random_formation_question_label.place(x=25, y=25)

        save_random_formation_okay_button = Button(self.save_random_formation_window, text='Okay',
                                                   command=self.publish_save_random_formation)
        save_random_formation_okay_button.place(x=150, y=75)

        self.save_random_formation_window.mainloop()

    def publish_save_random_formation(self):
        self.simulation_manager.publish_mission("save_random_formation")
        self.save_random_formation_window.destroy()

    def sequential_landing(self):
        self.sequential_landing_window = Tk()
        self.sequential_landing_window.title('Sequential Landing')
        self.sequential_landing_window.geometry('500x100')
        center(self.sequential_landing_window)

        sequential_landing_input_label = Label(self.sequential_landing_window, text="Enter Waiting Time(second): ")
        sequential_landing_input_label.place(x=25, y=25)

        self.sequential_landing_entry = Entry(self.sequential_landing_window)
        self.sequential_landing_entry.place(x=225, y=25)

        sequential_landing_okay_button = Button(self.sequential_landing_window, text='Okay',
                                                command=self.publish_sequential_landing)
        sequential_landing_okay_button.place(x=225, y=50)

        self.sequential_landing_window.mainloop()

    def publish_sequential_landing(self):
        waiting_time = int(self.sequential_landing_entry.get())
        self.simulation_manager.publish_mission('sequential_landing', str(waiting_time))
        self.sequential_landing_window.destroy()


main = Main()
