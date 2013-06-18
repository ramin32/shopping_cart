To Run
======

Configuration
-------------
1. sudo apt-get install python-virtualenv python-pip
2. cd shopping_cart
3. virtualenv ENV
4. source ENV/bin/activate
5. pip install -r requirements.txt
6. python manage.py syncdb
7. python manage.py runserver

Admin
-----
1. Fire up http://localhost:8000/admin
2. Login using credentials entered with syncdb
3. Add a few stores.
4. Add a few products.

Use
---
1. Point browser to http://<store_name>.lvh.me:8000
