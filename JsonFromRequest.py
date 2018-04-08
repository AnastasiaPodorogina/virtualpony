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
        self.transf_coeff = 1 - transfers * 0.5
        self.price_coeff = 0.
        self.weight = self.transf_coeff

    def ticket_list(self):
        return [self.curr, self.airline, self.price, self.transfers]

    def calculate_weight(self, value):
        self.weight += value

    def get_price(self):
        return self.price

    def set_price_coeff(self, min_price):
        self.price_coeff = min_price / self.price

    def get_price_coeff(self):
        return self.price_coeff

    def get_airline(self):
        return self.airline


def ticket_list(js):
    array_tk = js.get_json()["data"]
    t_list = list()
    for key, value in array_tk.items():
        t_list.append(Ticket(js.get_json()["currency"], value["airline"], value["price"], value["transfers"]))
    return t_list


def get_json_port():
    json_port = json.load(open("aviaport.json"))
    # print(json.dumps(json_port, indent=4, sort_keys=True))
    return json_port


def get_json_city():
    json_city = requests.get(url="http://api.travelpayouts.com/data/cities.json")
    js_c = json.dumps(json_city.json(), indent=4, sort_keys=True)
    city_dict = dict()
    for d in json_city.json():
        city_dict[d["name_translations"]["ru"]] = d["code"]
    return city_dict


def min_price(*args):
    price_list = list()
    for arg in args:
        price_list.append(arg.get_price())
    price_list.sort()
    return price_list[0]

def YOBANI_VROT(test_dict):
    js_cities = get_json_city()

    js = JsonFromRequest("2018-04", js_cities[test_dict["origin"]], js_cities[test_dict["destination"]])
    t_list = ticket_list(js)
    print(t_list)
    price_list = list()
    for arg in t_list:
        price_list.append(arg.get_price())
    price_list.sort()
    min = price_list[0]

    for tk in t_list:
        tk.set_price_coeff(int(min))

    coeffs = get_json_port()

    for arg in t_list:
        if arg.get_airline() in coeffs:
            d = coeffs[arg.get_airline()]
            arg.calculate_weight(d["bort_feed"]*0.01*int(test_dict["bort_feed"]))
            arg.calculate_weight(d['hand_clad'] * 0.01 * int(test_dict['hand_clad']))
            arg.calculate_weight(d['p_space'] * 0.01 * int(test_dict['p_space']))
            arg.calculate_weight(d["entertain"] * 0.01 * int(test_dict["entertain"]))
            arg.calculate_weight(d["clean"] * 0.01 * int(test_dict["clean"]))
            arg.calculate_weight(d["sells"] * 0.01 * int(test_dict["sells"]))
            arg.calculate_weight(d["staff_work"] * 0.01 * int(test_dict["staff_work"]))
            arg.calculate_weight(arg.get_price_coeff())
        else:
            arg.calculate_weight(0.5)
            arg.calculate_weight(arg.get_price_coeff())

    return t_list

