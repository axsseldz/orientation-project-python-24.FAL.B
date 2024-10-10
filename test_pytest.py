'''
Tests in Pytest
'''
from app import app


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

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


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
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education


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

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill


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

    added_item_id = app.test_client().post('/resume/education', json=example_education).json['id']

    app.test_client().delete(f'/resume/education/{added_item_id}')

    response = app.test_client().get(f'/resume/education/{added_item_id}')
    assert response.json['message'] == "Education not found"


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

    index = app.test_client().post('/resume/education', json=example_education).json['id']
    app.test_client().put(f'/resume/education/{index}', json=edited_education)
    response = app.test_client().get(f'/resume/education/{index}')

    assert response["course"] == edited_education["course"]

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
    
    added_item_id = app.test_client().post('/resume/skill', json=example_skill).json['id']
    
    app.test_client().delete(f'/resume/skill/{added_item_id}')
    
    response = app.test_client().get(f'/resume/skill/{added_item_id}')
    assert response.json['message'] == "Skill not found"
    
    
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
    
    index = app.test_client().post('/resume/skill', json=example_skill).json['id']
    app.test_client().put(f'/resume/skill/{index}', json=edited_skill)
    response = app.test_client().get(f'/resume/skill/{index}')
    
    assert response["name"] == edited_skill["name"]