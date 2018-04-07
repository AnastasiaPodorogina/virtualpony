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


class Ticket:
	def __init__(self, curr, airline, price, transfers): 
		self.curr = curr
		self.airline = airline
		self.price = price
		self.transfers = transfers
		self.weight = 0

	def ticket_list(self):
		return [self.curr, self.airline, self.price, self.transfers]



if __name__ == "__main__":
	js = JsonFromRequest("2018-04", "MOW", "BCN")
	array_tk = js.get_json()["data"]
	ticket_list = list()
	for key, value in array_tk.items():
		ticket_list.append(Ticket(js.get_json()["currency"], value["airline"], value["price"], value["transfers"]))
	print (ticket_list)	
	#print(array_tk[0])
	#tk = Ticket(js.get_json()["currency"], array_tk[0])
	#print(json.dumps(js.get_json()["data"], indent=4, sort_keys=True))