import pytest


class TestShowSummary:
    def setup_method(self):
        self.valid_email = "test@test.co"
        self.invalid_email = "invalid@test.co"

    def test_valid_email_return_code_ok(self, client):
        response = client.post('/showSummary', data={'email': self.valid_email})
        assert response.status_code == 200
        assert "Welcome, test@test.co" in response.data.decode()
    
    def test_invalid_email_handling(self, client):
        response = client.post('/showSummary', data={'email': self.invalid_email})
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()
    
    def test_no_email_handling(self, client):
        response = client.post('/showSummary', data={'email': ''})
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()


class TestPurchasePlaces:
    def test_enough_points_for_purchase_places(self, client, tests_clubs, test_competitions):
        response = client.post('/purchasePlaces', data={'club': 'name', 'competition': 'name', 'places': '1'})
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()

    def test_not_enough_points_for_purchase_places(self, client, tests_clubs, test_competitions):
        response = client.post('/purchasePlaces', data={'club': 'name', 'competition': 'name', 'places': '2'})
        assert response.status_code == 200
        assert "You do not have enough points. Try again" in response.data.decode()