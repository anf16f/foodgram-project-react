
# Проект foodgram

**«Продуктовый помощник»** - это сайт, на котором пользователи могут _публиковать_ рецепты, добавлять чужие рецепты в _избранное_ и _подписываться_ на публикации других авторов. Сервис **«Список покупок»** позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
 
## Развернутый проект можо посмотреть здесь:

http://84.201.179.109

# Админ-панель

Данные для доступа в админ-панель:

username: admin

email: admin@yandex.ru

password: admin

# Документация

Для просмотра документации к API перейдите по адресу:
- http://84.201.179.109/api/docs/

-------------
## Ресурсы:

- Рецепты на всех страницах **сортируются** по дате публикации (новые — выше)
- Работает **фильтрация** по тегам, в том числе на странице избранного и на странице рецептов одного автора
- Работает **пагинатор** (в том числе при фильтрации по тегам)
- Для **авторизованных** пользователей:
  * Доступна **главная страница**
  * Доступна **страница другого пользователя**
  * Доступна **страница отдельного рецепта**
  * Доступна страница **«Мои подписки»**:
    1. Можно подписаться и отписаться на странице рецепта
    2. Можно подписаться и отписаться на странице автора
    3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки
  * Доступна страница **«Избранное»**:
    1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда
  * Доступна страница **«Список покупок»**:
    1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда
    3. Есть возможность выгрузить файл (.pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок»
    4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента
  * Доступна страница **«Создать рецепт»**:
    1. Есть возможность опубликовать свой рецепт
    2. Есть возможность отредактировать и сохранить изменения в своём рецепте
    3. Есть возможность удалить свой рецепт
  * Доступна и работает форма **изменения пароля**
  * Доступна возможность **выйти из системы** (разлогиниться)
- Для **неавторизованных** пользователей:
  * Доступна **главная страница**
  * Доступна **страница отдельного рецепта**
  * Доступна и работает **форма авторизации**
  * Доступна и работает **система восстановления пароля**
  * Доступна и работает **форма регистрации**
- **Администратор** и **админ-зона**:
  * Все модели выведены в админ-зону
  * Для модели пользователей включена **фильтрация** по имени и email
  * Для модели рецептов включена **фильтрация** по названию, автору и тегам
  * На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное
  * Для модели ингредиентов включена **фильтрация** по названию

-------------

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
`
git clone git@github.com:anf16f/foodgram-project-react.git
`

Перейти в каталог infra:
`
cd infra
`

Запустить docker-compose:
`
docker-compose up -d


Выполнить миграции:
`
docker compose exec web python manage.py migrate


Создать суперпользователя:
`
docker compose exec web python manage.py createsuperuser

Собрать статику:
`
docker compose exec web python manage.py collectstatic --no-input
`

### Заполнение базы из csv файла:

Вы можетеавтоматически заполнить базу ингредиентов из подготовленного файла. 

`
docker-compose exec web python manage.py csv_to_db
`
------------   
