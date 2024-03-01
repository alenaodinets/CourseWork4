from queue import Queue

from src.api_HH import HhVacancies
from src.vacancies import Vacancy
from src.save_file import SaveToJson, SaveToCsv, SaveToText
from typing import Type, Literal, Union


class StopUserProgram(Exception):
    """ Остановка пользовательской программы """


class EmptyResult(Exception):
    """ Ошибка пустого ответа """


class UserInteraction:
    """Взаимодействие с пользователем"""

    @classmethod
    def validate_int(cls, int_: str) -> bool:
        """Валидация строки, которая является числом"""
        if not int_.isdigit() or int(int_) < 0:
            print('Введи число, оно должно быть не меньше нуля')
            return False
        return True

    @classmethod
    def user_notification_choise(cls):
        print('Если нет, нажми Enter')
        print('Если да, то вводи любой символ')

    @classmethod
    def _ask_format(self, format: str,
                    mode: Literal['w', 'a'],
                    queue: Type[Queue]) -> None:
        """В зависимости от полученного числа делает действие
        Args:
            format (str): Формат сохранения
            mode (str): Тип записи
            queue (Type[Queue]): Очередь с объектами"""
        match format:
            case '1':
                SaveToJson(mode=mode).save_to_file(vacancy=queue)
            case '2':
                SaveToText(mode=mode).save_to_file(vacancy=queue)
            case '3':
                SaveToCsv(mode=mode).save_to_file(vacancy=queue)

    @classmethod
    def _ask_mode(self, mode: Literal['1', '2']) -> Literal['w', 'a']:
        """Выбор типа записи"""
        match mode:
            case '1':
                return "w"
            case '2':
                return 'a'

    @classmethod
    def save_to_file(cls,
                     name: Union[str, None],
                     page: Union[int, None],
                     per_page: Union[int, None],
                     convert_to_RUB: bool,
                     town: Union[str, None]):
        """Работа программы
        Args:
            name (Union[str, None]): Професcия
            page (Union[int, None]): Страница
            per_page (Union[int, None]): Количество объектов
            convert_to_RUB (bool): Конвертирование валюты
            town (Union[str, None]): Выбор города
        """
        per_page = int(per_page)
        user_page = int(page)
        while True:
            if per_page == 0:
                print('Таких вакансий нет(')
                break
            try:
                vacancies = HhVacancies(name=name, per_page=per_page, page=page, convert_to_RUB=convert_to_RUB,
                                        town=town)
                if len(vacancies.response) == 0:
                    raise EmptyResult
                print('Обработка закончена')
            except EmptyResult:
                per_page -= 1
                continue

            print(f'На странице {user_page}')
            print(f'Мы нашли {len(vacancies.response)} вакансий')
            print('Ты можешь отменить операцию')

            while True:
                print('\nВ какой тип файла ты хочешь сохранить результат?')
                print('1. JSON')
                print('2. TXT')
                print('3. CSV')
                choice_format = input()
                if not choice_format or not choice_format.isdigit():
                    break
                if 0 < int(choice_format) < 4:
                    while True:
                        print('\n1. Перепишем файл?')
                        print('2. Дополним файл?')
                        choice_mode = input()
                        if not choice_mode.isdigit():
                            continue
                        if cls.validate_int(choice_mode) and int(choice_mode) < 3:
                            choice_mode = cls._ask_mode(mode=choice_mode)
                        else:
                            continue
                        queue_models = Queue()
                        [queue_models.put(Vacancy.model_validate(item)) for item in vacancies.response]
                        cls._ask_format(format=choice_format, mode=choice_mode, queue=queue_models)
                        break

                    print('\nЗапишем в другом формате?')
                    cls.user_notification_choise()

                    if not input():
                        break
                    continue
                else:
                    return
            break
