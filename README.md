## 💻 Технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)

## Описание проекта Django_sprint4
Данный проект представляет из себя соц. сеть, где люди могут выкладывать свои посты, а так же комментировать посты друг друга

## Инструкция как развернуть проект:

- Нужно склонировать проект из репозитория командой:
```bash
git clone  git@github.com:BogdanBrock/django_sprint4.git
```

- Находясь в проекте, перейти в папку под названием blogicum:
```bash
cd blogicum
```

- Выполнить миграции для создания базы данных
```bash
python manage.py migrate
```

- Запускаем сервер локально через команду
```bash
python manage.py runserver
```

- Загружаем данные в базу данных
```bash
python manage.py loaddata db.json
```

-Вводим в браузер локальную ссылку проекта
```bash
http://127.0.0.1:8000/
```



