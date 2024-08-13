## socialsphere


# 1.Run docker:
    To run all services:
                --docker compose up -d --build 
    To run particular services:
                --docker compose up -d --build <service-name>

# 2.Run Django:
    To migrate models:
                --python manage.py makemigration
                --python manage.py migrate
    To Start django in dev version:
                --python manage.py runserver 0.0.0.0:8000
    
# 3.Api calls:
    With postman:
                -- Added postman collection in following path('apps/django/socialsphere.postman_collection.json')
    With swagger-ui:
                --Created swagger ui to test apis on ui use following link('http://127.0.0.1:7000/schema/swagger-ui/)
#### swagger-api-test
![Alt text](apps/images/api_test.png)

    
# 4.Api Docs:
    With Swagger:
                -- Use following link to see documentation for all APIs('http://127.0.0.1:7000/schema/redoc/')

# 5.To access Db:
    Pgadmin:
                -- Connect postgress server with pgadmin to access database in UI
                -- credential for pgadmin 
                            user name = admin@admin.com
                            password  = admin
                -- credential for postgress
                            user name = ssuser
                            password  = Admin@123
![Alt text](apps/images/pgadmin.png)

#### swagger-docs

![Alt text](apps/images/api_docs.png)


## Tools Used
![Django](https://img.shields.io/badge/Django-4.2.15-092E20?logo=django&logoColor=092E20&labelColor=44B78B) 

![Python](https://img.shields.io/badge/Python-3.10.14-FFD343?logo=python&logoColor=3776AB&labelColor=306998) 

![Docker](https://img.shields.io/badge/Docker-26.1.4-0db7ed?logo=docker&logoColor=2496ED&labelColor=384D54) 

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?logo=postgresql&logoColor=FFFFFF&labelColor=0064a5) 

![Git](https://img.shields.io/badge/Git-2.30-F1502F?logo=git&logoColor=F05032&labelColor=E44C30) 

![Linux](https://img.shields.io/badge/Linux-Ubuntu%2020.04-E95420?logo=ubuntu&logoColor=E95420&labelColor=DD4814)

