def test_root(client):
    end_point = "/"
    response = client.get(end_point)
    assert response.status_code == 200
    
def create_customer(client, auth_headers):
    customer_data = {
        "first_name": "SaleItem",
        "last_name": "Customer",
        "email": "saleitem.customer@gmail.com"
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


def create_product(client, auth_headers):
    product_data = {
        "name": "Sale Item Product",
        "sku": "SALE-ITEM-001",
        "price": 1500.00
    }

    response = client.post(
        "/products",
        json=product_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_create_sale_item(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 2
    assert float(data["unit_price"]) == 750.00

def test_create_sale_item_missing_sale_id_returns_422(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "product_id": product_id,
        "quantity": 2,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    
def test_create_sale_item_missing_product_id_returns_422(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "quantity": 2,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    
def test_create_sale_item_missing_quantity_returns_422(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    
def test_create_sale_item_missing_unit_price_returns_422(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 422

def test_create_sale_item_with_invalid_sale_id_returns_404(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "sale_id": 9999,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 404

def test_create_sale_item_with_invalid_product_id_returns_404(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "product_id": 9999,
        "quantity": 2,
        "unit_price": 750.00
    }
    response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert response.status_code == 404

def test_update_sale_item(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    product_id = create_product(client, auth_headers)
    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": 750.00
    }
    create_response = client.post(
        "/sale-items/",
        json=sale_item_data,
        headers=auth_headers
    )
    assert create_response.status_code == 201
    sale_item_id = create_response.json()["id"]
    update_data = {
        "quantity": 5,
        "unit_price": 800.00
    }
    response = client.put(
        f"/sale-items/{sale_item_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
        
def test_delete_payment_with_invalid_id_return_404(client, auth_headers):
    invalid_payment_id = 9999
    response = client.delete(
        f"/payments/{invalid_payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 404