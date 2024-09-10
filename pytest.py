import requests

def test_image_processing():
    files = {'file': open('app/test_image.jpg', 'rb')}
    response = requests.post('http://localhost:8000/recognize', files=files)
    assert response.status_code == 200
    assert 'expected_output' in response.json()  # Adjust based on your expected response
