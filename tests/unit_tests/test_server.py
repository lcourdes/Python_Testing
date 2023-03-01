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
    def test_enough_points_for_purchase_places(self, client):
        response = client.post('/purchasePlaces', data={'club': 'name', 'competition': 'name', 'places': '1'})
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()

    def test_not_enough_points_for_purchase_places(self, client):
        response = client.post('/purchasePlaces', data={'club': 'name', 'competition': 'name', 'places': '2'})
        assert response.status_code == 200
        assert "You do not have enough points. Try again" in response.data.decode()
    
    def test_should_not_purchase_more_than_12_places(self, client):
        response = client.post('/purchasePlaces', data={'club': 'name2', 'competition': 'name2', 'places': '13'})
        assert response.status_code == 200
        assert "You can&#39;t purchase more than 12 places." in response.data.decode()
    
    def test_should_not_purchase_more_than_available_places(self, client):
        response = client.post('/purchasePlaces', data={'club': 'name2', 'competition': 'name', 'places': '6'})
        assert response.status_code == 200
        assert "You can&#39;t purchase more than available places." in response.data.decode()

    def test_should_redeem_correct_clubs_points(self, client):
        response = client.post('/showSummary', data={'email': 'test2@test.co'})
        assert 'Points available: 13' in response.data.decode()
        response = client.post('/purchasePlaces', data={'club': 'name2', 'competition': 'name2', 'places': '1'})
        assert response.status_code == 200
        assert 'Points available: 12' in response.data.decode()
    
    def test_should_redeem_correct_competitions_points(self, client):
        response = client.post('/showSummary', data={'email': 'test2@test.co'})
        assert 'Number of Places: 15' in response.data.decode()
        response = client.post('/purchasePlaces', data={'club': 'name2', 'competition': 'name2', 'places': '1'})
        assert response.status_code == 200
        assert 'Number of Places: 14' in response.data.decode()


class TestBook:
    def test_should_return_code_ok(self, client):
        response = client.get('/book/name/name')
        assert '<form action="/purchasePlaces" method="post">' in response.data.decode()
        assert response.status_code == 200
        
    def test_no_competition_found(self, client):
        response = client.get('/book/notaname/name')
        assert 'Something went wrong-please try again' in response.data.decode()
        assert response.status_code == 200

    def test_no_club_found(self, client):
        response = client.get('/book/name/notaname')
        assert 'Something went wrong-please login' in response.data.decode()
        assert response.status_code == 200
    
    def test_no_booking_for_past_event(self, client):
        response = client.get('/book/past event/name')
        assert 'This is a past event. Please choose a future competition.' in response.data.decode()
        assert response.status_code == 200
