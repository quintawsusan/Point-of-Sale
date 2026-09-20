def test_root(client):
    end_point = "/"  #arrange
    response = client.get(end_point)  #act
    assert response.status_code == 200  #assert

def test_list_products(client, auth_headers):
    end_point = "/products"  #arrange
    response = client.get(end_point, headers=auth_headers)  #act
    assert response.status_code == 200  #assert

def test_create_product(client, auth_headers):
    product_data ={
      "name": "coca",
      "sku": "SKU123",
      "price": 10.99 
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    

def test_update_product(client, auth_headers):

    product_data ={
      "name": "coca",
      "sku": "SKU123",
      "price": 10.99 
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    
    updated_product= {
      "name": "Fanta",
      "sku": "SKU123",
      "price": 10.99
    }
    product_id = response.json()["id"]
    response = client.put(f"/products/{product_id}", json=updated_product, headers=auth_headers)
    assert response.json()["name"] == "Fanta"
    
def test_delete_product(client, auth_headers):
    
    product_data ={
      "name": "coca",
      "sku": "SKU123",
      "price": 10.99 
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = response.json()["id"]
    client.delete(f"/products/{product_id}", headers=auth_headers)
    
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 404
    
def test_create_product_with_missing_name_return_422(client, auth_headers):
    product_data = {
      "sku": "SKU123",
      "price": 10.99 
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 422
    

def test_listing_products_without_credentials_returns_401(client):
    response = client.get("/products")
    assert response.status_code == 401
    


    