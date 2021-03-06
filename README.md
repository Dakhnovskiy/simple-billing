# simple-billing
Simple billing service

## Запуск приложения
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

`POST: /transfers`

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


## Особенности реализации
* Конфигруация настраивается из переменных окружения
* Масштабировать приложение внутри контейнера можно заданием колчества воркеров `uvicorn`
* Миграции модели данных накатываются при старте приложения в `entrypoint.sh`
* При запуске тестов миграции модели данных накатываются фикстурой
* При запуске тестов подключения к БД находится в режиме `force_rollback=True`, т.е. при закрытии каждого коннекта все изменения откатываются
* API позволяет создавать клиентов с одним кошельком - это единая операция
* Модель данных предполагает наличие у клиента нескольких кошельков (такая модель выглядит более расширяемой)
* Информация о клиентах хранится в таблице `clients`
* Информация о кошельках и остатках средств на них хранится в таблице `wallets`
* История операций сохраняется в таблицах `transactions` и `wallets_operations`, API на получение истории не реализовано, т.к. этого не требовало задание
* Операции проводятся в одной транзакции, чтобы недопустить несогласованности данных
* В таблице `wallets` есть ограничение(constraint) на положительный баланс, таким образом за соблюдением логической целостности следит СУБД (т.е. операция перевода средств не выполнится, если это приводит к отрицательному балансу клиента) 
* API "в онлайн режиме" отдаёт клиенту информацию о совершённой операции (информация об остатках, успешность операции)
* Если предположить, что клиенту не нужна информация о совершенной операции "здесь и сейчас", то я бы предложил вариант реализации с очередью заданий. Это позволило бы отдельно масштабировать интерфейс с HTTP-API и воркеры, выполняющие операции, также мы бы получили прирост в производительности HTTP-API и возможность задавать приоритеты на выполнение операций
    