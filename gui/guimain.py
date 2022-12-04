import os
import sys
from threading import Thread

import pygubu

sys.path.insert(1, '/home/john/raz/487W')
from ClassScheduling import ClassScheduling
from config import Config


# using a gui builder from https://pypi.org/project/pygubu/
# pygubu https://github.com/alejandroautalan/pygubu/blob/master/README.md
# pygubu designer https://github.com/alejandroautalan/pygubu-designer


class CourseSchedulingApp:

    def __init__(self):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        # file in xml format
        builder.add_from_file('/home/john/raz/487W/gui/cs_gui.ui')

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('main_window')
        builder.connect_callbacks(self)

        # 4: Setting up remaining widgets
        # tab 1 widgets
        self.input_filepath = builder.get_object('input_file_name')
        self.output_filepath = builder.get_object('output_file_name')

        self.execution_stats_text = builder.get_object("execution_stats_text")
        self.start_button = builder.get_object("start_button")
        self.stop_button = builder.get_object("stop_button")

        builder.get_variable("show_stats").set(1)  # default checkbox to selected

        # Settings tab widgets
        self.population_entry = builder.get_object('pop_entry')
        self.num_elite_schedules = builder.get_object('num_elite_schedules_entry')
        self.mutation_rate = builder.get_object("mutation_rate_entry")
        self.tournament_size = builder.get_object("tournament_selection_size_entry")
        self.max_iteration = builder.get_object("max_iteration_entry")

        # Reference to class scheduler object
        self.class_scheduler = None
        self.config = Config.getInstance()

        # variable that controls start/stop flow of the program
        self.stop_scheduling = False

        # disallow multiple times 'start' button click
        self.start_button_clicked = False

    def start_button_pressed(self, event=None):
        # clear previous text
        self.execution_stats_text.delete('1.0', 'end')
        self.execution_stats_text.insert('end', 'Processing, please wait ...')


        if self.config.get_FILE_PATH() is None:
            self.execution_stats_text.insert('end', '\nRequired! Please specify the input file ...\n')
            self.execution_stats_text.update()
            return

        if len(self.output_filepath.cget('path')) == 0:
            self.execution_stats_text.insert('end', '\nRequired! Please specify the output directory ...\n')
            self.execution_stats_text.update()
            return

        # if start button not clicked already
        if not self.start_button_clicked:
            self.start_button_clicked = True
            self.stop_scheduling = False

            # passing in the text widget reference to be updated
            self.class_scheduler = ClassScheduling()
            # https://realpython.com/intro-to-python-threading/
            class_scheduling_thread = Thread(target=self.class_scheduler.start, args=(self,), daemon=True)
            class_scheduling_thread.start()

    def stop_button_pressed(self, event=None):
        """if user presses stop it will print out current best schedule"""
        self.stop_scheduling = True

        # reset start button clicked
        self.start_button_clicked = False

    def show_stats(self):
        """return 0 or 1 depending on whether checkbox is marked or not"""
        return self.builder.get_variable("show_stats").get()

    def input_path_changed(self, event=None):
        # Get the path chosen by the user
        path = self.input_filepath.cget('path')

        # add path to config
        self.config.set_FILE_PATH(path)

    def output_path_changed(self, event=None):
        # just changes the current working directory so the file schedule.xlsx will be placed in there
        # https://stackoverflow.com/questions/35005585/cannot-export-pandas-dataframe-to-specified-file-path-in-python-for-csv-and-exce

        path = self.output_filepath.cget('path')
        os.chdir(path)

    def save_button_pressed(self, event=None):
        # if 'Start' button is not already clicked
        if not self.start_button_clicked:
            population = self.population_entry.get()
            num_elite_schedule = self.num_elite_schedules.get()
            mutation_rate = self.mutation_rate.get()
            tournament_size = self.tournament_size.get()
            max_iteration = self.max_iteration.get()

            try:
                population = int(population)
                num_elite_schedule = int(num_elite_schedule)
                mutation_rate = float(mutation_rate)
                tournament_size = int(tournament_size)
                max_iteration = int(max_iteration)

                self.config.set_POPULATION_SIZE(population)
                self.config.set_NUM_OF_ELITE_SCHEDULES(num_elite_schedule)
                self.config.set_MUTATION_RATE(mutation_rate)
                self.config.set_TOURNAMENT_SELECTION_SIZE(tournament_size)
                self.config.set_MAX_ITERATION(max_iteration)

            except Exception as ex:
                print(ex)
                self.execution_stats_text.insert('end', 'Please correct the settings values, reverting to default.\n')
                self.execution_stats_text.update()
                self.reset_settings_pressed()

    def reset_settings_pressed(self, event=None):
        # TODO: hard coded for now
        self.config.set_POPULATION_SIZE(23)
        self.config.set_NUM_OF_ELITE_SCHEDULES(2)
        self.config.set_MUTATION_RATE(0.002)
        self.config.set_TOURNAMENT_SELECTION_SIZE(7)
        self.config.set_MAX_ITERATION(600)

        # clear and set fields
        self.population_entry.delete(0, len(self.population_entry.get()))
        self.population_entry.insert('end', '23')

        self.num_elite_schedules.delete(0, len(self.num_elite_schedules.get()))
        self.num_elite_schedules.insert('end', '2')

        self.mutation_rate.delete(0, len(self.mutation_rate.get()))
        self.mutation_rate.insert('end', '0.002')

        self.tournament_size.delete(0, len(self.tournament_size.get()))
        self.tournament_size.insert('end', '7')

        self.max_iteration.delete(0, len(self.max_iteration.get()))
        self.max_iteration.insert('end', '600')

    def run(self):
        try:
            self.mainwindow.mainloop()
        except UnicodeDecodeError:
            error_msg = "Mouse scrolling within the window casued an error.\nIt's a known system/Python bug.\nPlease re-run the program."
            print(error_msg)
            self.execution_stats_text.insert('end', error_msg)
            self.execution_stats_text.update()
            input("Press any key to exit")
            pass


if __name__ == '__main__':
    app = CourseSchedulingApp()
    app.run()
