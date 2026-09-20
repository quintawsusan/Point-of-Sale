def test_root(client):
    end_point = "/"
    response = client.get(end_point)
    assert response.status_code == 200
    
def create_customer(client, auth_headers):
    customer_data = {
        "first_name": "Sale",
        "last_name": "Customer",
        "email": "sale.customer@gmail.com"
    }
    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_sale(client, auth_headers):
    customer_id = create_customer(client, auth_headers)
    sale_data = {
        "total_amount": 1500.00,
        "customer_id": customer_id,
        "user_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]

def test_create_sale(client, auth_headers):
    customer_id = create_customer(client, auth_headers)
    sale_data = {
        "total_amount": 1500.00,
        "customer_id": customer_id,
        "user_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == "1500.00" or float(data["total_amount"]) == 1500.00
    assert data["customer_id"] == customer_id
    assert data["user_id"] == 1
    print(data)


def test_create_sale_with_missing_total_amount_return_422(client,auth_headers):
    sale_data = {
        "customer_id": 1,
        "user_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_create_sale_with_missing_user_id_return_422(client,auth_headers):
    sale_data = {
        "total_amount": 1500.00,
        "customer_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_create_sale_without_customer_id(client,auth_headers):
    sale_data = {
        "total_amount": 1500.00,
        "user_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] is None
    assert data["user_id"] == 1
    print(data)

def test_create_sale_with_empty_total_amount_return_422(client,auth_headers):
    sale_data = {
        "total_amount": "",
        "customer_id": 1,
        "user_id": 1
    }
    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_update_sale(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    update_data = {
        "total_amount": 2000.00,
        "user_id": 1
    }
    response = client.put(
        f"/sales/{sale_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["total_amount"]) == 2000.00
    assert data["user_id"] == 1
    print(data)

def test_list_sales(client, auth_headers):
    response = client.get(
        "/sales",
        headers=auth_headers
    )
    assert response.status_code == 200
    print(response.json())


def test_delete_sale(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.delete(
        f"/sales/{sale_id}",
        headers=auth_headers
    )
    assert response.status_code == 204


def test_delete_sale_with_invalid_id_return_404(client,auth_headers):
    response = client.delete(
        "/sales/9999",
        headers=auth_headers
    )
    assert response.status_code == 404
    print(response.json())