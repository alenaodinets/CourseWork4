from src.user_inter import UserInteraction, StopUserProgram


def main():

    while True:
        print('Какую професcию ты ищешь?')
        prof = input()
        if not prof:
            print('Ну же, выбери профессию!')
            continue

        print('\nВ каком именно городе хотел бы работать?')
        print('Если нет конкретного города, жми Enter')
        town = input()
        if not town:
            town = None

        while True:
            print('\nCколько вакансий тебе показать?')
            print('Выведется топ по зарплатам\n')
            vacancies = input()
            if not UserInteraction.validate_int(vacancies):
                continue

            print('\nВыбирай любую страницу каталога\n')
            page = input()
            if not UserInteraction.validate_int(page):
                continue

            print('\nПереведем любую иностранную валюту в рубли?\n')
            UserInteraction.user_notification_choise()
            convert = input()
            if not convert:
                convert = False
            else:
                convert = True

            print('\nОбрабатываем, ожидайте')

            try:
                UserInteraction.save_to_file(name=prof, page=page, per_page=vacancies, convert_to_RUB=convert,
                                             town=town)

            except StopUserProgram:
                break

            print('\nПоищем ещё?')
            print('Изменим  страницу и количество вакансий?')
            UserInteraction.user_notification_choise()

            if not input():
                break
            continue

        print('\nПосморим другую профессию?')
        print('Посмотрим другой город?')
        UserInteraction.user_notification_choise()

        if not input():
            print('\nМы надеемся, что ты нашел, что искал! А если нет - будем ждать снова) До встречи!')
            break
        continue


if __name__ == '__main__':
    main()

