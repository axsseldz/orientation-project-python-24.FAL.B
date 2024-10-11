'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from spellchecker import SpellChecker
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

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

spell = SpellChecker()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_suggestions(prompt):
    """
    Sends a prompt to GeminiAPI and returns a list of suggestions.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50,
                "max_output_tokens": 150,
                "response_mime_type": "text/plain"
            }
        )
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        
        # Process the response to extract suggestions
        suggestions_text = response.text
        suggestions = [s.strip("- ").strip() for s in suggestions_text.split('\n') if s.strip()]
        
        return suggestions
    except Exception as e:
        app.logger.error(f"GeminiAPI Error: {e}")
        return []

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
        return jsonify(experiences), 200

    if request.method == 'POST':
        experience_data = request.json
        new_experience = Experience(**experience_data)
        data['experience'].append(new_experience)
        index = len(data['experience']) - 1
        return jsonify({'id': str(index)}), 201

    return jsonify({}), 400

@app.route('/resume/experience/<int:experience_id>', methods=['PUT'])
def experience_at_id(experience_id):
    '''
    Handles PUT request to update an Experience at a specific ID
    '''
    if request.method == 'PUT':
        if 0 <= experience_id < len(data['experience']):
            updated_data = request.get_json()

            # Validate that all required fields are present
            required_fields = ['title', 'company', 'start_date', 'end_date', 'description', 'logo']
            if not all(field in updated_data for field in required_fields):
                return jsonify({'error': f'All fields {required_fields} are required'}), 400

            data['experience'][experience_id] = Experience(
                title=updated_data['title'],
                company=updated_data['company'],
                start_date=updated_data['start_date'],
                end_date=updated_data['end_date'],
                description=updated_data['description'],
                logo=updated_data['logo']
            )

            return jsonify(data['experience'][experience_id].__dict__), 200
        else:
            return jsonify({'error': 'Experience not found'}), 404
        
@app.route('/resume/experience/<int:experience_id>/suggestions', methods=['GET'])
def experience_suggestions(experience_id):
    """
    Provides suggestions to improve the description field of a specific Experience entry.
    """
    if 0 <= experience_id < len(data['experience']):
        current_description = data['experience'][experience_id].description
        prompt = (
            f"The following is a job description:\n\"{current_description}\"\n\n"
            "Provide three suggestions to enhance this job description for better clarity and impact."
        )
        
        suggestions = get_gemini_suggestions(prompt)
        
        if suggestions:
            return jsonify({"suggestions": suggestions}), 200
        else:
            return jsonify({"error": "Failed to generate suggestions"}), 500
    else:
        return jsonify({'error': 'Experience not found'}), 404

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        educations = [edu.__dict__ for edu in data['education']]
        return jsonify(educations), 200

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
            return jsonify({'error': 'All fields are required'}), 400

        new_edu = Education(**new_education)
        data['education'].append(new_edu)

        return jsonify({'message': 'Education added', 'data': new_edu.__dict__, 'index': len(data['education']) - 1}), 201

    return jsonify({}), 400

@app.route('/resume/education/<int:education_id>', methods=['GET', 'PUT', 'DELETE'])
def education_at_id(education_id=None):
    '''
    Handles education requests at a specific ID
    '''
    if request.method == 'GET':
        if 0 <= education_id < len(data['education']):
            return jsonify(data['education'][education_id].__dict__), 200
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

            return jsonify({'message': 'Education updated', 'data': data['education'][education_id].__dict__}), 200
        else:
            return jsonify({'error': 'Education not found'}), 404    

    if request.method == 'DELETE':
        if 0 <= education_id < len(data['education']):
            deleted_education = data['education'].pop(education_id)
            return jsonify({"message": "Education deleted", "data": deleted_education.__dict__}), 200
        else:
            return jsonify({"error": "Education not found"}), 404

@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        skills = [skill.__dict__ for skill in data['skill']]
        return jsonify(skills), 200

    if request.method == 'POST':
        new_skill = request.json
        
        if "name" not in new_skill or "proficiency" not in new_skill or "logo" not in new_skill:
            return jsonify({"error": "Invalid input, all fields (name, proficiency, logo) are required"}), 400
        
        new_skill_obj = Skill(**new_skill)
        data['skill'].append(new_skill_obj)
        
        return jsonify({'message': 'Skill added', 'data': new_skill_obj.__dict__, 'index': len(data['skill']) - 1}), 201

    return jsonify({}), 400

@app.route('/resume/skill/<int:skill_id>', methods=['GET', 'PUT', 'DELETE'])
def skill_at_id(skill_id=None):
    '''
    Handles Skill requests at a specific ID
    '''
    if request.method == 'GET':
        if 0 <= skill_id < len(data['skill']):
            return jsonify(data['skill'][skill_id].__dict__), 200
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

            return jsonify({'message': 'Skill updated', 'data': data['skill'][skill_id].__dict__}), 200
        else:
            return jsonify({'error': 'Skill not found'}), 404    

    if request.method == 'DELETE':
        if 0 <= skill_id < len(data['skill']):
            deleted_skill = data['skill'].pop(skill_id)
            return jsonify({"message": "Skill deleted", "data": deleted_skill.__dict__}), 200
        else:
            return jsonify({"error": "Skill not found"}), 404

@app.route('/resume/', methods=['GET'])
def spellcheck():
    '''
    Checks for spelling errors in Experience, Education, and Skill sections.
    Returns a list of corrections in the specified format.
    '''
    corrections = []

    # Function to check and collect corrections while preserving case
    def check_text(text):
        words = text.split()
        misspelled = spell.unknown(words)
        for word in misspelled:
            correction = spell.correction(word)
            if correction:
                # Preserve the case of the original word
                if word.istitle():
                    correction = correction.capitalize()
                elif word.isupper():
                    correction = correction.upper()
                else:
                    # If the word is lowercase or mixed case, keep the correction as is
                    correction = correction
                corrections.append({
                    "before": word,
                    "after": correction
                })

    # Check Experience titles, descriptions, and companies
    for exp in data['experience']:
        check_text(exp.title)
        check_text(exp.description)
        check_text(exp.company)

    # Check Education courses and schools
    for edu in data['education']:
        check_text(edu.course)
        check_text(edu.school)

    # Check Skill names
    for skill in data['skill']:
        check_text(skill.name)

    return jsonify(corrections), 200

