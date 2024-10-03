from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}

@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handles GET and POST requests for experience data

    GET:
        Returns:
            a JSON object: the current list of experience data

    POST:
        Expects a dictionary containing the experience details to be added 
        
        Returns:
            JSON: The updated experience list after adding the new entry
    '''
    if request.method == 'GET':
        return jsonify(data['experience'])

    if request.method == 'POST':
        new_experience = request.json
        data['experience'].append(new_experience)
        return jsonify(data['experience'])


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles GET and POST requests for education data

    GET:
        Returns:
            JSON: The current list of education data

    POST:
        Expects request.json: A dictionary containing the education details 
            to be added
        
        Returns:
            JSON: The updated education list after adding the new entry
    '''
    if request.method == 'GET':
        return jsonify(data['education'])

    if request.method == 'POST':
        new_education = request.json
        data['education'].append(new_education)
        return jsonify(data['education'])


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles GET and POST requests for skill data

    GET:
        Returns:
            JSON: The current list of skill data

    POST:
        Expects request.json: a dictionary containing the skill details to be added
        
        Returns:
            JSON: The updated skill list after adding the new entry
    '''
    if request.method == 'GET':
        return jsonify(data['skill'])

    if request.method == 'POST':
        new_skill = request.json
        data['skill'].append(new_skill)
        return jsonify(data['skill'])
