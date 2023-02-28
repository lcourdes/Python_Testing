import pytest


class TestShowSummary:
    def setup_method(self):
        self.valid_email = "test@test.co"
        self.invalid_email = "invalid@test.co"

    def test_valid_email_return_code_ok(self, client, mocker, tests_clubs):
        mocker.patch('server.clubs', tests_clubs)
        response = client.post('/showSummary', data={'email': self.valid_email})
        assert response.status_code == 200
        assert "Welcome, test@test.co" in response.data.decode()
    
    def test_invalid_email_handling(self, client, mocker, tests_clubs):
        mocker.patch('server.clubs', tests_clubs)
        response = client.post('/showSummary', data={'email': self.invalid_email})
        print(response.data.decode())
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()
    
    def test_no_email_handling(self, client, mocker, tests_clubs):
        mocker.patch('server.clubs', tests_clubs)
        response = client.post('/showSummary', data={'email': ''})
        print(response.data.decode())
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()
