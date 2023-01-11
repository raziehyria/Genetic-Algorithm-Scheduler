# Initial Project Setup

This is the initial setup you need to do on your machine to get everything up and running,
after you have done this, you can skip this section and go straight to the `Running the server and webapp section`
## Flask Setup
### set up venv
Set up your python virtual environment (you only have to do this once)
https://docs.python.org/3/library/venv.html
`python3 -m venv venv`

#### Activate venv
You have to do this everytime before launching the programs
##### Windows
`PS> venv\Scripts\activate`
##### Linux/MacOS
`source venv/bin/activate`

##### Install pip requirements
This installs all of the pip requirements for the project, you only need to do this once,
and make sure that you have activated your virtual environment (venv) before running this command
`pip install -r requirements.txt`

## Web App Setup

### Install Node.js
Install [Node.JS](https://nodejs.org/en/) on your computer if you have not done so already

## Install Node Modules for webapp
Navigate to the `webapp` directory in your terminal/powershell
and run `npm install`. You only have to do this one time.

# Running the server and webapp

1. Activate your python venv (virtual environment)
##### Windows
`PS> venv\Scripts\activate`
##### Linux/MacOS
`source venv/bin/activate`

2. Run Flask with `python -m flask run`
3. Navigate to `webapp` directory
4. Run `npm start` to launch the webapp


# Troubleshooting

### Python Version
Make sure to use the most recent version of python, *ideally* 3.10.8 and up. 
Adjust the Python interpretter settings in your IDE and ensure the most recent version is being used for the project environment.

### Bad JSON Request
The json.get() request can sometimes run inconsistently and break the connection with Flask if the reponse is not valid, and then throws the following error:
> requests.exceptions.JSONDecodeError

To combat this issue,

1. Navigate to the Project Folder -> `ClassScheduling.py`
2. Replace lines 51 & 52 with the following:

```
try:
    is_running = r.json().get('is_running')
except:
    is_running = True
 ```
 
 This should allow for consistent checking of the website status.
    
### File Path
Before running the application, you need to feed the program a base file.
To do this, 

1. Access the Project Folder, and move the "Course list and attributes(1).xlsx" file elsewhere, i.e your desktop or your documents. You will use this later.
2. Make a copy of the "Course list and attributes(1).xlsx", from wherever you placed it, and paste it into the Project Folder.
3. Rename the copied file to "default", or something arbitrary.
4. Open the project in your IDE, Navigate to Project folder -> `config.py`.
5. Replace line 22, with the following or what you renamed your copy to:
`self._FILE_PATH = './default.xlsx'` 
6. Save and repeat the steps to run the server/wepapp listed above.


# Video
[![Scheduler Web App Demo](http://img.youtube.com/vi/BXaJ-nTZHqY&t/0.jpg)](http://www.youtube.com/watch?v=BXaJ-nTZHqY&t "Scheduler Web App Demo")

*For more information*: [Scheduler App Manual](https://docs.google.com/document/d/1hrPahWyVSWL596jP1vAtecgKZBnhjUHVqU1jUHVvA0M/edit?usp=sharing)
