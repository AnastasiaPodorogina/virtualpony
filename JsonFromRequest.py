import requests
import json

API_TOKEN = 'ee755899ac1d914b2477e8203e7c7584'
API_REQUEST = 'http://api.travelpayouts.com/v1/prices/calendar?depart_date={0}&origin={1}&destination={2}&calendar_type=departure_date&token={3}'

class JsonFromRequest:
	"""docstring for ClassName"""
	def __init__(self, d_date, origin, destination):
		self.request = API_REQUEST
		self.token = API_TOKEN
		self.origin = origin
		self.destination = destination
		self.d_date = d_date
		#self.curr = curr

	def get_json(self):
		r = requests.get(url=self.request.format(self.d_date, self.origin, self.destination, self.token))	
		return r.json()

if __name__ == "__main__":
	js = JsonFromRequest("2018-04", "MOW", "BCN")
	print(js.get_json())