import socket
import sys
import os

# Функция для отправки и получения данных с сервера
def send_and_receive(a, b):
    # Создаем сокет
    s = socket.socket()
    # Устанавливаем соединение с сервером
    s.connect((os.environ['SERVER_ADDRESS'], int(os.environ['SERVER_PORT'])))
    # Отправляем данные на сервер
    s.sendall(str(a).encode())
    s.sendall(str(b).encode())
    # Получаем ответ от сервера
    data = s.recv(1024)
    # Закрываем соединение
    s.close()
    # Возвращаем полученные данные
    return data.decode()

# Функция для проверки суммы
def check_sum(a, b, c):
    # Вызываем функцию для отправки и получения данных с сервера
    data = send_and_receive(a, b)
    # Разделяем полученные данные на два числа
    a_prime, b_prime = data.split()
    # Проверяем, равна ли сумма чисел a_prime и b_prime числу c
    if int(a_prime) + int(b_prime) == c:
        print("Сумма верна")
        # Пишем результат в лог
        if '--log' in sys.argv:
            with open('/var/log/syslog', 'a') as f:
                f.write('Сумма верна\n')
    else:
        print("Сумма неверна")
        # Пишем результат в лог
        if '--log' in sys.argv:
            with open('/var/log/syslog', 'a') as f:
                f.write('Сумма неверна\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Не указан порт!")
    else:
        port = int(sys.argv[1])

    # Создаем сокет
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Связываем сокет с портом
    s.bind(('', port))

    # Слушаем порт
    s.listen(1)

    # Принимаем соединение
    conn, addr = s.accept()
    
    while True:
        # Получаем данные
        data = conn.recv(1024)

        # Проверяем данные на корректность
        try:
            a, b, c = map(int, data.split())
        except ValueError:
            print("Некорректные данные")
            return

        # Вызываем функцию для проверки суммы
        check_sum(a, b, c)

    # Закрываем соединение
    conn.close()

pass
