import pygubu
from config import Config
from ClassScheduling import ClassScheduling
from threading import Thread

# using a gui builder from https://pypi.org/project/pygubu/
# pygubu https://github.com/alejandroautalan/pygubu/blob/master/README.md
# pygubu designer https://github.com/alejandroautalan/pygubu-designer


class CourseSchedulingApp:

    def __init__(self):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        # file in xml format
        builder.add_from_file('cs_gui.ui')

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('main_window')
        builder.connect_callbacks(self)

        # 4: Setting up remaining widgets
        # tab 1 widgets
        self.input_filepath = builder.get_object('input_file_name')
        self.execution_stats_text = builder.get_object("execution_stats_text")
        self.start_button = builder.get_object("start_button")
        self.stop_button = builder.get_object("stop_button")

        # tab 2 widgets
        self.pop_entry = builder.get_object('pop_entry')

        # Reference to class scheduler object
        self.class_scheduler = None
        self.config = Config.getInstance()

    def start_button_pressed(self, event=None):
        # passing in the text widget reference to be updated
        self.class_scheduler = ClassScheduling()
        # https://realpython.com/intro-to-python-threading/
        Thread(target=self.class_scheduler.start(self.execution_stats_text)).start()  # TODO: gui very slow, tried using threading

    def stop_button_pressed(self, event=None):  # TODO: Need to make it cancel and write schedule when user hits stop
        pass

    def input_path_changed(self, event=None):
        # Get the path chosen by the user
        path = self.input_filepath.cget('path')

        # add path to config
        self.config.set_FILE_PATH(path)

    def output_path_changed(self, event=None):
        pass

    def save_button_pressed(self, event=None):
        pop = self.pop_entry.get()
        print(pop)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = CourseSchedulingApp()
    app.run()