def test_root(client):
    end_point = "/"
    response = client.get(end_point)
    assert response.status_code == 200
    
def create_customer(client, auth_headers):
    customer_data = {
        "first_name": "Payment",
        "last_name": "Customer",
        "email": "payment.customer@example.com"
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


def create_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    payment_data = {
        "sale_id": sale_id,
        "amount": 1500.00,
        "payment_type": "cash"
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]

def test_create_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    payment_data = {
        "sale_id": sale_id,
        "amount": 1500.00,
        "payment_type": "cash"
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sale_id"] == sale_id
    assert float(data["amount"]) == 1500.00
    assert data["payment_type"] == "cash"
    print(data)


def test_create_payment_with_missing_sale_id_return_422(client, auth_headers):
    payment_data = {
        "amount": 1500.00,
        "payment_type": "cash"
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_create_payment_with_missing_amount_return_422(client,auth_headers):
    sale_id = create_sale(client, auth_headers)
    payment_data = {
        "sale_id": sale_id,
        "payment_type": "cash"
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_create_payment_with_missing_payment_type_return_422(client,auth_headers):
    sale_id = create_sale(client, auth_headers)
    payment_data = {
        "sale_id": sale_id,
        "amount": 1500.00
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    print(response.json())


def test_create_payment_with_invalid_sale_id_return_404(client,auth_headers):
    payment_data = {
        "sale_id": 9999,
        "amount": 1500.00,
        "payment_type": "cash"
    }
    response = client.post(
        "/payments",
        json=payment_data,
        headers=auth_headers
    )
    assert response.status_code == 404
    print(response.json())


def test_list_payments(client, auth_headers):
    response = client.get(
        "/payments",
        headers=auth_headers
    )
    assert response.status_code == 200
    print(response.json())


def test_update_payment(client, auth_headers):
    payment_id = create_payment(client, auth_headers)
    update_data = {
        "amount": 2000.00,
        "payment_type": "mpesa"
    }
    response = client.put(
        f"/payments/{payment_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["amount"]) == 2000.00
    assert data["payment_type"] == "mpesa"
    print(data)


def test_delete_payment(client, auth_headers):
    payment_id = create_payment(client, auth_headers)
    response = client.delete(
        f"/payments/{payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 204

def test_get_deleted_payment_returns_404(client,auth_headers):
    payment_id = create_payment(client, auth_headers)
    response = client.delete(
        f"/payments/{payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 204
    response = client.get(
        f"/payments/{payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_payment_with_invalid_id_return_404(client,auth_headers):
    invalid_payment_id = 9999
    response = client.delete(
        f"/payments/{invalid_payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 404

def test_listing_payments_without_credentials_returns_401(client):
    response = client.get("/payments")
    assert response.status_code == 401