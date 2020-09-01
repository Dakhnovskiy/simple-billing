# simple-billing
Simple billing service

## Заупуск приложения
`docker-compose up`

## Запуск тестов
`docker-compose -f docker-compose-test.yml build`

`docker-compose -f docker-compose-test.yml run --rm --entrypoint "python -m pytest -W ignore::DeprecationWarning" app`

## API:

**Создание клиента с кошельком**

`POST: /clients`

Пример запроса

    Media type: application/json
    Body: 
    {
        "name": "myLogin",
        "login": "Иванов Иван" 
    }

Пример ответа     
   
    {
      "login": "myLogin",
      "name": "Иванов Иван",
      "id": 3,
      "walletId": 2
    }

**Зачисление денежных средств на кошелек клиента**

`POST: /resupplies`

Пример запроса

    Media type: application/json
    Body: 
    {
        "walletId": 1,
        "amount": 500.5
    }

Пример ответа     
   
    {
      "walletId": 1,
      "amount": 500.5,
      "transactionNumber": "f1e0fb1b-0323-4e83-a69e-cffabb60b469",
      "walletBalance": 1001.0
    }

**Перевод денежных средств с одного кошелька на другой**

`POST: /resupplies`

Пример запроса

    Media type: application/json
    Body: 
    {
        "walletFromId": 1,
        "walletToId": 2,
        "amount": 1000
    }

Пример ответа     
   
    {
      "walletFromId": 1,
      "walletToId": 2,
      "amount": 1000.0,
      "transactionNumber": "1608015c-0754-413d-9ae2-d576cbffb621",
      "walletFromBalance": 1.0,
      "walletToBalance": 1000.0
    }


## Стек

* FastAPI - Вэб фреймворк
* Databases[asyncpg, SQLAlchemy] -  Абстракция для аснихронной работы с БД (берёт на себя управление пулом коннектов, транзакциями и т.д.)
* Alembic - Управление миграциями модели данных
* PostgreSQL - РСУБД
* Python 3.8 - Язык разработки


    