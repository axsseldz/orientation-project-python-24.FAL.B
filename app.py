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
        experiences = [exp.__dict__ for exp in data['experience']]
        return jsonify(experiences)

    if request.method == 'POST':
        experience_data = request.json
        new_experience = Experience(**experience_data)
        data['experience'].append(new_experience)
        index = len(data['experience']) - 1
        
        return jsonify({'id': str(index)}), 201

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify(data['education']), 200

    if request.method == 'POST':
        new_education = request.json

        if (
            'course' not in new_education
            or 'school' not in new_education
            or 'start_date' not in new_education
            or 'end_date' not in new_education
            or 'grade' not in new_education
            or 'logo' not in new_education
        ):
            return jsonify({'error': 'Invalid input, all fields (course, school, start_date, end_date, grade, logo) are required'}), 400

        data['education'].append(new_education)

        return jsonify({'message': 'Education added', 'data': new_education, 'index': len(data['education']) - 1}), 201

    return jsonify({})


@app.route('/resume/education/<int:education_id>', methods=['GET', 'PUT', 'DELETE'])
def education_at_id(education_id=None):
    '''
    Handles education requests at a specific ID
    '''
    if request.method == 'GET':
        if 0 <= education_id < len(data['education']):
            return jsonify(data['education'][education_id]), 200
        else:
            return jsonify({'error': 'Education not found'}), 404

    if request.method == 'PUT':
        if 0 <= education_id < len(data['education']):
            updated_data = request.get_json()

            course = updated_data.get('course')
            school = updated_data.get('school')
            start_date = updated_data.get('start_date')
            end_date = updated_data.get('end_date')
            grade = updated_data.get('grade')
            logo = updated_data.get('logo')

            if not (course and school and start_date and end_date and grade and logo):
                return jsonify({'error': 'Invalid input, all fields (course, school, start_date, end_date, grade, logo) are required'}), 400

            data['education'][education_id] = Education(course, school, start_date, end_date, grade, logo)

            return jsonify({'message': 'Education updated', 'data': data['education'][education_id]}), 200
        else:
            return jsonify({'error': 'Education not found'}), 404    

    if request.method == 'DELETE':
        if 0 <= education_id < len(data['education']):
            deleted_education = data['education'].pop(education_id)

            return jsonify({"message": "Education deleted", "data": deleted_education}), 200
        else:
            return jsonify({"error": "Education not found"}), 404


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
