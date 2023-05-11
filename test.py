import requests
import json

API_KEY = "38a2fd4b1f346029a8726858c44e389c"
API_PASS = "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"

headers = {"Content-Type": "application/json; charset=utf-8"}
URL = "https://{}:{}@canhstore.myshopify.com/admin".format(API_KEY, API_PASS)

# Create collection:

def create_custom_collection():
    endpoint = "/api/2023-04/custom_collections.json"
    payload = {
    "custom_collection": {
        "body_html": "Custom Collections",
        "published_scope": "web",
        "title": "Custom Collections",
        }
    }
    response = requests.post(URL + endpoint, json=payload, headers=headers)
    return response.json()

def create_smart_collection():
    endpoint = "/api/2023-04/smart_collections.json"
    payload = {
	    "smart_collection": {
	    "title": "Smart Collection",
	    "rules": [
				{
					"column": "vendor",
					"relation": "equals",
					"condition": "50",
				}
			],
	    }
    }
    response = requests.post(URL + endpoint, json=payload, headers=headers)
    return response.json()

# Delete collection

def delete_custom_collection(collection_id):
    endpoint = f"/api/2023-04/custom_collections/{collection_id}.json"
    response = requests.delete(URL + endpoint)
    return response.status_code

def delete_smart_collection(collection_id):
    endpoint = f"/api/2023-04/smart_collections/{collection_id}.json"
    response = requests.delete(URL + endpoint)
    return response.status_code

# Create product

def create_product():
    endpoint = "/api/2023-04/products.json"
    new_data = {
        "product": {
            "title": "My new product",
            "body_html": "This is body",
            "vendor": "canhstore",
            "product_type": "Test",
            "status": "active",
            "published_scope": "global",
            "tags": "Test",
            "variants": [],
            "options": [],
            "images": [],
            "image": None,
        }
    }
    response = requests.post(URL + endpoint, json=new_data, headers=headers)
    return response.json()

def add_option(product_id):
    endpoint = f"/api/2023-04/products/{product_id}.json"
    new_data = {
        "product": {
            "variants": [
                    {
                        "option1": "Red",
                        "option2": "Medium"
                    },
                    {
                        "option1": "White",
                        "option2": "Large"
                    }
                ],
            "options": [
                    {
                        "name": "Color",
                        "position": 1,
                        "values": [
                            "Red",
                            "White"
                        ]
                    },
                    {
                        "name": "Size",
                        "position": 2,
                        "values": [
                            "Medium",
                            "Large"
                        ]
                    }
                ],
        }
    }
    response = requests.put(URL + endpoint, json=new_data, headers=headers)
    return response.status_code

#Update products

def update_price(variants_id: int):
    endpoint = f"/api/2023-04/variants/{variants_id}.json"
    update_data = {
        "variant": {
            "price": 55,
            "compare_at_price": 150,
            "inventory_management": "shopify",
            }
        }
    response = requests.put(URL + endpoint, json=update_data, headers=headers)
    return response

def update_image(product_id: int):
    endpoint = f"/api/2023-04/products/{product_id}/images.json"
    new_data = {
        "image": {
            "product_id": product_id,
            "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Desktop_computer_clipart_-_Yellow_theme.svg/281px-Desktop_computer_clipart_-_Yellow_theme.svg.png",
        }
    }
    response = requests.post(URL + endpoint, json=new_data)
    return response

def update_quantity(inventory_item_id, available):
    tracked = {
        "inventory_item": {
            "tracked": True
        }
    }
    requests.put(URL + f"/api/2023-04/inventory_items/{inventory_item_id}.json", json=tracked, headers=headers)

    endpoint_get_level = f"/api/2023-04/inventory_levels.json?inventory_item_ids={inventory_item_id}"

    inventory_level = requests.get(URL + endpoint_get_level, headers=headers)
    print(inventory_level.json())
    location_id = inventory_level.json()["inventory_levels"][0]["location_id"]

    qty = {
        "inventory_item_id": inventory_item_id,
        "location_id": location_id,
        "available": available,
    }

    endpoint_set_qty = "/api/2023-04/inventory_levels/set.json"

    response = requests.post(URL + endpoint_set_qty, json=qty, headers=headers)
    return response

