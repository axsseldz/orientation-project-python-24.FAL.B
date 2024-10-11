'''
Tests in Pytest
'''
from app import app, data
import pytest


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    item_id = int(post_response.json['id'])

    get_response = app.test_client().get('/resume/experience')
    assert get_response.status_code == 200
    assert get_response.json[item_id] == example_experience


def test_edit_experience():
    '''
    Update an existing experience and verify the update.
    '''
    experience_id = 0  

    updated_experience = {
        "title": "Senior Backend Developer",
        "company": "Tech Solutions Inc.",
        "start_date": "January 2021",
        "end_date": "Present",
        "description": "Developing and maintaining APIs",
        "logo": "tech-solutions-inc.png"
    }

    put_response = app.test_client().put(f'/resume/experience/{experience_id}', json=updated_experience)
    
    assert put_response.status_code == 200, f"Expected status code 200, got {put_response.status_code}"

    response_data = put_response.get_json()
    assert response_data == updated_experience, "Response data does not match the updated experience"

    assert data['experience'][experience_id].__dict__ == updated_experience, "Data not updated correctly in the application"


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    post_response = app.test_client().post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    item_id = int(post_response.json['index'])  # Changed from 'id' to 'index'

    get_response = app.test_client().get('/resume/education')
    assert get_response.status_code == 200
    assert get_response.json[item_id] == example_education

    # Clean up
    delete_response = app.test_client().delete(f'/resume/education/{item_id}')
    assert delete_response.status_code == 200


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/skill', json=example_skill)
    assert post_response.status_code == 201
    item_id = int(post_response.json['index'])  # Changed from 'id' to 'index'

    get_response = app.test_client().get('/resume/skill')
    assert get_response.status_code == 200
    assert get_response.json[item_id] == example_skill

    # Clean up
    delete_response = app.test_client().delete(f'/resume/skill/{item_id}')
    assert delete_response.status_code == 200


def delete_education():
    '''
    Add a new education and then delete it.
    
    Check that the education is no longer in the list.
    '''
    example_education = {
        "course": "Computer Science",
        "end_date": "July 2022",
        "grade": "80%",
        "logo": "updated-logo.png",
        "school": "University of Tech",
        "start_date": "September 2019"
    }

    added_item_id = int(app.test_client().post('/resume/education', json=example_education).json['index'])  # Changed from 'id' to 'index'

    delete_response = app.test_client().delete(f'/resume/education/{added_item_id}')
    assert delete_response.status_code == 200

    get_response = app.test_client().get(f'/resume/education/{added_item_id}')
    assert get_response.status_code == 404
    assert get_response.json['error'] == "Education not found"


def edit_education():
    '''
    Add a new education and then edit it.
    
    Check that the education is updated in the list.
    '''
    example_education = {
        "course": "Computer Science",
        "end_date": "July 2022",
        "grade": "80%",
        "logo": "updated-logo.png",
        "school": "University of Tech",
        "start_date": "September 2019"
    }

    edited_education = {
        "course": "NEW Computer Science",
        "end_date": "July 2022",
        "grade": "NEW 80%",
        "logo": "updated-logo.png",
        "school": "NEW University of Tech",
        "start_date": "September 2019"
    }

    post_response = app.test_client().post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    index = int(post_response.json['index'])  # Changed from 'id' to 'index'

    put_response = app.test_client().put(f'/resume/education/{index}', json=edited_education)
    assert put_response.status_code == 200

    get_response = app.test_client().get(f'/resume/education/{index}')
    assert get_response.status_code == 200
    assert get_response.json['course'] == edited_education['course']
    assert get_response.json['grade'] == edited_education['grade']
    assert get_response.json['school'] == edited_education['school']


def delete_skill():
    '''
    Add a new skill and then delete it.
    
    Check that the skill is no longer in the list.
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }
    
    post_response = app.test_client().post('/resume/skill', json=example_skill)
    assert post_response.status_code == 201
    added_item_id = int(post_response.json['index'])  # Changed from 'id' to 'index'
    
    delete_response = app.test_client().delete(f'/resume/skill/{added_item_id}')
    assert delete_response.status_code == 200
    
    get_response = app.test_client().get(f'/resume/skill/{added_item_id}')
    assert get_response.status_code == 404
    assert get_response.json['error'] == "Skill not found"
    

def edit_skill():
    '''
    Add a new skill and then edit it.
    
    Check that the skill is updated in the list.
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }
    
    edited_skill = {
        "name": "Python",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }
    
    post_response = app.test_client().post('/resume/skill', json=example_skill)
    assert post_response.status_code == 201
    index = int(post_response.json['index'])  # Changed from 'id' to 'index'

    put_response = app.test_client().put(f'/resume/skill/{index}', json=edited_skill)
    assert put_response.status_code == 200

    get_response = app.test_client().get(f'/resume/skill/{index}')
    assert get_response.status_code == 200
    assert get_response.json['name'] == edited_skill['name']


def test_spellcheck():
    '''
    Tests the spellcheck endpoint by introducing a spelling error and checking the correction.
    '''
    # Add an experience with a deliberate spelling error
    faulty_experience = {
        "title": "Software Developer",
        "company": "A Cool Comapny",  # 'Company' misspelled as 'Comapny'
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writting Python Code",  # 'Writing' misspelled as 'Writting'
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/experience', json=faulty_experience)
    assert post_response.status_code == 201
    experience_id = int(post_response.json['id'])

    # Perform spell check
    spellcheck_response = app.test_client().get('/resume/spellcheck')
    assert spellcheck_response.status_code == 200
    corrections = spellcheck_response.json

    # Expected corrections with correct casing
    expected_corrections = [
        {"before": "Comapny", "after": "Company"},
        {"before": "Writting", "after": "Writing"}
    ]

    # Check that all expected corrections are in the response
    for expected in expected_corrections:
        assert expected in corrections

    # Clean up by deleting the faulty experience
    delete_response = app.test_client().delete(f'/resume/experience/{experience_id}')
    assert delete_response.status_code == 200
