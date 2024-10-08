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


def test_delete_education():
    '''
    adds a new education and then deletes it, and checks if it's no longer in the list
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
    assert post_response.status_code == 200

    get_response = app.test_client().get('/resume/education')
    assert get_response.status_code == 200
    original_length = len(get_response.json)
    
    item_id = len(get_response.json) - 1

    print("Current education entries:", get_response.json)

    delete_response = app.test_client().delete(f'/resume/education/{item_id}')
    print(item_id)
    print("Delete response:", delete_response.status_code, delete_response.json)  

    get_response_after_delete = app.test_client().get('/resume/education')
    assert get_response_after_delete.status_code == 200
    assert len(get_response_after_delete.json) == original_length - 1  

def test_delete_experience():
    '''
    adds a new experience, deletes it, and checks that it's no longer in the list
    '''
    example_experience = {
        "title": "Backend Developer",
        "company": "Another Cool Company",
        "start_date": "January 2023",
        "end_date": "Present",
        "description": "Working on APIs",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/experience', json=example_experience)
    assert post_response.status_code == 200

    get_response = app.test_client().get('/resume/experience')
    assert get_response.status_code == 200
    original_length = len(get_response.json)

    item_id = len(get_response.json) - 1

    print("Current experience entries:", get_response.json)

    delete_response = app.test_client().delete(f'/resume/experience/{item_id}')
    print(item_id)
    print("Delete response:", delete_response.status_code, delete_response.json)

    assert delete_response.status_code == 200
    assert delete_response.json == {"message": "Experience deleted successfully."}

    get_response_after_delete = app.test_client().get('/resume/experience')
    assert get_response_after_delete.status_code == 200
    assert len(get_response_after_delete.json) == original_length - 1
