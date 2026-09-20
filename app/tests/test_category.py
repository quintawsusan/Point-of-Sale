def test_root(client):
    end_point = "/"
    response = client.get(end_point)
    assert response.status_code == 200

def test_create_category(client, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())

def test_create_category_with_missing_name_return_422(client, auth_headers):    
    category_data = {
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())
    
def test_create_category_with_missing_description_return_422(client, auth_headers):    
    category_data = {
        "name": "Electronics"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())

def test_create_category_with_empty_name_return_422(client, auth_headers):
    category_data = {
        "name": "",
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())
    
def test_create_category_with_empty_description_return_422(client, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": ""
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())

def test_list_categories(client, auth_headers):
    end_point = "/categories"
    response = client.get(end_point, headers=auth_headers)
    assert response.status_code == 200

def test_update_category(client, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    print(response.json())
    
    
def test_update_category_with_empty_name_return_422(client, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    category_id = response.json()["id"]

    update_data = {
        "name": "",
        "description": "Updated description"
    }

    response = client.put(
        f"/categories/{category_id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())

def test_update_category_with_empty_description_return_422(client, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
    }

    response = client.post(
        "/categories",
        json=category_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    category_id = response.json()["id"]

    update_data = {
        "name": "Updated Name",
        "description": ""
    }

    response = client.put(
        f"/categories/{category_id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 422
    print(response.json())

def test_delete_category(client, auth_headers): 
    category_data = {
          "name": "Electronics",
          "description": "Electronic devices and gadgets"
     }
    
    response = client.post(
          "/categories",
          json=category_data,
          headers=auth_headers
     )
    
     
    assert response.status_code == 201
    category_id = response.json()["id"]
    
    response = client.delete(
          f"/categories/{category_id}",
          headers=auth_headers
    )
    
    assert response.status_code == 204
    
def test_delete_category_with_invalid_id_return_404(client, auth_headers):
    invalid_category_id = 9999

    response = client.delete(
        f"/categories/{invalid_category_id}",
        headers=auth_headers
    )

    assert response.status_code == 404
    print(response.json())