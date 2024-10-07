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
        return jsonify(data['skill']), 200

    if request.method == 'POST':
        new_skill = request.json
        
        if "name" not in new_skill or "proficiency" not in new_skill or "logo" not in new_skill:
            return jsonify({"error": "Invalid input, all fields (name, proficiency, logo) are required"}), 400
        
        data['skill'].append(new_skill)
        
        return jsonify({'message': 'Skill added', 'data': new_skill, 'index': len(data['skill']) - 1}), 201

    return jsonify({})


@app.route('/resume/skill/<int:skill_id>', methods=['GET', 'PUT', 'DELETE'])
def skill_at_id(skill_id=None):
    '''
    Handles Skill requests at a specific ID
    '''
    if request.method == 'GET':
        if 0 <= skill_id < len(data['skill']):
            return jsonify(data['skill'][skill_id]), 200
        else:
            return jsonify({'error': 'Skill not found'}), 404
    
    if request.method == 'PUT':
        if 0 <= skill_id < len(data['skill']):
            updated_data = request.get_json()

            name = updated_data.get('name')
            proficiency = updated_data.get('proficiency')
            logo = updated_data.get('logo')

            if not name or not proficiency or not logo:
                return jsonify({'error': 'Invalid input, all fields (name, proficiency, logo) are required'}), 400

            data['skill'][skill_id] = Skill(name, proficiency, logo)

            return jsonify({'message': 'Skill updated', 'data': data['skill'][skill_id]}), 200
        else:
            return jsonify({'error': 'Skill not found'}), 404    

    if request.method == 'DELETE':
        if 0 <= skill_id < len(data['skill']):
            deleted_skill = data['skill'].pop(skill_id)
            
            return jsonify({"message": "Skill deleted", "data": deleted_skill}), 200
        else:
            return jsonify({"error": "Skill not found"}), 404