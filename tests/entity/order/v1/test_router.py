from starlette.testclient import TestClient


def get_address_dict():
    return {
        "address_1": "test address_1",
        "city": "test city",
        "state_province": "test state_province",
        "country": "test country",
        "postal_code": "60654",
        "timezone": "test timezone",
        "latitude": 41.88287152401032,
        "longitude": -87.623321533746,
    }


def get_order_dict(address):
    return {
        "id": "1234",
        "name": "ipad",
        "price": 712.54,
        "pickup_address": address,
        "dropoff_address": address,
    }


def assert_valid_order(address_dict, response):
    response_json = response.json()
    assert len(response_json["order_number"]) == 6
    assert response_json["name"] == "ipad"
    assert response_json["price"] == 712.54
    pickup_address = response_json["pickup_address"]
    assert pickup_address["address_1"] == address_dict["address_1"]
    assert pickup_address["city"] == address_dict["city"]
    assert pickup_address["state_province"] == address_dict["state_province"]
    assert pickup_address["country"] == address_dict["country"]
    assert pickup_address["postal_code"] == address_dict["postal_code"]
    assert pickup_address["timezone"] == address_dict["timezone"]
    assert pickup_address["latitude"] == address_dict["latitude"]
    assert pickup_address["longitude"] == address_dict["longitude"]


class TestOrderRouter:
    def test_create_order(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)

        response = client.post("api/v1/order", json=order_dict)

        if response.status_code != 201:
            print(response.json())

        assert response.status_code == 201
        assert_valid_order(address_dict, response)

    def test_create_order_error(self, client: TestClient):
        address_dict = get_address_dict()
        address_dict["postal_code"] += "123123"
        order_dict = get_order_dict(address_dict)
        order_dict["price"] = None

        response = client.post("/api/v1/order", json=order_dict)

        assert response.status_code == 422
        assert response.json()["errors"] == [{'msg': 'Input should be a valid number',
                                              'source': 'body/price',
                                              'title': 'Request Validation Error'},
                                             {'msg': 'String should have at most 10 characters',
                                              'source': 'body/pickup_address/postal_code',
                                              'title': 'Request Validation Error'},
                                             {'msg': 'String should have at most 10 characters',
                                              'source': 'body/dropoff_address/postal_code',
                                              'title': 'Request Validation Error'}]

    def test_get_order(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)
        response = client.post("/api/v1/order", json=order_dict)
        order_id = response.json()["id"]

        response2 = client.get(f"/api/v1/order/{order_id}")
        if response2.status_code != 200:
            print(response2.json())

        assert response2.status_code == 200
        assert_valid_order(address_dict, response2)

    def test_get_order_error(self, client: TestClient):
        response = client.get("/api/v1/order/123")

        assert response.status_code == 404
        assert response.json()["errors"] == [{
            "title": "Not Found Error",
            "msg": "No row was found when one was required"
        }]

    def test_get_order_by_address(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)
        response = client.post("/api/v1/order", json=order_dict)
        address_id = response.json()["dropoff_address"]["id"]

        response2 = client.get(f"/api/v1/order/address/{address_id}")
        if response2.status_code != 200:
            print(response2.json())

        assert response2.status_code == 200
        assert_valid_order(address_dict, response2)

    def test_update_order(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)
        response = client.post("/api/v1/order", json=order_dict)
        order_id = response.json()["id"]
        order_dict["name"] = "iphone"

        response2 = client.put(f"/api/v1/order/{order_id}", json=order_dict)

        assert response2.status_code == 200
        assert order_id == response2.json()["id"]
        assert response2.json()["name"] == "iphone"

    def test_list_order(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)

        for i in range(10):
            order_dict["name"] = f"order {i}"
            client.post("/api/v1/order", json=order_dict)

        response = client.get("/api/v1/order?page=1&size=6&sort=name&order=ASC")

        assert response.status_code == 200
        assert len(response.json()["data"]) == 6
        assert response.json()["total_count"] == 10

    def test_list_order_error(self, client: TestClient):
        address_dict = get_address_dict()
        order_dict = get_order_dict(address_dict)

        for i in range(10):
            order_dict["name"] = f"order {i}"
            client.post("/api/v1/order", json=order_dict)

        response = client.get("/api/v1/order?page=1&size=6&sort=test&order=ASC")

        assert response.status_code == 422
        assert response.json()["errors"] == [{
            'title': 'Attribute Error',
            'msg': "type object 'OrderOrm' has no attribute 'test'"
        }]
