from pydantic import BaseModel, ConfigDict, Field, HttpUrl, computed_field
from abc import ABC
from typing import Union, Dict, List


class AbstractVacancies(BaseModel, ABC):
    name: str
    area: Dict
    professional_roles: List
    salary: Dict
    experience: Dict
    employment: Dict
    schedule: Dict
    alternate_url: HttpUrl
    snippet: Dict
    employer: Dict


class Area(BaseModel):
    name: Union[str, None]


class ProfessionalRoles(BaseModel):
    name: Union[str, None]


class Salary(BaseModel):
    from_: Union[int, None] = Field(alias='from')
    to: Union[int, None]
    currency: str


class Experience(BaseModel):
    name: Union[str, None]


class Employment(BaseModel):
    name: Union[str, None]


class Schedule(BaseModel):
    name: Union[str, None]


class Snippet(BaseModel):
    requirement: Union[str, None]
    responsibility: Union[str, None]


class Employer(BaseModel):
    name: Union[str, None]
    alternate_url: Union[HttpUrl, None]


class Vacancy(AbstractVacancies):
    """Cериализации и обработка данных """

    model_config = ConfigDict(frozen=True)

    name: str
    area: Area
    professional_roles: List[ProfessionalRoles]
    salary: Salary
    experience: Experience
    employment: Employment
    schedule: Schedule
    alternate_url: HttpUrl
    snippet: Snippet
    employer: Employer

    def __le__(self, other):
        """ Метод сравнения "меньше или равно" вакансий между собой по зарплате. """

        return self.salary <= other.salary

    def __ge__(self, other):
        """ Метод сравнения "больше или равно" вакансий между собой по зарплате. """

        return self.salary >= other.salary
