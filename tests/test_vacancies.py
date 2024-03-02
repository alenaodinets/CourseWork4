import pytest
from src.vacancies import Vacancy
from tests.conf import _test_model


@pytest.mark.vacancy
class TestVacancy:

    def test_vacancy(self, test_model):
        vacancy = Vacancy.model_validate(test_model)
        assert vacancy.area.model_dump() == {'name': 'Самара'}
