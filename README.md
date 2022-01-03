# Flask_podari_s_lyubov_final_exam
Storage Warehouse
Users which do not have a profile yet or haven't signed into the website, are able to see limited resources.

Non-Signed in users:

load only site and can see only list of Category and Products

Signed in users:

have functionality to manage categories and products - CRU; have functionality to manage increase and decrease of quantities with their delivery price; can see current quantities and average delivery price;

Only admin have rights to:

delete products and categories - CRUD;


## Register a New User

### Request
POST /register/

### Response
HTTP/1.1 201 OK
Status: 201 OK
Connection: close
Content-Type: application/json

{
    "token": "eyJ......w9NGcz9zpJosOE"
}



## Login exist User

### Request
POST /login/

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "role": "user",
    "token": [
    "token": "eyJ......w9NGcz9zpJosOE",
        2
    ]
}




## Create exist User as Admin

### Request
POST /admins/create-admin/5

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "role": "admin"
}





## Get a list of Category

### Request
GET /category/

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

[
    {
        "id": 1,
        "category_name": "Test"
    },
    {
        "id": 5,
        "category_name": "Test1"
    }
]






## Create a Category
POST /category/

### Response
HTTP/1.1 201 OK
Status: 201 OK
Connection: close
Content-Type: application/json

{
    "id": 11,
    "category_name": "Test"
}






## Edit a Category
PUT /category/id

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "id": 1,
    "category_name": "Test1"
}






## Delete a Category
DELETE /category/id

### Response
HTTP/1.1 204 OK
Status: 204 OK
Connection: close
Content-Type: application/json






## Display all products in one Category
GET /category/id

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

[
    {
        "product_delivery_price": 16.0,
        "product_code": "99-99999",
        "product_description": "Test",
        "product_image": "https://exambucketpodarisl......tral-1.amazonaws.com/e3d02d8a-feae-4f7c-a10e-6423361d6614.jpg",
        "product_name": "Test Test",
        "id": 12,
        "product_type_id": 5,
        "product_quantity": 20,
        "category_name": "Test"
    },
    {
        "product_delivery_price": 16.0,
        "product_code": "99-9999",
        "product_description": "Test1",
        "product_image": "https://exambucketpod.....1.amazonaws.com/315101d2-9fc9-46b6-b2c3-61624877fb46.jpg",
        "product_name": "Test Test",
        "id": 13,
        "product_type_id": 5,
        "product_quantity": 20,
        "category_name": "Test Test"
    }
]







## Get a list of Product

### Request
GET /products/

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json


{
    "count": 2,
    "limit": 4,
    "next": "",
    "previous": "",
    "results": [
        {
            "category_name": "Test",
            "product_code": "99-999999",
            "product_image": "https://examb........bov.s3.eu-central-1.amazonaws.com/315101d2-9fc9-46b6-b2c3-61624877fb46.jpg",
            "product_name": "Test Test",
            "product_quantity": 20
        },
        {
            "category_name": "Test",
            "product_code": "99-9999",
            "product_image": "https://exam.......eu-central-1.amazonaws.com/e3d02d8a-feae-4f7c-a10e-6423361d6614.jpg",
            "product_name": "Test Test1",
            "product_quantity": 20
        }
    ],
    "start": 1
}







## Create a Product
POST /products/

### Response
HTTP/1.1 204 OK
Status: 204 OK
Connection: close
Content-Type: application/json

{
    "product_code": "01-4029",
    "product_name": "Test sdsaf",
    "product_quantity": 20,
    "product_delivery_price": 16,
    "product_description": "Test sfdfs",
    "product_image": "/9j/4AA.................iiigAooooAKKKKACiiigAooooAKKKKAP/9k=",
    "image_extension": "jpg",
    "product_type_id": 5
}





## Edit a Product
PUT /products/id

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "product_delivery_price": 16,
    "product_code": "99-999",
    "product_image": "https://exa......bov.s3.eu-central-1.amazonaws.com/9787a30e-ec74-45f5-b354-bb8153608aa0.jpg",
    "product_name": "Test",
    "product_quantity": 20
}






## Edit a Product Quantity
PUT /products/edit-quantity/id

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "product_delivery_price": 14,
    "product_code": "99-9999999",
    "product_image": "https://exambuck......entral-1.amazonaws.com/e3d02d8a-feae-4f7c-a10e-6423361d6614.jpg",
    "product_name": "Test",
    "product_quantity": 30
}







## Delete a Product
DELETE /products/id

### Response
HTTP/1.1 204 OK
Status: 204 OK
Connection: close
Content-Type: application/json






## Display details for One Product
GET /products/id

### Response
HTTP/1.1 200 OK
Status: 200 OK
Connection: close
Content-Type: application/json

{
    "product_delivery_price": 16,
    "product_code": "99-9999",
    "product_description": "Test",
    "product_image": "https://exambucket.....-central-1.amazonaws.com/e3d02d8a-feae-4f7c-a10e-6423361d6614.jpg",
    "product_name": "Test Test",
    "id": 12,
    "product_type_id": 5,
    "product_quantity": 20,
    "category_name": "Test"
}



