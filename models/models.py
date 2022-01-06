"""
Это внутренние представления объектов БД для питона.
Например, можно вызвать SELECT * FROM client;
Получим ответ (1, "88005553535", "Vasya", "Pupkin")
Чтобы удобно работать с этими данными, их можно запихнуть в питоновский класс
Еще одно преимущество, что можно добавить к классу методы, которые смогут что-то делать с этими данными
Например, в Contract можно добавить метод is_expired(), который проверит, актуален ли договор
Позже в контроллерах можно выводить только актуальные договоры, где is_expired() вернет False
"""

from datetime import datetime
from typing import Optional
from flask_app.models.base_model import BaseModel

class Client(BaseModel):
    table_name = 'client'

    def __init__(self, phone: str, first_name: str, last_name: str, id: Optional[int] = None):
        self.id = id
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        

class Address(BaseModel):
    table_name = 'address'

    def __init__(self, address: str, id: Optional[int] = None):
        self.id = id
        self.address = address

class ClientAddresses(BaseModel):
    table_name = 'client_addresses'

    def __init__(self, client: Client, address: Address, id: Optional[int] = None):
        self.id = id
        self.client = client
        self.address = address

class Contract(BaseModel):
    table_name = 'contract'

    def __init__(self, 
                 client: Client, 
                 address: Address, 
                 date: str, 
                 status: str, 
                 description: str, 
                 document: str, 
                 sum: int,
                 id: Optional[int] = None):
        self.id = id
        self.client = client
        self.address = address
        self.date = date
        self.status = status
        self.description = description
        self.document = document
        self.sum = sum