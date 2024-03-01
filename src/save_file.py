from pydantic import BaseModel, DirectoryPath
from abc import ABC, abstractmethod
from queue import Queue
from typing import Literal, Type
from csv import DictWriter


class AbstractSaveFile(BaseModel, ABC):
    """Абстрактный класс для работы с файлами"""

    mode: str

    @abstractmethod
    def save_to_file(self, vacancy, path):
        pass

    @abstractmethod
    def change_to_file(self, path):
        pass

    @abstractmethod
    def delete_of_file(self, path):
        pass


class SaveToJson(AbstractSaveFile):
    """Класс для работы с файлами JSON"""

    mode: Literal['w', 'a'] = 'w'

    def save_to_file(self, vacancy: Type[Queue],
                     path: DirectoryPath = 'vacancies.json') -> None:
        """Сохранeние файла JSON
        Args:
            vacancy (Type[Queue]): Очередь, которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'.
        """
        with open(path, self.mode, encoding='utf-8') as file:
            while vacancy.qsize() != 0:
                item = vacancy.get()
                file.write(item.model_dump_json(indent=2))

    def change_to_file(self, path):
        pass

    def delete_of_file(self, path):
        pass


class SaveToText(AbstractSaveFile):
    """Класс для работы с файлами TXT"""

    mode: Literal['w', 'a'] = 'w'

    def save_to_file(self, vacancy: Type[Queue],
                     path: DirectoryPath = 'vacancies.txt') -> None:
        """Сохранeние файла TXT
        Args:
            vacancy (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'."""
        with open(path, self.mode, encoding='utf-8') as file:
            while vacancy.qsize() != 0:
                item = vacancy.get()
                file.write(item.model_dump_json().replace(('{'), '\n').replace('}', '\n'))

    def change_to_file(self, path):
        pass

    def delete_of_file(self, path):
        pass


class SaveToCsv(AbstractSaveFile):
    """Класс для работы с файлами CSV"""

    mode: Literal['w', 'a'] = 'w'

    def save_to_file(self, vacancy: Type[Queue],
                     path: DirectoryPath = 'vacancies.csv'):
        """Сохранeние файла CSV
        Args:
            vacancy (Type[Queue]): Очередь которая имеет ссылки на вакансии
            path (DirectoryPath, optional): _description_. Defaults to 'vacancies.json'."""
        with open(path, self.mode, encoding='utf-8') as file:
            file_csv = DictWriter(file, ('name', 'area', 'professional_roles', 'salary', 'alternate_url'))
            file_csv.writeheader()
            while vacancy.qsize() != 0:
                item = vacancy.get()
                file_csv.writerow(
                    item.model_dump(exclude=('experience', 'schedule', 'snippet', 'employment', 'employer')))

    def change_to_file(self, path):
        pass

    def delete_of_file(self, path):
        pass


class SaveToDb(AbstractSaveFile):
    """Класс для работы с базой данных"""

    def save_to_file(self, vacancy, path):
        pass

    def change_to_file(self, path):
        pass

    def delete_of_file(self, path):
        pass

