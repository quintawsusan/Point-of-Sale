def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    
def test_create_user(client, auth_headers):
    user_data = {
        "username": "newuser",
        "password": "password123",
        "role": "cashier",
    }

    response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["role"] == "cashier"
    assert "id" in data  
    
def test_create_user_duplicate_username(client, auth_headers):
    user_data = {
        "username": "duplicateuser",
        "password": "password123",
        "role": "cashier",
    }
    response1 = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert response1.status_code == 201
    response2 = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Username already exists"

def test_create_user_missing_username(client, auth_headers):
    user_data = {
        "password": "password123",
        "role": "cashier",
    }

    response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert response.status_code == 422
    
def test_create_user_missing_password(client, auth_headers):
    user_data = {
        "username": "newuser",
        "role": "cashier",
    }

    response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )

    assert response.status_code == 422
    
def test_create_user_missing_role(client, auth_headers):
    user_data = {
        "username": "newuser",
        "password": "password123",
    }

    response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )

    assert response.status_code == 422
    
def test_read_user(client, auth_headers):
    user_data = {
        "username": "readuser",
        "password": "password123",
        "role": "cashier",
    }

    create_response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]

    read_response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert read_response.status_code == 200

    data = read_response.json()
    assert data["username"] == "readuser"
    assert data["role"] == "cashier"
    assert data["id"] == user_id  
    
def test_update_user(client, auth_headers):
    user_data = {
        "username": "updateuser",
        "password": "password123",
        "role": "cashier",
    }

    create_response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]

    update_data = {
        "username": "updateduser",
        "role": "admin",
    }

    update_response = client.put(
        f"/users/{user_id}",
        json=update_data,
        headers=auth_headers,
    )
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["username"] == "updateduser"
    assert data["role"] == "admin"
    assert data["id"] == user_id

def test_delete_user(client, auth_headers): 
    user_data = {
        "username": "deleteuser",
        "password": "password123",
        "role": "cashier",
    }

    create_response = client.post(
        "/users/",
        json=user_data,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]

    delete_response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    read_response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert read_response.status_code == 404
