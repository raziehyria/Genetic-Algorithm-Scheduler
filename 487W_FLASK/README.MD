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
