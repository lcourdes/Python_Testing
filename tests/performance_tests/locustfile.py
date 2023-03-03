from locust import HttpUser, task

class PerformanceTests(HttpUser):
    @task
    def index(self):
        self.client.get('/')
    
    @task 
    def showSummary(self):
        self.client.post('/showSummary', {'email': "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('/book/Spring Festival/Simply Lift')
    
    @task 
    def purchasePlaces(self):
        self.client.post('/purchasePlaces', {'competition': 'Spring Festival', "club": 'Simply Lift', 'places': '2'})

    @task
    def clubs(self):
        self.client.get('/clubs')

    @task
    def logout(self):
        self.client.get('/logout')