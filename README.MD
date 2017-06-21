Python script using Selenium for placing orders on https://driedfruits.ro

Installation:
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

How to use:
./order.py [email] [password] [products].
  Ex: ./order.py John.Doe@example.com password products.txt

Obs: The fortmat of products file is:
  [quantity_1] [product_link_1]
  Ex: 3	https://driedfruits.ro/index.php?_route_=quinoa-alba-500g-
      1	https://driedfruits.ro/index.php?_route_=caju-crud-500-g-
