Driedfruits-shopper helps you place collaborative orders on [Driedfruits](https://driedfruits.ro)

# Motivation:
You can share a file with your friends where they can write what they want to buy 
by specifying the quantity and the link. After that, one of you can add all the products 
in the cart automatically and place the order.
  
# Installation:
The script was tested only on Linux and it is assumed you have Python 3+ already installed.

`$ virtualenv venv`

`$ source venv/bin/activate`

`$ pip install -r requirements.txt`

# How to use:
`./order.py [email] [password] [products].`
 > Example:
 
 `./order.py John.Doe@example.com password products.txt`

Obs: The fortmat of products file is:
  `[quantity_1] [product_link_1]`
> Example:

3	https://driedfruits.ro/index.php?_route_=quinoa-alba-500g-

1	https://driedfruits.ro/index.php?_route_=caju-crud-500-g-
