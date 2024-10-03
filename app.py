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

@app.route('/resume/education/<int:education_id>', methods=['PUT'])
def education_at_id(education_id=None):
    '''
    Handles Education requests at a specific ID
    '''
    if request.method == 'PUT':
        if 0 <= education_id < len(data['education']):
            updated_data = request.get_json()

            course = updated_data.get('course')
            school = updated_data.get('school')
            start_date = updated_data.get('start_date')
            end_date = updated_data.get('end_date')
            grade = updated_data.get('grade')
            logo = updated_data.get('logo')
    
            if (
                not course 
                or not school 
                or not start_date 
                or not end_date 
                or not grade 
                or not logo
            ):
                return jsonify({'error': 'Invalid input, all fields (course, school, start_date, end_date, grade, logo) are required'}), 400
            
            data['education'][education_id] = Education(course, school, start_date, end_date, grade, logo)

            return jsonify({'message': 'Education updated', 'updated_education': data['education'][education_id]}), 200
        else:
            return jsonify({'error': 'Education not found'}), 404

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
