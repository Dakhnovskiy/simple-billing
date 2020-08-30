# simple-billing
Simple billing service

## Заупуск приложения
`docker-compose up`

## Запуск тестов
`docker-compose -f docker-compose-test.yml build`

`docker-compose -f docker-compose-test.yml run --rm --entrypoint "python -m pytest -W ignore::DeprecationWarning" app`
