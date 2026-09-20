def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def create_customer(client, auth_headers):
    customer_data = {
        "first_name": "Receipt",
        "last_name": "Customer",
        "email": "receipt.customer@gmail.com",
    }

    response = client.post(
        "/customers",
        json=customer_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_sale(client, auth_headers):
    customer_id = create_customer(client, auth_headers)

    sale_data = {
        "total_amount": 1500.00,
        "customer_id": customer_id,
        "user_id": 1,
    }

    response = client.post(
        "/sales",
        json=sale_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-001",
    }

    response = client.post(
        "/receipts/",
        json=receipt_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-001",
    }

    response = client.post(
        "/receipts/",
        json=receipt_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sale_id"] == sale_id
    assert data["receipt_number"] == "REC-001"
    assert "id" in data


def test_create_receipt_missing_sale_id(client, auth_headers):
    receipt_data = {
        "receipt_number": "REC-002",
    }

    response = client.post(
        "/receipts/",
        json=receipt_data,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_receipt_missing_receipt_number(client, auth_headers):
    sale_id = create_sale(client, auth_headers)

    receipt_data = {
        "sale_id": sale_id,
    }

    response = client.post(
        "/receipts/",
        json=receipt_data,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_receipt_with_invalid_sale_id(client, auth_headers):
    receipt_data = {
        "sale_id": 9999,
        "receipt_number": "REC-003",
    }

    response = client.post(
        "/receipts/",
        json=receipt_data,
        headers=auth_headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Sale 9999 not found"


def test_list_receipts(client, auth_headers):
    create_receipt(client, auth_headers)

    response = client.get(
        "/receipts/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_receipt(client, auth_headers):
    receipt_id = create_receipt(client, auth_headers)

    response = client.get(
        f"/receipts/{receipt_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == receipt_id
    assert "sale_id" in data
    assert "receipt_number" in data


def test_read_receipt_with_invalid_id(client, auth_headers):
    response = client.get(
        "/receipts/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Receipt not found"

def test_update_receipt_with_invalid_sale_id(client, auth_headers):
    receipt_id = create_receipt(client, auth_headers)

    update_data = {
        "sale_id": 9999,
        "receipt_number": "REC-INVALID",
    }

    response = client.put(
        f"/receipts/{receipt_id}",
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Sale 9999 not found"


def test_delete_receipt(client, auth_headers):
    receipt_id = create_receipt(client, auth_headers)

    response = client.delete(
        f"/receipts/{receipt_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/receipts/{receipt_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_delete_receipt_with_invalid_id(client, auth_headers):
    response = client.delete(
        "/receipts/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Receipt not found"


def test_receipt_endpoints_require_authentication(client):
    response = client.get("/receipts/")

    assert response.status_code == 401