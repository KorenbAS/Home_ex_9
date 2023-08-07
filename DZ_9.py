import os
# списки можливих команд
EXIT_CMD = ['good bye', 'close', 'exit'] 
NO_ARGS_CMD = ['hello', 'show all']
WITH_ARGS_CMD = ['add', 'change', 'phone']
EXIT_ANSWER = 'Good bye!'

# повідомлення запрошення
INVITATION = """ 
------------------------------------------------------------------------------------------------------------------------------------------------
|                                                PHONE BOOK BOT WELCOMES YOU!                                                                  |
------------------------------------------------------------------------------------------------------------------------------------------------
|    COMMANDS:                                                                                                                                 |
|    o	"hello"                                                                                                                                |
|    o	"add ..." По этой команде бот сохраняет в памяти новый контакт.                                                                        |
|        Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.                                                        |
|    o	"change ..." По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта.                                   |
|        Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.                                                        |
|    o	"phone ...." По этой команде бот выводит в консоль номер телефона для указанного контакта.                                             |
|        Вместо ... пользователь вводит имя контакта, чей номер нужно показать.                                                                |
|    o	"show all". По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.                                       |
|    o	"good bye", "close", "exit" по любой из этих команд бот завершает свою роботу.                                                         |
------------------------------------------------------------------------------------------------------------------------------------------------"""


def input_error(func):
    """ Декоратор обробник помилок """
    def wrapper(*args, **kwargs):
        # намагаємось виконати хандлер
        try:
            result = func(*args, **kwargs)
        # відловлюємо помилки
        except SyntaxError:
            result = 'Your command is incorrect!'
        except KeyError:
            result = 'Name was not found or incorrect!'
        except ValueError:
            result = 'Phone number is incorrect!'
        return result
    return wrapper


def hello_handler(*args):
    """ Обробник команди hello """
    return 'How can I help you?'


def exit_handler(*args):
    """ Обробник команди на вихід """
    return EXIT_ANSWER


def show_all_handler(dictionary):
    """ Обробник команди вивести всі записи """
    # випадок : словнки не пустий
    if len(dictionary.items()) > 0:
        # список рядків
        strings = []
        # обходимо книгу записів
        for k, v in dictionary.items():
            # друкуємо ключ значення в рядок
            strings.append(f'{k} - {v}\n')
        # повертаємо всі рядки об'єднані в один великий загальний 
        return ''.join(strings)
    else:
        return 'Phone book is EMPTY!'


@input_error
def parser(expression):
    """ Розбиває рядок на команду та можливі аргументи """
    # розіб'ємо рядок по пробілам та зберемо заново всі частки
    expression = ' '.join(expression.split())
    # випадок : якщо рядок є командою з одного із списків
    if expression in EXIT_CMD or expression in NO_ARGS_CMD:
        # повертаємо вираз як команду і пустий список аргументів
        return expression, []
    # інашке розбиваємо по пробілу
    args = expression.split()
    # випадок : якщо кількість частин від 1 до 3включно
    if len(args) > 1 and len(args) < 4 and args[0] in WITH_ARGS_CMD:
        # повертаємо першу частину як команду а інщі частини як агрументи
        return args[0], args[1:]
    else:
        # інакше кидаємо виключення
        raise SyntaxError


@input_error
def add_handler(dictionary, *args):
    """ Обробка додавання в книгу  """
    # випадок : якщо кількість агрументівн не коректна
    if len(args) != 2:
        raise SyntaxError
    
    name, tel = args
    # випадок номер не число
    if not tel.isnumeric():
        raise ValueError
    # випадок : ім'я закоротке
    if len(name) < 2:
        raise KeyError
    # додамо в словник
    dictionary[name] = tel
    return f'{name} was included into phone book!'


@input_error
def phone_handler(dictionary, *args):
    """ Відображення заданого запису по імені """
    # випадок : аргументів забагато або мало
    if len(args) != 1:
        # кидаємо виключення
        raise SyntaxError
    name = args[0]
    #  випадок : ім'я відсутне в книгі
    if name not in dictionary.keys():
        raise KeyError
    # повертаємо рядок
    return f'{name} - {dictionary[name]}'


@input_error
def change_handler(dictionary, *args):
    """ Обробка команди внесення змін по номеру """
    # випадок : аргументи не коректні
    if len(args) != 2:
        raise SyntaxError
    name = args[0]
    tel = args[1]

    # випадок : ім'я відсутне в книзі
    if name not in dictionary.keys():
        raise KeyError

    # випадок : номер не коректний
    if not tel.isnumeric():
        raise ValueError

    # робимо зміни
    dictionary[name] = tel
    return f'{name} was updated!'


def main():
    # пуста книга словник
    phone_book = {}

    # словник обробників команд
    # команда - назва функції
    handlers = {
        'hello': hello_handler,
        'good bye': exit_handler,
        'close': exit_handler,
        'exit': exit_handler,
        'show all': show_all_handler,
        'add': add_handler,
        'phone': phone_handler,
        'change': change_handler
    }

    # безкінечнйи цикл запитів
    while True:
        # очистка консолі
        os.system('cls')
        # друк привітання запрошення
        print(INVITATION)
        # читаємо рядок команд
        # відразу переводимо в нижній регістр
        expression = input('->').lower().strip()
        # якщо рядок пустийт то все заново
        if len(expression) == 0:
            continue
        # отримуємо результат парсингу
        answer = parser(expression)
        # випадок : якщо результат не рядок з помилкою
        if not isinstance(answer,str):
            # розпаковуємо кортеж команд і аргументів
            cmd, args = answer 
            # викликаємо хандлер по назві команди та передаємо в ного словник-книгу + агрументи
            answer = handlers[cmd](phone_book, *args)
        # друкуємо отриманий результат
        print(answer)
        # пауза
        os.system('pause')

        # випадок : отримано команду на вихід
        if answer == EXIT_ANSWER:
            break


if __name__ == "__main__":
    main()
