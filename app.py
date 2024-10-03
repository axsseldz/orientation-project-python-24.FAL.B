'''
Flask Application
'''
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
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/skill/<int:skill_id>', methods=['GET', 'PUT'])
def skill_at_id(skill_id=None):
    '''
    Handles Skill requests at a specific ID
    '''
    if request.method == 'PUT':
        if 0 <= skill_id < len(data['skill']):
            updated_data = request.get_json()

            name = updated_data.get('name')
            experience = updated_data.get('experience')
            logo = updated_data.get('logo')

            if not name or not experience or not logo:
                return jsonify({"error": "Invalid input, all fields (name, experience, logo) are required"}), 400
            
            data['skill'][skill_id] = Skill(name, experience, logo)

            return jsonify({"message": "Skill updated", "updated_skill": data['skill'][skill_id]}), 200
        else:
            return jsonify({"error": "Skill not found"}), 404