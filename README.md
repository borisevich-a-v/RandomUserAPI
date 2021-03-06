# Work with the external API

## Description

The web application is designed to work with the API https://randomuser.me/.
The table with data of downloaded users and the form for additional downloading users from the API are located on the main page.
There are three ways to get a full profile of a user: directly by a user's id (http://homepage/user_id), click on a URL in
a cell in the last table's column or get a random user's profile by clicking on "Random user" in the main menu.

There are abilities to edit a user's profile and create a new user. Open user's profile and select
"Change text" or "Change photo" for editing a user's profile. To create a new one, select "New user” in the main menu.

## How to run

1. Install Docker and Docker-compose
2. Download docker-compose.yml from this repository
3. Change SECRET_KEY in docker-compose.yml
4. Select directory with docker-compose.yml
5. Up docker-compose:
```
docker-compose up
```

# Работа с внешним API

## Описание
Веб приложение служит для работы с API https://randomuser.me/. 
На главной странице размещена таблица с данными загруженных пользователей и форма для
дополнительной загрузки пользователей c API.
Доступ к полному профилю пользователя доступен по адресу: http://homepage/user_id. 
Перейти к пользователю можно перейти напрямую по адресу пользователя, из таблицы на
главной странице, или с помощью кнопки "Random user" в главном меню.

Существует возможность редактирования пользователя и создание нового. 
Для редактирования необходимо перейти в профиль пользователя и выбрать "Change text" или 
"Change photo". Для создания нового выбрать в главном меню "New user".

## Установка
1. Установить Docker, Docker-compose
2. Скачать файл docker-compose.yml из текущего репозитория.
3. В файле docker-compose.yml изменить значение SECRET_KEY
4. Перейти в директорию с файлом docker-compose.yml 
5. Поднять docker-compose


## Задание
Необходимо разработать приложение для взаимодействия с внешним API: https://randomuser.me/.
Основная страница приложение представляет из себя простую web страницу с полем для ввода количества человек, которых необходимо загрузить с API, а также таблица с информацией обо всех людях, содержащихся в базе данных.

Нужно учесть, что количество человек может быть огромным, соответственно отображать сразу всю информацию может быть не очень хорошей идеей.

Требования:
1) Таблица с информацией должна содержать следующую информацию: пол человека, имя, фамилию, номер телефона, email, место проживания, фото в небольшом разрешении, а также дополнительное поле по нажатию на которое можно перейти на страницу пользователя из пункта 5.
2) Вся информация о людях хранится в базе данных. 
3) Использовать любой веб фреймворк и базу данных (выбор необходимо будет обосновать)
4) Когда сервер стартует, то он должен загрузить 1000 случайных людей из API.
5) Можно получить информацию о конкретном человеке обратившись к нему по адресу: http://homepage/user_id
6) Информацию на странице с конкретным человеком можно редактировать.
7) Можно создать новую запись о человеке и сохранить её в базе данных.
8) Можно получить информацию о случайном человеке обратившись к нему по адресу: http://homepage/random. При обновлении этой страницы каждый раз с сервера должна возвращаться новая информация. 
9) Выполнение программы должно происходить внутри docker контейнера.
10) Интерфейс должен выглядеть более или менее приятно
11) Покрыть функциональность тестами в разумных пределах. Тесты с внешним API должны быть замоканы.