def update_product(product, available):
    update_image(product['product']['id'])
    for variant in product['variants']:
        update_price(variant['id'])
        update_quantity(variant['inventory_item_id', available])


# Delete product

def delete_product(product_id: int):
    endpoint = f"/api/2023-04/products/{product_id}.json"
    response = requests.delete(URL + endpoint)
    if response.status_code == 200:
        return "Product is deleted!"
    else:
        return "Try again!"

# Create Customer

def create_customer():
    endpoint = "/api/2023-04/customers.json"
    payload = {
        "customer": {
            "first_name": "First",
            "last_name": "Last",
            "email": "customer@example.com",
            "phone": "+12345678902"
        }
    }
    response = requests.post(URL + endpoint, json=payload, headers=headers)
    return response.json()

def add_customer_address(customer_id):
    endpoint = f"/api/2023-04/customers/{customer_id}/addresses.json"
    new_address = {
        "customer_address": {
            "customer_id": customer_id,
            "first_name": "Samuel",
            "last_name": "de Champlain",
            "company": "Fancy Co.",
            "address1": "1 Rue des Carrieres",
            "address2": "Suite 1234",
            "city": "Montreal",
            "province": "Quebec",
            "country": "Canada",
            "zip": "G1R 4P5",
            "phone": "819-555-5555",
            "name": "Samuel de Champlain",
            "province_code": "QC",
            "country_code": "CA",
            "country_name": "Canada",
            "default": False
        }
    }
    response = requests.post(URL + endpoint, json=new_address, headers=headers)
    return response.status_code
# Delete Customer

def delete_customer(customer_id):
    endpoint = f"/api/2023-04/customers/{customer_id}.json"
    response = requests.delete(URL + endpoint)
    if response.status_code == 200:
        print('deleted!')
    else:
        print('try again!')
        
# Create an order

def add_order(customer_email):
    endpoint = "/api/2023-04/orders.json"
    payload = {
        "order":{
            "line_items": [
                {
                    "variant_id": 45185470038296,
                    "quantity": 2
                }
            ],
            "customer": {
                "email": customer_email,
            },
            "shipping_address": {
                "first_name": "Bob",
                "address1": "Chestnut Street 92",
                "phone": "+1(502)-459-2181",
                "city": "Louisville",
                "zip": "40202",
                "province": "Kentucky",
                "country": "United States",
                "last_name": "Norman",
                "address2": "",
                "company": None,
                "name": "Bob Norman",
                "country_code": "US",
                "province_code": "KY"
            }
        }
    }
    response = requests.post(URL + endpoint, json=payload, headers=headers)
    return response.json()

# Delete order

def delete_order(order_id):
    endpoint = f"/api/2023-04/orders/{order_id}.json"
    response = requests.delete(URL + endpoint)
    if response.status_code == 200:
        print('deleted!')
    else:
        print('try again!')
        
if __name__ == "__main__":
    #Create:
    custom_collection = create_custom_collection()
    smart_collection = create_smart_collection()
    product1 = create_product()
    product2 = create_product()
    option2 = add_option(product2['product']['id'])
    update_product(product1, 10)
    update_product(product2, 10)
    customer = create_customer()
    add_customer_address(customer['customer']['id'])
    order = add_order(customer['customer']['email'])
    
    #Delete:
    '''
    delete_custom_collection(custom_collection['custom_collection']['id'])
    delete_smart_collection(smart_collection['smart_collection']['id'])
    delete_product(product1['product']['id'])
    delete_product(product2['product']['id'])
    delete_customer(customer['customer']['id'])
    delete_order(order['order']['id'])
    '''