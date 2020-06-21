# callboard
Django+Mongodb+Redis(for caching)

Перед запуском приложения необходимо:
    1. Запустить докер контейнер с redis командой:
        docker run --name redis-instance --rm -d -p 6379:6379 redis:5.0.7 redis-server
    2. Запустить докер контейнер с базой данный Mongodb командой:
        docker run --name mongo-instance --rm -d -p "27017:27017" mongo:4.2.3
    3. Перейти в Mongo Shell командой:
        docker exec -it mongo-instance bash
    4. Создать базу данных командой: use имя_базы_данных
    5. В папке settings.py в разделе DATABASES указать имя вашей базы данных, которую вы создали в пункте выше.

Функционал:
    Добавление объявления происходит с помощью формы, создать которую можно с помощью кнопки Создать объявление по пути
    "list/"
    Получить объявление можно с помощью соответствующей кнопки или с помощью GET запроса по адресу /post/<slug>/
    Добавление тэгов и комментариев происходит также с помощью формы по адресу /post/<slug>/
    Статистику тэгов и комментариев можно узнать по пути /post/<slug>/count/

    Slug это уникальный идентификатор объявления

