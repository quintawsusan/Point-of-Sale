def test_root(client):
    end_point = "/"
    response = client.get(end_point)
    assert response.status_code == 200


def test_list_customers(client, auth_headers):
    end_point = "/customers"
    response = client.get(end_point, headers=auth_headers)
    assert response.status_code == 200


def test_create_customer(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())


def test_create_customer_with_missing_name_return_422(client, auth_headers):
    customer_data = {
        "email": "john.doe@example.com"
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())


def test_update_customer(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())

    updated_customer = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    }

    customer_id = response.json()["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json=updated_customer,
        headers=auth_headers
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "jane.doe@example.com"


def test_delete_customer(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())

    customer_id = response.json()["id"]

    response = client.delete(
        f"/customers/{customer_id}",
        headers=auth_headers
    )

    assert response.status_code == 204


def test_get_deleted_customer_returns_404(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())

    customer_id = response.json()["id"]

    response = client.delete(
        f"/customers/{customer_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    response = client.get(
        f"/customers/{customer_id}",
        headers=auth_headers
    )

    assert response.status_code == 404

def test_listing_customers_without_credentials_returns_401(client):
    response = client.get("/customers")
    assert response.status_code == 401

