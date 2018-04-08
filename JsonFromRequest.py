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

    # self.curr = curr

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

    def calculate_weight(self, value):
        self.weight += value


def ticket_list(js):
    array_tk = js.get_json()["data"]
    t_list = list()
    for key, value in array_tk.items():
        t_list.append(Ticket(js.get_json()["currency"], value["airline"], value["price"], value["transfers"]))
    return t_list


def get_json_port():
    json_port = json.load(open("aviaport.json"))
    print(json.dumps(json_port, indent=4, sort_keys=True))
    return json_port


def get_json_city():
    json_city = requests.get(url="http://api.travelpayouts.com/data/cities.json")
    js_c = json.dumps(json_city.json(), indent=4, sort_keys=True)
    city_dict = dict()
    for d in json_city.json():
        city_dict[d["code"]] = d["name_translations"]["ru"]
    return json_city.json()


if __name__ == "__main__":
    js = JsonFromRequest("2018-04", "MOW", "BCN")
    get_json_city()
    get_json_port()

# print(array_tk[0])
# tk = Ticket(js.get_json()["currency"], array_tk[0])
# print(json.dumps(js.get_json()["data"], indent=4, sort_keys=True))
