def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_supplier(client, auth_headers):
    supplier_data = {
        "name": "Supplier A",
        "contact_info": "   123-456-7890",
        "address": "123 Main St",
    }    
    
def test_create_supplier_missing_name(client, auth_headers):
    supplier_data = {
        "contact_info": "123-456-7890",
        "address": "123 Main St",
    }
    
    response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )
    assert response.status_code == 422

def test_create_supplier_missing_contact_info(client, auth_headers):
    supplier_data = {
        "name": "Supplier A",
        "address": "123 Main St",
    }
    
    response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )
    assert response.status_code == 422

def test_create_supplier_missing_address(client, auth_headers):
    supplier_data = {
        "name": "Supplier A",
        "contact_info": "123-456-7890",
    }
    
    response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )
    assert response.status_code == 422
    
def test_read_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "XYZ Suppliers",
        "contact_info": "0723456789",
    }

    create_response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    response = client.get(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == supplier_id
    assert data["company_name"] == "XYZ Suppliers"
    assert data["contact_info"] == "0723456789"
    
def test_update_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "Old Supplier",
        "contact_info": "0700000000",
    }
    create_response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    supplier_id = create_response.json()["id"]
    update_data = {
        "company_name": "New Supplier",
        "contact_info": "0711111111",
    }

    response = client.put(
        f"/suppliers/{supplier_id}",
        json=update_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "New Supplier"
    assert data["contact_info"] == "0711111111"
    
def test_delete_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "Delete Supplier",
        "contact_info": "0799999999",
    }
    create_response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    supplier_id = create_response.json()["id"]
    response = client.delete(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204

def test_get_deleted_supplier_returns_404(client, auth_headers):
    supplier_data = {
        "company_name": "Deleted Supplier",
        "contact_info": "0788888888",
    }
    
    create_response = client.post(
        "/suppliers/",
        json=supplier_data,
        headers=auth_headers,
    )

    assert create_response.status_code == 201
    supplier_id = create_response.json()["id"]
    delete_response = client.delete(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 204
    response = client.get(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
    )
    assert response.status_code == 404