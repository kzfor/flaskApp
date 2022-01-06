"""
Базовый класс для моделей, который содержит общий функционал
"""
from typing import Optional


class BaseModel:
    table_name = None

    def __init__(self, id: Optional[int]):
        self.id = id

    def get_table_name(self):
        return self.table_name

    def __str__(self):
        description = f"Model from table [{self.table_name}] with fields: ["
        fields = vars(self)
        for key, value in fields.items():
            description += f"{key}={value}, "
        description = description[:-2] + "]"
        return description

