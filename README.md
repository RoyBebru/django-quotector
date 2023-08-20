# django-quotector


To initialize postgress database you need to press red button in admin panel (see the following pic):


![alt text](https://github.com/RoyBebru/django-quotector/blob/main/ScrapeButton.png)


To work correctly there is needed to add quotector/.env file like the following:
```
SECRET_KEY=django-insecure-this-string-must-be-changed-with-true-secret-chars

DATABASE_NAME=HERO_DATABASE_NAME
DATABASE_USER=HERO_DATABASE_USERNAME
DATABASE_PASSWORD=HERO_DATABASE_PASSWORD
DATABASE_HOST=HERO_DATABASE_HOST
DATABASE_PORT=HERO_DATABASE_PORT

EMAIL_HOST=HERO_EMAIL_HOST
EMAIL_PORT=HERO_EMAIL_PORT
EMAIL_HOST_USER=HERO@EMAIL.COM
EMAIL_HOST_PASSWORD=HERO_EMAIL_PASSWORD
```
