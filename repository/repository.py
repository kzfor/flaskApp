"""
Самое веселье. Это набор классов для того, чтобы "маппить" модели в БД и обратно.
Можно делать все это в самих моделях, но тогда нарушается SRP (Single Responsibility Principle)
Короче, именно тут модели записываются и достаются из БД
"""

import inspect

from sqlite3 import Cursor

from flask_app.models.models import *
from flask_app.utils.db.connection import DatabaseConnection

class Repository:
    model = BaseModel

    def __init__(self):
        self.connection = DatabaseConnection()

    def save(self, model: BaseModel):
        cur: Cursor = self.connection.get_cursor()
        try:
            fields = vars(model).copy()
            fields.pop("id")
            cur.execute(f'INSERT INTO {model.table_name} ({",".join([field for field in fields])}) VALUES ({"?," * (len(fields) - 1) + "?"});',
                    [val for val in fields.values()])
            return cur.lastrowid
        except Exception as e:
            print(f'Ошиб очка save: {str(e)}')
        finally:
            cur.close()
            self.connection.commit()

    def update(self, id: int, model: BaseModel):
        cur: Cursor = self.connection.get_cursor()
        try:
            fields = vars(model).copy()
            fields.pop("id")
            cur.execute(f'UPDATE {model.table_name} SET {", ".join([f"{x}=?" for x in fields])} WHERE id = {id};', [val for val in fields.values()])
        except Exception as e:
            print(f'Ошиб очка update: {str(e)}')
        finally:
            cur.close()
            self.connection.commit()
    
    def get_all(self):
        models: list[self.model] = []
        cur: Cursor = self.connection.get_cursor()
        try:
            cur.execute(f'SELECT * FROM {self.model.table_name};')
            db_records = cur.fetchall()
            fields = inspect.signature(self.model.__init__)
            fields = [x for x in fields.parameters if x != "self" and x != "id"]

            for record in db_records:
                model_obj = {'id': record[0]}
                for i, field in enumerate(fields):
                    model_obj[field] = record[i + 1]
                models.append(self.model(**model_obj))
            return models
        except Exception as e:
            print(f'Ошиб очка get_all: {str(e)}')
        finally:
            cur.close()
    
    def get_by_id(self, id: int):
        cur: Cursor = self.connection.get_cursor()
        try:
            cur.execute(f'SELECT * FROM {self.model.table_name} WHERE id=?;',(id,))
            record = cur.fetchone()
            fields = inspect.signature(self.model.__init__)
            fields = [x for x in fields.parameters if x != "self" and x != "id"]
            model_obj = {'id': record[0]}
            for i, field in enumerate(fields):
                    model_obj[field] = record[i + 1]
            return self.model(**model_obj)
        except Exception as e:
            print(f'Ошиб очка get_by_id: {str(e)}')
        finally:
            cur.close()
    
    def delete(self, id: int):
        cur: Cursor = self.connection.get_cursor()
        try:
            cur.execute(f'DELETE FROM {self.model.table_name} WHERE id=?;', (id,))
        except Exception as e:
            print(f"Ошиб очка delete: {str(e)}")
        finally:
            cur.close()
            self.connection.commit()

class AddressRepository(Repository):
    model = Address

    def __init__(self):
        super().__init__()

class ClientAddressesRepository(Repository):
    model = ClientAddresses

    address_rep = AddressRepository()

    def __init__(self):
        super().__init__()

    def save(self, client_address: ClientAddresses):
        cur: Cursor = self.connection.get_cursor()
        address_id = self.address_rep.save(client_address.address)
        client_address.address.id = address_id
        try:
            cur.execute(f"INSERT INTO {self.model.table_name} (client_id, address_id) VALUES (?, ?);", 
                        (client_address.client.id, client_address.address.id))
        except Exception as e:
            print(f"Client address save ошиб очка {str(e)}")
        finally:
            cur.close()
            self.connection.commit()
    
    def get_addresses_by_client_id(self, id: int) -> "list[Address]":
        cur: Cursor = self.connection.get_cursor()
        try:
            cur.execute(f"SELECT * FROM {self.model.table_name} WHERE client_id = ?;",
                        (id,))
            db_records = cur.fetchall()
            models: list[Address] = []
            for record in db_records:
                address = self.address_rep.get_by_id(record[2])
                models.append(address)
            return models
        except Exception as e:
            print(f"Ошиб очка get_address_by_client_id {str(e)}")
        finally:
            cur.close()

    def delete(self, id: int):
        record: ClientAddresses = self.get_by_id(id)
        self.address_rep.delete(record.address)
        super().delete(id)

class ClientRepository(Repository):
    model = Client
    client_address_rep = ClientAddressesRepository()

    def __init__(self):
        super().__init__()

    def add_address(self, client: Client, address: Address):
        self.client_address_rep.save(ClientAddresses(client, address))

    def get_addresses(self, id: int) -> "list[Address]":
           return self.client_address_rep.get_addresses_by_client_id(id)

class ContractRepository(Repository):
    model = Contract

    address_rep = AddressRepository()
    client_rep = ClientRepository()

    def __init__(self):
        super().__init__()

    def get_by_client_id(self, id: int):
        cur: Cursor = self.connection.get_cursor()
        client = self.client_rep.get_by_id(id)
        try:
            cur.execute(f"SELECT * FROM {self.model.table_name} WHERE client_id = ?", (id,))
            db_records = cur.fetchall()
            models: list[Contract] = []
            for record in db_records:
                contract = Contract(client,
                                    self.address_rep.get_by_id(record[2]),
                                    record[3],
                                    record[4],
                                    record[5],
                                    record[6],
                                    record[7],
                                    id=record[0])
                models.append(contract)
            return models
        except Exception as e:
            print(f"get_by_client_id oshib o4ka {str(e)}")
        finally:
            cur.close()

    def save(self, contract: Contract):
        cur: Cursor = self.connection.get_cursor()

        try:
            cur.execute(f"INSERT INTO {self.model.table_name} (client_id, address_id, date, status, description, document, sum) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (contract.client.id, contract.address.id, contract.date, contract.status, contract.description, contract.document, contract.sum))
        except Exception as e:
            print(f"Oshib ochka contract.save: {str(e)}")
        finally:
            cur.close()
            self.connection.commit()