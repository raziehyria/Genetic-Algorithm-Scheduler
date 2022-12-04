import os
from flask import Flask, request, flash, redirect, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ClassScheduling import ClassScheduling 

app = Flask(__name__)
CORS(app)
app.secret_key = 'super secret key'


UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ClassScheduling relies on `is_running` to know when to manually stop iterations
is_running = False


cs = ClassScheduling()

# variable used to keep track of uploaded filename from user, to delete after we are done
# implementing the algorithmn on it
uploaded_filename = None

# Recieves config data from website and sets its corresponding values to the
# config object
@app.route('/additional-settings', methods=['POST'])
def set_additional_settings():
    range_data = request.json

    if range_data is not None and cs.config:
        cs.config.set_POPULATION_SIZE(range_data.get("populationSize"))
        cs.config.set_NUM_OF_ELITE_SCHEDULES(range_data.get("numOfEliteSchedules"))
        cs.config.set_MUTATION_RATE(range_data.get("mutationRate"))
        cs.config.set_TOURNAMENT_SELECTION_SIZE(range_data.get("tournamentSelectionSize"))
        cs.config.set_MAX_ITERATION(range_data.get("maxIteration"))

    return ('config changed', 200)


# returns the completion percent
# completion percent is calculated in ClassScheduling file in the while loop
@app.route('/get-progress-percent')
def get_progress_percent():
    return { 'progress': cs.progress_percent }

# Download link for output schedule.xlsx
@app.route('/download')
def download_schedule():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'schedule.xlsx', as_attachment=True)

# Sets `is_running` to false, triggering `ClassScheduling`'s while loop to stop
@app.route("/stop", methods=['GET'])
def stop():
    global is_running
    is_running = False

    if uploaded_filename and os.path.exists("./" + uploaded_filename):
        os.remove("./" + uploaded_filename)
    return 'stopped'

# Used for `ClassScheduling`'s while loop to check if the algorithmn should 
# keep running
@app.route("/is_running_status", methods=['GET'])
def get_stopped_status():
    return { 'is_running': is_running }

# Route for website to send their file
@app.route("/upload", methods=['POST'])
def upload_file():
    # Retrieving the file and storing in the variable 'file'  based off of:
    # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # If there is no filename
    if file.filename == '':
        flash('No selected file')

    # If a file exists, and there is a filename
    if file and file.filename:
        filename = secure_filename(file.filename)

        # store  filename to uploaded_filename to delete when we are done with it
        global uploaded_filename
        uploaded_filename = filename

        # save the user's uploaded file to our filesystem
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # start algorithmn
    global is_running
    is_running = True
    cs.start()

    return ('upload complete', 200)
