# neo4j-node-work-api: API для работы с базой данных Neo4J
Neo4j Node Work API - API, позволяющее взаимодействовать с узлами графовой базы данных neo4j. <br>
## Стек
Python 3.10 <br>
FastAPI <br>
Neomodel <br>
Pydantic <br>
## Функционал:
### GET-методы: <br>
- Получение информации по всем узлам базы данных (/nodes/) <br>
- Получение информации по конкретному узлу при указании значения параметра "node_id" (nodes/{node_id}) <br>
### POST-метод: <br>
- Занесение в БД узла и связей (/graph/insert) <br>
### DELETE-метод: <br>
- Удаление узла и его связей по его node_id (/nodes/{node_id}) <br>
## Использование API
1. Клонируйте репозиторий: <br>
```git clone https://github.com/evgeshkins/neo4j-node-work-api.git . ``` <br>
2. Создайте виртуальное окружение: <br>
```python -m venv venv``` <br>
либо <br>
```py -m venv venv``` <br>
3. Активируйте виртуальное окружение: <br>
На Windows: <br>
```.venv\Scripts\activate``` <br>
На Linux: <br>
```source venv/bin/activate``` <br>
4. Установите библиотеки: <br>
```pip install -r requirements.txt``` <br>
5. Создайте файл .env в корне проекта и внесите туда значения следующих переменных: <br>
```python
DB_USER="имя пользователя БД"
DB_PASSWORD="пароль от БД"
SECRET_API_TOKEN ="значение токена для API"
```
6. Запустите сервер: <br>
```uvicorn main:app --reload``` <br>
Сервер успешно запущен по адресу localhost:8000! <br>
## Описание точек доступа API:
1. Получение всех узлов из БД:
``` GET \nodes\ ``` <br>
Пример ответа: <br>
```python
[
    {"id": 1, "label": "User"},
    {"id": 2, "label": "Group"}
]
```
2. Получение определенного узла по его node_id:
``` GET \nodes\{node_id}\ ```
Пример ответа: <br>
```python
[
    {"n": {"id": 1, "name": "John Doe"}, "r": {"type": "Follow"}, "m": {"id": 2, "name": "Jane Doe"}}
]
``` 
3. Добавление узла и связей <br>
``` POST /insert/graph/ ```
Тело запроса:
```python
"node": {
            "node_id": 34444,
            "label": "User",
            "name": "Жорик Мажорик",
            "screen_name": "jmurik",
            "sex": 2,
            "home_town": "San Francisco"
        },
        "relationships": [
            {
                "id": 34444,
                "type": "Follow",
                "end_node_id": 2548
            }]
```
Пример ответа: <br>
```{"status": "Узел и связи добавлены.", "response": "Узел и связи добавлены."}```
4. Удаление узла и его связей: <br>
``` DELETE /nodes/{node_id} ``` <br>
Пример ответа: <br>
```{"status": "Узел удален.", "response": "Узел удален."}```
## Тестирование
Для запуска тестов достаточно написать: <br>
```pytest tests.py``` <br>
При этом сервер должен быть запущен.
