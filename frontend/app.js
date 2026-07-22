// ── Internationalization (ru / kz) ──────────────────────────────────────
const TRANSLATIONS = {
  kz: {
    // Navigation
    "Главная": "Басты бет",
    "Товары и склады": "Тауарлар мен қоймалар",
    "Товары": "Тауарлар",
    "Категории": "Санаттар",
    "Склады": "Қоймалар",
    "Поставщики": "Жеткізушілер",
    "Партии": "Топтамалар",
    "Приход": "Кіріс",
    "Списать / переместить": "Шығару / ауыстыру",
    "Бронирование": "Брондау",
    "Заявки": "Өтінімдер",
    "Инвентаризация": "Инвентаризация",
    "Условия хранения": "Сақтау шарттары",
    "Аналитика": "Аналитика",
    "Уведомления": "Хабарламалар",
    "Журнал действий": "Іс-әрекеттер журналы",
    "Пользователи": "Пайдаланушылар",
    "Карта поставщиков": "Жеткізушілер картасы",
    "Аукционы": "Аукциондар",
    // Common actions
    "Добавить": "Қосу",
    "Сохранить": "Сақтау",
    "Отмена": "Болдырмау",
    "Удалить": "Жою",
    "Изменить": "Өзгерту",
    "Закрыть": "Жабу",
    "Обновить": "Жаңарту",
    "Поиск": "Іздеу",
    "Фильтр": "Сүзгі",
    "Экспорт": "Экспорт",
    "Выгрузить CSV": "CSV жүктеу",
    "Подтвердить": "Растау",
    "Применить": "Қолдану",
    "Выбрать": "Таңдау",
    "Назад": "Артқа",
    "Далее": "Әрі қарай",
    // Status
    "Система доступна": "Жүйе қолжетімді",
    "Нет связи с сервером": "Сервермен байланыс жоқ",
    "Загрузка": "Жүктелуде",
    // Table labels
    "Номер": "Нөмір",
    "Название": "Атауы",
    "Количество": "Саны",
    "Единица": "Өлшем бірлігі",
    "Цена": "Бағасы",
    "Дата": "Күні",
    "Статус": "Күйі",
    "Склад": "Қойма",
    "Партия": "Топтама",
    "Товар": "Тауар",
    "Поставщик": "Жеткізуші",
    "Серия": "Сериясы",
    "Срок годности": "Жарамдылық мерзімі",
    "Создан": "Жасалды",
    "Создано": "Жасалды",
    "Обновлено": "Жаңартылды",
    "Действие": "Іс-әрекет",
    "Ответственный": "Жауапты",
    "Причина": "Себеп",
    "Решение": "Шешім",
    "Ошибки": "Қателер",
    "Начало": "Басталу",
    "Длит.": "Ұзақтығы",
    "Увед.": "Хабарл.",
    "Резервы": "Брондар",
    // Dashboard
    "Рабочее место склада": "Қойма жұмыс орны",
    "Работаем как": "Жұмыс режимі",
    "Настройки администратора": "Әкімші параметрлері",
    "Компактный вид": "Жинақы көрініс",
    "Обычный вид": "Қалыпты көрініс",
    // Batch/product statuses
    "active": "белсенді",
    "blocked": "бұғатталған",
    "quarantine": "карантин",
    "expired": "мерзімі өткен",
    "available": "қолжетімді",
    // Doc statuses
    "draft": "жоба",
    "approved": "бекітілген",
    "posted": "жүргізілген",
    "rejected": "қабылданбаған",
    "pending": "күтілуде",
    "in_review": "тексерілуде",
    "done": "орындалды",
    "running": "орындалуда",
    "failed": "сәтсіз",
    "idle": "бос",
    // Quarantine
    "Допустить": "Жіберу",
    "Забраковать": "Қабылдамау",
    "Начать проверку": "Тексеруді бастау",
    "Разблокировать": "Бұғатты алу",
    // Inventory
    "Инвентаризация в процессе": "Инвентаризация жүріп жатыр",
    "Завершить": "Аяқтау",
    // Recall
    "Всего отзывов": "Барлық қайтарулар",
    "Заблокировано партий": "Бұғатталған топтамалар",
    "Источник": "Дереккөз",
    "Основание": "Негіз",
    "Создал": "Жасаған",
    // Notifications
    "Непрочитанных": "Оқылмаған",
    "Прочитать": "Оқу",
    // Background jobs
    "Фоновые задачи": "Фондық тапсырмалар",
    "Запустить сейчас": "Қазір іске қосу",
    "Последний запуск": "Соңғы іске қосу",
    "Резервы снято": "Брондар алынды",
    "ABC/XYZ снимков": "ABC/XYZ суреттері",
    "Фоновые задачи": "Фондық тапсырмалар",
    // humanStatus values
    "Активно": "Белсенді",
    "Допущено": "Жіберілді",
    "Можно использовать": "Қолдануға болады",
    "Заблокировано": "Бұғатталды",
    "Отменено": "Болдырылмады",
    "Черновик": "Жоба",
    "Ошибка": "Қате",
    "На проверке": "Тексерілуде",
    "В порядке": "Норма",
    "Открыто": "Ашық",
    "Проведен": "Жүргізілді",
    "В обработке": "Өңделуде",
    "Ожидает проверки": "Тексерілуін күтеді",
    "Прочитано": "Оқылды",
    "Получено": "Алынды",
    "Фасовка": "Дайындама",
    "Результат фасовки": "Дайындама нәтижесі",
    "Исходная партия": "Бастапқы топтама",
    "Запрошено": "Сұралды",
    "Забраковано": "Қабылданбады",
    "Снято": "Алынды",
    "Возврат от отделения": "Бөлімнен қайтару",
    "Возврат поставщику": "Жеткізушіге қайтару",
    "Отправлено": "Жіберілді",
    "Выполнено": "Орындалды",
    "Новое": "Жаңа",
    "Использовано": "Пайдаланылды",
    "Внимание": "Назар аудар",
    // humanDocumentType
    "Фасовка / переупаковка": "Дайындама / қайта оралым",
    // humanNotificationType
    "Мало остатка": "Аз қалды",
    "Мониторинг Grafana": "Grafana мониторингі",
    "Нарушения лимитов ПКУ": "ПКУ лимит бұзушылықтары",
    "Нарушений лимитов не обнаружено": "ПКУ лимит бұзушылықтары табылмады",
    "Истекает срок годности (30 дней)": "Жарамдылық мерзімі аяқталады (30 күн)",
    "Все остатки": "Барлық қалдықтар",
    "Сканировать товар": "Тауарды сканерлеу",
    "Найти товар": "Тауарды табу",
    "Превышение: текущие остатки": "Асып кету: ағымдағы қалдықтар",
    "Проверить": "Тексеру",
    // Form field labels
    "Склад или кабинет": "Қойма немесе кабинет",
    "Серийный номер": "Сериялық нөмір",
    "Тип": "Түрі",
    "Мин. температура °C": "Мин. температура °C",
    "Макс. температура °C": "Макс. температура °C",
    "Мин. влажность %": "Мин. ылғалдылық %",
    "Макс. влажность %": "Макс. ылғалдылық %",
    "Источник или заметка": "Дереккөз немесе ескертпе",
    "Температура °C": "Температура °C",
    "Влажность %": "Ылғалдылық %",
    "Ед. изм.": "Өлч. бір.",
    "Штрихкод": "Штрихкод",
    "Категория": "Санат",
    "Ответственные": "Жауаптылар",
    "Категории для проверки": "Тексерілетін санаттар",
    "Ед. измерения": "Өлшем бірлігі",
    "Единица измерения": "Өлшем бірлігі",
    "Контролируемое": "Бақыланатын",
    "Минимальный остаток": "Минималды қалдық",
    "Страховой запас": "Сақтандыру запасы",
    "ИНН / БИН": "ИНН / БИН",
    "Телефон": "Телефон",
    "Адрес": "Мекенжай",
    "Email": "Email",
    "Контактное лицо": "Байланыс тұлға",
    "Номер договора": "Шарт нөмірі",
    "Срок договора": "Шарт мерзімі",
    "Условия оплаты": "Төлем шарттары",
    "Постоянный поставщик": "Тұрақты жеткізуші",
    "Рейтинг": "Рейтинг",
    "Заметки": "Ескертпелер",
    "Отделение (Tetis)": "Бөлімше (Tetis)",
    "Зона хранения": "Сақтау аймағы",
    "Вместимость (ед.)": "Сыйымдылық (бір.)",
    "Ответственный": "Жауапты",
    "Лимит контролируемых (ед.)": "Бақыланатын лимит (бір.)",
    "Серия / партия": "Серия / топтама",
    "Срок годности": "Жарамдылық мерзімі",
    "Поместить в карантин": "Карантинға орналастыру",
    "Цена за ед.": "Бірлік бағасы",
    "Пациент": "Пациент",
    "Врач": "Дәрігер",
    "История болезни": "Ауру тарихы",
    "Второй подтверждающий": "Екінші растаушы",
    "Откуда (склад)": "Қайдан (қойма)",
    "Куда (склад)": "Қайда (қойма)",
    "Тип документа": "Құжат түрі",
    "Внешний номер": "Сыртқы нөмір",
    "Комментарий": "Түсіндірме",
    "Дата начала": "Басталу күні",
    "Дата окончания": "Аяқталу күні",
    "Начальная цена": "Бастапқы баға",
    "Минимальная цена": "Минималды баға",
    "Шаг снижения": "Төмендету қадамы",
    "Интервал шага (сек)": "Қадам аралығы (сек)",
    // Table column headers
    "Время": "Уақыт",
    "Тем-ра °C": "Темп. °C",
    "Влаж. %": "Ылғал. %",
    "Порог температуры": "Температура шегі",
    "Порог влажности": "Ылғалдылық шегі",
    "Последнее": "Соңғы",
    "Что не так": "Не дұрыс",
    "Класс ABC": "ABC класс",
    "Класс XYZ": "XYZ класс",
    "Рекомендуемый заказ": "Ұсынылатын тапсырыс",
    "Свободный остаток": "Бос қалдық",
    "Всего": "Барлығы",
    "Резерв": "Брон",
    "Мин. остаток": "Мин. қалдық",
    "Следующая поставка": "Келесі жеткізу",
    "Ставки": "Ставкалар",
    "Текущая цена": "Ағымдағы баға",
    "Мин. цена": "Мин. баға",
    "Описание": "Сипаттама",
    "Создан": "Жасалды",
    "Создано": "Жасалды",
    "Ед.": "Бір.",
    "Откуда": "Қайдан",
    "Куда": "Қайда",
    "Тип движения": "Қозғалыс түрі",
    "Кол-во": "Саны",
    "Стоимость": "Құны",
    "Поставщик": "Жеткізуші",
    "Тип": "Түрі",
    "Лот / серия": "Лот / серия",
    "Сотрудник": "Қызметкер",
    "Роль": "Рөл",
    "Склады": "Қоймалар",
    "Токен": "Токен",
    // Button text (submit)
    "Добавить датчик": "Датчик қосу",
    "Сохранить показание": "Көрсеткішті сақтау",
    "Добавить товар": "Тауар қосу",
    "Добавить склад": "Қойма қосу",
    "Добавить поставщика": "Жеткізуші қосу",
    "Добавить категорию": "Санат қосу",
    "Добавить партию": "Топтама қосу",
    "Списать (ФЕФО)": "Шығару (ФЕФО)",
    "Создать резерв": "Брон жасау",
    "Снять резерв": "Бронды алу",
    "Использовать резерв": "Бронды пайдалану",
    "Принять к учёту": "Есепке алу",
    "Провести документ": "Құжатты жүргізу",
    "Создать сессию": "Сессия жасау",
    "Завершить сессию": "Сессияны аяқтау",
    "Отменить сессию": "Сессияны болдырмау",
    "Создать фасовку": "Дайындама жасау",
    "Создать возврат": "Қайтаруды жасау",
    "Создать заявку": "Өтінім жасау",
    "Создать аукцион": "Аукцион жасау",
    "Создать перемещение": "Ауыстыру жасау",
    "Создать приход": "Кіріс жасау",
    "Добавить строку": "Жол қосу",
    "Войти": "Кіру",
    // Placeholders
    "Выберите склад": "Қойманы таңдаңыз",
    "Выберите датчик": "Датчикті таңдаңыз",
    "Выберите товар": "Тауарды таңдаңыз",
    "Выберите партию": "Топтаманы таңдаңыз",
    "Выберите поставщика": "Жеткізушіні таңдаңыз",
    "Выберите категорию": "Санатты таңдаңыз",
    "Выберите роль": "Рөлді таңдаңыз",
    "Выберите тип": "Түрді таңдаңыз",
    "Выберите единицу": "Бірлікті таңдаңыз",
    "Выберите документ": "Құжатты таңдаңыз",
    "Все доступные склады": "Барлық қоймалар",
    // Empty states
    "Данных пока нет": "Деректер жоқ",
    "Товаров пока нет": "Тауарлар жоқ",
    "Партий пока нет": "Топтамалар жоқ",
    "Уведомлений пока нет": "Хабарламалар жоқ",
    "Заявок пока нет": "Өтінімдер жоқ",
    "Аукционов пока нет": "Аукциондар жоқ",
    "Датчиков пока нет. Добавьте датчик для склада или кабинета.": "Датчиктер жоқ. Қойма немесе кабинетке датчик қосыңыз.",
    // Section titles / h2
    "Новый датчик": "Жаңа датчик",
    "Внести показание": "Көрсеткіш енгізу",
    "Датчики хранения": "Сақтау датчиктері",
    "Журнал температуры и влажности": "Температура және ылғалдылық журналы",
    "График условий хранения": "Сақтау шарттары графигі",
    "Журнал действий": "Іс-әрекеттер журналы",
    "Журнал отзывов партий": "Топтамаларды қайтару журналы",
    "Остатки": "Қалдықтар",
    "Все партии": "Барлық топтамалар",
    "Документы": "Құжаттар",
    "История перемещений": "Ауыстыру тарихы",
    "Фоновые задачи": "Фондық тапсырмалар",
    "Пользователи и доступ": "Пайдаланушылар мен қатынас",
    "Рабочее место склада": "Қойма жұмыс орны",
    "Работаем как": "Жұмыс режимі",
    // Section titles (h2/h3) — missing from prev pass
    "Забраковать партию": "Топтаманы бракқа шығару",
    "Допустить партию": "Топтаманы жіберу",
    "Договор и условия": "Шарт және шарттар",
    "Последние цены": "Соңғы бағалар",
    "Оценки и отзывы": "Бағалар мен пікірлер",
    "Первый запуск": "Бірінші іске қосу",
    "Что сделать, чтобы склад начал работать": "Қойманы іске қосу үшін не істеу керек",
    "Остатки по партиям": "Топтамалар бойынша қалдықтар",
    "Автообновление: включено": "Автожаңарту: қосылды",
    "Автообновление: нет связи": "Автожаңарту: байланыс жоқ",
    "Очередь действий": "Іс-әрекеттер кезегі",
    "Последние уведомления": "Соңғы хабарламалар",
    "Списать партию": "Топтаманы шығару",
    "Доступные остатки": "Қолжетімді қалдықтар",
    "Где лежит партия": "Топтама қай жерде",
    "Последние движения": "Соңғы қозғалыстар",
    "Цепочка фасовки": "Дайындама тізбегі",
    "Отзывы партии": "Топтама қайтарулары",
    "Новый товар": "Жаңа тауар",
    "Новая категория": "Жаңа санат",
    "Новый поставщик": "Жаңа жеткізуші",
    "Новый склад": "Жаңа қойма",
    "Справочник": "Анықтамалық",
    "Приемка сразу в остатки": "Тікелей қалдыққа қабылдау",
    "Черновик приходного документа": "Кіріс құжатының жобасы",
    "Черновик документа списания": "Шығарыс құжатының жобасы",
    "Складские документы": "Қойма құжаттары",
    "Строки прихода": "Кіріс жолдары",
    "Строки списания": "Шығарыс жолдары",
    "Минимальная форма списания партии": "Топтаманы шығарудың қысқа нысаны",
    "Недавние списания": "Соңғы шығарыстар",
    "Списание по ближайшему сроку": "Ең жақын мерзіммен шығару",
    "Списание партии": "Топтаманы шығару",
    "Перемещение": "Ауыстыру",
    "Статус партии": "Топтама мәртебесі",
    "Отзыв партии": "Топтаманы қайтару",
    "Карантинные проверки": "Карантиндік тексерулер",
    "Текущие остатки": "Ағымдағы қалдықтар",
    "Фасовка партии": "Топтаманы дайындау",
    "Журнал фасовки": "Дайындама журналы",
    "Остатки после операций": "Операциялардан кейінгі қалдықтар",
    "Партии для возврата": "Қайтарылатын топтамалар",
    "Дашборд отзывов партий": "Топтамаларды қайтару бақылауы",
    "История движения ТМЦ": "ТМЦ қозғалысы тарихы",
    "Лимиты ПКУ по кабинету": "Кабинет бойынша ПКУ лимиттері",
    "Текущие лимиты ПКУ": "Ағымдағы ПКУ лимиттері",
    "Новый резерв": "Жаңа брон",
    "Бронирование товаров": "Тауарларды брондау",
    "Новая заявка": "Жаңа өтінім",
    "Заявки на закупку": "Сатып алу өтінімдері",
    "Рекомендации к закупке": "Сатып алу ұсыныстары",
    "Создать инвентаризацию": "Инвентаризация жасау",
    "Завершение": "Аяқтау",
    "Сводка выбранной проверки": "Таңдалған тексерудің қорытындысы",
    "Проверки склада": "Қойма тексерулері",
    "Товары в выбранной проверке": "Таңдалған тексерудегі тауарлар",
    "Остатки для сверки": "Салыстыруға арналған қалдықтар",
    "Нужно проверить условия хранения": "Сақтау шарттарын тексеру қажет",
    "Матрица ABC/XYZ": "ABC/XYZ матрицасы",
    "Карта внимания ABC/XYZ": "ABC/XYZ назар картасы",
    "ABC/XYZ анализ и заказ": "ABC/XYZ талдауы және тапсырыс",
    "История расчетов": "Есептеулер тарихы",
    "Пользователи системы": "Жүйе пайдаланушылары",
    "Модерация отзывов поставщиков": "Жеткізуші пікірлерін модерациялау",
    "Доступ временно ограничен": "Қатынас уақытша шектелді",
    "Заявки на списание ПКУ (двойная подпись)": "ПКУ шығарыс өтінімдері (қос қол қою)",
    // Inline text
    "прочитано": "оқылды",
    "новое": "жаңа",
    "Снять просроченную бронь": "Мерзімі өткен бронды алу",
    "Экспорт ПКУ CSV": "ПКУ CSV экспорты",
    "↓ PDF журнал ПКУ": "↓ ПКУ PDF журналы",
    "Нужна перепечатка": "Қайта басып шығару қажет",
    "Отзывы на проверке": "Тексерудегі пікірлер",
    "Договоры истекают": "Шарттар мерзімі бітеді",
    "Справочники готовы к работе": "Анықтамалықтар жұмысқа дайын",
    "Заполните справочники по порядку": "Анықтамалықтарды кезекпен толтырыңыз",
    "Исправить": "Түзету",
    "Код товара": "Тауар коды",
    "Точка заказа": "Тапсырыс нүктесі",
    "ПКУ / контролируемый товар": "ПКУ / бақыланатын тауар",
    "Сертификат": "Сертификат",
    "Название категории": "Санат атауы",
    "Название поставщика": "Жеткізуші атауы",
    "БИН": "БИН",
    "Название склада или кабинета": "Қойма немесе кабинет атауы",
    "Отделение": "Бөлімше",
    "ID компании Tetis": "Tetis компания ID",
    "ID склада в Tetis": "Tetis қоймасының ID",
    "Лимит вместимости": "Сыйымдылық лимиті",
    "Условия хранения": "Сақтау шарттары",
    "Договор действует до": "Шарт мерзімі",
    "Только требующие перепечатки": "Тек қайта басып шығаруды қажет ететіндер",
    // Stock / barcode view
    "Склад": "Қойма",
    "Сканер штрихкода": "Штрихкод сканері",
    "Запустить камеру": "Камераны іске қосу",
    "Остановить": "Тоқтату",
    "Или введите штрихкод вручную": "Немесе штрихкодты қолмен енгізіңіз",
    "Найти": "Іздеу",
    "Отсканируйте штрихкод товара для фильтрации остатков": "Қалдықтарды сүзу үшін тауар штрихкодын сканерлеңіз",
    "Сбросить фильтр": "Сүзгіні тазалау",
    "Камера недоступна в этом браузере": "Бұл браузерде камера қолжетімсіз",
    "Код": "Код",
    "Поддерживаются USB и Bluetooth сканеры: нажмите в поле, затем пронесите сканером": "USB және Bluetooth сканерлер қолдауы: өрісті басып, сканермен өткізіңіз",
    "Наведите камеру на штрихкод": "Камераны штрихкодқа бағыттаңыз",
    "EAN-13 · EAN-8 · Code-128 · QR · DataMatrix · PDF417 · и другие": "EAN-13 · EAN-8 · Code-128 · QR · DataMatrix · PDF417 · және басқалар",

  }
};

let _lang = localStorage.getItem("sklad_lang") || "ru";

function t(text) {
  if (_lang === "ru") return text;
  return TRANSLATIONS[_lang]?.[text] ?? text;
}

function setLang(lang) {
  _lang = lang;
  localStorage.setItem("sklad_lang", lang);
  document.documentElement.lang = lang === "kz" ? "kk" : "ru";
  render();
}

function getLang() { return _lang; }

// ─────────────────────────────────────────────────────────────────────────────

const APP_BASE = window.location.pathname.startsWith("/sklad") ? "/sklad" : "";
const API = `${APP_BASE}/api/v1`;

const _savedSupplierToken = (function() {
  try { return localStorage.getItem("sklad_supplier_token") || ""; } catch(_) { return ""; }
})();
const state = {
  view: "dashboard",
  realtime: "offline",
  loadWarnings: [],
  auth: {
    source: _savedSupplierToken ? "login" : "demo",
    actor: null,
    blockedMessage: "",
    loginToken: _savedSupplierToken,
    supplierId: null,
  },
  ui: {
    density: "comfortable",
    search: "",
    scannerActive: false,
    barcodeProduct: null,
    scannerTarget: null,
    _scanRawTarget: null,
    batchFilterProductId: null,
    supplierMode: false,
    supplierView: "auctions",
    catalogSubTab: "items",
    catalogSearch: "",
    catalogStatusFilter: "all",
    marketplaceInquirySourceFilter: "all",
    marketplaceInquiryStatusFilter: "all",
    supplierInquirySourceFilter: "all",
    supplierInquiryStatusFilter: "all",
    compareItems: [],
  },
  data: {
    health: null,
    readiness: null,
    categories: [],
    suppliers: [],
    warehouses: [],
    productUnits: [],
    products: [],
    batches: [],
    batchRecalls: { items: [], total: 0 },
    recallStats: null,
    balances: { items: [], total: 0 },
    reservations: [],
    quarantineReviews: { items: [], total: 0 },
    controlledLimits: [],
    controlledViolations: [],
    pendingControlledWriteoffs: [],
    purchaseRequests: [],
    notifications: { items: [], total: 0 },
    audit: { items: [], total: 0 },
    documents: [],
    inventorySessions: [],
    movements: [],
    repackings: { items: [], total: 0 },
    repackTemplates: [],
    procedureConsumptionTemplates: [],
    supplierApplications: { items: [], total: 0 },
    supplierPortal: { auctions: [], myBids: {}, priceHistory: [], shipments: [], reviews: [], profile: null, myApplications: [], myCatalog: [], inquiries: [], stats: null, orders: { items: [], total: 0 }, catalogAnalytics: [], verificationDocs: [] },
    analytics: { items: [], analysis_days: 90, warehouse_id: null, generated_at: null },
    abcXyzRuns: { items: [], total: 0 },
    sensorDevices: [],
    sensorReadings: { items: [], total: 0 },
    users: [],
    supplierMap: [],
    shipments: { items: [], total: 0 },
  },
  documentForms: {
    receipt: {
      supplier_id: "",
      warehouse_id: "",
      lines: [{ product_id: "", quantity: "", unit_price: "0", lot: "", serial_number: "", expires_on: "" }],
    },
    writeoff: {
      warehouse_id: "",
      lines: [{ batch_id: "", quantity: "", reason: "Списание по документу", patient_id: "", doctor_id: "", medical_record_no: "", second_approver_id: "", second_approval_note: "" }],
    },
  },
};

let balanceSocket = null;
let realtimeRefreshTimer = null;

class AuthRequiredError extends Error {
  constructor(message) {
    super(message);
    this.name = "AuthRequiredError";
  }
}

class ApiError extends Error {
  constructor(message, status, code = "") {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

const views = [
  ["dashboard", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.3"/><rect x="14" y="3" width="7" height="7" rx="1.3"/><rect x="3" y="14" width="7" height="7" rx="1.3"/><rect x="14" y="14" width="7" height="7" rx="1.3"/></svg>`, "Главная"],
  ["tablet-writeoff", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><line x1="9" y1="12" x2="15" y2="12"/></svg>`, "Списание"],
  ["stock", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7.5 12 3l9 4.5-9 4.5-9-4.5z"/><path d="M3 7.5v9l9 4.5 9-4.5v-9"/><line x1="12" y1="12" x2="12" y2="21"/></svg>`, "Склад"],
  ["catalog", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4-8 4-8-4 8-4z"/><path d="M4 11l8 4 8-4"/><path d="M4 15l8 4 8-4"/></svg>`, "Товары и склады"],
  ["receipts", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="12" rx="1.5"/><path d="M4 8l8-5 8 5"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>`, "Приход товара"],
  ["documents", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l4 4v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v4h4"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="15" y2="16"/></svg>`, "Документы"],
  ["operations", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="9" x2="21" y2="9"/><polyline points="17 5 21 9 17 13"/><line x1="21" y1="15" x2="3" y2="15"/><polyline points="7 11 3 15 7 19"/></svg>`, "Списать / переместить"],
  ["repacking", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><polyline points="3 16 3 21 8 21"/><polyline points="21 8 21 3 16 3"/></svg>`, "Фасовка"],
  ["returns", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 14 4 9 9 4"/><path d="M4 9h11a5 5 0 0 1 5 5v1"/></svg>`, "Возвраты"],
  ["movements", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/></svg>`, "История склада"],
  ["reservations", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></svg>`, "Бронирование"],
  ["purchase-requests", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><line x1="9" y1="11" x2="15" y2="11"/><line x1="9" y1="15" x2="13" y2="15"/></svg>`, "Заявки"],
  ["inventory", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><polyline points="9 13 11 15 15 11"/></svg>`, "Инвентаризация"],
  ["conditions", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 14.5V4a2 2 0 0 0-4 0v10.5a4 4 0 1 0 4 0z"/></svg>`, "Условия хранения"],
  ["analytics", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="20" x2="4" y2="12"/><line x1="10" y1="20" x2="10" y2="6"/><line x1="16" y1="20" x2="16" y2="14"/><line x1="20" y1="20" x2="4" y2="20"/></svg>`, "Аналитика"],
  ["notifications", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 19a2 2 0 1 0 4 0"/><path d="M6 9a6 6 0 1 1 12 0c0 4 1.5 5 1.5 6.5H4.5C4.5 14 6 13 6 9z"/></svg>`, "Уведомления"],
  ["audit", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="6"/><line x1="14.5" y1="14.5" x2="20" y2="20"/></svg>`, "Журнал действий"],
  ["users", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14c2.4.4 3.8 2 3.8 5"/></svg>`, "Пользователи"],
  ["supplier-map", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.5-7-11.5a7 7 0 1 1 14 0C19 14.5 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>`, "Карта поставщиков"],
  ["auctions", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="20" x2="20" y2="20"/><polyline points="4 14 9 9 13 13 20 5"/><polyline points="15 5 20 5 20 10"/></svg>`, "Аукционы"],
  ["marketplace", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h18l-2 9H5L3 3z"/><path d="M5 12v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/><path d="M9 21v-6h6v6"/></svg>`, "Маркетплейс"],
  
  ["support", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-1.5c1.66 0 3-1.12 3-2.5S13.66 9.5 12 9.5 9 10.62 9 12"/><line x1="12" y1="18.5" x2="12" y2="18.51"/></svg>`, "Поддержка"],
  ["my-profile", `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`, "Мой профиль"],
];

const navGroups = [
  { label: "Обзор", ids: ["dashboard"] },
  { label: "Ежедневные операции", ids: ["tablet-writeoff", "stock", "operations", "repacking", "returns", "reservations"] },
  { label: "Снабжение", ids: ["receipts", "purchase-requests", "supplier-map", "auctions", "marketplace"] },
  { label: "Учёт и документы", ids: ["catalog", "documents", "movements", "inventory", "conditions"] },
  { label: "Аналитика", ids: ["analytics", "notifications"] },
  { label: "Администрирование", ids: ["audit", "users"] },
  { label: "Помощь", ids: ["support"] },
  { label: "Аккаунт", ids: ["my-profile"] },
];

const limitedRoleViews = new Set(["dashboard", "tablet-writeoff", "stock", "movements", "notifications", "support"]);
const limitedRoles = new Set(["nurse", "doctor", "other"]);
const managerOnlyViews = new Set(["audit", "users", "supplier-map", "auctions"]);

const el = (id) => document.getElementById(id);

function readTetisToken() {
  // tetis1.kz stores token as a plain string under "qormed_token"
  for (const storage of [window.localStorage, window.sessionStorage]) {
    try {
      const direct = storage.getItem("qormed_token");
      if (typeof direct === "string" && direct.trim()) return direct.trim();
    } catch { /* ignore */ }
  }
  // Fallback: older auth-storage format with JSON envelope
  for (const storage of [window.localStorage, window.sessionStorage]) {
    try {
      const raw = storage.getItem("auth-storage");
      if (!raw) continue;
      const token = JSON.parse(raw)?.state?.token;
      if (typeof token === "string" && token.trim()) return token.trim();
    } catch {
      continue;
    }
  }
  return "";
}

function hasTetisSession() {
  return !!readTetisToken();
}

function readTetisActiveOrgId() {
  for (const storage of [window.localStorage, window.sessionStorage]) {
    try {
      const raw = storage.getItem("org-storage");
      if (!raw) continue;
      const orgId = JSON.parse(raw)?.state?.activeOrgId;
      if (typeof orgId === "string" && orgId.trim()) return orgId.trim();
    } catch {
      continue;
    }
  }
  return "";
}

function activeTetisOrgId() {
  return readTetisActiveOrgId();
}

async function requestSkladTokenFromTetis() {
  if (!window.location.pathname.startsWith("/sklad")) return false;
  const tetisToken = readTetisToken();
  if (!tetisToken) {
    el("auth-token").value = "";
    state.auth.source = "demo";
    state.auth.blockedMessage = "";
    return false;
  }
  const orgId = readTetisActiveOrgId();
  // Try the full exchange endpoint first
  for (const url of [API + "/sklad/token", "/sklad/api/v1/sklad/token", "/api/v1/sklad/token"]) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tetisToken}`,
        },
        credentials: "include",
        body: JSON.stringify(orgId ? { org_id: orgId } : {}),
      });
      if (!response.ok) continue;
      const payload = await response.json();
      if (!payload?.access_token) continue;
      el("auth-token").value = payload.access_token;
      state.auth.source = "tetis";
      state.auth.blockedMessage = "";
      try { sessionStorage.setItem("sklad_tetis_session", payload.access_token); } catch(_) {}
      return true;
    } catch (_) { continue; }
  }
  return false;
}

async function showLoginScreen() {
  const isTetis = window.location.hostname === "tetis1.kz" || window.location.hostname === "www.tetis1.kz";
  if (isTetis) {
    const existing = document.getElementById("auth-error-banner");
    if (existing) return;
    const banner = document.createElement("div");
    banner.id = "auth-error-banner";
    banner.style.cssText = "position:fixed;top:0;left:0;right:0;background:#dc2626;color:#fff;text-align:center;padding:10px 16px;font-size:.9rem;font-weight:500;z-index:9999;display:flex;align-items:center;justify-content:center;gap:16px";
    banner.innerHTML = "<span>\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0441\u043a\u043b\u0430\u0434\u0443. \u041e\u0431\u043d\u043e\u0432\u0438\u0442\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443 \u0438\u043b\u0438 \u0432\u043e\u0439\u0434\u0438\u0442\u0435 \u0432 <a href=\"https://tetis1.kz/\" style=\"color:#fff;font-weight:700;text-decoration:underline\">tetis1.kz</a> \u0437\u0430\u043d\u043e\u0432\u043e.</span><button onclick=\"location.reload()\" style=\"background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.5);color:#fff;border-radius:6px;padding:4px 12px;cursor:pointer;font-size:.85rem\">\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c</button>";
    document.body.insertAdjacentElement("afterbegin", banner);
  } else {
    const loginScreen = el("login-screen");
    if (!loginScreen) return;
    const tetisBlock = document.getElementById("login-tetis-block");
    const directBlock = document.getElementById("login-direct-block");
    if (tetisBlock) tetisBlock.style.display = "none";
    if (directBlock) directBlock.style.display = "";
    loginScreen.style.display = "flex";
    const submitBtn = document.getElementById("login-direct-submit");
    if (submitBtn && !submitBtn._bound) {
      submitBtn._bound = true;
      const doLogin = async () => {
        const username = (document.getElementById("login-direct-username") || {}).value || "";
        const password = (document.getElementById("login-direct-password") || {}).value || "";
        const errEl = document.getElementById("login-error");
        if (!username.trim() || !password) {
          if (errEl) { errEl.textContent = "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043b\u043e\u0433\u0438\u043d \u0438 \u043f\u0430\u0440\u043e\u043b\u044c"; errEl.style.display = ""; }
          return;
        }
        submitBtn.disabled = true;
        submitBtn.textContent = "\u0412\u0445\u043e\u0436\u0443\u2026";
        try {
          const resp = await fetch(API + "/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username.trim(), password }),
          });
          const data = await resp.json().catch(() => ({}));
          if (!resp.ok) {
            if (errEl) { errEl.textContent = (data && (data.detail && data.detail.message || data.detail)) || "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043b\u043e\u0433\u0438\u043d \u0438\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c"; errEl.style.display = ""; }
            submitBtn.disabled = false;
            submitBtn.textContent = "\u0412\u043e\u0439\u0442\u0438";
            return;
          }
          const token = data.access_token;
          try { localStorage.setItem("sklad_supplier_token", token); } catch(_) {}
          state.auth.loginToken = token;
          state.auth.source = "login";
          el("auth-token").value = token;
          loginScreen.style.display = "none";
          if (errEl) errEl.style.display = "none";
          await loadAll();
        } catch(e) {
          if (errEl) { errEl.textContent = "\u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u044f: " + e.message; errEl.style.display = ""; }
          submitBtn.disabled = false;
          submitBtn.textContent = "\u0412\u043e\u0439\u0442\u0438";
        }
      };
      submitBtn.addEventListener("click", doLogin);
      const pwdEl = document.getElementById("login-direct-password");
      if (pwdEl) pwdEl.addEventListener("keydown", function(e) { if (e.key === "Enter") doLogin(); });
    }
    // Tab switching: Войти / Регистрация
    const tabLoginEl = document.getElementById("tab-login");
    const tabRegEl = document.getElementById("tab-register");
    if (tabLoginEl && tabRegEl && !tabLoginEl._tabBound) {
      tabLoginEl._tabBound = true;
      const fLogin = document.getElementById("auth-login-form");
      const fReg = document.getElementById("auth-register-form");
      const activateTab = (active, inactive, activeForm, inactiveForm) => {
        activeForm.style.display = ""; inactiveForm.style.display = "none";
        active.style.borderBottomColor = "#2563eb"; active.style.color = "#2563eb"; active.style.fontWeight = "600";
        inactive.style.borderBottomColor = "transparent"; inactive.style.color = "#64748b"; inactive.style.fontWeight = "500";
      };
      tabLoginEl.addEventListener("click", () => activateTab(tabLoginEl, tabRegEl, fLogin, fReg));
      tabRegEl.addEventListener("click", () => activateTab(tabRegEl, tabLoginEl, fReg, fLogin));
    }
    // Registration submit
    const regBtn = document.getElementById("register-submit");
    if (regBtn && !regBtn._bound) {
      regBtn._bound = true;
      regBtn.addEventListener("click", async () => {
        const errEl = document.getElementById("login-error");
        errEl.style.display = "none"; errEl.style.color = "#dc2626"; errEl.style.background = "#fff0f0";
        const username = (document.getElementById("reg-username") || {}).value?.trim() || "";
        const fullname = (document.getElementById("reg-fullname") || {}).value?.trim() || "";
        const password = (document.getElementById("reg-password") || {}).value || "";
        const password2 = (document.getElementById("reg-password2") || {}).value || "";
        const role = (document.getElementById("reg-role") || {}).value || "warehouse_manager";
        if (!username || !fullname || !password) { errEl.textContent = "Заполните все обязательные поля"; errEl.style.display = ""; return; }
        if (password.length < 8) { errEl.textContent = "Пароль должен быть не менее 8 символов"; errEl.style.display = ""; return; }
        if (password !== password2) { errEl.textContent = "Пароли не совпадают"; errEl.style.display = ""; return; }
        regBtn.disabled = true; regBtn.textContent = "Регистрация...";
        try {
          const resp = await fetch(API + "/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, full_name: fullname, password, role })
          });
          const data = await resp.json().catch(() => ({}));
          if (!resp.ok) { errEl.textContent = (data && (data.detail?.message || data.detail)) || "Ошибка регистрации"; errEl.style.display = ""; return; }
          // Auto-login
          const loginResp = await fetch(API + "/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
          });
          const loginData = await loginResp.json().catch(() => ({}));
          if (!loginResp.ok) {
            errEl.textContent = "Аккаунт создан! Войдите с вашими данными.";
            errEl.style.color = "#16a34a"; errEl.style.background = "#f0fdf4"; errEl.style.display = "";
            document.getElementById("tab-login")?.click();
            return;
          }
          const token = loginData.access_token;
          try { localStorage.setItem("sklad_supplier_token", token); } catch(_) {}
          state.auth.loginToken = token; state.auth.source = "login";
          el("auth-token").value = token;
          el("login-screen").style.display = "none";
          await loadAll();
        } catch(e) {
          errEl.textContent = "Ошибка соединения: " + e.message; errEl.style.display = "";
        } finally {
          regBtn.disabled = false; regBtn.textContent = "Зарегистрироваться";
        }
      });
    }
  }
}

function hideLoginScreen() {
  const loginScreen = el("login-screen");
  if (loginScreen) loginScreen.style.display = "none";
  document.getElementById("auth-error-banner")?.remove();
}


function showSupplierLoginModal() {
  const existing = document.getElementById("supplier-login-modal");
  if (existing) { existing.remove(); return; }
  const modal = document.createElement("div");
  modal.id = "supplier-login-modal";
  modal.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;z-index:1100";
  modal.innerHTML = `
    <div style="background:#fff;border-radius:10px;padding:1.5rem;min-width:300px;max-width:360px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.18)">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
        <h3 style="margin:0;font-size:1rem">Вход в портал поставщика</h3>
        <button id="supplier-login-close" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:#6b7280">x</button>
      </div>
      <div style="margin-bottom:.75rem">
        <label style="display:block;font-size:.82rem;color:#6b7280;margin-bottom:.25rem">Email</label>
        <input id="supplier-login-email" type="email" autocomplete="email" style="width:100%;box-sizing:border-box;padding:.5rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem" placeholder="email@example.com">
      </div>
      <div style="margin-bottom:1rem">
        <label style="display:block;font-size:.82rem;color:#6b7280;margin-bottom:.25rem">Пароль</label>
        <input id="supplier-login-password" type="password" autocomplete="current-password" style="width:100%;box-sizing:border-box;padding:.5rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem" placeholder="...">
      </div>
      <div id="supplier-login-error" style="display:none;background:#fef2f2;color:#dc2626;border-radius:6px;padding:.5rem .75rem;font-size:.83rem;margin-bottom:.75rem"></div>
      <button id="supplier-login-submit" class="primary" style="width:100%;margin:0">Войти</button>
    </div>`;
  document.body.appendChild(modal);
  const close = () => modal.remove();
  modal.querySelector("#supplier-login-close").addEventListener("click", close);
  modal.addEventListener("click", e => { if (e.target === modal) close(); });
  const submit = async () => {
    const email = modal.querySelector("#supplier-login-email").value.trim();
    const password = modal.querySelector("#supplier-login-password").value;
    const errEl = modal.querySelector("#supplier-login-error");
    const btn = modal.querySelector("#supplier-login-submit");
    errEl.style.display = "none";
    if (!email || !password) { errEl.textContent = "Введите email и пароль"; errEl.style.display = ""; return; }
    btn.disabled = true; btn.textContent = "Входим...";
    try {
      const resp = await fetch(API + "/auth/supplier-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await resp.json();
      if (!resp.ok) {
        errEl.textContent = data?.detail?.message || data?.detail || "Неверный email или пароль";
        errEl.style.display = "";
        btn.disabled = false; btn.textContent = "Войти";
        return;
      }
      const token = data.access_token;
      try { localStorage.setItem("sklad_supplier_token", token); } catch(_) {}
      state.auth.loginToken = token;
      state.auth.source = "login";
      el("auth-token").value = token;
      modal.remove();
      await loadAll();
    } catch(e) {
      errEl.textContent = "Ошибка соединения: " + e.message;
      errEl.style.display = "";
      btn.disabled = false; btn.textContent = "Войти";
    }
  };
  modal.querySelector("#supplier-login-submit").addEventListener("click", submit);
  modal.querySelector("#supplier-login-password").addEventListener("keydown", e => { if (e.key === "Enter") submit(); });
  setTimeout(() => modal.querySelector("#supplier-login-email")?.focus(), 50);
}

function supplierLogout() {
  try { localStorage.removeItem("sklad_supplier_token"); } catch(_) {}
  state.auth.loginToken = "";
  state.auth.source = "demo";
  el("auth-token").value = "";
  loadAll();
}

function showSupplierApplicationScreen() {
  const form = el("supplier-application-form");
  const result = el("supplier-application-result");
  if (form) {
    form.reset();
    form.style.display = "";
    form.querySelector("button[type=submit]").disabled = false;
  }
  if (result) {
    result.style.display = "none";
    result.textContent = "";
  }
  const screen = el("supplier-application-screen");
  if (screen) screen.style.display = "flex";
}

function hideSupplierApplicationScreen() {
  const screen = el("supplier-application-screen");
  if (screen) screen.style.display = "none";
}

async function submitSupplierApplication(event) {
  event.preventDefault();
  const form = event.target;
  const resultBox = el("supplier-application-result");
  resultBox.style.display = "none";
  const payload = {
    name: form.name.value.trim(),
    bin: form.bin.value.trim() || null,
    email: form.email.value.trim(),
    phone: form.phone.value.trim() || null,
    contact_person: form.contact_person.value.trim() || null,
    city: form.city.value.trim() || null,
    address: form.address.value.trim() || null,
    delivery_days: form.delivery_days.value ? Number(form.delivery_days.value) : null,
    notes: form.notes.value.trim() || null,
  };
  const submitButton = form.querySelector("button[type=submit]");
  submitButton.disabled = true;
  try {
    const authToken = el("auth-token")?.value?.trim();
    const reqHeaders = { "Content-Type": "application/json" };
    if (state.auth.source === "tetis" && authToken) reqHeaders.Authorization = `Bearer ${authToken}`;
    const resp = await fetch(`${API}/supplier-applications`, {
      method: "POST",
      headers: reqHeaders,
      body: JSON.stringify(payload),
    });
    const body = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      throw new Error(body?.detail?.message || body?.detail || "Не удалось отправить заявку");
    }
    resultBox.style.color = "var(--success, #1a7f37)";
    resultBox.textContent = state.auth.source === "tetis"
      ? "Заявка отправлена. После одобрения вы автоматически получите доступ — переключатель «Режим: Поставщик» появится в верхней панели."
      : "Заявка отправлена. После проверки Tetis вы получите доступ на указанный email.";
    resultBox.style.display = "block";
    form.style.display = "none";
  } catch (err) {
    resultBox.style.color = "var(--danger)";
    resultBox.textContent = err.message;
    resultBox.style.display = "block";
    submitButton.disabled = false;
  }
}

function applyActorProfile(profile) {
  if (!profile) return;
  if (!Array.isArray(profile.roles) || !profile.roles.length) {
    throw new Error("Профиль доступа к складу не содержит роль. Обратитесь к администратору Tetis.");
  }
  state.auth.actor = profile;
  el("actor-id").value = profile.actor_id || el("actor-id").value || "tetis-user";
  const primaryRole = profile.roles[0];
  el("actor-role").value = primaryRole;
  el("actor-warehouses").value = (profile.warehouse_ids || []).join(",");
  document.body.classList.toggle("tetis-auth", state.auth.source === "tetis");
  const context = el("auth-context");
  if (context) {
    const warehouses = profile.warehouse_ids?.length
      ? `Склады: ${profile.warehouse_ids.join(", ")}`
      : "Доступ ко всем складам";
    context.textContent = state.auth.source === "tetis"
      ? `Вход через Tetis: ${profile.actor_id}. ${warehouses}.`
      : "Демо-режим: роль и доступ задаются вручную.";
  }
  state.auth.supplierId = profile.supplier_id ?? null;
  state.auth.fullName = profile.full_name || profile.actor_id || "";
  const canBeSupplier = (profile.roles || []).includes("supplier");

  // Topbar user info for standalone (login source)
  const isStandalone = state.auth.source === "login";
  const topbarUser = el("topbar-user-info");
  if (topbarUser) {
    topbarUser.style.display = isStandalone ? "flex" : "none";
    if (isStandalone) {
      const roleLabel = canBeSupplier ? "Поставщик" : profile.roles?.includes("warehouse_manager") ? "Менеджер" : (profile.roles?.[0] || "");
      topbarUser.innerHTML = `
        <span style="font-size:.85rem;color:var(--muted)">
          <strong style="color:var(--text)">${escapeHtml(state.auth.fullName)}</strong>
          <span style="background:#e5e7eb;border-radius:4px;padding:1px 6px;font-size:.75rem;margin-left:4px">${escapeHtml(roleLabel)}</span>
        </span>
        <button onclick="navigateTo('my-profile')" class="secondary" type="button" style="padding:.3rem .7rem;font-size:.8rem">Профиль</button>
        <button id="standalone-logout" class="secondary" type="button" style="padding:.3rem .7rem;font-size:.8rem">Выйти</button>
      `;
      el("standalone-logout")?.addEventListener("click", () => {
        try { localStorage.removeItem("sklad_supplier_token"); } catch(_) {}
        state.auth.loginToken = "";
        state.auth.source = "demo";
        el("auth-token").value = "";
        location.reload();
      });
    }
  }

  // Hide demo auth fields for standalone users
  const opPanel = document.querySelector(".work-context");
  if (opPanel) opPanel.style.display = isStandalone ? "none" : "";

  const supplierToggle = el("supplier-mode-toggle");
  if (supplierToggle) {
    supplierToggle.style.display = canBeSupplier ? "" : "none";
    if (canBeSupplier) {
      supplierToggle.textContent = state.ui.supplierMode ? "← Режим склада" : "Кабинет поставщика";
      supplierToggle.style.fontWeight = "600";
      supplierToggle.style.background = state.ui.supplierMode ? "" : "#2563eb";
      supplierToggle.style.color = state.ui.supplierMode ? "" : "#fff";
    }
    if (!canBeSupplier) state.ui.supplierMode = false;
  }
  const becomeSupplierButton = el("become-supplier-button");
  if (becomeSupplierButton) {
    const showBecome = isStandalone && !canBeSupplier;
    becomeSupplierButton.style.display = showBecome ? "" : "none";
    if (showBecome) becomeSupplierButton.textContent = "Стать поставщиком";
  }
  const supplierLoginBtn = el("supplier-login-button");
  if (supplierLoginBtn) {
    if (canBeSupplier || state.auth.source === "login") {
      supplierLoginBtn.style.display = "none";
    } else {
      supplierLoginBtn.style.display = "";
    }
  }
  const supplierLogoutBtn = el("supplier-logout-button");
  if (supplierLogoutBtn) {
    supplierLogoutBtn.style.display = (state.auth.source === "login") ? "" : "none";
  }
  // Show refresh banner if supplier access was approved since last login (token is stale)
  const existingBanner = document.getElementById("supplier-access-banner");
  if (profile.access_needs_refresh && !canBeSupplier && state.auth.source === "tetis") {
    if (!existingBanner) {
      const banner = document.createElement("div");
      banner.id = "supplier-access-banner";
      banner.style.cssText = "background:#16a34a;color:#fff;text-align:center;padding:10px 16px;font-size:14px;font-weight:500;";
      banner.textContent = "🎉 Ваша заявка поставщика одобрена! Перейдите на tetis1.kz и снова откройте Склад — переключатель «Режим: Поставщик» появится автоматически.";
      document.body.insertAdjacentElement("afterbegin", banner);
    }
  } else if (existingBanner) {
    existingBanner.remove();
  }
}

function headers(extra = {}) {
  const authToken = el("auth-token").value.trim();
  const shouldSendAuthToken = state.auth.source === "tetis" && authToken;
  const loginToken = state.auth.loginToken;
  const shouldSendLoginToken = state.auth.source === "login" && loginToken;
  return {
    "Content-Type": "application/json",
    "X-Actor-Id": el("actor-id").value || "manager",
    "X-Actor-Roles": el("actor-role").value || "warehouse_manager",
    "X-Actor-Warehouse-Ids": el("actor-warehouses").value || "",
    ...(shouldSendAuthToken ? { Authorization: `Bearer ${authToken}` } : {}),
    ...(shouldSendLoginToken ? { Authorization: `Bearer ${loginToken}` } : {}),
    ...extra,
  };
}

function warehouseFilterParam() {
  const role = el("actor-role").value;
  const warehouseId = el("warehouse-filter").value;
  if (warehouseId) return `warehouse_id=${encodeURIComponent(warehouseId)}`;
  if (role !== "warehouse_manager") {
    const firstScopedWarehouse = (el("actor-warehouses").value || "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)[0];
    return firstScopedWarehouse ? `warehouse_id=${encodeURIComponent(firstScopedWarehouse)}` : "";
  }
  return "";
}

function scopedWarehouseIds() {
  return (el("actor-warehouses").value || "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
}

function reconcileWarehouseScope() {
  const available = new Set(state.data.warehouses.map((warehouse) => String(warehouse.id)));
  const originalScoped = scopedWarehouseIds();
  const validScoped = originalScoped.filter((warehouseId) => available.has(String(warehouseId)));
  if (validScoped.length !== originalScoped.length) {
    el("actor-warehouses").value = validScoped.join(",");
  }
  updateWarehouseSelector();
  const selected = el("warehouse-filter").value;
  if (selected && !available.has(String(selected))) {
    el("warehouse-filter").value = "";
  }
  const orgId = activeTetisOrgId();
  const orgWarehouses = orgId
    ? state.data.warehouses.filter((warehouse) => String(warehouse.tetis_org_id || "") === String(orgId))
    : [];
  if (state.auth.source === "tetis" && originalScoped.length && !validScoped.length && orgWarehouses.length) {
    el("actor-warehouses").value = orgWarehouses.map((warehouse) => warehouse.id).join(",");
    updateWarehouseSelector();
    if (!el("warehouse-filter").value && orgWarehouses.length === 1) {
      el("warehouse-filter").value = String(orgWarehouses[0].id);
    }
    return;
  }
}

function currentRole() {
  return el("actor-role")?.value || "warehouse_manager";
}

function hasPermission(permission) {
  const permissions = state.auth.actor?.permissions || [];
  if (!permissions.length && state.auth.source !== "tetis") {
    return currentRole() === "warehouse_manager";
  }
  return permissions.includes(permission);
}

function currentActorId() {
  return el("actor-id")?.value || "";
}

function isLimitedRole() {
  return limitedRoles.has(currentRole());
}

function isManagerRole() {
  return currentRole() === "warehouse_manager";
}

function visibleViews() {
  const allowed = isLimitedRole() ? views.filter(([id]) => limitedRoleViews.has(id)) : views;
  return allowed.filter(([id]) => canAccessView(id));
}

function canAccessView(viewId) {
  if (managerOnlyViews.has(viewId) && !hasPermission("audit:read")) return false;
  return !isLimitedRole() || limitedRoleViews.has(viewId);
}

function ensureAccessibleView() {
  if (canAccessView(state.view) && renderers[state.view]) return;
  state.view = isLimitedRole() ? "tablet-writeoff" : "dashboard";
}

function safeViewTarget(viewId) {
  if (canAccessView(viewId)) return viewId;
  return isLimitedRole() ? "tablet-writeoff" : viewId;
}

function roleAccessNotice() {
  if (!isLimitedRole()) return "";
  return `
    <div class="role-notice">
      <strong>Упрощенный режим</strong>
      <span>Для этой роли в меню оставлены списание, остатки, история и уведомления. Административные операции скрыты на фронте.</span>
    </div>
  `;
}

async function request(path, options = {}) {
  const { isFormData, ...fetchOptions } = options;
  const reqHeaders = isFormData
    ? (() => { const h = headers({}); delete h["Content-Type"]; return h; })()
    : headers(options.headers || {});
  const response = await fetch(`${API}${path}`, {
    ...fetchOptions,
    headers: reqHeaders,
  });
  const text = await response.text();
  const body = parseJson(text);
  if (!response.ok) {
    const message = body?.detail?.message || body?.detail || body?.message || response.statusText || `HTTP ${response.status}`;
    if (response.status === 401) {
      throw new AuthRequiredError(message);
    }
    throw new ApiError(message, response.status, body?.detail?.code || body?.code || "");
  }
  return body;
}

function parseJson(text, fallback = null) {
  if (!text) return fallback;
  try {
    return JSON.parse(text);
  } catch {
    return fallback;
  }
}

function escapeHtml(value) {
  return String(value ?? "—")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}

function csvCell(value) {
  const text = String(value ?? "").replaceAll('"', '""');
  return `"${text}"`;
}

function downloadCsv(filename, columns, rows) {
  const header = columns.map((column) => csvCell(column.label)).join(",");
  const body = rows.map((row) => columns.map((column) => {
    const value = column.value ? column.value(row) : row[column.key];
    return csvCell(value);
  }).join(","));
  const blob = new Blob([[header, ...body].join("\n")], { type: "text/csv;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  URL.revokeObjectURL(link.href);
  link.remove();
}

function downloadText(filename, text, type = "text/plain;charset=utf-8") {
  const blob = new Blob([text], { type });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  URL.revokeObjectURL(link.href);
  link.remove();
}

async function mutate(path, payload, method = "POST") {
  return request(path, {
    method,
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: JSON.stringify(payload),
  });
}

async function removeResource(path) {
  return request(path, {
    method: "DELETE",
    headers: { "Idempotency-Key": crypto.randomUUID() },
  });
}

function showAlert(message, type = "success") {
  const item = document.createElement("div");
  item.className = `alert ${type}`;
  item.textContent = message;
  el("alerts").replaceChildren(item);
  window.setTimeout(() => item.remove(), 4200);
}

function clearFormError(formElement) {
  formElement.querySelector(".form-error")?.remove();
}

function showFormError(formElement, message) {
  clearFormError(formElement);
  const item = document.createElement("div");
  item.className = "form-error full";
  item.setAttribute("role", "alert");
  item.textContent = message;
  const actions = formElement.querySelector(".actions");
  if (actions) {
    actions.insertAdjacentElement("beforebegin", item);
    return;
  }
  formElement.appendChild(item);
}

function money(value) {
  if (value === null || value === undefined || value === "") return "—";
  return String(value);
}

function qty(value) {
  if (value === null || value === undefined || value === "") return "—";
  return String(value);
}

function dateText(value) {
  if (!value) return "—";
  return new Date(value).toLocaleString("ru-RU");
}

function badge(value) {
  const text = String(value ?? "—");
  let cls = "badge";
  if (["available", "posted", "active", "ok", "succeeded"].includes(text)) cls += " ok";
  if (["quarantine", "draft", "approved", "processing", "warning"].includes(text)) cls += " warn";
  if (["blocked", "cancelled", "failed", "released"].includes(text)) cls += " bad";
  return `<span class="${cls}">${escapeHtml(humanStatus(text))}</span>`;
}

function humanStatus(value) {
  const ru = ({
    active: "Активно",
    approved: "Допущено",
    available: "Можно использовать",
    blocked: "Заблокировано",
    cancelled: "Отменено",
    draft: "Черновик",
    failed: "Ошибка",
    in_review: "На проверке",
    locked: "Заблокировано",
    ok: "В порядке",
    open: "Открыто",
    posted: "Проведен",
    processing: "В обработке",
    quarantine: "Карантин",
    pending: "Ожидает проверки",
    read: "Прочитано",
    received: "Получено",
    repack: "Фасовка",
    repack_in: "Результат фасовки",
    repack_out: "Исходная партия",
    receipt: "Приход",
    requested: "Запрошено",
    rejected: "Забраковано",
    released: "Снято",
    return_from_department: "Возврат от отделения",
    return_to_supplier: "Возврат поставщику",
    sent: "Отправлено",
    succeeded: "Выполнено",
    transfer: "Перемещение",
    unread: "Новое",
    used: "Использовано",
    warning: "Внимание",
    write_off: "Списание",
  })[String(value)] || String(value ?? "—");
  return t(ru);
}

function humanDocumentType(value) {
  return ({
    receipt: "Приход",
    write_off: "Списание",
    transfer: "Перемещение",
    repack: "Фасовка / переупаковка",
    return_from_department: "Возврат от отделения",
    return_to_supplier: "Возврат поставщику",
  })[String(value)] || humanStatus(value);
}

function humanNotificationType(value) {
  return ({
    low_stock: "Мало остатка",
    expiry: "Срок годности",
    inventory: "Инвентаризация",
    quarantine: "Карантин",
    sensor_warning: "Условия хранения",
    stock: "Склад",
    grafana_alert: "Мониторинг Grafana",
    supplier_contract_expiry: "Договор поставщика",
  })[String(value)] || humanStatus(value);
}

function analyticsClassBadge(value, kind) {
  const text = String(value || "—");
  const cls = kind === "abc" && text === "A" ? "badge ok"
    : kind === "abc" && text === "B" ? "badge warn"
    : kind === "xyz" && text === "Z" ? "badge bad"
    : "badge";
  return `<span class="${cls}">${escapeHtml(text)}</span>`;
}

function activeSearchQuery() {
  return state.ui.search.trim();
}

function searchEmptyText(defaultText) {
  const query = activeSearchQuery();
  if (!query) return defaultText;
  return `По запросу “${query}” ничего не найдено. Сбросьте поиск или измените текст.`;
}

function searchNotice() {
  const query = activeSearchQuery();
  if (!query) return "";
  return `
    <div class="search-banner">
      <span>Показаны результаты по запросу: <strong>${escapeHtml(query)}</strong></span>
      <button class="secondary" type="button" data-clear-search>Сбросить</button>
    </div>
  `;
}

function table(columns, rows, empty = "Данных пока нет") {
  if (!rows || rows.length === 0) return `<div class="empty">${escapeHtml(searchEmptyText(t(empty)))}</div>`;
  return `
    <div class="table-summary">
      <span>Найдено записей: ${escapeHtml(rows.length)}</span>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr>${columns.map((col) => `<th>${escapeHtml(t(col.label))}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((row) => `
            <tr>
              ${columns.map((col) => `<td>${col.render ? col.render(row) : escapeHtml(row[col.key] ?? "—")}</td>`).join("")}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function batchButton(batchId, label = null) {
  if (!batchId) return "—";
  return `<button class="link-button" type="button" data-batch-detail="${escapeAttr(batchId)}">${label || `#${escapeHtml(batchId)}`}</button>`;
}

function extraFieldAttrs(field) {
  return [
    field.batchWarehouseField ? `data-batch-warehouse-field="${escapeAttr(field.batchWarehouseField)}"` : "",
  ].filter(Boolean).join(" ");
}

function form(id, fields, buttonText, options = {}) {
  const disabled = Boolean(options.disabledSubmit);
  return `
    <form id="${escapeAttr(id)}" class="form-grid" ${options.batchAware ? "data-batch-aware=\"true\"" : ""}>
      ${fields.map((field) => field.type === "select" ? `
        <label class="${field.full ? "full" : ""}">${escapeHtml(t(field.label))}
          <select name="${escapeAttr(field.name)}" ${field.required ? "required" : ""} ${extraFieldAttrs(field)}>
            ${(field.options || []).map((option) => `
              <option value="${escapeAttr(option.value)}" ${String(option.value) === String(field.value ?? "") ? "selected" : ""}>${option.label}</option>
            `).join("")}
          </select>
        </label>
      ` : field.type === "textarea" ? `
        <label class="${field.full ? "full" : ""}">${escapeHtml(t(field.label))}
          <textarea name="${escapeAttr(field.name)}" ${field.required ? "required" : ""}>${escapeHtml(field.value || "")}</textarea>
        </label>
      ` : field.suffixActions ? `
        <label class="${field.full ? "full" : ""}">${escapeHtml(t(field.label))}
          <div class="field-with-actions">
            <input name="${escapeAttr(field.name)}" type="text" value="${escapeAttr(field.value || "")}" ${field.required ? "required" : ""} ${extraFieldAttrs(field)} />
            ${field.suffixActions.map((action) => `
              <button type="button" class="icon-button" data-action="${escapeAttr(action.action)}" data-target-field="${escapeAttr(field.name)}" title="${escapeAttr(action.title)}">${action.icon}</button>
            `).join("")}
          </div>
        </label>
      ` : `
        <label class="${field.full ? "full" : ""}">${escapeHtml(t(field.label))}
          <input name="${escapeAttr(field.name)}" type="${escapeAttr(field.type || "text")}" value="${escapeAttr(field.value || "")}" ${field.required ? "required" : ""} ${field.step ? `step="${escapeAttr(field.step)}"` : ""} ${field.min ? `min="${escapeAttr(field.min)}"` : ""} ${extraFieldAttrs(field)} />
        </label>
      `).join("")}
      ${options.batchAware ? '<div class="batch-summary full" data-selected-batch-summary>Выберите партию, и здесь появится доступный остаток и склад.</div>' : ""}
      ${options.submitHint ? `<div class="form-hint full ${disabled ? "blocked" : ""}">${escapeHtml(options.submitHint)}</div>` : ""}
      <div class="actions full"><button class="primary" type="submit" ${disabled ? "disabled" : ""}>${escapeHtml(t(buttonText))}</button></div>
    </form>
  `;
}

function generateEan13() {
  let digits = "";
  for (let i = 0; i < 12; i++) digits += Math.floor(Math.random() * 10);
  let sum = 0;
  for (let i = 0; i < 12; i++) sum += Number(digits[i]) * (i % 2 === 0 ? 1 : 3);
  const checkDigit = (10 - (sum % 10)) % 10;
  return digits + String(checkDigit);
}

function optionsFrom(collection, placeholder, label = (item) => item.name) {
  return [
    { value: "", label: escapeHtml(t(placeholder)) },
    ...state.data[collection].map((item) => ({ value: item.id, label: `${escapeHtml(label(item))} (#${escapeHtml(item.id)})` })),
  ];
}

function staticOptions(items, placeholder) {
  return [{ value: "", label: escapeHtml(placeholder) }, ...items.map(([value, label]) => ({ value, label: escapeHtml(label) }))];
}

function productUnitOptions(placeholder = "Выберите единицу") {
  const units = state.data.productUnits.length
    ? state.data.productUnits
    : ["шт", "уп", "рулон", "флакон", "бут", "ампула"];
  return staticOptions(units.map((unit) => [unit, unit]), placeholder);
}

function pageItems(payload) {
  return Array.isArray(payload) ? payload : (payload?.items || []);
}

function searchText(...parts) {
  return parts
    .filter((part) => part !== null && part !== undefined)
    .join(" ")
    .toLowerCase();
}

function matchesSearch(row, ...parts) {
  const query = state.ui.search.trim().toLowerCase();
  if (!query) return true;
  return searchText(...parts).includes(query);
}

function filteredBalances(rows = state.data.balances.items) {
  return rows.filter((row) => matchesSearch(
    row,
    row.batch_id,
    row.batch_status,
    row.expires_on,
    rawNameById("products", row.product_id),
    rawNameById("warehouses", row.warehouse_id),
  ));
}

function filteredRows(rows, selector) {
  return rows.filter((row) => {
    const parts = selector(row);
    return matchesSearch(row, ...(Array.isArray(parts) ? parts : [parts]));
  });
}

const reportConfigs = {
  balances: {
    filename: "sklad-balances.csv",
    columns: [
      { label: "Товар", value: (row) => rawNameById("products", row.product_id) },
      { label: "Партия", key: "batch_id" },
      { label: "Склад", value: (row) => rawNameById("warehouses", row.warehouse_id) },
      { label: "Всего", key: "total_quantity" },
      { label: "Резерв", key: "reserved_quantity" },
      { label: "Свободно", key: "free_quantity" },
      { label: "Статус партии", value: (row) => humanStatus(row.batch_status) },
      { label: "Годен до", key: "expires_on" },
    ],
    rows: () => filteredBalances(state.data.balances.items),
  },
  movements: {
    filename: "sklad-movements.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Действие", value: (row) => humanStatus(row.movement_type) },
      { label: "Партия", value: (row) => rawBatchLabel(row.batch_id) },
      { label: "Склад", value: (row) => rawNameById("warehouses", row.warehouse_id) },
      { label: "Количество", key: "quantity" },
      { label: "Причина", key: "reason" },
      { label: "Время", value: (row) => dateText(row.created_at) },
    ],
    rows: () => filteredRows(state.data.movements, (row) => [
      row.id,
      row.movement_type,
      rawBatchLabel(row.batch_id),
      rawNameById("warehouses", row.warehouse_id),
      row.quantity,
      row.reason,
      row.created_at,
    ]),
  },
  documents: {
    filename: "sklad-documents.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Тип", value: (row) => humanDocumentType(row.document_type) },
      { label: "Статус", value: (row) => humanStatus(row.status) },
      { label: "Склад", value: (row) => rawNameById("warehouses", row.warehouse_id) },
      { label: "Строк", value: (row) => row.lines?.length || 0 },
      { label: "Создал", key: "created_by" },
      { label: "Создан", value: (row) => dateText(row.created_at) },
      { label: "Утвердил", key: "approved_by" },
      { label: "Утвержден", value: (row) => dateText(row.approved_at) },
      { label: "Проведен", value: (row) => dateText(row.posted_at) },
    ],
    rows: () => filteredRows(state.data.documents, (row) => [
      row.id,
      row.document_type,
      row.status,
      rawNameById("warehouses", row.warehouse_id),
      row.created_by,
      row.created_at,
      row.approved_by,
      row.approved_at,
      row.posted_at,
    ]),
  },
  analytics: {
    filename: "sklad-abc-xyz.csv",
    columns: [
      { label: "Товар", key: "product_name" },
      { label: "Код товара", key: "sku" },
      { label: "ABC", key: "abc_class" },
      { label: "XYZ", key: "xyz_class" },
      { label: "Расход", key: "consumption_quantity" },
      { label: "Стоимость расхода", key: "consumption_value" },
      { label: "Свободно", key: "current_free_quantity" },
      { label: "Точка заказа", key: "reorder_point" },
      { label: "Страховой запас", key: "safety_stock" },
      { label: "Заказать", key: "recommended_order_quantity" },
      { label: "Рекомендация", key: "recommendation" },
    ],
    rows: () => filteredRows(state.data.analytics.items || [], (row) => [
      row.product_name,
      row.sku,
      row.abc_class,
      row.xyz_class,
      row.recommendation,
      row.recommended_order_quantity,
    ]),
  },
  abcXyzRuns: {
    filename: "sklad-abc-xyz-history.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Склад", value: (row) => row.warehouse_id ? rawNameById("warehouses", row.warehouse_id) : "Все склады" },
      { label: "Дней анализа", key: "analysis_days" },
      { label: "Период с", value: (row) => dateText(row.period_start) },
      { label: "Период по", value: (row) => dateText(row.period_end) },
      { label: "Источник", key: "source" },
      { label: "Статус", value: (row) => humanStatus(row.status) },
      { label: "Позиций", key: "items_count" },
      { label: "Создан", value: (row) => dateText(row.generated_at) },
    ],
    rows: () => filteredRows(state.data.abcXyzRuns.items || [], (row) => [
      row.id,
      row.warehouse_id,
      row.analysis_days,
      row.source,
      row.status,
      row.generated_at,
    ]),
  },
  purchaseRequests: {
    filename: "sklad-purchase-requests.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Товар", value: (row) => rawNameById("products", row.product_id) },
      { label: "Склад", value: (row) => row.warehouse_id ? rawNameById("warehouses", row.warehouse_id) : "" },
      { label: "Количество", key: "quantity" },
      { label: "Статус", value: (row) => humanStatus(row.status) },
      { label: "Причина", key: "reason" },
      { label: "Создано", value: (row) => dateText(row.created_at) },
    ],
    rows: () => filteredRows(state.data.purchaseRequests, (row) => [
      row.id,
      rawNameById("products", row.product_id),
      rawNameById("warehouses", row.warehouse_id),
      row.quantity,
      row.status,
      row.reason,
      row.created_at,
    ]),
  },
  batchRecalls: {
    filename: "sklad-batch-recalls.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Товар", key: "product_name" },
      { label: "Партия", key: "lot" },
      { label: "Источник", key: "source" },
      { label: "Основание", key: "reference" },
      { label: "Причина", key: "reason" },
      { label: "Создал", key: "created_by" },
      { label: "Создано", value: (row) => dateText(row.created_at) },
    ],
    rows: () => filteredRows(state.data.batchRecalls.items || [], (row) => [
      row.id,
      row.product_name,
      row.lot,
      row.source,
      row.reference,
      row.reason,
      row.created_by,
      row.created_at,
    ]),
  },
  audit: {
    filename: "sklad-audit-log.csv",
    columns: [
      { label: "Время", value: (row) => dateText(row.created_at) },
      { label: "Пользователь", key: "actor_id" },
      { label: "Действие", key: "action" },
      { label: "Сущность", value: (row) => `${row.entity_type} #${row.entity_id}` },
      { label: "Склад", value: (row) => row.warehouse_id || "" },
      { label: "Данные", value: (row) => JSON.stringify(row.payload || {}) },
    ],
    rows: () => filteredRows(state.data.audit.items || [], (row) => [
      row.created_at,
      row.actor_id,
      row.action,
      row.entity_type,
      row.entity_id,
      row.warehouse_id,
      JSON.stringify(row.payload),
    ]),
  },
  sensorReadings: {
    filename: "sklad-storage-conditions.csv",
    columns: [
      { label: "Время", value: (row) => dateText(row.recorded_at) },
      { label: "Склад", value: (row) => row.warehouse_name || rawNameById("warehouses", row.warehouse_id) },
      { label: "Датчик", value: (row) => row.device_name || `#${row.device_id}` },
      { label: "Температура", key: "temperature_c" },
      { label: "Влажность", key: "humidity_percent" },
      { label: "Статус", value: (row) => humanStatus(row.status) },
      { label: "Источник", key: "raw_payload" },
    ],
    rows: () => filteredRows(state.data.sensorReadings.items || [], (row) => [
      row.recorded_at,
      row.warehouse_name,
      row.device_name,
      row.temperature_c,
      row.humidity_percent,
      row.status,
      row.raw_payload,
    ]),
  },
  repackings: {
    filename: "sklad-repackings.csv",
    columns: [
      { label: "Номер", key: "id" },
      { label: "Документ", key: "document_id" },
      { label: "Исходная партия", value: (row) => rawBatchLabel(row.source_batch_id) },
      { label: "Результат", value: (row) => rawBatchLabel(row.target_batch_id) },
      { label: "Склад", value: (row) => rawNameById("warehouses", row.warehouse_id) },
      { label: "Исходное количество", key: "source_quantity" },
      { label: "Получено", key: "target_quantity" },
      { label: "Коэффициент", key: "conversion_factor" },
      { label: "Потери", key: "loss_quantity" },
      { label: "Причина", key: "reason" },
      { label: "Создал", key: "created_by" },
      { label: "Создано", value: (row) => dateText(row.created_at) },
    ],
    rows: () => filteredRows(pageItems(state.data.repackings), (row) => [
      row.id,
      row.document_id,
      rawBatchLabel(row.source_batch_id),
      rawBatchLabel(row.target_batch_id),
      rawNameById("warehouses", row.warehouse_id),
      row.source_quantity,
      row.target_quantity,
      row.conversion_factor,
      row.loss_quantity,
      row.reason,
      row.created_by,
      row.created_at,
    ]),
  },
  inventorySheet: {
    filename: "sklad-inventory-sheet.csv",
    columns: [
      { label: "Сессия", value: (row) => row.session_id },
      { label: "Склад", value: (row) => rawNameById("warehouses", row.warehouse_id) },
      { label: "Товар", value: (row) => rawNameById("products", row.product_id) },
      { label: "Партия", value: (row) => rawBatchLabel(row.batch_id) },
      { label: "Ожидалось", key: "expected_quantity" },
      { label: "Факт", value: (row) => row.actual_quantity ?? "" },
      { label: "Расхождение", value: (row) => row.difference_quantity ?? "" },
    ],
    rows: () => {
      const session = selectedInventorySession();
      return (session?.lines || []).map((line) => ({
        ...line,
        session_id: session.id,
        warehouse_id: session.warehouse_id,
      }));
    },
  },
};

function exportReport(reportName) {
  const config = reportConfigs[reportName];
  if (!config) return;
  const rows = config.rows();
  if (!rows.length) {
    showAlert("В отчете нет строк для выгрузки", "error");
    return;
  }
  downloadCsv(config.filename, config.columns, rows);
  showAlert("Отчет выгружен");
}

async function loadOptional(label, requestPromise, fallback) {
  try {
    return await requestPromise;
  } catch (error) {
    if (error instanceof AuthRequiredError) throw error;
    if (error instanceof ApiError && [401, 403, 404].includes(error.status)) {
      return fallback;
    }
    state.loadWarnings.push(`${label}: раздел не загрузился, обновите страницу`);
    return fallback;
  }
}

function batchOptions(placeholder, { onlyAvailable = true, productId = null } = {}) {
  const seen = new Set();
  const options = state.data.balances.items
    .filter((item) => Number(item.free_quantity || 0) > 0)
    .filter((item) => !onlyAvailable || item.batch_status === "available")
    .filter((item) => !productId || Number(item.product_id) === Number(productId))
    .filter((item) => {
      const key = `${item.batch_id}:${item.warehouse_id}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .map((item) => {
      const batch = state.data.batches.find((entry) => Number(entry.id) === Number(item.batch_id));
      const lot = batch?.lot || item.lot || "—";
      const expires = item.expires_on ? ` · до ${item.expires_on}` : "";
      return {
        value: item.batch_id,
        label: escapeHtml(`${rawNameById("products", item.product_id)} · серия ${lot} · ${rawNameById("warehouses", item.warehouse_id)} · свободно ${item.free_quantity}${expires} · ${humanStatus(item.batch_status)}`),
      };
    });
  return [{ value: "", label: escapeHtml(placeholder) }, ...options];
}

function batchById(batchId) {
  return state.data.batches.find((entry) => Number(entry.id) === Number(batchId));
}

function productForBatch(batchId) {
  const batch = batchById(batchId);
  if (!batch) return null;
  return state.data.products.find((product) => Number(product.id) === Number(batch.product_id)) || null;
}

function isControlledProduct(productId) {
  const product = state.data.products.find((entry) => Number(entry.id) === Number(productId));
  return Boolean(product?.is_controlled);
}

function controlledWriteoffMetadataMissing(payload) {
  const controlled = payload.batch_id
    ? Boolean(productForBatch(payload.batch_id)?.is_controlled)
    : isControlledProduct(payload.product_id);
  if (!controlled) return [];
  return ["patient_id", "doctor_id", "medical_record_no", "second_approver_id"].filter((field) => !String(payload[field] || "").trim());
}

function controlledWriteoffMessage() {
  return "Для ПКУ заполните пациента, врача, номер истории болезни и второго подтверждающего.";
}

function applyControlledWriteoffRequirements(formElement, payload = null) {
  const data = payload || collect(formElement);
  const missing = controlledWriteoffMetadataMissing(data);
  const controlled = missing.length > 0 || (data.batch_id
    ? Boolean(productForBatch(data.batch_id)?.is_controlled)
    : isControlledProduct(data.product_id));
  ["patient_id", "doctor_id", "medical_record_no", "second_approver_id"].forEach((field) => {
    const input = formElement.elements[field];
    if (!input) return;
    input.required = controlled;
    input.closest("label")?.classList.toggle("controlled-required", controlled);
  });
  return missing;
}

function balanceForBatch(batchId, warehouseId = null) {
  return state.data.balances.items.find((item) => {
    if (Number(item.batch_id) !== Number(batchId)) return false;
    if (warehouseId && Number(item.warehouse_id) !== Number(warehouseId)) return false;
    return Number(item.free_quantity || 0) > 0;
  });
}

function selectedBatchSummary(batchId, warehouseId = null) {
  const batch = batchById(batchId);
  const balance = balanceForBatch(batchId, warehouseId);
  if (!batch || !balance) return null;
  return {
    batch,
    balance,
    productName: rawNameById("products", batch.product_id),
    warehouseName: rawNameById("warehouses", balance.warehouse_id),
    supplierName: rawNameById("suppliers", batch.supplier_id),
  };
}

function selectedBatchSummaryHtml(batchId, warehouseId = null) {
  const summary = selectedBatchSummary(batchId, warehouseId);
  if (!batchId) return "Выберите партию, и здесь появится доступный остаток и склад.";
  if (!summary) return "По выбранной партии нет свободного остатка на выбранном складе.";
  return [
    `<strong>${escapeHtml(summary.productName)}</strong>`,
    `серия ${escapeHtml(summary.batch.lot)}`,
    `склад: ${escapeHtml(summary.warehouseName)}`,
    `свободно: ${escapeHtml(summary.balance.free_quantity)}`,
    `годен до: ${escapeHtml(summary.batch.expires_on || "не указан")}`,
    `поставщик: ${escapeHtml(summary.supplierName)}`,
    batchButton(batchId, "Открыть карточку партии"),
  ].join(" · ");
}

function operationPreview(kind, payload) {
  const warehouseId = payload.warehouse_id || payload.source_warehouse_id;
  const summary = selectedBatchSummary(payload.batch_id, warehouseId);
  const quantity = Number(payload.quantity || 0);
  const free = Number(summary?.balance?.free_quantity || 0);
  const remaining = Number.isFinite(quantity) ? Math.max(0, free - quantity) : free;
  if (!summary) return `Партия #${payload.batch_id}: проверьте выбранный склад и количество.`;
  if (kind === "transfer" || kind === "department-return") {
    const sourceName = rawNameById("warehouses", payload.source_warehouse_id);
    const targetName = rawNameById("warehouses", payload.target_warehouse_id);
    return `${summary.productName}, серия ${summary.batch.lot}: ${payload.quantity} уйдет со склада “${sourceName}” на склад “${targetName}”. На источнике останется ${remaining}.`;
  }
  if (kind === "supplier-return") {
    return `${summary.productName}, серия ${summary.batch.lot}: ${payload.quantity} будет возвращено поставщику “${rawNameById("suppliers", payload.supplier_id)}”. На складе останется ${remaining}.`;
  }
  return `${summary.productName}, серия ${summary.batch.lot}: будет списано ${payload.quantity}. На складе “${summary.warehouseName}” останется ${remaining}.`;
}

function normalizeRepackingPayload(payload) {
  const sourceQuantity = Number(payload.quantity || 0);
  const targetQuantity = Number(payload.target_quantity || 0);
  const lossQuantity = Number(payload.loss_quantity || 0);
  const usableSource = Math.max(0, sourceQuantity - lossQuantity);
  const conversionFactor = usableSource > 0 && targetQuantity > 0
    ? (targetQuantity / usableSource).toFixed(6)
    : payload.conversion_factor || "1";
  return {
    warehouse_id: payload.warehouse_id,
    lines: [{
      batch_id: payload.batch_id,
      target_product_id: payload.target_product_id,
      quantity: payload.quantity,
      target_quantity: payload.target_quantity,
      conversion_factor: conversionFactor,
      loss_quantity: payload.loss_quantity || "0",
      target_lot: payload.target_lot,
      target_expires_on: payload.target_expires_on || null,
      target_unit_price: payload.target_unit_price || null,
      quarantine: Boolean(payload.quarantine),
      reason: payload.reason || "Фасовка / переупаковка",
    }],
  };
}

function repackingPreview(payload) {
  const summary = selectedBatchSummary(payload.batch_id, payload.warehouse_id);
  const sourceQuantity = Number(payload.quantity || 0);
  const targetQuantity = Number(payload.target_quantity || 0);
  const lossQuantity = Number(payload.loss_quantity || 0);
  const free = Number(summary?.balance?.free_quantity || 0);
  const remaining = Number.isFinite(sourceQuantity) ? Math.max(0, free - sourceQuantity) : free;
  const targetName = rawNameById("products", payload.target_product_id);
  if (!summary) return `Партия #${payload.batch_id}: проверьте выбранный склад и доступный остаток.`;
  return `${summary.productName}, серия ${summary.batch.lot}: ${payload.quantity} уйдет в фасовку, получится ${payload.target_quantity} “${targetName}”, потери ${lossQuantity || 0}. На складе останется ${remaining}.`;
}

function renderRecallStats() {
  const s = state.data.recallStats;
  if (!s) return '<p style="color:#6b7280">Загрузка статистики...</p>';
  const bySource = s.by_source || [];
  return `
    <div style="display:flex;gap:2rem;flex-wrap:wrap;padding:.5rem 0 1rem">
      <div style="text-align:center">
        <div style="font-size:2rem;font-weight:700;color:#1e3a5f">${s.total_recalls}</div>
        <div style="font-size:.8rem;color:#6b7280">Всего отзывов</div>
      </div>
      <div style="text-align:center">
        <div style="font-size:2rem;font-weight:700;color:${s.blocked_batches > 0 ? "#dc2626" : "#16a34a"}">${s.blocked_batches}</div>
        <div style="font-size:.8rem;color:#6b7280">Заблокировано партий</div>
      </div>
      ${bySource.map(r => `
        <div style="text-align:center">
          <div style="font-size:1.5rem;font-weight:600;color:#374151">${r.cnt}</div>
          <div style="font-size:.8rem;color:#6b7280">Источник: ${escapeHtml(r.source)}</div>
        </div>
      `).join("")}
    </div>
    ${s.recent && s.recent.length ? `
      <div style="font-size:.85rem;color:#374151;margin-bottom:.25rem"><b>Последние отзывы</b></div>
      <div style="display:flex;flex-direction:column;gap:.3rem">
        ${s.recent.map(r => `
          <div style="display:flex;align-items:center;gap:.75rem;padding:.4rem;background:#f9fafb;border-radius:4px;flex-wrap:wrap">
            ${badge(r.batch_status)}
            <span>${escapeHtml(r.product_name || "—")}</span>
            <span style="font-size:.8rem;color:#6b7280">Серия: ${escapeHtml(r.lot || "—")}${r.serial_number ? " | S/N: " + escapeHtml(r.serial_number) : ""}</span>
            <span style="font-size:.8rem">${escapeHtml(r.reason || "")}</span>
            <span style="font-size:.75rem;color:#6b7280">${(r.created_at||"").slice(0,10)}</span>
            ${r.batch_status === "blocked" ? `<button class="secondary" data-action="unblock-batch" data-batch-id="${r.batch_id}" style="font-size:.8rem;padding:.2rem .5rem">Разблокировать</button>` : ""}
          </div>
        `).join("")}
      </div>
    ` : ""}
  `;
}

function recallPreview(payload) {
  const summary = selectedBatchSummary(payload.batch_id, payload.warehouse_id);
  if (!summary) return `Партия #${payload.batch_id}: проверьте выбранный склад и остаток.`;
  return `${summary.productName}, серия ${summary.batch.lot}: партия будет заблокирована на всех складах с остатком. Причина: ${payload.reason || "не указана"}.`;
}

function inventoryProgress(session) {
  const lines = session?.lines || [];
  const filled = lines.filter((line) => line.actual_quantity !== null && line.actual_quantity !== undefined && line.actual_quantity !== "").length;
  return {
    total: lines.length,
    filled,
    missing: Math.max(0, lines.length - filled),
  };
}

function inventorySummary(session) {
  if (session?.summary) return session.summary;
  const lines = session?.lines || [];
  return lines.reduce((summary, line) => {
    const expected = Number(line.expected_quantity || 0);
    const actualRaw = line.actual_quantity;
    const filled = actualRaw !== null && actualRaw !== undefined && actualRaw !== "";
    const actual = filled ? Number(actualRaw || 0) : 0;
    const difference = filled ? Number(line.difference_quantity ?? actual - expected) : 0;
    summary.total_lines += 1;
    summary.total_expected_quantity += expected;
    if (!filled) {
      summary.missing_lines += 1;
      return summary;
    }
    summary.filled_lines += 1;
    summary.total_actual_quantity += actual;
    if (difference > 0) {
      summary.surplus_lines += 1;
      summary.total_surplus_quantity += difference;
    } else if (difference < 0) {
      summary.shortage_lines += 1;
      summary.total_shortage_quantity += Math.abs(difference);
    } else {
      summary.matched_lines += 1;
    }
    return summary;
  }, {
    total_lines: 0,
    filled_lines: 0,
    missing_lines: 0,
    surplus_lines: 0,
    shortage_lines: 0,
    matched_lines: 0,
    total_expected_quantity: 0,
    total_actual_quantity: 0,
    total_surplus_quantity: 0,
    total_shortage_quantity: 0,
  });
}

function selectedInventorySession() {
  return state.data.inventorySessions.find((session) => session.status === "in_progress")
    || state.data.inventorySessions[0];
}

function inventorySummaryHtml(session) {
  const summary = inventorySummary(session);
  const items = [
    ["Строк", summary.total_lines],
    ["Заполнено", `${summary.filled_lines}/${summary.total_lines}`],
    ["Недостачи", `${summary.shortage_lines} · ${qty(summary.total_shortage_quantity)}`],
    ["Излишки", `${summary.surplus_lines} · ${qty(summary.total_surplus_quantity)}`],
    ["Без расхождений", summary.matched_lines],
  ];
  return `<div class="inventory-summary">${items.map(([label, value]) => `
    <div><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>
  `).join("")}</div>`;
}

function inventoryProgressText(session) {
  if (!session) return "Выберите проверку склада.";
  const progress = inventoryProgress(session);
  if (!progress.total) return "В проверке нет строк. Проверьте остатки выбранного склада.";
  if (progress.missing > 0) {
    return `Заполнено ${progress.filled} из ${progress.total}. Осталось внести факт по ${progress.missing} строкам.`;
  }
  return `Все ${progress.total} строк заполнены. Можно завершать проверку.`;
}

function inventoryCompletionPreview(sessionId) {
  const session = state.data.inventorySessions.find((item) => Number(item.id) === Number(sessionId));
  if (!session) return `Провести инвентаризацию #${sessionId}?`;
  const progress = inventoryProgress(session);
  if (progress.missing > 0) {
    return `В проверке #${session.id} еще не заполнено ${progress.missing} строк. Система не проведет инвентаризацию, пока все факты не внесены.`;
  }
  return `Провести инвентаризацию #${session.id}? Будут применены расхождения по ${progress.total} строкам.`;
}

function setPending(control, pending, pendingText = "Выполняется...") {
  if (!control) return;
  if (pending) {
    control.dataset.originalText = control.textContent;
    control.textContent = pendingText;
    control.disabled = true;
    control.classList.add("pending");
    control.setAttribute("aria-busy", "true");
    return;
  }
  control.textContent = control.dataset.originalText || control.textContent;
  delete control.dataset.originalText;
  control.disabled = false;
  control.classList.remove("pending");
  control.removeAttribute("aria-busy");
}

function confirmAction(message, { title = "Подтвердите действие", confirmText = "Да, выполнить", cancelText = "Отмена", tone = "danger" } = {}) {
  return new Promise((resolve) => {
    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML = `
      <section class="confirm-modal ${escapeAttr(tone)}" role="dialog" aria-modal="true" aria-labelledby="confirm-title">
        <header>
          <h2 id="confirm-title">${escapeHtml(title)}</h2>
        </header>
        <p class="confirm-message">${escapeHtml(message)}</p>
        <footer>
          <button class="secondary" type="button" data-confirm-cancel>${escapeHtml(cancelText)}</button>
          <button class="${tone === "danger" ? "danger" : "primary"}" type="button" data-confirm-ok>${escapeHtml(confirmText)}</button>
        </footer>
      </section>
    `;
    document.body.appendChild(backdrop);

    const cancelButton = backdrop.querySelector("[data-confirm-cancel]");
    const okButton = backdrop.querySelector("[data-confirm-ok]");
    const previousFocus = document.activeElement;

    const close = (answer) => {
      backdrop.remove();
      document.removeEventListener("keydown", onKeydown);
      if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
      resolve(answer);
    };
    const onKeydown = (event) => {
      if (event.key === "Escape") close(false);
    };

    cancelButton.addEventListener("click", () => close(false));
    okButton.addEventListener("click", () => close(true));
    backdrop.addEventListener("click", (event) => {
      if (event.target === backdrop) close(false);
    });
    document.addEventListener("keydown", onKeydown);
    (tone === "danger" ? cancelButton : okButton).focus();
  });
}

function showQuarantineDecisionModal(nextStatus) {
  return new Promise((resolve) => {
    const isReject = nextStatus === "rejected";
    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML = `
      <section class="confirm-modal" role="dialog" aria-modal="true" style="max-width:520px">
        <header><h2>${t(isReject ? "Забраковать партию" : "Допустить партию")}</h2></header>
        <div style="padding:.5rem 0;display:flex;flex-direction:column;gap:.75rem">
          <div>
            <label style="display:block;font-size:.85rem;margin-bottom:.25rem">Причина решения <span style="color:#dc2626">*</span></label>
            <textarea id="qd-reason" rows="3" placeholder="${isReject ? "Партия не прошла проверку: укажите причину" : "Документы и качество проверены, претензий нет"}" style="width:100%;box-sizing:border-box;padding:.4rem;border:1px solid #ccc;border-radius:4px;font-size:.9rem"></textarea>
          </div>
          <div>
            <label style="display:block;font-size:.85rem;margin-bottom:.25rem">Члены комиссии (через запятую)</label>
            <input id="qd-commission" type="text" placeholder="Иванов И.И., Петрова А.А." style="width:100%;box-sizing:border-box;padding:.4rem;border:1px solid #ccc;border-radius:4px">
          </div>
          ${isReject ? `
          <div>
            <label style="display:block;font-size:.85rem;margin-bottom:.5rem">Тип решения</label>
            <div style="display:flex;flex-direction:column;gap:.35rem">
              <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer">
                <input type="radio" name="qd-resolution" value="return_to_supplier" checked> Возврат поставщику
              </label>
              <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer">
                <input type="radio" name="qd-resolution" value="disposal"> Утилизация (списание)
              </label>
            </div>
          </div>
          <div id="qd-disposal-qty-block" style="display:none">
            <label style="display:block;font-size:.85rem;margin-bottom:.25rem">Количество для утилизации</label>
            <input id="qd-disposal-qty" type="number" min="0" step="0.001" placeholder="0.000" style="width:100%;box-sizing:border-box;padding:.4rem;border:1px solid #ccc;border-radius:4px">
          </div>
          ` : ""}
        </div>
        <footer style="margin-top:.75rem">
          <button class="secondary" type="button" id="qd-cancel">Отмена</button>
          <button class="${isReject ? "danger" : "primary"}" type="button" id="qd-ok">${isReject ? "Забраковать" : "Допустить"}</button>
        </footer>
      </section>
    `;
    document.body.appendChild(backdrop);
    const previousFocus = document.activeElement;
    const close = (result) => {
      backdrop.remove();
      if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
      resolve(result);
    };
    backdrop.querySelector("#qd-cancel").addEventListener("click", () => close(null));
    backdrop.addEventListener("click", (e) => { if (e.target === backdrop) close(null); });
    if (isReject) {
      backdrop.querySelectorAll("input[name='qd-resolution']").forEach(radio => {
        radio.addEventListener("change", () => {
          const block = backdrop.querySelector("#qd-disposal-qty-block");
          if (block) block.style.display = radio.value === "disposal" ? "block" : "none";
        });
      });
    }
    backdrop.querySelector("#qd-ok").addEventListener("click", () => {
      const reason = backdrop.querySelector("#qd-reason").value.trim();
      if (!reason) { backdrop.querySelector("#qd-reason").style.outline = "2px solid red"; return; }
      const commRaw = backdrop.querySelector("#qd-commission").value.trim();
      const commission = commRaw ? commRaw.split(",").map(s => s.trim()).filter(Boolean) : null;
      let resolution = null;
      let disposalQty = null;
      if (isReject) {
        const checkedRadio = backdrop.querySelector("input[name='qd-resolution']:checked");
        resolution = checkedRadio ? checkedRadio.value : "return_to_supplier";
        if (resolution === "disposal") {
          const qtyEl = backdrop.querySelector("#qd-disposal-qty");
          disposalQty = qtyEl ? parseFloat(qtyEl.value) || null : null;
        }
      }
      close({ reason, commission, resolution, disposalQty });
    });
    backdrop.querySelector("#qd-reason").focus();
  });
}


function catalogKindLabel(kind) {
  return ({
    category: "категорию",
    product: "товар",
    supplier: "поставщика",
    warehouse: "склад",
  })[kind] || "запись";
}

function catalogEditConfig(kind, row) {
  const configs = {
    category: {
      endpoint: `/categories/${row.id}`,
      fields: [
        { label: "Название категории", name: "name", value: row.name, required: true },
      ],
      normalize: (payload) => payload,
    },
    supplier: {
      endpoint: `/suppliers/${row.id}`,
      fields: [
        { label: "Название поставщика", name: "name", value: row.name, required: true },
        { label: "БИН", name: "bin", value: row.bin || "" },
        { label: "Телефон", name: "phone", type: "tel", value: row.phone || "" },
        { label: "Адрес", name: "address", value: row.address || "" },
        { label: "Рейтинг", name: "rating", type: "number", min: "1", max: "5", step: "1", value: row.rating || "" },
        { label: "Постоянный поставщик", name: "is_preferred", type: "select", options: staticOptions([["false", "Нет"], ["true", "Да"]], "Выберите значение"), value: row.is_preferred ? "true" : "false" },
        { label: "Контактное лицо", name: "contact_person", value: row.contact_person || "" },
        { label: "Email", name: "email", type: "email", value: row.email || "" },
        { label: "Номер договора", name: "contract_number", value: row.contract_number || "" },
        { label: "Договор действует до", name: "contract_expires_on", type: "date", value: row.contract_expires_on || "" },
        { label: "Условия оплаты", name: "payment_terms", value: row.payment_terms || "" },
        { label: "Заметки", name: "notes", type: "textarea", full: true, value: row.notes || "" },
      ],
      normalize: normalizeSupplierPayload,
    },
    warehouse: {
      endpoint: `/warehouses/${row.id}`,
      fields: [
        { label: "Название склада или кабинета", name: "name", value: row.name, required: true },
        { label: "Отделение", name: "department", value: row.department || "" },
        { label: "ID компании Tetis", name: "tetis_org_id", value: row.tetis_org_id || "" },
        { label: "ID склада в Tetis", name: "external_tetis_id", value: row.external_tetis_id || "" },
        { label: "ID клиники в МИС", name: "mis_clinic_id", value: row.mis_clinic_id || "" },
        { label: "ID кабинета в МИС", name: "mis_room_id", value: row.mis_room_id || "" },
        { label: "Зона хранения", name: "storage_zone", value: row.storage_zone || "" },
        { label: "Лимит вместимости", name: "capacity_limit", type: "number", step: "0.001", min: "0", value: row.capacity_limit || "" },
        { label: "Условия хранения", name: "storage_conditions", value: row.storage_conditions || "" },
        { label: "Ответственный", name: "responsible_person", value: row.responsible_person || "" },
      ],
      normalize: (payload) => ({
        ...payload,
        department: payload.department || null,
        tetis_org_id: payload.tetis_org_id || null,
        external_tetis_id: payload.external_tetis_id || null,
        mis_clinic_id: payload.mis_clinic_id || null,
        mis_room_id: payload.mis_room_id || null,
        storage_zone: payload.storage_zone || null,
        capacity_limit: payload.capacity_limit ? Number(payload.capacity_limit) : null,
        storage_conditions: payload.storage_conditions || null,
        responsible_person: payload.responsible_person || null,
      }),
    },
    product: {
      endpoint: `/products/${row.id}`,
      fields: [
        { label: "Название", name: "name", value: row.name, required: true },
        { label: "Код товара", name: "sku", value: row.sku, required: true },
        { label: "Ед. изм.", name: "unit", type: "select", options: productUnitOptions("Выберите единицу"), value: row.unit, required: true },
        { label: "Категория", name: "category_id", type: "select", options: optionsFrom("categories", "Выберите категорию"), value: row.category_id, required: true },
        { label: "Точка заказа", name: "reorder_point", type: "number", step: "0.001", min: "0", value: row.reorder_point || "0" },
        { label: "Страховой запас", name: "safety_stock", type: "number", step: "0.001", min: "0", value: row.safety_stock || "0" },
        { label: "ПКУ / контролируемый товар", name: "is_controlled", type: "select", options: staticOptions([["false", "Нет"], ["true", "Да"]], "Выберите значение"), value: row.is_controlled ? "true" : "false" },
        { label: "Штрихкод", name: "barcode", value: row.barcode || "", suffixActions: [
          { action: "scan-for-barcode-field", icon: "📷", title: "Сканировать штрихкод" },
          { action: "generate-barcode-field", icon: "🎲", title: "Сгенерировать EAN-13" },
        ] },
        { label: "Сертификат", name: "certificate_ref", value: row.certificate_ref || "" },
        { label: "Описание", name: "description", type: "textarea", full: true, value: row.description || "" },
      ],
      normalize: normalizeProductPayload,
    },
  };
  return configs[kind] || null;
}

function normalizeProductPayload(payload) {
  return {
    ...payload,
    reorder_point: payload.reorder_point || "0",
    safety_stock: payload.safety_stock || "0",
    is_controlled: payload.is_controlled === true || payload.is_controlled === "true",
    barcode: payload.barcode || null,
    description: payload.description || null,
    certificate_ref: payload.certificate_ref || null,
  };
}

function normalizeSupplierPayload(payload) {
  return {
    ...payload,
    bin: payload.bin || null,
    phone: payload.phone || null,
    address: payload.address || null,
    rating: payload.rating ? Number(payload.rating) : null,
    is_preferred: payload.is_preferred === true || payload.is_preferred === "true",
    contact_person: payload.contact_person || null,
    email: payload.email || null,
    contract_number: payload.contract_number || null,
    contract_expires_on: payload.contract_expires_on || null,
    payment_terms: payload.payment_terms || null,
    notes: payload.notes || null,
  };
}

async function showSupplierCard(id) {
  const supplier = state.data.suppliers.find((item) => Number(item.id) === Number(id));
  if (!supplier) {
    showAlert("Поставщик не найден. Обновите страницу и попробуйте еще раз.", "error");
    return;
  }
  const priceHistory = await loadOptional(
    "История цен поставщика",
    request(`/suppliers/${id}/price-history?limit=5`),
    { items: [], total: 0 },
  );
  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop";
  backdrop.innerHTML = `
    <section class="confirm-modal trace-modal" role="dialog" aria-modal="true" aria-labelledby="supplier-card-title">
      <header>
        <h2 id="supplier-card-title">${escapeHtml(supplier.name)}</h2>
        <button class="icon-button" type="button" data-supplier-card-close title="Закрыть">×</button>
      </header>
      <div class="trace-body">
        <div class="trace-summary">
          <div><span>БИН</span><strong>${escapeHtml(supplier.bin || "не указан")}</strong></div>
          <div><span>Телефон</span><strong>${escapeHtml(supplier.phone || "не указан")}</strong></div>
          <div><span>Email</span><strong>${escapeHtml(supplier.email || "не указан")}</strong></div>
          <div><span>Контакт</span><strong>${escapeHtml(supplier.contact_person || "не указан")}</strong></div>
          <div><span>Рейтинг</span><strong>${supplier.rating ? `${"★".repeat(supplier.rating)}${"☆".repeat(5-supplier.rating)} (${supplier.rating}/5)` : "не указан"}</strong></div>
          <div><span>Статус</span>${supplier.is_preferred ? badge("постоянный") : badge("обычный")}</div>
        </div>
        <div class="trace-section">
          <h3>${t("Договор и условия")}</h3>
          ${compactTraceTable([
            { label: "Адрес", render: () => escapeHtml(supplier.address || "—") },
            { label: "Договор", render: () => escapeHtml(supplier.contract_number || "—") },
            { label: "Действует до", render: () => escapeHtml(supplier.contract_expires_on || "—") },
            { label: "Оплата", render: () => escapeHtml(supplier.payment_terms || "—") },
          ], [supplier], "Реквизиты договора пока не заполнены.")}
        </div>
        <div class="trace-section">
          <h3>${t("Доступ в режим поставщика")}</h3>
          <p class="confirm-message">Пароли больше не используются. Чтобы дать этому поставщику доступ: 1) убедитесь, что у него есть аккаунт на tetis1.kz; 2) в разделе «Пользователи» этого склада свяжите его пользователя с ID поставщика <strong>${escapeAttr(supplier.id)}</strong> — после этого он сможет переключиться в «Режим: Поставщик» в верхней панели склада.</p>
        </div>
        <div class="trace-section">
          <h3>${t("Последние цены")}</h3>
          ${compactTraceTable([
            { label: "Дата", render: (row) => dateText(row.recorded_at) },
            { label: "Товар", key: "product_name" },
            { label: "SKU", key: "sku" },
            { label: "Партия", render: (row) => escapeHtml(row.lot || "—") },
            { label: "Цена", key: "unit_price" },
          ], priceHistory.items || [], "Истории цен по поставщику пока нет.")}
        </div>
        <div class="trace-section">
          <h3>${t("Заметки")}</h3>
          <p class="confirm-message">${escapeHtml(supplier.notes || "Заметок пока нет.")}</p>
        </div>
        <div class="trace-section">
          <h3>${t("Оценки и отзывы")}</h3>
          <div id="supplier-reviews-list" style="margin-bottom:.75rem;font-size:.85rem">
            <span style="color:#6b7280">Загрузка...</span>
          </div>
          <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">
            <label style="font-size:.82rem;color:var(--muted)">Оценить:</label>
            <select id="review-rating" style="width:auto;padding:.3rem;font-size:.85rem">
              <option value="5">★★★★★ Отлично</option>
              <option value="4">★★★★☆ Хорошо</option>
              <option value="3" selected>★★★☆☆ Нормально</option>
              <option value="2">★★☆☆☆ Плохо</option>
              <option value="1">★☆☆☆☆ Ужасно</option>
            </select>
            <input id="review-comment" placeholder="Комментарий (необязательно)" style="flex:1;min-width:120px;padding:.3rem .5rem;font-size:.85rem">
            <button id="submit-review-btn" class="primary" data-supplier-review-id="${escapeAttr(supplier.id)}" style="font-size:.85rem;min-height:32px;padding:.3rem .7rem">Отправить</button>
          </div>
        </div>
      </div>
      <footer>
        <button class="secondary" type="button" data-supplier-card-close>Закрыть</button>
      </footer>
    </section>
  `;
  document.body.appendChild(backdrop);
  // Load reviews
  request(`/suppliers/${supplier.id}/reviews?status=approved`).then(reviews => {
    const el = backdrop.querySelector("#supplier-reviews-list");
    if (!el) return;
    if (!reviews.length) { el.innerHTML = '<span style="color:var(--muted)">Отзывов пока нет.</span>'; return; }
    el.innerHTML = reviews.map(r =>
      `<div style="padding:.4rem 0;border-bottom:1px solid var(--line)">` +
      `<span style="color:var(--warning)">${"★".repeat(r.rating)}${"☆".repeat(5-r.rating)}</span> ` +
      `<span style="font-size:.78rem;color:var(--muted)">${r.reviewer_id||"Аноним"} · ${(r.created_at||"").slice(0,10)}</span>` +
      (r.comment ? `<div style="color:var(--text);margin-top:.2rem">${escapeHtml(r.comment)}</div>` : "") +
      `</div>`
    ).join("");
  }).catch(() => {
    const el = backdrop.querySelector("#supplier-reviews-list");
    if (el) el.innerHTML = '<span style="color:var(--muted)">Не удалось загрузить.</span>';
  });
  backdrop.querySelector("#submit-review-btn")?.addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    const rating = Number(backdrop.querySelector("#review-rating")?.value || 3);
    const comment = backdrop.querySelector("#review-comment")?.value?.trim() || null;
    try {
      btn.disabled = true; btn.textContent = "Отправка...";
      await request(`/suppliers/${btn.dataset.supplierReviewId}/reviews`, {
        method: "POST", body: JSON.stringify({ rating, comment }),
      });
      backdrop.querySelector("#review-comment").value = "";
      showAlert("Отзыв отправлен на модерацию");
    } catch (err) { showAlert(err.message, "error"); }
    finally { btn.disabled = false; btn.textContent = "Отправить"; }
  });
  const previousFocus = document.activeElement;
  const close = () => {
    backdrop.remove();
    document.removeEventListener("keydown", onKeydown);
    if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
  };
  const onKeydown = (event) => {
    if (event.key === "Escape") close();
  };
  document.addEventListener("keydown", onKeydown);
  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) close();
  });
  backdrop.querySelectorAll("[data-supplier-card-close]").forEach((button) => button.addEventListener("click", close));
  backdrop.querySelector("[data-supplier-card-close]")?.focus();
}

function showCatalogEditModal(kind, id) {
  const collections = {
    category: "categories",
    product: "products",
    supplier: "suppliers",
    warehouse: "warehouses",
  };
  const collection = collections[kind];
  const row = state.data[collection]?.find((item) => Number(item.id) === Number(id));
  const config = row ? catalogEditConfig(kind, row) : null;
  if (!config) {
    showAlert("Запись не найдена. Обновите страницу и попробуйте еще раз.", "error");
    return;
  }

  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop";
  backdrop.innerHTML = `
    <section class="confirm-modal edit-modal" role="dialog" aria-modal="true" aria-labelledby="catalog-edit-title">
      <header>
        <h2 id="catalog-edit-title">Исправить ${escapeHtml(catalogKindLabel(kind))}</h2>
      </header>
      <p class="confirm-message">Изменения сохранятся в справочнике и будут видны в новых и старых документах.</p>
      ${form("catalog-edit-form", config.fields, "Сохранить изменения")}
      <footer>
        <button class="secondary" type="button" data-catalog-edit-close>Отмена</button>
      </footer>
    </section>
  `;
  document.body.appendChild(backdrop);
  const previousFocus = document.activeElement;
  const formElement = backdrop.querySelector("#catalog-edit-form");
  const close = () => {
    backdrop.remove();
    document.removeEventListener("keydown", onKeydown);
    if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
  };
  const onKeydown = (event) => {
    if (event.key === "Escape") close();
  };
  document.addEventListener("keydown", onKeydown);
  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) close();
  });
  backdrop.querySelector("[data-catalog-edit-close]").addEventListener("click", close);
  formElement.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (formElement.dataset.pending === "true") return;
    const submitButton = formElement.querySelector('button[type="submit"]');
    try {
      clearFormError(formElement);
      formElement.dataset.pending = "true";
      setPending(submitButton, true, "Сохраняем");
      await mutate(config.endpoint, config.normalize(collect(formElement)), "PATCH");
      showAlert("Справочник обновлен");
      close();
      await loadAll();
    } catch (error) {
      showFormError(formElement, error.message);
      showAlert(error.message, "error");
    } finally {
      delete formElement.dataset.pending;
      setPending(submitButton, false);
    }
  });

  // Certificate file upload zone (products only)
  if (kind === "product" && row) {
    const certField = formElement.querySelector('[name="certificate_ref"]');
    if (certField) {
      const certWrap = certField.parentElement;
      const uploadZone = document.createElement("div");
      const existingCert = row.certificate_ref || "";
      const isFile = existingCert.startsWith("/uploads/");
      uploadZone.innerHTML = `
        <div class="cert-upload-zone" id="cert-upload-zone-${escapeAttr(String(row.id))}">
          <input type="file" id="cert-file-input-${escapeAttr(String(row.id))}" accept=".pdf,.jpg,.jpeg,.png,.webp" />
          <span class="cert-file-label" id="cert-file-label-${escapeAttr(String(row.id))}">
            ${isFile ? '📄 Файл загружен' : 'PDF, JPG или PNG · до 10 МБ'}
          </span>
          <button type="button" class="cert-btn" id="cert-upload-btn-${escapeAttr(String(row.id))}">
            ${isFile ? 'Заменить' : 'Выбрать файл'}
          </button>
        </div>
        ${isFile ? `<div style="margin-top:4px;display:flex;align-items:center;gap:8px"><a href="${escapeAttr(existingCert)}" target="_blank" rel="noopener" class="cert-preview-link">📄 Просмотреть сертификат ↗</a><button type="button" class="cert-remove-btn" id="cert-remove-btn-${escapeAttr(String(row.id))}">✕ Удалить</button></div>` : ''}
      `;
      certWrap.after(uploadZone);

      const fileInput = uploadZone.querySelector(`#cert-file-input-${row.id}`);
      const uploadBtn = uploadZone.querySelector(`#cert-upload-btn-${row.id}`);
      const fileLabel = uploadZone.querySelector(`#cert-file-label-${row.id}`);
      const removeBtn = uploadZone.querySelector(`#cert-remove-btn-${row.id}`);

      if (uploadBtn && fileInput) {
        uploadBtn.addEventListener("click", () => fileInput.click());

        fileInput.addEventListener("change", async () => {
          const file = fileInput.files[0];
          if (!file) return;
          fileLabel.textContent = `⏳ Загружаем: ${file.name}`;
          uploadBtn.disabled = true;
          try {
            const formData = new FormData();
            formData.append("file", file);
            const uploadHeaders = {
              "X-Actor-Id": el("actor-id").value || "manager",
              "X-Actor-Roles": el("actor-role").value || "warehouse_manager",
              "X-Actor-Warehouse-Ids": el("actor-warehouses").value || "",
            };
            const authToken = el("auth-token").value.trim();
            const loginToken = state.auth.loginToken;
            if (state.auth.source === "tetis" && authToken) uploadHeaders.Authorization = `Bearer ${authToken}`;
            else if (state.auth.source === "login" && loginToken) uploadHeaders.Authorization = `Bearer ${loginToken}`;
            const resp = await fetch(`${API}/products/${row.id}/certificate/upload`, {
              method: "POST",
              headers: uploadHeaders,
              body: formData,
            });
            const result = await resp.json();
            if (!resp.ok) throw new Error(result.detail?.message || result.detail || "Ошибка загрузки");
            const newUrl = result.certificate_url;
            certField.value = newUrl;
            fileLabel.textContent = `✅ ${file.name}`;
            uploadBtn.textContent = "Заменить";
            showAlert("Сертификат загружен");
            await loadAll();
          } catch (err) {
            fileLabel.textContent = `❌ Ошибка: ${err.message}`;
            showAlert(`Ошибка загрузки: ${err.message}`, "error");
          } finally {
            uploadBtn.disabled = false;
          }
        });

        // Drag-and-drop
        const zone = uploadZone.querySelector(".cert-upload-zone");
        if (zone) {
          zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("drag-over"); });
          zone.addEventListener("dragleave", () => zone.classList.remove("drag-over"));
          zone.addEventListener("drop", (e) => {
            e.preventDefault();
            zone.classList.remove("drag-over");
            if (e.dataTransfer.files.length) {
              fileInput.files = e.dataTransfer.files;
              fileInput.dispatchEvent(new Event("change"));
            }
          });
        }
      }

      if (removeBtn) {
        removeBtn.addEventListener("click", async () => {
          if (!await confirmAction(`Удалить сертификат товара «${escapeHtml(row.name)}»?`)) return;
          removeBtn.disabled = true;
          try {
            await request(`/products/${row.id}/certificate`, { method: "DELETE" });
            certField.value = "";
            uploadZone.innerHTML = `
              <div class="cert-upload-zone">
                <input type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" />
                <span class="cert-file-label">PDF, JPG или PNG · до 10 МБ</span>
                <button type="button" class="cert-btn" id="cert-upload-btn-after-${escapeAttr(String(row.id))}">Выбрать файл</button>
              </div>
            `;
            showAlert("Сертификат удалён");
            await loadAll();
          } catch (err) {
            showAlert(`Ошибка: ${err.message}`, "error");
            removeBtn.disabled = false;
          }
        });
      }
    }
  }

  // Product photo upload zone
  if (kind === "product" && row) {
    const actionsBlock = formElement.querySelector(".actions");
    if (actionsBlock) {
      const existingImage = row.image_path || "";
      const photoZone = document.createElement("div");
      photoZone.className = "full";
      photoZone.innerHTML = `
        <label>${escapeHtml(t("Фото товара"))}</label>
        <div class="cert-upload-zone" id="photo-upload-zone-${escapeAttr(String(row.id))}">
          <input type="file" id="photo-file-input-${escapeAttr(String(row.id))}" accept=".jpg,.jpeg,.png,.webp" />
          <span class="cert-file-label" id="photo-file-label-${escapeAttr(String(row.id))}">
            ${existingImage ? "🖼 Фото загружено" : "JPG, PNG или WEBP · до 8 МБ"}
          </span>
          <button type="button" class="cert-btn" id="photo-upload-btn-${escapeAttr(String(row.id))}">
            ${existingImage ? "Заменить" : "Выбрать файл"}
          </button>
        </div>
        ${existingImage ? `<div style="margin-top:6px;display:flex;align-items:center;gap:8px">
          <img src="${escapeAttr(existingImage)}" alt="" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid var(--line)" />
          <button type="button" class="cert-remove-btn" id="photo-remove-btn-${escapeAttr(String(row.id))}">✕ Удалить</button>
        </div>` : ""}
      `;
      actionsBlock.before(photoZone);

      const photoInput = photoZone.querySelector(`#photo-file-input-${row.id}`);
      const photoUploadBtn = photoZone.querySelector(`#photo-upload-btn-${row.id}`);
      const photoLabel = photoZone.querySelector(`#photo-file-label-${row.id}`);
      const photoRemoveBtn = photoZone.querySelector(`#photo-remove-btn-${row.id}`);

      if (photoUploadBtn && photoInput) {
        photoUploadBtn.addEventListener("click", () => photoInput.click());
        photoInput.addEventListener("change", async () => {
          const file = photoInput.files[0];
          if (!file) return;
          photoLabel.textContent = `⏳ Загружаем: ${file.name}`;
          photoUploadBtn.disabled = true;
          try {
            const formData = new FormData();
            formData.append("file", file);
            const uploadHeaders = {
              "X-Actor-Id": el("actor-id").value || "manager",
              "X-Actor-Roles": el("actor-role").value || "warehouse_manager",
              "X-Actor-Warehouse-Ids": el("actor-warehouses").value || "",
            };
            const authToken = el("auth-token").value.trim();
            const loginToken = state.auth.loginToken;
            if (state.auth.source === "tetis" && authToken) uploadHeaders.Authorization = `Bearer ${authToken}`;
            else if (state.auth.source === "login" && loginToken) uploadHeaders.Authorization = `Bearer ${loginToken}`;
            const resp = await fetch(`${API}/products/${row.id}/image/upload`, {
              method: "POST",
              headers: uploadHeaders,
              body: formData,
            });
            const result = await resp.json();
            if (!resp.ok) throw new Error(result.detail?.message || result.detail || "Ошибка загрузки");
            photoLabel.textContent = `✅ ${file.name}`;
            photoUploadBtn.textContent = "Заменить";
            showAlert("Фото товара загружено");
            await loadAll();
          } catch (err) {
            photoLabel.textContent = `❌ Ошибка: ${err.message}`;
            showAlert(`Ошибка загрузки: ${err.message}`, "error");
          } finally {
            photoUploadBtn.disabled = false;
          }
        });
      }

      if (photoRemoveBtn) {
        photoRemoveBtn.addEventListener("click", async () => {
          if (!await confirmAction(`Удалить фото товара «${escapeHtml(row.name)}»?`)) return;
          photoRemoveBtn.disabled = true;
          try {
            await request(`/products/${row.id}/image`, { method: "DELETE" });
            showAlert("Фото удалено");
            await loadAll();
          } catch (err) {
            showAlert(`Ошибка: ${err.message}`, "error");
            photoRemoveBtn.disabled = false;
          }
        });
      }
    }
  }

  formElement.querySelector("input, select, textarea")?.focus();
}

async function deleteCatalogEntry(kind, id, button) {
  const collections = {
    category: "categories",
    product: "products",
  };
  const endpoints = {
    category: `/categories/${id}`,
    product: `/products/${id}`,
  };
  const row = state.data[collections[kind]]?.find((item) => Number(item.id) === Number(id));
  if (!row || !endpoints[kind]) {
    showAlert("Запись не найдена. Обновите страницу и попробуйте еще раз.", "error");
    return;
  }
  const label = kind === "category" ? "категорию" : "товар";
  const isDeletion = kind === "product";
  const ok = await confirmAction(
    isDeletion
      ? `Удалить товар «${row.name}» из справочника? Он исчезнет из форм прихода и списания. История партий и документов сохранится.`
      : `Скрыть ${label} «${row.name}»? Новые операции больше не будут предлагать эту запись, но история документов сохранится.`,
    { title: isDeletion ? "Удалить товар" : "Скрыть запись", confirmText: isDeletion ? "Удалить" : "Скрыть", tone: "danger" },
  );
  if (!ok) return;
  try {
    setPending(button, true, "Скрываем");
    await removeResource(endpoints[kind]);
    showAlert("Запись скрыта из справочника");
    await loadAll();
  } catch (error) {
    showAlert(error.message, "error");
  } finally {
    setPending(button, false);
  }
}

function daysUntil(value) {
  if (!value) return null;
  const end = new Date(`${value}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.ceil((end - today) / 86400000);
}

function productFreeQuantity(productId) {
  return state.data.balances.items
    .filter((row) => Number(row.product_id) === Number(productId))
    .reduce((sum, row) => sum + Number(row.free_quantity || 0), 0);
}

function lowStockProducts() {
  return state.data.products.filter((product) => {
    const reorderPoint = Number(product.reorder_point || 0);
    return reorderPoint > 0 && productFreeQuantity(product.id) < reorderPoint;
  });
}

function expiringBalances(days = 30) {
  return state.data.balances.items.filter((row) => {
    const left = daysUntil(row.expires_on);
    return left !== null && left >= 0 && left <= days;
  });
}

function deviceById(deviceId) {
  return state.data.sensorDevices.find((device) => Number(device.id) === Number(deviceId)) || null;
}

function conditionRangeText(min, max, unit) {
  if (min !== null && min !== undefined && max !== null && max !== undefined) return `${min}…${max} ${unit}`;
  if (min !== null && min !== undefined) return `от ${min} ${unit}`;
  if (max !== null && max !== undefined) return `до ${max} ${unit}`;
  return `норма не задана`;
}

function conditionBreachDetails(reading, device = deviceById(reading.device_id)) {
  const details = [];
  if (!device) return details;
  const temperature = Number(reading.temperature_c);
  if (reading.temperature_c !== null && reading.temperature_c !== undefined && !Number.isNaN(temperature)) {
    const min = device.min_temperature_c === null || device.min_temperature_c === undefined ? null : Number(device.min_temperature_c);
    const max = device.max_temperature_c === null || device.max_temperature_c === undefined ? null : Number(device.max_temperature_c);
    const range = conditionRangeText(device.min_temperature_c, device.max_temperature_c, "°C");
    if (min !== null && temperature < min) details.push(`Температура ниже нормы: ${reading.temperature_c} °C, норма ${range}`);
    if (max !== null && temperature > max) details.push(`Температура выше нормы: ${reading.temperature_c} °C, норма ${range}`);
  }
  const humidity = Number(reading.humidity_percent);
  if (reading.humidity_percent !== null && reading.humidity_percent !== undefined && !Number.isNaN(humidity)) {
    const min = device.min_humidity_percent === null || device.min_humidity_percent === undefined ? null : Number(device.min_humidity_percent);
    const max = device.max_humidity_percent === null || device.max_humidity_percent === undefined ? null : Number(device.max_humidity_percent);
    const range = conditionRangeText(device.min_humidity_percent, device.max_humidity_percent, "%");
    if (min !== null && humidity < min) details.push(`Влажность ниже нормы: ${reading.humidity_percent} %, норма ${range}`);
    if (max !== null && humidity > max) details.push(`Влажность выше нормы: ${reading.humidity_percent} %, норма ${range}`);
  }
  return details;
}

function latestConditionWarnings() {
  const latestByDevice = new Map();
  [...(state.data.sensorReadings.items || [])]
    .sort((a, b) => new Date(b.recorded_at || 0) - new Date(a.recorded_at || 0) || Number(b.id || 0) - Number(a.id || 0))
    .forEach((reading) => {
      if (!latestByDevice.has(reading.device_id)) latestByDevice.set(reading.device_id, reading);
    });
  return [...latestByDevice.values()].filter((reading) => reading.status === "warning");
}

function conditionActionText(reading) {
  const details = conditionBreachDetails(reading);
  const temperatureProblem = details.some((item) => item.includes("Температура"));
  if (temperatureProblem) return "Проверьте дверь, питание холодильника и перенесите чувствительные партии при необходимости.";
  return "Проверьте вентиляцию, упаковку и состояние помещения.";
}

function actionQueue() {
  return [
    ...latestConditionWarnings()
      .slice(0, 3)
      .map((reading) => ({
        severity: "bad",
        title: `Проверьте склад: ${reading.device_name || `датчик #${reading.device_id}`}`,
        meta: `${conditionBreachDetails(reading).join(" · ") || "Показание вне нормы"} · ${rawNameById("warehouses", reading.warehouse_id)}`,
        view: "conditions",
      })),
    ...state.data.warehouses
      .filter((warehouse) => warehouse.inventory_lock)
      .map((warehouse) => ({
        severity: "bad",
        title: `Склад заблокирован: ${warehouse.name}`,
        meta: "Движения остановлены до завершения инвентаризации",
        view: "inventory",
      })),
    ...state.data.documents
      .filter((document) => document.status === "draft")
      .map((document) => ({
        severity: "warn",
        title: `Черновик документа #${document.id}`,
        meta: `${humanDocumentType(document.document_type)} · ${rawNameById("warehouses", document.warehouse_id)} · строк: ${document.lines?.length || 0}`,
        view: "documents",
      })),
    ...lowStockProducts().map((product) => ({
      severity: "warn",
      title: `Ниже точки заказа: ${product.name}`,
      meta: `Свободно ${productFreeQuantity(product.id).toFixed(3)} · точка ${product.reorder_point}`,
      view: "purchase-requests",
    })),
    ...state.data.purchaseRequests
      .filter((request) => ["draft", "requested", "open"].includes(String(request.status || "open")))
      .map((request) => ({
        severity: "warn",
        title: `Заявка на закупку #${request.id}`,
        meta: `${rawNameById("products", request.product_id)} · нужно ${request.quantity || "—"}`,
        view: "purchase-requests",
      })),
    ...state.data.batches
      .filter((batch) => ["quarantine", "blocked"].includes(batch.status))
      .map((batch) => ({
        severity: batch.status === "blocked" ? "bad" : "warn",
        title: `${batch.status === "blocked" ? "Заблокирована" : "Карантин"} партия #${batch.id}`,
        meta: `${rawNameById("products", batch.product_id)} · серия ${batch.lot}`,
        view: "operations",
      })),
    ...expiringBalances(30).map((balance) => ({
      severity: "warn",
      title: `Срок годности до ${balance.expires_on}`,
      meta: `${rawNameById("products", balance.product_id)} · партия #${balance.batch_id} · ${rawNameById("warehouses", balance.warehouse_id)}`,
      view: "receipts",
    })),
  ].slice(0, 12);
}

function collect(formElement) {
  const data = new FormData(formElement);
  const result = {};
  for (const [key, value] of data.entries()) {
    if (value === "") continue;
    if (key.endsWith("_id") || ["batch_id", "product_id", "supplier_id", "warehouse_id", "source_warehouse_id", "target_warehouse_id"].includes(key)) {
      result[key] = Number(value);
    } else if (["quantity", "target_quantity", "conversion_factor", "loss_quantity", "unit_price", "target_unit_price", "reorder_point", "safety_stock", "actual_quantity", "temperature_c", "humidity_percent", "min_temperature_c", "max_temperature_c", "min_humidity_percent", "max_humidity_percent"].includes(key)) {
      result[key] = String(value);
    } else if (key === "quarantine" || key === "is_controlled") {
      result[key] = value === "true";
    } else {
      result[key] = value;
    }
  }
  return result;
}

function newReceiptDocumentLine() {
  return { product_id: "", quantity: "", unit_price: "0", lot: "", serial_number: "", expires_on: "" };
}

function newWriteoffDocumentLine() {
  return { batch_id: "", quantity: "", reason: "Списание по документу", patient_id: "", doctor_id: "", medical_record_no: "", second_approver_id: "", second_approval_note: "" };
}

function compactLine(line) {
  return Object.fromEntries(Object.entries(line).filter(([, value]) => value !== "" && value !== null && value !== undefined));
}

function receiptDocumentLinesPayload() {
  return state.documentForms.receipt.lines.map((line) => ({
    ...compactLine(line),
    product_id: Number(line.product_id),
    quantity: String(line.quantity),
    unit_price: String(line.unit_price || "0"),
    expires_on: line.expires_on || null,
    quarantine: true,
  }));
}

function writeoffDocumentLinesPayload() {
  return state.documentForms.writeoff.lines.map((line) => ({
    ...compactLine(line),
    batch_id: Number(line.batch_id),
    quantity: String(line.quantity),
    reason: line.reason,
    patient_id: line.patient_id || null,
    doctor_id: line.doctor_id || null,
    medical_record_no: line.medical_record_no || null,
    second_approver_id: line.second_approver_id || null,
    second_approval_note: line.second_approval_note || null,
  }));
}

function controlledWriteoffDocumentIssues(document) {
  if (!document || document.document_type !== "write_off") return [];
  return (document.lines || []).filter((line) => {
    if (!Object.prototype.hasOwnProperty.call(line, "patient_id")) return false;
    const missing = controlledWriteoffMetadataMissing({
      batch_id: line.batch_id,
      patient_id: line.patient_id,
      doctor_id: line.doctor_id,
      medical_record_no: line.medical_record_no,
      second_approver_id: line.second_approver_id,
    });
    return missing.length > 0;
  });
}

function resetDocumentLines(kind) {
  if (kind === "receipt") {
    state.documentForms.receipt.lines = [newReceiptDocumentLine()];
  }
  if (kind === "writeoff") {
    state.documentForms.writeoff.lines = [newWriteoffDocumentLine()];
  }
}

function renderNav() {
  ensureAccessibleView();
  const unreadCount = (state.data.notifications?.items || []).filter((n) => !n.is_read).length;
  const respondedInquiries = (state.data.myInquiries?.items || []).filter((i) => i.status === "responded").length;
  const pendingApplications = (state.data.supplierApplications?.items || []).filter((a) => a.status === "pending").length;
  const allowedIds = new Set(visibleViews().map(([id]) => id));
  const viewById = new Map(views.map((view) => [view[0], view]));
  el("nav").innerHTML = navGroups.map((group) => {
    const ids = group.ids.filter((id) => allowedIds.has(id));
    if (!ids.length) return "";
    const buttons = ids.map((id) => {
      const [, icon, label] = viewById.get(id);
      let badge = "";
      if (id === "notifications" && unreadCount > 0) {
        badge = `<span style="position:absolute;top:4px;right:4px;background:#dc2626;color:#fff;border-radius:9999px;font-size:.6rem;font-weight:700;min-width:1.1rem;height:1.1rem;display:inline-flex;align-items:center;justify-content:center;padding:0 .2rem">${unreadCount > 99 ? "99+" : unreadCount}</span>`;
      } else if (id === "marketplace" && respondedInquiries > 0) {
        badge = `<span style="position:absolute;top:4px;right:4px;background:#16a34a;color:#fff;border-radius:9999px;font-size:.6rem;font-weight:700;min-width:1.1rem;height:1.1rem;display:inline-flex;align-items:center;justify-content:center;padding:0 .2rem">${respondedInquiries}</span>`;
      } else if (id === "users" && pendingApplications > 0) {
        badge = `<span style="position:absolute;top:4px;right:4px;background:#d97706;color:#fff;border-radius:9999px;font-size:.6rem;font-weight:700;min-width:1.1rem;height:1.1rem;display:inline-flex;align-items:center;justify-content:center;padding:0 .2rem">${pendingApplications}</span>`;
      }
      return `
      <button class="${state.view === id ? "active" : ""}" data-view="${id}" style="position:relative">
        <span>${icon}</span><span>${t(label)}</span>${badge}
      </button>`;
    }).join("");
    return `<div class="nav-group"><div class="nav-group-label">${t(group.label)}</div>${buttons}</div>`;
  }).join("");
  el("nav").querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.view;
      document.querySelector(".sidebar")?.classList.remove("nav-open");
      el("nav-toggle")?.setAttribute("aria-expanded", "false");
      render();
    });
  });
}

function updateWarehouseSelector() {
  const node = el("warehouse-filter");
  if (!node) return;
  const selected = node.value;
  const scoped = new Set((state.auth.actor?.warehouse_ids || []).map(String));
  const warehouses = scoped.size
    ? state.data.warehouses.filter((warehouse) => scoped.has(String(warehouse.id)))
    : state.data.warehouses;
  node.innerHTML = [
    `<option value="">Все доступные склады</option>`,
    ...warehouses.map((warehouse) => (
      `<option value="${escapeAttr(warehouse.id)}">${escapeHtml(warehouse.name)} (#${escapeHtml(warehouse.id)})</option>`
    )),
  ].join("");
  if ([...node.options].some((option) => option.value === selected)) {
    node.value = selected;
  } else if (warehouses.length === 1) {
    node.value = String(warehouses[0].id);
  }
}

function setupSteps() {
  return [
    {
      key: "categories",
      title: "Добавьте категорию",
      meta: "Например: медикаменты, расходники, оборудование.",
      done: state.data.categories.length > 0,
      view: "catalog",
    },
    {
      key: "products",
      title: "Создайте товар",
      meta: "Укажите название, код, единицу измерения и категорию.",
      done: state.data.products.length > 0,
      view: "catalog",
    },
    {
      key: "suppliers",
      title: "Добавьте поставщика",
      meta: "Поставщик нужен для прихода партии на склад.",
      done: state.data.suppliers.length > 0,
      view: "catalog",
    },
    {
      key: "warehouses",
      title: "Добавьте склад",
      meta: "Это может быть основной склад, отделение или кабинет.",
      done: state.data.warehouses.length > 0,
      view: "catalog",
    },
    {
      key: "receipts",
      title: "Примите первую партию",
      meta: "После прихода товар появится в остатках и станет доступен для операций.",
      done: state.data.balances.items.length > 0,
      view: "receipts",
    },
  ];
}

function renderSetupGuide() {
  const steps = setupSteps();
  if (steps.every((step) => step.done)) return "";
  const nextStep = steps.find((step) => !step.done);
  return `
    <div class="panel span-12 setup-guide">
      <div class="setup-head">
        <div>
          <span class="eyebrow">${t("Первый запуск")}</span>
          <h2>${t("Что сделать, чтобы склад начал работать")}</h2>
        </div>
        ${nextStep ? `<button class="primary" type="button" data-go-view="${escapeAttr(nextStep.view)}">${escapeHtml(nextStep.title)}</button>` : ""}
      </div>
      <div class="setup-steps">
        ${steps.map((step, index) => `
          <button class="setup-step ${step.done ? "done" : ""}" type="button" data-go-view="${escapeAttr(step.view)}">
            <span>${step.done ? "✓" : index + 1}</span>
            <strong>${escapeHtml(step.title)}</strong>
            <small>${escapeHtml(step.meta)}</small>
          </button>
        `).join("")}
      </div>
    </div>
  `;
}

function receiptPrerequisites() {
  const missing = [];
  if (!state.data.categories.length) missing.push("категорию");
  if (!state.data.products.length) missing.push("товар");
  if (!state.data.suppliers.length) missing.push("поставщика");
  if (!state.data.warehouses.length) missing.push("склад");
  if (!missing.length) return "";
  return `
    <div class="panel span-12 warning-panel receipt-prerequisites">
      <strong>Приход пока нельзя оформить</strong>
      <span>Сначала добавьте: ${escapeHtml(missing.join(", "))}.</span>
      <button class="secondary" type="button" data-go-view="catalog">Перейти в товары и склады</button>
    </div>
  `;
}

function workflowNotice(title, text, view, buttonText) {
  return `
    <div class="panel span-12 warning-panel workflow-notice">
      <div>
        <strong>${escapeHtml(title)}</strong>
        <span>${escapeHtml(text)}</span>
      </div>
      <button class="secondary" type="button" data-go-view="${escapeAttr(view)}">${escapeHtml(buttonText)}</button>
    </div>
  `;
}

function needsStockNotice(actionText = "Продолжить") {
  if (state.data.balances.items.length > 0) return "";
  return workflowNotice(
    "Нет доступных остатков",
    "Сначала примите товар на склад. После этого здесь появятся партии для выбора.",
    "receipts",
    actionText,
  );
}

function needsWarehouseNotice(actionText = "Добавить склад") {
  if (state.data.warehouses.length > 0) return "";
  return workflowNotice(
    "Склад еще не создан",
    "Для этой операции нужен хотя бы один склад или кабинет.",
    "catalog",
    actionText,
  );
}

function needsProductNotice(actionText = "Создать товар") {
  if (state.data.products.length > 0) return "";
  return workflowNotice(
    "Товары еще не созданы",
    "Сначала добавьте категорию и товар, чтобы можно было оформить заявку или приход.",
    "catalog",
    actionText,
  );
}

function renderDashboard() {
  if (isLimitedRole()) return renderLimitedDashboard();
  const balances = state.data.balances.items;
  const free = balances.reduce((sum, item) => sum + Number(item.free_quantity || 0), 0);
  const reserved = balances.reduce((sum, item) => sum + Number(item.reserved_quantity || 0), 0);
  const quarantine = state.data.batches.filter((batch) => batch.status === "quarantine").length;
  const activeInventory = state.data.inventorySessions.filter((session) => session.status === "in_progress").length;
  const purchaseAttention = state.data.purchaseRequests.length
    + state.data.analytics.items.filter((row) => Number(row.recommended_order_quantity || 0) > 0).length;
  const conditionWarnings = state.data.sensorReadings.items.filter((row) => row.status === "warning").length;
  const now = new Date();
  const in30days = new Date(now.getTime() + 30 * 86400000).toISOString().slice(0, 10);
  const contractsExpiring = (state.data.suppliers || []).filter(s =>
    s.contract_expires_on && s.contract_expires_on <= in30days && s.contract_expires_on >= now.toISOString().slice(0, 10)
  ).length;
  const queue = actionQueue();
  return `
    <div class="grid">
      ${state.loadWarnings.length ? `<div class="panel span-12 warning-panel">${state.loadWarnings.map((warning) => `<div>${escapeHtml(warning)}</div>`).join("")}</div>` : ""}
      ${renderSetupGuide()}
      <div class="panel span-3 metric"><span>Свободный остаток</span><strong>${free.toFixed(3)}</strong><span style="font-size:.75rem;color:#6b7280;margin-top:.15rem;display:block">${(() => { const v = balances.reduce((s,b) => { const bt = state.data.batches.find(bt=>Number(bt.id)===Number(b.batch_id)); return s + Number(b.free_quantity||0)*Number(bt?.unit_price||0); }, 0); return v > 0 ? "≈ " + v.toFixed(2) + " ₸" : ""; })()}</span></div>
      <div class="panel span-3 metric"><span>В резерве</span><strong>${reserved.toFixed(3)}</strong></div>
      <div class="panel span-3 metric"><span>Партии в карантине</span><strong>${quarantine}</strong></div>
      <div class="panel span-3 metric"><span>Уведомления</span><strong>${state.data.notifications.total || 0}</strong></div>
      <div class="panel span-12 control-strip">
        ${controlItem("Мало на складе", lowStockProducts().length, "catalog")}
        ${controlItem("Срок до 30 дней", expiringBalances(30).length, "receipts")}
        ${controlItem("Документы ждут", state.data.documents.filter((row) => row.status === "draft").length, "documents")}
        ${controlItem("Заказать", purchaseAttention, "purchase-requests")}
        ${controlItem("Идет проверка", activeInventory, "inventory")}
        ${controlItem("Температура/влажность", conditionWarnings, "conditions")}
        ${(state.data.auctions?.items || []).filter(a=>a.status==="active").length ? controlItem("Активные аукционы", (state.data.auctions?.items || []).filter(a=>a.status==="active").length, "auctions") : ""}
        ${(state.data.products||[]).filter(p=>p.label_needs_reprint).length ? controlItem("Нужна перепечатка", (state.data.products||[]).filter(p=>p.label_needs_reprint).length, "catalog") : ""}
        ${(state.data.pendingReviews||[]).length ? controlItem("Отзывы на проверке", (state.data.pendingReviews||[]).length, "users") : ""}
        ${contractsExpiring ? controlItem("Договоры истекают", contractsExpiring, "catalog") : ""}
        ${(state.data.controlledViolations||[]).length ? controlItem("Нарушения ПКУ", (state.data.controlledViolations||[]).length, "movements") : ""}
        ${(state.data.pendingControlledWriteoffs||[]).filter(r=>r.status==="pending").length ? controlItem("Ожидают подписи ПКУ", (state.data.pendingControlledWriteoffs||[]).filter(r=>r.status==="pending").length, "movements") : ""}
      </div>
      <div class="table-panel span-8">
        <div class="toolbar"><h2>${t("Остатки по партиям")}</h2><span class="status-dot ${state.realtime === "online" ? "ok" : ""}">${t(state.realtime === "online" ? "Автообновление: включено" : "Автообновление: нет связи")}</span><div class="row-actions"><button class="secondary" data-export-report="balances">Выгрузить CSV</button><button class="secondary" data-action="reload">Обновить</button></div></div>
        ${balancesTable(filteredBalances(balances), "Остатков пока нет. Добавьте приход товара или выберите другой склад.")}
        ${state.data.balances.total > state.data.balances.items.length ?
          `<div style="text-align:center;margin:.75rem 0">
            <button class="secondary" data-action="load-more-balances">
              Загрузить ещё (показано ${state.data.balances.items.length} из ${state.data.balances.total})
            </button>
          </div>` : ''}
      </div>
      <div class="table-panel span-4">
        <h2>${t("Очередь действий")}</h2>
        ${renderActionQueue(queue)}
      </div>
      ${(() => {
        const expiring = expiringBalances(30).slice().sort((a, b) => (daysUntil(a.expires_on) ?? 999) - (daysUntil(b.expires_on) ?? 999)).slice(0, 15);
        if (!expiring.length) return "";
        const urgencyColor = (days) => days <= 7 ? "#dc2626" : days <= 14 ? "#d97706" : "#92400e";
        return `
        <div class="table-panel span-12">
          <div class="toolbar"><h2>${t("Истекает срок годности (30 дней)")}</h2><button class="secondary" data-go-view="receipts">${t("Все остатки")}</button></div>
          <div class="table-wrap"><table>
            <thead><tr><th>Товар</th><th>Партия</th><th>Склад</th><th>Количество</th><th>Истекает</th><th>Осталось дней</th></tr></thead>
            <tbody>
              ${expiring.map((row) => {
                const days = daysUntil(row.expires_on) ?? 999;
                const color = urgencyColor(days);
                return `<tr style="background:${color}15">
                  <td>${escapeHtml(rawNameById("products", row.product_id))}</td>
                  <td>${batchDetailLabel(row.batch_id)}</td>
                  <td>${nameById("warehouses", row.warehouse_id)}</td>
                  <td>${qty(row.free_quantity)}</td>
                  <td style="color:${color};font-weight:600">${escapeHtml(row.expires_on || "—")}</td>
                  <td style="color:${color};font-weight:700">${days <= 0 ? "Просрочено" : days + " дн."}</td>
                </tr>`;
              }).join("")}
            </tbody>
          </table></div>
        </div>`;
      })()}
      <div class="table-panel span-12">
        <h2>${t("Последние уведомления")}</h2>
        ${table([
          { label: "Событие", render: (row) => humanNotificationType(row.notification_type) },
          { label: "Сообщение", render: (row) => `${escapeHtml(row.title)}<br><span class="badge ${row.is_read ? "" : "warn"}">${t(row.is_read ? "прочитано" : "новое")}</span>` },
          { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "—" },
          { label: "Создано", render: (row) => dateText(row.created_at) },
        ], state.data.notifications.items.slice(0, 8))}
      </div>
    </div>
  `;
}

function controlItem(label, value, view) {
  const tone = Number(value) > 0 ? "warn" : "ok";
  return `<button class="control-item ${tone}" data-go-view="${escapeAttr(safeViewTarget(view))}"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></button>`;
}

function renderActionQueue(items) {
  if (!items.length) return `<div class="empty-state"><strong>Критичных действий нет</strong><span>Складские риски появятся здесь автоматически</span></div>`;
  return `<div class="action-list">${items.map((item) => `
    <button class="action-item ${escapeAttr(item.severity)}" data-go-view="${escapeAttr(safeViewTarget(item.view))}">
      <strong>${escapeHtml(item.title)}</strong>
      <span>${escapeHtml(item.meta)}</span>
    </button>
  `).join("")}</div>`;
}

function renderLimitedDashboard() {
  const balances = state.data.balances.items;
  const free = balances.reduce((sum, item) => sum + Number(item.free_quantity || 0), 0);
  const expiring = expiringBalances(30).length;
  return `
    <div class="grid">
      ${roleAccessNotice()}
      ${state.loadWarnings.length ? `<div class="panel span-12 warning-panel">${state.loadWarnings.map((warning) => `<div>${escapeHtml(warning)}</div>`).join("")}</div>` : ""}
      <div class="panel span-4 metric"><span>Свободный остаток</span><strong>${free.toFixed(3)}</strong></div>
      <div class="panel span-4 metric"><span>Срок до 30 дней</span><strong>${expiring}</strong></div>
      <div class="panel span-4 metric"><span>Уведомления</span><strong>${state.data.notifications.total || 0}</strong></div>
      <div class="tablet-writeoff-panel span-12">
        <div class="tablet-copy">
          <span class="eyebrow">Планшетный режим</span>
          <h2>${t("Списать партию")}</h2>
        </div>
        ${tabletWriteoffForm()}
      </div>
      <div class="table-panel span-12">
        <div class="toolbar"><h2>${t("Доступные остатки")}</h2><button class="secondary" data-action="reload">${t("Обновить")}</button></div>
        ${balancesTable(filteredBalances(balances), "Остатков пока нет. Проверьте выбранный склад или обратитесь к заведующему складом.")}
      </div>
    </div>
  `;
}

function balanceSummary(rows) {
  if (!rows.length) return "";
  const productCount = new Set(rows.map((row) => row.product_id)).size;
  const warehouseCount = new Set(rows.map((row) => row.warehouse_id)).size;
  const availableBatchCount = new Set(rows
    .filter((row) => Number(row.free_quantity || 0) > 0)
    .map((row) => row.batch_id)).size;
  const free = rows.reduce((sum, row) => sum + Number(row.free_quantity || 0), 0);
  const expiring = rows.filter((row) => {
    const left = daysUntil(row.expires_on);
    return left !== null && left >= 0 && left <= 30;
  }).length;
  return `
    <div class="balance-summary" aria-label="Краткая сводка остатков">
      <div><span>Позиции</span><strong>${escapeHtml(rows.length)}</strong></div>
      <div><span>Товары</span><strong>${escapeHtml(productCount)}</strong></div>
      <div><span>Склады</span><strong>${escapeHtml(warehouseCount)}</strong></div>
      <div><span>Партии с остатком</span><strong>${escapeHtml(availableBatchCount)}</strong></div>
      <div><span>Свободно к использованию</span><strong>${escapeHtml(free.toFixed(3))}</strong></div>
      <div><span>Срок до 30 дней</span><strong>${escapeHtml(expiring)}</strong></div>
    </div>
  `;
}

function balancesTable(rows, empty = "Данных пока нет") {
  return `${balanceSummary(rows)}${table([
    { label: "Товар", render: (row) => nameById("products", row.product_id) },
    { label: "Партия", render: (row) => batchButton(row.batch_id) },
    { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
    { label: "Всего", key: "total_quantity" },
    { label: "Резерв", key: "reserved_quantity" },
    { label: "Свободно", key: "free_quantity" },
    { label: "Статус", render: (row) => badge(row.batch_status) },
    { label: "Годен до", render: (row) => row.expires_on || "—" },
    { label: "", render: (row) => {
      const offers = findMarketplaceOffersForProduct(row.product_id);
      if (!offers.length) return "";
      const best = offers.reduce((a, b) => a.unit_price <= b.unit_price ? a : b);
      return `<button class="secondary compact-action" style="white-space:nowrap" data-show-pr-offers="${row.product_id}" title="${offers.length} предложений от ${fmtMoneyKzt(best.unit_price)} тг">📦 ${offers.length}</button>`;
    }},
  ], rows, searchEmptyText(empty))}
  <div id="pr-offers-panel-balances" style="display:none;margin-top:12px"></div>`;
}

function nameById(collection, id) {
  return escapeHtml(rawNameById(collection, id));
}

function rawNameById(collection, id) {
  const item = state.data[collection].find((entry) => Number(entry.id) === Number(id));
  return item ? `${item.name} (#${id})` : `#${id}`;
}

function rawBatchLabel(batchId) {
  if (!batchId) return "—";
  const batch = state.data.batches.find((entry) => Number(entry.id) === Number(batchId));
  if (!batch) return `#${batchId}`;
  return `${rawNameById("products", batch.product_id)} · серия ${batch.lot} (#${batch.id})`;
}

function batchLabel(batchId) {
  if (!batchId) return "—";
  const batch = state.data.batches.find((entry) => Number(entry.id) === Number(batchId));
  if (!batch) return `#${batchId}`;
  return `${nameById("products", batch.product_id)} · серия ${escapeHtml(batch.lot)} (#${escapeHtml(batch.id)})`;
}

function batchDetailLabel(batchId) {
  return batchButton(batchId, batchLabel(batchId));
}

function documentTitle(document) {
  return `${humanDocumentType(document.document_type)} #${document.id} · ${humanStatus(document.status)}`;
}

function compactTraceTable(columns, rows, empty) {
  return table(columns, rows, empty).replaceAll("table-wrap", "table-wrap compact-trace-table");
}

function traceabilitySummary(detail) {
  const free = (detail.balances || []).reduce((sum, row) => sum + Number(row.free_quantity || 0), 0);
  const reserved = (detail.balances || []).reduce((sum, row) => sum + Number(row.reserved_quantity || 0), 0);
  const movements = detail.movements || [];
  return {
    free,
    reserved,
    movements: movements.length,
    documents: (detail.documents || []).length,
    transformations: (detail.transformations || []).length,
    recalls: (detail.recalls || []).length,
  };
}

function renderBatchTraceability(detail) {
  const batch = detail.batch;
  const summary = traceabilitySummary(detail);
  return `
    <section class="confirm-modal trace-modal" role="dialog" aria-modal="true" aria-labelledby="batch-trace-title">
      <header>
        <div>
          <h2 id="batch-trace-title">${escapeHtml(rawNameById("products", batch.product_id))}</h2>
          <span class="helper-text">Партия #${escapeHtml(batch.id)} · серия ${escapeHtml(batch.lot)}${batch.serial_number ? ` · серийный ${escapeHtml(batch.serial_number)}` : ""}</span>
        </div>
        <button class="icon-button" type="button" data-trace-close title="Закрыть">×</button>
      </header>
      <div class="trace-body">
        <div class="trace-summary">
          <div><span>Поставщик</span><strong>${nameById("suppliers", batch.supplier_id)}</strong></div>
          <div><span>Статус</span>${badge(batch.status)}</div>
          <div><span>Серийный номер</span><strong>${escapeHtml(batch.serial_number || "не указан")}</strong></div>
          <div><span>Годен до</span><strong>${escapeHtml(batch.expires_on || "не указан")}</strong></div>
          <div><span>Свободно</span><strong>${summary.free.toFixed(3)}</strong></div>
          <div><span>В резерве</span><strong>${summary.reserved.toFixed(3)}</strong></div>
          <div><span>Движений</span><strong>${summary.movements}</strong></div>
          <div><span>Фасовок</span><strong>${summary.transformations}</strong></div>
          <div><span>Отзывов</span><strong>${summary.recalls}</strong></div>
        </div>
        <div class="trace-section">
          <h3>${t("Где лежит партия")}</h3>
          ${compactTraceTable([
            { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
            { label: "Всего", key: "total_quantity" },
            { label: "Резерв", key: "reserved_quantity" },
            { label: "Свободно", key: "free_quantity" },
            { label: "Статус", render: (row) => badge(row.batch_status) },
          ], detail.balances || [], "По партии нет остатков на складах.")}
        </div>
        <div class="trace-section">
          <h3>${t("Последние движения")}</h3>
          ${compactTraceTable([
            { label: "Время", render: (row) => dateText(row.created_at) },
            { label: "Действие", render: (row) => badge(row.movement_type) },
            { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
            { label: "Количество", key: "quantity" },
            { label: "Причина", key: "reason" },
          ], detail.movements || [], "Движений по партии пока нет.")}
        </div>
        <div class="trace-section">
          <h3>${t("Цепочка фасовки")}</h3>
          ${compactTraceTable([
            { label: "Время", render: (row) => dateText(row.created_at) },
            { label: "Исходная партия", render: (row) => batchDetailLabel(row.source_batch_id) },
            { label: "Полученная партия", render: (row) => batchDetailLabel(row.target_batch_id) },
            { label: "Взяли", key: "source_quantity" },
            { label: "Получили", key: "target_quantity" },
            { label: "Потери", key: "loss_quantity" },
            { label: "Причина", key: "reason" },
          ], detail.transformations || [], "Эта партия пока не участвовала в фасовке.")}
        </div>
        <div class="trace-section">
          <h3>${t("Отзывы партии")}</h3>
          ${compactTraceTable([
            { label: "Время", render: (row) => dateText(row.created_at) },
            { label: "Причина", key: "reason" },
            { label: "Источник", key: "source" },
            { label: "Основание", render: (row) => escapeHtml(row.reference || "—") },
            { label: "Создал", key: "created_by" },
          ], detail.recalls || [], "Отзывов по партии нет.")}
        </div>
        <div class="trace-section">
          <h3>${t("Документы")}</h3>
          ${compactTraceTable([
            { label: "Документ", render: (row) => escapeHtml(documentTitle(row)) },
            { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
            { label: "Создал", key: "created_by" },
            { label: "Утвердил", render: (row) => escapeHtml(row.approved_by || "—") },
            { label: "Создан", render: (row) => dateText(row.created_at) },
        { label: "№ ЭСФ / накладной", render: (row) => escapeHtml(row.external_ref || "—") },
            { label: "Утвержден", render: (row) => dateText(row.approved_at) },
            { label: "Проведен", render: (row) => dateText(row.posted_at) },
          ], detail.documents || [], "Документов по партии пока нет.")}
        </div>
      </div>
      <footer>
        <button class="secondary" type="button" data-trace-close>Закрыть</button>
      </footer>
    </section>
  `;
}

async function showBatchTraceability(batchId) {
  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop";
  backdrop.innerHTML = `
    <section class="confirm-modal trace-modal" role="dialog" aria-modal="true" aria-labelledby="batch-trace-title">
      <header>
        <h2 id="batch-trace-title">Загружаем партию #${escapeHtml(batchId)}</h2>
      </header>
      <p class="confirm-message">Собираем остатки, движения и документы партии.</p>
    </section>
  `;
  document.body.appendChild(backdrop);
  const previousFocus = document.activeElement;
  const close = () => {
    backdrop.remove();
    document.removeEventListener("keydown", onKeydown);
    if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
  };
  const onKeydown = (event) => {
    if (event.key === "Escape") close();
  };
  document.addEventListener("keydown", onKeydown);
  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) close();
  });
  try {
    const detail = await request(`/batches/${batchId}/traceability?limit=50`);
    backdrop.innerHTML = renderBatchTraceability(detail);
    backdrop.querySelectorAll("[data-trace-close]").forEach((button) => {
      button.addEventListener("click", close);
    });
    backdrop.querySelector("[data-trace-close]")?.focus();
  } catch (error) {
    backdrop.innerHTML = `
      <section class="confirm-modal danger" role="dialog" aria-modal="true" aria-labelledby="batch-trace-title">
        <header><h2 id="batch-trace-title">Не удалось открыть партию</h2></header>
        <p class="confirm-message">${escapeHtml(error.message)}</p>
        <footer><button class="secondary" type="button" data-trace-close>Закрыть</button></footer>
      </section>
    `;
    backdrop.querySelector("[data-trace-close]").addEventListener("click", close);
  }
}

// ── Stock view with barcode scanner ──────────────────────────────────────
function renderStock() {
  const bp = state.ui.barcodeProduct || null;
  const filtered = bp
    ? filteredBalances(state.data.balances.items.filter((row) => row.product_id === bp.id))
    : filteredBalances(state.data.balances.items);
  const cameraAvailable = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
  return `
    <div class="grid">
      ${needsStockNotice("Перейти к приходу")}
      <div class="panel span-4 barcode-scanner-panel">
        <h2 style="margin:0 0 .75rem">${t("Сканер штрихкода")}</h2>
        ${cameraAvailable ? `
          <button class="primary" data-action="toggle-scanner" type="button" style="width:100%;margin-bottom:.75rem">
            📷 ${t("Запустить камеру")}
          </button>
        ` : `<p style="color:#dc2626;font-size:.85rem;margin-bottom:.75rem">${t("Камера недоступна в этом браузере")}</p>`}
        <div style="border-top:1px solid #e5e7eb;padding-top:.75rem">
          <label style="font-size:.82rem;font-weight:600;display:block;margin-bottom:.4rem">${t("Или введите штрихкод вручную")}</label>
          <div style="display:flex;gap:.5rem">
            <input id="barcode-manual" type="text" inputmode="numeric" placeholder="4600000000000"
              style="flex:1;padding:.4rem;border:1px solid #ccc;border-radius:4px;font-size:.95rem">
            <button class="secondary" data-action="barcode-manual-search" type="button">${t("Найти")}</button>
          </div>
          <p style="font-size:.76rem;color:#94a3b8;margin:.4rem 0 0">
            ${t("Поддерживаются USB и Bluetooth сканеры: нажмите в поле, затем пронесите сканером")}
          </p>
        </div>
        ${bp ? `
          <div style="margin-top:.75rem;background:#f0fdf4;border:1px solid #86efac;padding:.75rem;border-radius:6px">
            <strong style="display:block;margin-bottom:.25rem">${escapeHtml(bp.name)}</strong>
            <span style="font-size:.82rem;color:#555">${t("Код")}: ${escapeHtml(bp.sku || "—")} · ${t("Ед.")}: ${escapeHtml(bp.unit || "—")}</span>
            ${bp.barcode ? `<br><span style="font-size:.82rem;color:#555">${t("Штрихкод")}: ${escapeHtml(bp.barcode)}</span>` : ""}
            <button class="secondary" data-action="barcode-clear" type="button" style="margin-top:.5rem;width:100%">${t("Сбросить фильтр")}</button>
          </div>
        ` : `<p style="font-size:.82rem;color:#888;margin-top:.75rem">${t("Отсканируйте штрихкод товара для фильтрации остатков")}</p>`}
      </div>
      <div class="table-panel span-8">
        <div class="toolbar">
          <h2>${t("Текущие остатки")}${bp ? ` — ${escapeHtml(bp.name)}` : ""}</h2>
          <div class="row-actions">
            <button class="secondary" data-export-report="balances">${t("Выгрузить CSV")}</button>
            <a href="${`${API}/balances/pdf${warehouseFilterParam() ? '?' + warehouseFilterParam() : ''}`}" target="_blank" class="secondary" style="display:inline-block;padding:.35rem .7rem;border:1px solid #d1d5db;border-radius:6px;font-size:.82rem;text-decoration:none;color:#374151">📄 PDF</a>
            <button class="secondary" data-action="reload">${t("Обновить")}</button>
          </div>
        </div>
        ${balancesTable(filtered, "Остатков пока нет. Примите товар на склад или выберите другой склад в верхней панели.")}
        ${state.data.balances.total > state.data.balances.items.length ?
          `<div style="text-align:center;margin:.75rem 0">
            <button class="secondary" data-action="load-more-balances">
              Загрузить ещё (показано ${state.data.balances.items.length} из ${state.data.balances.total})
            </button>
          </div>` : ''}
      </div>
    </div>
  `;
}

function renderCatalog() {
  const directoryRows = [
    ...state.data.warehouses.map((row) => ({ ...row, kind: "Склад", catalogKind: "warehouse" })),
    ...state.data.suppliers.map((row) => ({ ...row, kind: "Поставщик", catalogKind: "supplier" })),
    ...state.data.categories.map((row) => ({ ...row, kind: "Категория", catalogKind: "category" })),
  ];
  const catalogStats = [
    ["Категории", state.data.categories.length],
    ["Товары", state.data.products.length],
    ["Поставщики", state.data.suppliers.length],
    ["Склады", state.data.warehouses.length],
  ];
  const catalogReady = state.data.categories.length
    && state.data.products.length
    && state.data.suppliers.length
    && state.data.warehouses.length;
  return `
    <div class="grid">
      <div class="panel span-12 catalog-overview">
        ${catalogStats.map(([label, value]) => `
          <div>
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `).join("")}
      </div>
      <div class="panel span-12 catalog-guidance ${catalogReady ? "ok" : "warn"}">
        <strong>${catalogReady ? "Справочники готовы к работе" : "Заполните справочники по порядку"}</strong>
        <span>${catalogReady
          ? "Можно оформлять приход, списание, перемещение, заявки и инвентаризацию."
          : "Сначала добавьте категорию справа, затем создайте товар слева. После этого добавьте поставщика и склад."}</span>
      </div>
      <div class="form-panel span-7"><h2>${t("Новый товар")}</h2>${form("product-form", [
        { label: "Название", name: "name", required: true },
        { label: "Код товара", name: "sku", required: true },
        { label: "Ед. изм.", name: "unit", type: "select", options: productUnitOptions("Выберите единицу"), value: "шт", required: true },
        { label: "Категория", name: "category_id", type: "select", options: optionsFrom("categories", "Выберите категорию"), required: true },
        { label: "Точка заказа", name: "reorder_point", type: "number", step: "0.001", min: "0", value: "0" },
        { label: "Страховой запас", name: "safety_stock", type: "number", step: "0.001", min: "0", value: "0" },
        { label: "ПКУ / контролируемый товар", name: "is_controlled", type: "select", options: staticOptions([["false", "Нет"], ["true", "Да"]], "Выберите значение"), value: "false" },
        { label: "Штрихкод", name: "barcode", suffixActions: [
          { action: "scan-for-barcode-field", icon: "📷", title: "Сканировать штрихкод" },
          { action: "generate-barcode-field", icon: "🎲", title: "Сгенерировать EAN-13" },
        ] },
        { label: "Сертификат", name: "certificate_ref" },
        { label: "Описание", name: "description", type: "textarea", full: true },
      ], "Создать товар", {
        disabledSubmit: state.data.categories.length === 0,
        submitHint: state.data.categories.length === 0 ? "Сначала добавьте категорию справа." : "",
      })}</div>
      <div class="span-5 quick-directory">
        <div class="form-panel"><h2>${t("Новая категория")}</h2>${form("category-form", [
          { label: "Название категории", name: "name", required: true },
        ], "Добавить категорию")}</div>
        <div class="form-panel"><h2>${t("Новый поставщик")}</h2>${form("supplier-form", [
          { label: "Название поставщика", name: "name", required: true },
          { label: "БИН", name: "bin" },
          { label: "Телефон", name: "phone", type: "tel" },
          { label: "Адрес", name: "address" },
          { label: "Рейтинг", name: "rating", type: "number", min: "1", max: "5", step: "1" },
          { label: "Постоянный поставщик", name: "is_preferred", type: "select", options: staticOptions([["false", "Нет"], ["true", "Да"]], "Выберите значение"), value: "false" },
          { label: "Контактное лицо", name: "contact_person" },
          { label: "Email", name: "email", type: "email" },
          { label: "Номер договора", name: "contract_number" },
          { label: "Договор действует до", name: "contract_expires_on", type: "date" },
          { label: "Условия оплаты", name: "payment_terms" },
          { label: "Заметки", name: "notes", type: "textarea", full: true },
        ], "Добавить поставщика")}</div>
        <div class="form-panel"><h2>${t("Новый склад")}</h2>${form("warehouse-form", [
          { label: "Название склада или кабинета", name: "name", required: true },
          { label: "Отделение", name: "department" },
          { label: "ID компании Tetis", name: "tetis_org_id" },
          { label: "ID склада в Tetis", name: "external_tetis_id" },
          { label: "ID клиники в МИС", name: "mis_clinic_id" },
          { label: "ID кабинета в МИС", name: "mis_room_id" },
          { label: "Зона хранения", name: "storage_zone" },
          { label: "Лимит вместимости", name: "capacity_limit", type: "number", step: "0.001", min: "0" },
          { label: "Условия хранения", name: "storage_conditions" },
          { label: "Ответственный", name: "responsible_person" },
        ], "Добавить склад")}</div>
      </div>
      <div class="table-panel span-7">
        <div class="toolbar">
          <h2>${t("Товары")}</h2>
          <div class="row-actions">
            ${state.data.products.filter(p=>p.label_needs_reprint).length > 0
              ? `<button class="secondary" data-action="mass-reprint-labels">🔴 Перепечатать (${state.data.products.filter(p=>p.label_needs_reprint).length})</button>` : ""}
            <button class="secondary" data-export-report="products">CSV</button>
          </div>
          <label style="display:flex;align-items:center;gap:.35rem;font-size:.82rem;font-weight:400;cursor:pointer">
            <input type="checkbox" id="filter-reprint-only" ${state.ui?.reprintFilterOn ? "checked" : ""} style="cursor:pointer">
            Только требующие перепечатки
          </label>
        </div>
        ${table([
        { label: "", render: (row) => row.image_path
          ? `<img src="${escapeAttr(row.image_path)}" alt="" style="width:32px;height:32px;object-fit:cover;border-radius:5px;border:1px solid var(--line)" />`
          : `<span style="display:inline-flex;width:32px;height:32px;align-items:center;justify-content:center;border-radius:5px;border:1px dashed var(--line);color:var(--muted);font-size:.7rem">—</span>` },
        { label: "Номер", key: "id" }, { label: "Название", key: "name" }, { label: "Код товара", key: "sku" },
        { label: "Ед.", key: "unit" },
        { label: "Категория", render: (row) => nameById("categories", row.category_id) },
        { label: "Штрихкод", render: (row) => escapeHtml(row.barcode || "—") },
        { label: "Сертификат", render: (row) => row.certificate_ref
          ? (row.certificate_ref.startsWith("http") || row.certificate_ref.startsWith("/uploads/")
            ? `<a href="${escapeAttr(row.certificate_ref)}" target="_blank" rel="noopener" class="cert-preview-link">📄 Открыть ↗</a>`
            : escapeHtml(row.certificate_ref))
          : '<span style="color:#f59e0b;font-size:.78rem">Не загружен</span>' },
        { label: "Точка заказа", render: (row) => qty(row.reorder_point) },
        { label: "Страховой запас", render: (row) => qty(row.safety_stock) },
        { label: "ПКУ", render: (row) => row.is_controlled ? badge("да") : "нет" },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-print-product-label="${escapeAttr(row.id)}">${row.label_needs_reprint ? "🔴 Перепечатать" : "Этикетка"}</button>` },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-show-barcode="${escapeAttr(row.id)}">Штрихкод</button>` },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-edit-catalog="product" data-edit-id="${escapeAttr(row.id)}">Исправить</button>` },
        { label: "", render: (row) => `<button class="danger compact-action" type="button" data-delete-catalog="product" data-delete-id="${escapeAttr(row.id)}" title="Удалить товар из справочника">Удалить</button>` },
      ], filteredRows((state.ui?.reprintFilterOn ? state.data.products.filter(p => p.label_needs_reprint) : state.data.products), (row) => [row.id, row.name, row.sku, row.unit, row.barcode, row.certificate_ref, row.description, rawNameById("categories", row.category_id)]), "Товаров пока нет. Создайте категорию и новый товар в форме слева.")}
      </div>
      <div class="table-panel span-5"><h2>${t("Справочник")}</h2>${table([
        { label: "Тип", render: (row) => row.kind },
        { label: "Номер", key: "id" },
        { label: "Название", key: "name" },
        { label: "Детали", render: (row) => escapeHtml([row.department, row.storage_zone ? `Зона: ${row.storage_zone}` : "", row.capacity_limit ? `Лимит: ${row.capacity_limit}` : "", row.storage_conditions, row.responsible_person ? `Ответственный: ${row.responsible_person}` : "", row.bin, row.phone, row.email, row.contact_person, row.address, row.contract_number ? `Договор: ${row.contract_number}` : "", row.contract_expires_on ? `до ${row.contract_expires_on}` : "", row.rating ? `Рейтинг: ${"★".repeat(row.rating)}${"☆".repeat(5-row.rating)}` : "", row.is_preferred ? "Постоянный" : "", row.tetis_org_id ? `Tetis: ${row.tetis_org_id}` : "", row.external_tetis_id ? `Склад Tetis: ${row.external_tetis_id}` : "", row.mis_clinic_id ? `МИС-клиника: ${row.mis_clinic_id}` : "", row.mis_room_id ? `МИС-кабинет: ${row.mis_room_id}` : ""].filter(Boolean).join(" · ") || "—") },
        { label: "Статус", render: (row) => row.kind === "Склад" ? badge(row.inventory_lock ? "locked" : "open") : "—" },
        { label: "", render: (row) => row.kind === "Склад"
          ? `<button class="${row.inventory_lock ? "secondary" : "danger"}" data-lock-warehouse="${row.id}" data-lock-value="${row.inventory_lock ? "false" : "true"}">${row.inventory_lock ? "Разблокировать" : "Заблокировать"}</button>`
          : "" },
        { label: "", render: (row) => row.catalogKind === "supplier" ? `<button class="secondary compact-action" type="button" data-supplier-card="${escapeAttr(row.id)}">Карточка</button>` : "" },
        { label: "", render: (row) => row.catalogKind === "supplier" ? `<button class="secondary compact-action" type="button" data-export-price-history="${escapeAttr(row.id)}">История цен</button>` : "" },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-edit-catalog="${escapeAttr(row.catalogKind)}" data-edit-id="${escapeAttr(row.id)}">Исправить</button>` },
        { label: "", render: (row) => row.catalogKind === "category" ? `<button class="danger compact-action" type="button" data-delete-catalog="category" data-delete-id="${escapeAttr(row.id)}">Скрыть</button>` : "" },
      ], filteredRows(directoryRows, (row) => [row.kind, row.id, row.name, row.department, row.storage_zone, row.storage_conditions, row.responsible_person, row.bin, row.phone, row.email, row.contact_person, row.contract_number, row.notes]), "Справочник пуст. Добавьте категорию, поставщика или склад в формах выше.")}</div>
    </div>
  `;
}

function renderReceipts() {
  const cameraAvail = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
  return `
    <div class="grid">
      ${receiptPrerequisites()}
      <div class="form-panel span-5">
        <div class="toolbar"><h2>${t("Приемка сразу в остатки")}</h2>${cameraAvail ? `<button class="secondary" type="button" data-action="scan-for-receipt" style="font-size:.8rem">📷 ${t("Сканировать товар")}</button>` : ""}</div>
        ${form("receipt-form", [
        { label: "Товар", name: "product_id", type: "select", options: optionsFrom("products", "Выберите товар"), required: true },
        { label: "Поставщик", name: "supplier_id", type: "select", options: optionsFrom("suppliers", "Выберите поставщика"), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Цена", name: "unit_price", type: "number", step: "0.01", value: "0" },
        { label: "Серия партии", name: "lot", required: true },
        { label: "Серийный номер", name: "serial_number" },
        { label: "Срок годности", name: "expires_on", type: "date" },
      ], "Принять товар", {
        disabledSubmit: Boolean(receiptPrerequisites()),
        submitHint: receiptPrerequisites() ? "Заполните справочники выше, затем приход станет доступен." : "",
      })}</div>
      <div class="table-panel span-7"><h2>${t("Партии")}</h2>${table([
        { label: "Номер", key: "id" },
        { label: "Товар", render: (row) => nameById("products", row.product_id) },
        { label: "Поставщик", render: (row) => nameById("suppliers", row.supplier_id) },
        { label: "Серия", key: "lot" },
        { label: "Серийный", render: (row) => escapeHtml(row.serial_number || "—") },
        { label: "Цена", render: (row) => money(row.unit_price) },
        { label: "Годен до", key: "expires_on" },
        { label: "Статус", render: (row) => badge(row.status) },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-print-batch-price-label="${escapeAttr(row.id)}">Ценник</button>` },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-print-receipt-batch="${escapeAttr(row.id)}">Ордер</button>` },
        { label: "", render: (row) => {
            const rev = (state.data.quarantineReviews?.items || []).find(r => r.batch_id === row.id && ["pending","in_review"].includes(r.status));
            return (row.status === "quarantine" && rev
              ? `<button class="primary compact-action" type="button" data-quarantine-review="${escapeAttr(rev.id)}" data-quarantine-next-status="approved" title="Одобрить и сделать партию доступной">&#10003; Допустить</button> `
              : "") + batchButton(row.id, "Открыть");
          }},
      ], filteredRows(state.data.batches, (row) => [row.id, rawNameById("products", row.product_id), rawNameById("suppliers", row.supplier_id), row.lot, row.serial_number, row.expires_on, row.status]), "Партий пока нет. Сначала создайте товар, поставщика и примите товар на склад.")}</div>
    </div>
  `;
}

function receiptPrintHtml(form) {
  return `<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><title>Приходный ордер</title>
  <style>
    body { font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }
    h2 { font-size: 14px; margin-bottom: 4px; }
    .org { font-size: 11px; color: #666; margin-bottom: 16px; }
    table { border-collapse: collapse; width: 100%; margin: 12px 0; }
    th, td { border: 1px solid #333; padding: 4px 8px; text-align: left; }
    th { background: #f0f0f0; font-size: 11px; }
    .sign-block { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 24px; }
    .sign-line { border-top: 1px solid #333; margin-top: 30px; font-size: 11px; }
    @media print { @page { margin: 15mm; } }
  </style></head><body>
  <h2>ПРИХОДНЫЙ ОРДЕР \u2116 ${escapeHtml(String(form.batch_id))}</h2>
  <div class="org">Дата: ${escapeHtml(form.received_at ? form.received_at.slice(0,10) : '\u2014')}</div>
  <table>
    <tr><th>Наименование</th><td>${escapeHtml(form.product_name)}</td></tr>
    <tr><th>Артикул (SKU)</th><td>${escapeHtml(form.sku || '\u2014')}</td></tr>
    <tr><th>Серия партии</th><td>${escapeHtml(form.lot)}</td></tr>
    <tr><th>Серийный номер</th><td>${escapeHtml(form.serial_number || '\u2014')}</td></tr>
    <tr><th>Срок годности</th><td>${escapeHtml(form.expires_on || '\u2014')}</td></tr>
    <tr><th>Количество</th><td>${escapeHtml(String(form.quantity))} ${escapeHtml(form.unit || '\u0448\u0442')}</td></tr>
    <tr><th>Цена за единицу</th><td>${escapeHtml(String(form.unit_price || 0))} \u20b8</td></tr>
    <tr><th>Сумма</th><td>${escapeHtml(String((Number(form.quantity||0)*Number(form.unit_price||0)).toFixed(2)))} \u20b8</td></tr>
    <tr><th>Поставщик</th><td>${escapeHtml(form.supplier_name)}</td></tr>
    <tr><th>Склад</th><td>${escapeHtml(form.warehouse_name)}</td></tr>
    ${form.barcode ? `<tr><th>Штрихкод</th><td>${escapeHtml(form.barcode)}</td></tr>` : ''}
  </table>
  <div class="sign-block">
    <div><div class="sign-line">Принял: ___________________</div></div>
    <div><div class="sign-line">Сдал: ___________________</div></div>
  </div>
  </body></html>`;
}

function renderDocuments() {
  return `
    <div class="grid">
      ${!state.data.products.length || !state.data.suppliers.length || !state.data.warehouses.length
        ? workflowNotice("Не хватает справочников", "Для документов нужны товар, поставщик и склад.", "catalog", "Заполнить справочники")
        : ""}
      <div class="form-panel span-6"><h2>${t("Черновик приходного документа")}</h2>${receiptDocumentForm()}</div>
      <div class="form-panel span-6"><h2>${t("Черновик документа списания")}</h2>${writeoffDocumentForm()}</div>
      <div class="table-panel span-12"><div class="toolbar"><h2>${t("Складские документы")}</h2><button class="secondary" data-export-report="documents">${t("Выгрузить CSV")}</button></div>${table([
        { label: "Номер", key: "id" },
        { label: "Тип", render: (row) => humanDocumentType(row.document_type) },
        { label: "Статус", render: (row) => badge(row.status) },
        { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
        { label: "Строк", render: (row) => row.lines?.length || 0 },
        { label: "Создал", key: "created_by" },
        { label: "Утвердил", render: (row) => escapeHtml(row.approved_by || "—") },
        { label: "Создан", render: (row) => dateText(row.created_at) },
        { label: "", render: (row) => row.document_type === "transfer" ? `<button class="secondary compact-action" data-download-transfer-form="${escapeAttr(row.id)}">Печатная форма</button>` : "" },
        { label: "", render: (row) => ["draft", "approved"].includes(String(row.status)) ? `<div class="row-actions">${row.status === "draft" ? `<button class="secondary" data-approve-document="${row.id}">Утвердить</button>` : `<button class="secondary" data-post-document="${row.id}">Провести и изменить остатки</button>`}<button class="danger" data-cancel-document="${row.id}">Отменить</button></div>` : "" },
      ], filteredRows(state.data.documents, (row) => [row.id, row.document_type, row.status, rawNameById("warehouses", row.warehouse_id), row.created_by, row.approved_by, row.created_at]), "Документов пока нет. Создайте черновик прихода или списания выше.")}</div>
    </div>
  `;
}

function receiptDocumentForm() {
  const unavailable = !state.data.products.length || !state.data.suppliers.length || !state.data.warehouses.length;
  return `
    <form id="receipt-doc-form" class="form-grid">
      <label>Поставщик
        <select name="supplier_id" required data-doc-header-field="supplier_id" data-doc-line-kind="receipt">
          ${optionsFrom("suppliers", "Выберите поставщика").map((option) => `<option value="${escapeAttr(option.value)}" ${String(option.value) === String(state.documentForms.receipt.supplier_id) ? "selected" : ""}>${option.label}</option>`).join("")}
        </select>
      </label>
      <label>Склад
        <select name="warehouse_id" required data-doc-header-field="warehouse_id" data-doc-line-kind="receipt">
          ${optionsFrom("warehouses", "Выберите склад").map((option) => `<option value="${escapeAttr(option.value)}" ${String(option.value) === String(state.documentForms.receipt.warehouse_id) ? "selected" : ""}>${option.label}</option>`).join("")}
        </select>
      </label>
      <label>№ ЭСФ / накладной <span style="font-weight:400;font-size:.8rem;color:#6b7280">(необязательно)</span>
        <input name="external_ref" type="text" maxlength="200" placeholder="Например: ЭСФ-000123 или НАК-2026-001" value="${escapeHtml(state.documentForms.receipt.external_ref || '')}">
      </label>
      <label>Примечание к документу
        <input name="notes" type="text" maxlength="500" placeholder="Комментарий к приходу" value="${escapeHtml(state.documentForms.receipt.notes || '')}">
      </label>
      <div class="full">
        <div class="toolbar">
          <h3>${t("Строки прихода")}</h3>
          <button class="secondary" type="button" data-doc-line-add="receipt">Добавить строку</button>
        </div>
        ${receiptDocumentLinesTable()}
      </div>
      ${unavailable ? '<div class="form-hint blocked full">Сначала добавьте товар, поставщика и склад.</div>' : ""}
      <div class="actions full"><button class="primary" type="submit" ${unavailable ? "disabled" : ""}>Создать черновик прихода</button></div>
    </form>
  `;
}

function writeoffDocumentForm() {
  const unavailable = state.data.balances.items.length === 0;
  return `
    <form id="writeoff-doc-form" class="form-grid">
      <label class="full">Склад
        <select name="warehouse_id" required data-doc-header-field="warehouse_id" data-doc-line-kind="writeoff">
          ${optionsFrom("warehouses", "Выберите склад").map((option) => `<option value="${escapeAttr(option.value)}" ${String(option.value) === String(state.documentForms.writeoff.warehouse_id) ? "selected" : ""}>${option.label}</option>`).join("")}
        </select>
      </label>
      <div class="full">
        <div class="toolbar">
          <h3>${t("Строки списания")}</h3>
          <button class="secondary" type="button" data-doc-line-add="writeoff">Добавить строку</button>
        </div>
        ${writeoffDocumentLinesTable()}
      </div>
      ${unavailable ? '<div class="form-hint blocked full">Сначала примите товар на склад.</div>' : ""}
      <div class="actions full"><button class="primary" type="submit" ${unavailable ? "disabled" : ""}>Создать черновик списания</button></div>
    </form>
  `;
}

function docLineAttrs(kind, index, field) {
  return `data-doc-line-field="${field}" data-doc-line-kind="${kind}" data-doc-line-index="${index}"`;
}

function receiptDocumentLinesTable() {
  return `
    <div class="table-wrap">
      <table>
        <thead><tr><th>Товар</th><th>Количество</th><th>Цена</th><th>Серия партии</th><th>Серийный номер</th><th>Срок годности</th><th></th></tr></thead>
        <tbody>
          ${state.documentForms.receipt.lines.map((line, index) => `
            <tr>
              <td><select required ${docLineAttrs("receipt", index, "product_id")}>
                ${optionsFrom("products", "Выберите товар").map((option) => `<option value="${escapeAttr(option.value)}" ${String(option.value) === String(line.product_id) ? "selected" : ""}>${option.label}</option>`).join("")}
              </select></td>
              <td><input required type="number" step="0.001" value="${escapeAttr(line.quantity)}" ${docLineAttrs("receipt", index, "quantity")} /></td>
              <td><input required type="number" step="0.01" value="${escapeAttr(line.unit_price)}" ${docLineAttrs("receipt", index, "unit_price")} /></td>
              <td><input required value="${escapeAttr(line.lot)}" ${docLineAttrs("receipt", index, "lot")} /></td>
              <td><input value="${escapeAttr(line.serial_number)}" ${docLineAttrs("receipt", index, "serial_number")} /></td>
              <td><input type="date" value="${escapeAttr(line.expires_on)}" ${docLineAttrs("receipt", index, "expires_on")} /></td>
              <td><button class="danger" type="button" data-doc-line-remove="receipt" data-doc-line-index="${index}" ${state.documentForms.receipt.lines.length === 1 ? "disabled" : ""}>Удалить</button></td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function writeoffDocumentLinesTable() {
  return `
    <div class="table-wrap">
      <table>
        <thead><tr><th>Партия</th><th>Количество</th><th>Причина</th><th>Пациент</th><th>Врач</th><th>История болезни</th><th>2-й подтверждающий</th><th>Комментарий ПКУ</th><th></th></tr></thead>
        <tbody>
          ${state.documentForms.writeoff.lines.map((line, index) => `
            <tr class="${controlledWriteoffMetadataMissing(line).length ? "controlled-warning" : ""}">
              <td><select required ${docLineAttrs("writeoff", index, "batch_id")}>
                ${batchOptions("Выберите партию с остатком").map((option) => `<option value="${escapeAttr(option.value)}" ${String(option.value) === String(line.batch_id) ? "selected" : ""}>${option.label}</option>`).join("")}
              </select></td>
              <td><input required type="number" step="0.001" value="${escapeAttr(line.quantity)}" ${docLineAttrs("writeoff", index, "quantity")} /></td>
              <td><input required value="${escapeAttr(line.reason)}" ${docLineAttrs("writeoff", index, "reason")} /></td>
              <td><input value="${escapeAttr(line.patient_id)}" ${docLineAttrs("writeoff", index, "patient_id")} /></td>
              <td><input value="${escapeAttr(line.doctor_id)}" ${docLineAttrs("writeoff", index, "doctor_id")} /></td>
              <td><input value="${escapeAttr(line.medical_record_no)}" ${docLineAttrs("writeoff", index, "medical_record_no")} /></td>
              <td><input value="${escapeAttr(line.second_approver_id)}" ${docLineAttrs("writeoff", index, "second_approver_id")} /></td>
              <td><input value="${escapeAttr(line.second_approval_note)}" ${docLineAttrs("writeoff", index, "second_approval_note")} /></td>
              <td><button class="danger" type="button" data-doc-line-remove="writeoff" data-doc-line-index="${index}" ${state.documentForms.writeoff.lines.length === 1 ? "disabled" : ""}>Удалить</button></td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function tabletWriteoffForm() {
  const stockUnavailable = state.data.balances.items.length === 0;
  const cameraAvailTW = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
  const filterProd = state.ui.batchFilterProductId
    ? state.data.products.find((p) => Number(p.id) === Number(state.ui.batchFilterProductId))
    : null;
  const filterBar = filterProd ? `<div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem;background:#fef9c3;padding:.4rem .75rem;border-radius:6px;font-size:.85rem"><span>📦 ${escapeHtml(filterProd.name)}</span><button type="button" class="secondary compact-action" data-action="clear-batch-filter">✕</button></div>` : "";
  const scanBtn = cameraAvailTW ? `<button type="button" class="secondary" data-action="scan-for-batch-filter" style="font-size:.8rem;margin-bottom:.5rem;width:100%">📷 Найти товар сканером</button>` : "";
  return scanBtn + filterBar + form("tablet-writeoff-form", [
    { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком", { productId: state.ui.batchFilterProductId }), required: true, full: true },
    { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Автоматически по партии"), required: true, batchWarehouseField: "warehouse_id" },
    { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
    { label: "Причина", name: "reason", value: "Списание в отделении", required: true, full: true },
    { label: "Пациент", name: "patient_id" },
    { label: "История болезни", name: "medical_record_no" },
    { label: "Врач", name: "doctor_id", value: currentRole() === "doctor" ? currentActorId() : "" },
    { label: "2-й подтверждающий", name: "second_approver_id" },
    { label: "Комментарий ПКУ", name: "second_approval_note" },
  ], "Списать", {
    batchAware: true,
    disabledSubmit: stockUnavailable,
    submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
  });
}

function renderTabletWriteoff() {
  return `
    <div class="grid tablet-view">
      ${roleAccessNotice()}
      <div class="tablet-writeoff-panel span-7">
        <div class="tablet-copy">
          <span class="eyebrow">Планшетное списание</span>
          <h2>${t("Минимальная форма списания партии")}</h2>
        </div>
        ${tabletWriteoffForm()}
      </div>
      <div class="table-panel span-5">
        <div class="toolbar">
          <h2>${t("Остатки")}</h2>
          <button class="secondary" data-action="reload">${t("Обновить")}</button>
        </div>
        ${balancesTable(filteredBalances(state.data.balances.items), "Остатков пока нет. Проверьте склад в верхней панели.")}
      </div>
      <div class="table-panel span-12">
        <h2>${t("Недавние списания")}</h2>
        ${table([
          { label: "Партия", render: (row) => batchDetailLabel(row.batch_id) },
          { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
          { label: "Количество", key: "quantity" },
          { label: "Причина", key: "reason" },
          { label: "Пациент", render: (row) => escapeHtml(row.patient_id || "—") },
          { label: "Время", render: (row) => dateText(row.created_at) },
        ], filteredRows(state.data.movements.filter((row) => row.movement_type === "write_off").slice(0, 12), (row) => [row.batch_id, rawNameById("warehouses", row.warehouse_id), row.quantity, row.reason, row.patient_id, row.created_at]), "Списаний пока нет.")}
      </div>
    </div>
  `;
}

function renderOperations() {
  const stockUnavailable = state.data.balances.items.length === 0;
  const quarantineReviews = pageItems(state.data.quarantineReviews);
  return `
    <div class="grid">
      ${needsStockNotice("Перейти к приходу")}
      <div class="form-panel span-3">
        <div class="toolbar"><h2>${t("Списание по ближайшему сроку")}</h2>${!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia) ? `<button class="secondary" type="button" data-action="scan-for-fefo" style="font-size:.8rem">📷 ${t("Сканировать товар")}</button>` : ""}</div>
        ${form("fefo-form", [
        { label: "Товар", name: "product_id", type: "select", options: optionsFrom("products", "Выберите товар"), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Списание по требованию", required: true },
        { label: "Пациент", name: "patient_id" },
        { label: "Врач", name: "doctor_id" },
        { label: "История болезни", name: "medical_record_no" },
        { label: "2-й подтверждающий", name: "second_approver_id" },
        { label: "Комментарий ПКУ", name: "second_approval_note" },
      ], "Списать по сроку годности", {
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="form-panel span-3"><h2>${t("Списание партии")}</h2>${form("writeoff-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком"), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true, batchWarehouseField: "warehouse_id" },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Списание конкретной партии", required: true },
        { label: "Пациент", name: "patient_id" },
        { label: "Врач", name: "doctor_id" },
        { label: "История болезни", name: "medical_record_no" },
        { label: "2-й подтверждающий", name: "second_approver_id" },
        { label: "Комментарий ПКУ", name: "second_approval_note" },
      ], "Списать партию", {
        batchAware: true,
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="form-panel span-3"><h2>${t("Перемещение")}</h2>${form("transfer-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком"), required: true },
        { label: "Склад-источник", name: "source_warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true, batchWarehouseField: "source_warehouse_id" },
        { label: "Склад-получатель", name: "target_warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Внутреннее перемещение", required: true },
      ], "Переместить", {
        batchAware: true,
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="form-panel span-3"><h2>${t("Статус партии")}</h2>${form("batch-status-form", [
        { label: "Партия", name: "batch_id", type: "select", options: optionsFrom("batches", "Выберите партию", (batch) => `${rawNameById("products", batch.product_id)} · серия ${batch.lot}`), required: true },
        { label: "Статус", name: "status", type: "select", options: staticOptions([["available", "Допущен"], ["quarantine", "Карантин"], ["blocked", "Заблокирован"]], "Выберите статус"), value: "available", required: true },
        { label: "Причина", name: "reason" },
      ], "Обновить статус", {
        disabledSubmit: state.data.batches.length === 0,
        submitHint: state.data.batches.length === 0 ? "Сначала примите партию на склад." : "",
      })}</div>
      <div class="form-panel span-3"><h2>${t("Отзыв партии")}</h2>${form("batch-recall-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком", { onlyAvailable: false }), required: true },
        { label: "Склад для проверки", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Автоматически по партии"), required: true, batchWarehouseField: "warehouse_id" },
        { label: "Источник", name: "source", value: "Поставщик / производитель" },
        { label: "Документ-основание", name: "reference" },
        { label: "Причина отзыва", name: "reason", type: "textarea", required: true, full: true },
      ], "Отозвать и заблокировать", {
        batchAware: true,
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Нет партий с остатком для отзыва." : "Партия будет заблокирована, а склады получат уведомления.",
      })}</div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <div>
            <h2>${t("Карантинные проверки")}</h2>
            <span class="helper-text">Партия из карантина станет доступной только после решения проверки.</span>
          </div>
          <button class="secondary" data-action="reload">Обновить</button>
        </div>
        ${table([
          { label: "Партия", render: (row) => `${batchButton(row.batch_id)}<br><span class="badge">${escapeHtml(row.lot)}</span>` },
          { label: "Товар", render: (row) => escapeHtml(row.product_name) },
          { label: "Статус", render: (row) => badge(row.status) },
          { label: "Ответственный", render: (row) => escapeHtml(row.responsible_id || "Не назначен") },
          { label: "Комиссия", render: (row) => {
            const m = row.commission_members;
            return m && m.length ? escapeHtml(m.join(", ")) : "—";
          }},
          { label: "Срок", render: (row) => row.due_at ? dateText(row.due_at) : "—" },
          { label: "Тип решения", render: (row) => {
            const types = { approved_for_use: "К использованию", return_to_supplier: "Возврат", disposal: "Утилизация" };
            return row.resolution_type ? (types[row.resolution_type] || escapeHtml(row.resolution_type)) : "—";
          }},
          { label: "Решение", render: (row) => escapeHtml((row.decision_reason || "").slice(0,80)) },
          { label: "", render: (row) => `<button class="secondary compact-action" data-download-quarantine-protocol="${escapeAttr(row.id)}">Протокол</button>` },
          { label: "", render: (row) => ["pending", "in_review"].includes(String(row.status)) ? `
            <div class="row-actions">
              <button class="secondary" data-quarantine-review="${row.id}" data-quarantine-next-status="in_review">Начать проверку</button>
              <button class="primary" data-quarantine-review="${row.id}" data-quarantine-next-status="approved">Допустить</button>
              <button class="danger" data-quarantine-review="${row.id}" data-quarantine-next-status="rejected">Забраковать</button>
            </div>
          ` : "" },
        ], filteredRows(quarantineReviews, (row) => [row.batch_id, row.product_name, row.lot, row.status, row.responsible_id, row.decision_reason]), "Карантинных проверок пока нет. Новые партии в карантине появятся здесь автоматически.")}
      </div>
      <div class="table-panel span-12"><h2>${t("Текущие остатки")}</h2>${balancesTable(filteredBalances(state.data.balances.items), "Остатков пока нет. Примите товар на склад или проверьте выбранный фильтр склада.")}</div>
    </div>
  `;
}

function renderRepacking() {
  const stockUnavailable = state.data.balances.items.length === 0;
  const rows = pageItems(state.data.repackings);
  return `
    <div class="grid">
      ${needsStockNotice("Принять товар")}
      <div class="form-panel span-4">
        <h2>${t("Фасовка партии")}</h2>
        ${state.data.repackTemplates.length ? `
          <div style="margin-bottom:.75rem;padding:.5rem;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:6px">
            <label style="font-size:.82rem;font-weight:600;display:block;margin-bottom:.35rem">${t("Шаблон фасовки")}</label>
            <div style="display:flex;gap:.5rem;align-items:center">
              <select id="repack-template-select" style="flex:1;padding:.35rem;border:1px solid #d1d5db;border-radius:4px;font-size:.85rem">
                <option value="">${t("Выберите шаблон")}</option>
                ${state.data.repackTemplates.map(tpl => `<option value="${escapeAttr(tpl.id)}">${escapeHtml(tpl.name)}</option>`).join("")}
              </select>
              <button type="button" class="secondary" data-action="apply-repack-template" style="padding:.3rem .7rem;font-size:.82rem">${t("Применить")}</button>
            </div>
          </div>
        ` : ""}
        ${form("repacking-form", [
          { label: "Исходная партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком"), required: true },
          { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Склад партии"), required: true, batchWarehouseField: "warehouse_id" },
          { label: "Что получится", name: "target_product_id", type: "select", options: optionsFrom("products", "Выберите товар результата"), required: true },
          { label: "Сколько взять", name: "quantity", type: "number", step: "0.001", required: true },
          { label: "Сколько получится", name: "target_quantity", type: "number", step: "0.001", required: true },
          { label: "Потери", name: "loss_quantity", type: "number", step: "0.001", value: "0" },
          { label: "Новая серия / лот", name: "target_lot", required: true },
          { label: "Годен до", name: "target_expires_on", type: "date" },
          { label: "Цена результата", name: "target_unit_price", type: "number", step: "0.0001" },
          { label: "Статус результата", name: "quarantine", type: "select", options: staticOptions([["false", "Сразу доступен"], ["true", "Через карантин"]], "Выберите статус"), value: "false" },
          { label: "Причина", name: "reason", value: "Фасовка / переупаковка", required: true, full: true },
        ], "Создать черновик фасовки", {
          batchAware: true,
          disabledSubmit: stockUnavailable,
          submitHint: stockUnavailable ? "Сначала примите товар на склад." : "После создания черновик нужно провести в разделе документов.",
        })}
        <div style="margin-top:.5rem">
          <button type="button" class="secondary" data-action="save-repack-template" style="font-size:.82rem;padding:.3rem .7rem">${t("Сохранить как шаблон")}</button>
        </div>
      </div>
      <div class="table-panel span-8">
        <div class="toolbar">
          <div>
            <h2>${t("Журнал фасовки")}</h2>
            <span class="helper-text">Здесь видно, какая партия стала источником и какая появилась после фасовки.</span>
          </div>
          <button class="secondary" data-export-report="repackings">Выгрузить CSV</button>
        </div>
        ${table([
          { label: "Номер", key: "id" },
          { label: "Исходная партия", render: (row) => batchDetailLabel(row.source_batch_id) },
          { label: "Полученная партия", render: (row) => batchDetailLabel(row.target_batch_id) },
          { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
          { label: "Взяли", key: "source_quantity" },
          { label: "Получили", key: "target_quantity" },
          { label: "Потери", key: "loss_quantity" },
          { label: "Коэф.", key: "conversion_factor" },
          { label: "Время", render: (row) => dateText(row.created_at) },
          { label: "", render: (row) => row.document_id ? `<button class="secondary compact-action" data-download-repack-form="${escapeAttr(row.document_id)}">Печатная форма</button>` : "" },
        ], filteredRows(rows, (row) => [
          row.id,
          row.document_id,
          row.source_batch_id,
          row.target_batch_id,
          row.source_product_name,
          row.target_product_name,
          row.source_lot,
          row.target_lot,
          rawNameById("warehouses", row.warehouse_id),
          row.reason,
          row.created_at,
        ]), "Фасовок пока нет. Создайте черновик и проведите его в документах.")}
      </div>
      <div class="table-panel span-12"><h2>${t("Остатки после операций")}</h2>${balancesTable(filteredBalances(state.data.balances.items), "Остатков пока нет. Примите товар на склад или проверьте выбранный фильтр склада.")}</div>
    </div>
  `;
}

function renderReturns() {
  const stockUnavailable = state.data.balances.items.length === 0;
  return `
    <div class="grid">
      ${needsStockNotice("Принять товар")}
      <div class="form-panel span-6"><h2>${t("Возврат от отделения")}</h2>${form("department-return-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком"), required: true },
        { label: "Откуда", name: "source_warehouse_id", type: "select", options: optionsFrom("warehouses", "Кабинет / отделение"), required: true, batchWarehouseField: "source_warehouse_id" },
        { label: "Куда", name: "target_warehouse_id", type: "select", options: optionsFrom("warehouses", "Основной склад"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Возврат неиспользованных материалов", required: true },
      ], "Оформить возврат", {
        batchAware: true,
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="form-panel span-6"><h2>${t("Возврат поставщику")}</h2>${form("supplier-return-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком", { onlyAvailable: false }), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true, batchWarehouseField: "warehouse_id" },
        { label: "Поставщик", name: "supplier_id", type: "select", options: optionsFrom("suppliers", "Выберите поставщика"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Брак / несоответствие поставке", required: true },
      ], "Вернуть поставщику", {
        batchAware: true,
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="table-panel span-12"><h2>${t("Партии для возврата")}</h2>${table([
        { label: "Номер", key: "id" },
        { label: "Товар", render: (row) => nameById("products", row.product_id) },
        { label: "Поставщик", render: (row) => nameById("suppliers", row.supplier_id) },
        { label: "Серия", key: "lot" },
        { label: "Годен до", key: "expires_on" },
        { label: "Статус", render: (row) => badge(row.status) },
        { label: "", render: (row) => batchButton(row.id, "Открыть") },
      ], filteredRows(state.data.batches, (row) => [row.id, rawNameById("products", row.product_id), rawNameById("suppliers", row.supplier_id), row.lot, row.expires_on, row.status]), "Партий для возврата пока нет. Сначала примите товар на склад.")}</div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("Дашборд отзывов партий")}</h2>
        </div>
        ${renderRecallStats()}
      </div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("Журнал отзывов партий")}</h2>
          <div class="row-actions">
            <button class="secondary" data-export-report="batchRecalls">Выгрузить CSV</button>
          </div>
        </div>
        ${table([
          { label: "#", key: "id" },
          { label: "Товар", render: (row) => escapeHtml(row.product_name || "—") },
          { label: "Партия / Серия", render: (row) => {
            const bBtn = row.batch_id ? batchButton(row.batch_id, row.lot || `#${row.batch_id}`) : "—";
            const sn = row.serial_number ? `<br><span style="font-size:.8rem;color:#6b7280">S/N: ${escapeHtml(row.serial_number)}</span>` : "";
            return bBtn + sn;
          }},
          { label: "Статус", render: (row) => badge(row.batch_status || "active") },
          { label: "Источник", key: "source" },
          { label: "Основание", render: (row) => escapeHtml(row.reference || "—") },
          { label: "Причина", render: (row) => escapeHtml((row.reason || "").slice(0, 80)) },
          { label: "Создал", key: "created_by" },
          { label: "Создано", render: (row) => dateText(row.created_at) },
          { label: "", render: (row) => row.batch_status === "blocked"
            ? `<button class="secondary" data-action="unblock-batch" data-batch-id="${row.batch_id}">Разблокировать</button>`
            : "" },
        ], filteredRows(state.data.batchRecalls.items || [], (row) => [row.id, row.product_name, row.lot, row.serial_number, row.source, row.reference, row.reason, row.created_by, row.created_at]), "Отзывов партий пока нет. Если производитель отзывает серию, оформите отзыв в разделе партий.")}
      </div>
    </div>
  `;
}

function renderMovements() {
  const controlledLimits = state.data.controlledLimits || [];
  const controlledProducts = (state.data.products || []).filter((p) => p.is_controlled);
  const wfParam = warehouseFilterParam();
  const currentWarehouseId = wfParam ? new URLSearchParams(wfParam).get("warehouse_id") : null;
  return `
    <div class="grid">
      <div class="panel span-3 metric"><span>Всего движений</span><strong>${state.data.movements.length}</strong></div>
      <div class="panel span-3 metric"><span>Поступления</span><strong>${state.data.movements.filter((row) => row.movement_type === "receipt").length}</strong></div>
      <div class="panel span-3 metric"><span>Списания</span><strong>${state.data.movements.filter((row) => row.movement_type === "write_off").length}</strong></div>
      <div class="panel span-3 metric"><span>Возвраты поставщику</span><strong>${state.data.movements.filter((row) => row.movement_type === "return_to_supplier").length}</strong></div>
      <div class="table-panel span-12"><div class="toolbar"><h2>${t("История движения ТМЦ")}</h2><div class="row-actions"><button class="secondary" data-download-controlled-ledger>${t("Экспорт ПКУ CSV")}</button><a id="pku-pdf-link" href="#" data-download-pku-pdf style="display:inline-block;padding:.35rem .7rem;background:#dc2626;color:white;border-radius:4px;text-decoration:none;font-size:.82rem;cursor:pointer;border:none">${t("↓ PDF журнал ПКУ")}</a><button class="secondary" data-export-report="movements">${t("Выгрузить CSV")}</button></div></div>${table([
        { label: "Номер", key: "id" },
        { label: "Действие", render: (row) => badge(row.movement_type) },
        { label: "Партия", render: (row) => batchDetailLabel(row.batch_id) },
        { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
        { label: "Количество", key: "quantity" },
        { label: "Причина", key: "reason" },
        { label: "Пациент", render: (row) => escapeHtml(row.patient_id || "—") },
        { label: "Время", render: (row) => dateText(row.created_at) },
      ], filteredRows(state.data.movements, (row) => [row.id, row.movement_type, batchLabel(row.batch_id), rawNameById("warehouses", row.warehouse_id), row.quantity, row.reason, row.patient_id, row.created_at]))}</div>
      ${currentWarehouseId && isManagerRole() ? `
      <div class="form-panel span-4">
        <h2>${t("Лимиты ПКУ по кабинету")}</h2>
        <p style="font-size:.82rem;color:#6b7280;margin:0 0 .75rem">Настройте максимальное количество хранения контролируемых веществ для выбранного кабинета.</p>
        ${form("controlled-limit-form", [
          { label: "Товар (ПКУ)", name: "product_id", type: "select", options: staticOptions(controlledProducts.map((p) => [String(p.id), p.name + (p.sku ? " (" + p.sku + ")" : "")]), "Выберите товар"), required: true },
          { label: "Макс. кол-во", name: "max_quantity", type: "number", step: "0.001", min: "0", required: true },
          { label: "Единица", name: "unit", value: "" },
        ], "Сохранить лимит")}
      </div>
      <div class="table-panel span-8">
        <div class="toolbar">
          <h2>${t("Текущие лимиты ПКУ")}</h2>
          <button class="secondary" data-action="reload-controlled-limits">Обновить</button>
        </div>
        <div id="controlled-limits-table">${controlledLimits.length === 0 ? "<p class=\"empty-state\">Лимиты не установлены.</p>" : table([
          { label: "Товар", render: (row) => escapeHtml(row.product_name) },
          { label: "Макс. кол-во", render: (row) => qty(row.max_quantity) + " " + escapeHtml(row.unit || "") },
          { label: "", render: (row) => "<button class=\"danger compact-action\" data-delete-controlled-limit=\"" + escapeAttr(row.id) + "\">Удалить</button>" },
        ], controlledLimits, "")}</div>
      </div>
      ` : ""}
      ${currentWarehouseId ? `
      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("Нарушения лимитов ПКУ")}</h2>
          <div class="row-actions">
            <button class="secondary" data-action="check-violations">${t("Проверить")}</button>
          </div>
        </div>
        ${(() => {
          const violations = state.data.controlledViolations || [];
          if (violations.length === 0) {
            return `<p class="empty-state" style="color:#16a34a">&#10003; ${t("Нарушений лимитов не обнаружено")}</p>`;
          }
          return table([
            { label: "Товар", render: (row) => escapeHtml(row.product_name) },
            { label: t("Превышение: текущие остатки"), render: (row) => `<span style="color:#dc2626;font-weight:600">${qty(row.current_quantity)}</span>` },
            { label: "Лимит", render: (row) => qty(row.max_quantity) + " " + escapeHtml(row.unit || "") },
            { label: "Превышение на", render: (row) => `<span style="color:#dc2626">+${qty(row.current_quantity - row.max_quantity)}</span>` },
          ], violations, "");
        })()}
      </div>
      ` : ""}
      ${renderPendingControlledWriteoffs()}
    </div>
  `;
}

function renderReservations() {
  const stockUnavailable = state.data.balances.items.length === 0;
  return `
    <div class="grid">
      ${needsStockNotice("Принять товар")}
      <div class="form-panel span-4"><h2>${t("Новый резерв")}</h2>${form("reservation-form", [
        { label: "Партия", name: "batch_id", type: "select", options: batchOptions("Выберите партию с остатком"), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Для кого", name: "reserved_for", required: true },
        { label: "Истекает", name: "expires_at", type: "datetime-local" },
      ], "Зарезервировать", {
        disabledSubmit: stockUnavailable,
        submitHint: stockUnavailable ? "Сначала примите товар на склад." : "",
      })}</div>
      <div class="table-panel span-8"><div class="toolbar"><h2>${t("Бронирование товаров")}</h2><button class="secondary" data-action="expire-reservations">${t("Снять просроченную бронь")}</button></div>${table([
        { label: "Номер", key: "id" },
        { label: "Партия", render: (row) => batchButton(row.batch_id) },
        { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
        { label: "Кол-во", key: "quantity" },
        { label: "Для", key: "reserved_for" },
        { label: "Статус", render: (row) => badge(row.status) },
        { label: "Истекает", render: (row) => dateText(row.expires_at) },
        { label: "", render: (row) => `
          <div class="row-actions">
            <button class="primary" data-use-reservation="${row.id}" ${["used", "released", "cancelled"].includes(String(row.status)) ? "disabled" : ""}>Использовать резерв</button>
            <button class="secondary" data-release="${row.id}" ${["used", "released", "cancelled"].includes(String(row.status)) ? "disabled" : ""}>Снять бронь</button>
          </div>
        ` },
      ], filteredRows(state.data.reservations, (row) => [row.id, row.batch_id, rawNameById("warehouses", row.warehouse_id), row.quantity, row.reserved_for, row.status, row.expires_at]), "Брони пока нет. Выберите партию с остатком и создайте резерв слева.")}</div>
    </div>
  `;
}

function suggestedPurchaseRequests() {
  return state.data.analytics.items
    .filter((row) => Number(row.recommended_order_quantity || 0) > 0)
    .map((row) => ({
      product_id: row.product_id,
      product_name: row.product_name,
      sku: row.sku,
      warehouse_id: row.warehouse_id || state.data.analytics.warehouse_id,
      quantity: row.recommended_order_quantity,
      reason: row.recommendation || "Ниже точки заказа",
      source: "analytics",
    }));
}

function findMarketplaceOffersForProduct(productId) {
  const product = state.data.products.find((p) => p.id === productId);
  if (!product) return [];
  const productName = (product.name || "").toLowerCase();
  return (state.data.marketplace?.items || []).filter((item) => {
    const itemName = (item.product_name || "").toLowerCase();
    return (
      (item.product_id && item.product_id === productId) ||
      itemName.includes(productName) ||
      (productName.length > 4 && productName.includes(itemName.slice(0, 4)))
    );
  });
}

function renderPurchaseRequests() {
  const productUnavailable = state.data.products.length === 0;
  const suggestions = suggestedPurchaseRequests();
  const requests = filteredRows(state.data.purchaseRequests, (row) => [
    row.id,
    rawNameById("products", row.product_id),
    rawNameById("warehouses", row.warehouse_id),
    row.recommended_quantity,
    row.status,
    row.reason,
    row.created_at,
  ]);
  return `
    <div class="grid">
      ${needsProductNotice("Создать товар")}
      <div class="form-panel span-4"><h2>${t("Новая заявка")}</h2>${form("purchase-request-form", [
        { label: "Товар", name: "product_id", type: "select", options: optionsFrom("products", "Выберите товар"), required: true },
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Для какого склада") },
        { label: "Количество", name: "quantity", type: "number", step: "0.001", required: true },
        { label: "Причина", name: "reason", value: "Пополнение склада", full: true },
        { label: "Требуемое состояние", name: "condition_accepted", type: "select", options: [
          { value: "any", label: "Любое" },
          { value: "new", label: "Только новый" },
          { value: "used", label: "Б/У принимается" },
        ]},
        { label: "Гос. закупка", name: "is_gov_procurement", type: "checkbox" },
      ], "Создать заявку", {
        disabledSubmit: productUnavailable,
        submitHint: productUnavailable ? "Сначала создайте товар." : "",
      })}</div>
      <div class="panel span-4 metric"><span>Открытые заявки</span><strong>${state.data.purchaseRequests.filter((row) => ["draft", "requested", "open"].includes(String(row.status || "open"))).length}</strong></div>
      <div class="panel span-4 metric"><span>Автозаявки к созданию</span><strong>${suggestions.length}</strong></div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <div>
            <h2>${t("Заявки на закупку")}</h2>
            <span class="helper-text">Если модуль закупок еще не включен на сервере, эта панель останется пустой и покажет предупреждение на главной.</span>
          </div>
          <div class="row-actions">
            <button class="secondary" data-export-report="purchaseRequests">Выгрузить CSV</button>
            <button class="secondary" data-action="download-purchase-pdf">Скачать PDF</button>
            <button class="primary" data-action="generate-purchase-requests">Сформировать автозаявки</button>
            <button class="secondary" data-action="ai-analyze-purchases" id="ai-analyze-btn" title="AI анализ рисков закупок">🤖 AI анализ</button>
            <button class="secondary" data-action="reload">Обновить</button>
          </div>
        </div>
        <div id="ai-analysis-result" style="display:none;margin:.5rem 0;padding:.75rem;background:#f0f9ff;border:1px solid #bae6fd;border-radius:6px;font-size:.85rem"></div>
        ${table([
          { label: "Номер", key: "id" },
          { label: "Товар", render: (row) => nameById("products", row.product_id) },
          { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "—" },
          { label: "Количество", render: (row) => escapeHtml(row.recommended_quantity || row.quantity || row.recommended_order_quantity || "—") },
          { label: "Статус", render: (row) => {
            let s = badge(row.status || "open");
            if (row.is_gov_procurement) {
              const govLabels = { demand: "Спрос", accepting: "Приём", closed: "Закрыт", feedback: "Фидбэк" };
              const govCls = { demand: "warning", accepting: "ok", closed: "", feedback: "ok" };
              const gl = govLabels[row.gov_status] || row.gov_status || "Спрос";
              const gc = govCls[row.gov_status] || "";
              s += ` <span class="badge ${gc}" title="Гос. закупка" style="font-size:.72rem">🏛 ${gl}</span>`;
            }
            if (row.condition_accepted && row.condition_accepted !== "any") {
              s += ` <span class="badge" style="font-size:.72rem">${row.condition_accepted === "new" ? "Только новый" : "Б/У ОК"}</span>`;
            }
            return s;
          }},
          { label: "Предложения", render: (row) => {
            const offers = findMarketplaceOffersForProduct(row.product_id);
            if (!offers.length) return `<button class="secondary" style="font-size:.75rem;padding:.2rem .6rem" data-goto-marketplace="${rawNameById("products", row.product_id)}">🔍 Найти</button>`;
            const best = offers.reduce((a, b) => a.unit_price <= b.unit_price ? a : b);
            return `<button class="secondary" style="font-size:.75rem;padding:.2rem .6rem;white-space:nowrap" data-show-pr-offers="${row.product_id}" data-pr-id="${row.id}">📦 ${offers.length} · от ${fmtMoneyKzt(best.unit_price)} тг</button>`;
          }},
          { label: "Создано", render: (row) => dateText(row.created_at) },
          { label: "", render: (row) => {
            let btns = "";
            if (row.status === "draft") {
              btns += `<button class="primary" data-purchase-status="${row.id}" data-purchase-next-status="ordered">Заказано</button>`;
              btns += `<button class="secondary" data-purchase-status="${row.id}" data-purchase-next-status="cancelled">Отменить</button>`;
            }
            if (row.is_gov_procurement && row.gov_status && row.gov_status !== "feedback") {
              const nextLabels = { demand: "→ Приём", accepting: "→ Закрыть", closed: "Добавить фидбэк" };
              const nl = nextLabels[row.gov_status];
              if (nl) btns += `<button class="secondary" style="font-size:.75rem" data-gov-advance="${row.id}" data-gov-status="${row.gov_status}">🏛 ${nl}</button>`;
            }
            return btns ? `<div class="row-actions">${btns}</div>` : "";
          }},
        ], requests, "Заявок пока нет. Нажмите «Сформировать автозаявки» или создайте заявку вручную слева.")}
        <div id="pr-offers-panel" style="display:none;margin-top:12px"></div>
      </div>
      <div class="table-panel span-12">
        <h2>${t("Рекомендации к закупке")}</h2>
        ${table([
          { label: "Товар", render: (row) => `${escapeHtml(row.product_name || rawNameById("products", row.product_id))}<br><span class="badge">${escapeHtml(row.sku || "без кода")}</span>` },
          { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "—" },
          { label: "Количество", key: "quantity" },
          { label: "Основание", key: "reason" },
          { label: "Предложения", render: (row) => {
            const pid = row.product_id;
            const name = row.product_name || rawNameById("products", pid);
            const offers = findMarketplaceOffersForProduct(pid);
            if (offers.length) {
              const best = offers.reduce((a, b) => a.unit_price <= b.unit_price ? a : b);
              return `<button class="secondary" style="font-size:.75rem;padding:.2rem .6rem;white-space:nowrap" data-show-pr-offers="${pid}">📦 ${offers.length} · от ${fmtMoneyKzt(best.unit_price)} тг</button>`;
            }
            return `<button class="secondary" style="font-size:.75rem;padding:.2rem .6rem" data-goto-marketplace="${escapeAttr(name)}">🔍 Найти</button>`;
          }},
        ], filteredRows(suggestions, (row) => [row.product_name, row.sku, rawNameById("warehouses", row.warehouse_id), row.quantity, row.reason]), "Автоматических рекомендаций пока нет. Они появятся после ABC/XYZ анализа и настроенных точек заказа.")}
      </div>
    </div>
  `;
}

function renderInventory() {
  const warehouseUnavailable = state.data.warehouses.length === 0;
  const selectedSession = selectedInventorySession();
  const progress = inventoryProgress(selectedSession);
  const progressTone = selectedSession && progress.missing === 0 && progress.total > 0 ? "ok" : "warn";
  return `
    <div class="grid">
      ${needsWarehouseNotice("Добавить склад")}
      <div class="form-panel span-4"><h2>${t("Создать инвентаризацию")}</h2>${form("inventory-form", [
        { label: "Склад", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
        { label: "Категория", name: "category_id", type: "select", options: optionsFrom("categories", "Все категории") },
        { label: "Ответственные", name: "responsible_ids", placeholder: "manager, nurse-1" },
      ], "Начать", {
        disabledSubmit: warehouseUnavailable,
        submitHint: warehouseUnavailable ? "Сначала добавьте склад." : "",
      })}</div>
      <div class="form-panel span-4"><h2>${t("Завершение")}</h2>${form("inventory-action-form", [
        { label: "Проверка", name: "session_id", type: "select", options: optionsFrom("inventorySessions", "Выберите проверку", (session) => `${rawNameById("warehouses", session.warehouse_id)} · ${humanStatus(session.status)}`), required: true },
      ], "Завершить проверку")}
        <div class="inventory-progress ${progressTone}" data-inventory-progress>${escapeHtml(inventoryProgressText(selectedSession))}</div>
        <div class="actions"><button class="danger" data-action="cancel-inventory">Отменить инвентаризацию</button></div>
      </div>
      <div class="panel span-4 metric"><span>Активная сессия</span><strong>${selectedSession ? `#${selectedSession.id}` : "—"}</strong></div>
      <div class="panel span-12">
        <div class="toolbar">
          <h2>${t("Сводка выбранной проверки")}</h2>
          <div class="row-actions">
            <button class="secondary" data-export-report="inventorySheet" ${selectedSession ? "" : "disabled"}>Выгрузить ведомость CSV</button>
            <button class="secondary" data-print-inventory ${selectedSession ? "" : "disabled"}>Печать ведомости</button>
            <button class="secondary" data-print-inventory-reconciliation ${selectedSession ? "" : "disabled"}>Сличительная ведомость</button>
            <button class="secondary" data-print-inventory-pdf ${selectedSession ? `data-session-id="${escapeAttr(selectedSession.id)}"` : "disabled"}>Скачать PDF</button>
          </div>
        </div>
        ${selectedSession ? inventorySummaryHtml(selectedSession) : '<div class="empty">Выберите или создайте инвентаризацию, чтобы увидеть сводку.</div>'}
      </div>
      <div class="table-panel span-12"><h2>${t("Проверки склада")}</h2>${table([
        { label: "Номер", key: "id" },
        { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
        { label: "Статус", render: (row) => badge(row.status) },
        { label: "Строк", render: (row) => row.lines?.length || 0 },
        { label: "Заполнено", render: (row) => {
          const rowProgress = inventoryProgress(row);
          return `${rowProgress.filled}/${rowProgress.total}`;
        } },
        { label: "Начал", key: "started_by" },
        { label: "Начата", render: (row) => dateText(row.started_at) },
        { label: "Проведена", render: (row) => dateText(row.posted_at) },
      ], filteredRows(state.data.inventorySessions, (row) => [row.id, rawNameById("warehouses", row.warehouse_id), row.status, row.started_by, row.started_at, row.posted_at]), "Проверок склада пока нет. Выберите склад и начните инвентаризацию.")}</div>
      <div class="table-panel span-12"><div class="toolbar"><h2>${t("Товары в выбранной проверке")}</h2>${selectedSession && !!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia) ? `<button class="secondary" type="button" data-action="scan-for-inventory" style="font-size:.8rem">📷 ${t("Найти товар")}</button>` : ""}</div>${selectedSession ? table([
        { label: "Номер строки", key: "id" },
        { label: "Товар", render: (row) => nameById("products", row.product_id) },
        { label: "Партия", render: (row) => batchDetailLabel(row.batch_id) },
        { label: "Ожидалось", key: "expected_quantity" },
        { label: "Факт", render: (row) => `<input class="inline-input" type="number" step="0.001" value="${escapeAttr(row.actual_quantity ?? "")}" data-actual-line="${escapeAttr(row.id)}" />` },
        { label: "Разница", render: (row) => escapeHtml(row.difference_quantity ?? "—") },
        { label: "Готовность", render: (row) => row.actual_quantity === null || row.actual_quantity === undefined || row.actual_quantity === "" ? badge("draft") : badge("ok") },
        { label: "", render: (row) => `<button class="secondary" data-save-inventory-line="${escapeAttr(row.id)}" data-session="${escapeAttr(selectedSession.id)}">Сохранить</button>` },
      ], filteredRows(selectedSession.lines || [], (row) => [row.id, rawNameById("products", row.product_id), batchLabel(row.batch_id), row.expected_quantity, row.actual_quantity, row.difference_quantity]), "В выбранной проверке нет строк. Проверьте, есть ли остатки на складе.") : '<div class="empty">Сессий пока нет. Сначала начните инвентаризацию склада.</div>'}</div>
      <div class="table-panel span-12"><h2>${t("Остатки для сверки")}</h2>${balancesTable(filteredBalances(state.data.balances.items), "Остатков для сверки пока нет. Примите товар на склад перед инвентаризацией.")}</div>
    </div>
  `;
}

function renderNotifications() {
  return `
    <div class="table-panel">
      <div class="toolbar">
        <h2>${t("Уведомления")}</h2>
        <div class="row-actions">
          <button class="secondary" data-action="generate-low-stock">Проверить малые остатки</button>
          <button class="secondary" data-action="generate-expiry">Проверить сроки годности</button>
          <button class="secondary" data-action="generate-quarantine">Проверить карантин</button>
          <button class="secondary" data-action="generate-supplier-contracts">Договоры поставщиков</button>
        </div>
      </div>
      ${table([
        { label: "Номер", key: "id" },
        { label: "Событие", render: (row) => humanNotificationType(row.notification_type) },
        { label: "Партия", render: (row) => row.batch_id ? batchDetailLabel(row.batch_id) : "—" },
        { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "—" },
        { label: "Заголовок", key: "title" },
        { label: "Сообщение", key: "message" },
        { label: "Статус", render: (row) => badge(row.is_read ? "read" : "unread") },
        { label: "", render: (row) => `<button class="secondary" data-read="${row.id}">Прочитано</button>` },
      ], filteredRows(state.data.notifications.items, (row) => [row.id, row.notification_type, batchLabel(row.batch_id), rawNameById("warehouses", row.warehouse_id), row.title, row.message, row.is_read ? "read" : "unread"]))}
    </div>
  `;
}

function abcXyzMatrixData(items) {
  const matrix = {};
  ["A", "B", "C"].forEach((abcClass) => {
    ["X", "Y", "Z"].forEach((xyzClass) => {
      matrix[`${abcClass}${xyzClass}`] = {
        abcClass,
        xyzClass,
        items: [],
        recommended: 0,
        free: 0,
      };
    });
  });
  items.forEach((item) => {
    const key = `${item.abc_class}${item.xyz_class}`;
    if (!matrix[key]) return;
    matrix[key].items.push(item);
    matrix[key].recommended += Number(item.recommended_order_quantity || 0);
    matrix[key].free += Number(item.current_free_quantity || 0);
  });
  return matrix;
}

function abcXyzRecommendation(abcClass, xyzClass) {
  const recommendations = {
    AX: "Критичный стабильный расход: держать страховой запас и контролировать ежедневно.",
    AY: "Критичный переменный расход: проверять сезонность и согласовывать точку заказа.",
    AZ: "Критичный нерегулярный расход: закупать осторожно, проверять потребность перед заказом.",
    BX: "Средний стабильный расход: пополнять по точке заказа.",
    BY: "Средний переменный расход: смотреть динамику и не держать лишний запас.",
    BZ: "Средний нерегулярный расход: заказывать по подтвержденной потребности.",
    CX: "Низкий стабильный расход: поддерживать минимальный запас.",
    CY: "Низкий переменный расход: держать небольшой запас, пересматривать редко.",
    CZ: "Низкий нерегулярный расход: не закупать без заявки отделения.",
  };
  return recommendations[`${abcClass}${xyzClass}`] || "Проверьте расход и остатки перед заказом.";
}

function renderAbcXyzMatrix(items) {
  if (!items.length) return `<div class="empty">Матрица появится после приемки и расхода товаров.</div>`;
  const matrix = abcXyzMatrixData(items);
  return `
    <div class="abc-matrix" role="table" aria-label="Матрица ABC XYZ">
      <div class="abc-matrix-corner">ABC / XYZ</div>
      ${["X", "Y", "Z"].map((xyzClass) => `<div class="abc-matrix-head">XYZ ${xyzClass}</div>`).join("")}
      ${["A", "B", "C"].map((abcClass) => `
        <div class="abc-matrix-head">ABC ${abcClass}</div>
        ${["X", "Y", "Z"].map((xyzClass) => {
          const cell = matrix[`${abcClass}${xyzClass}`];
          const attention = cell.items.filter((item) => Number(item.recommended_order_quantity || 0) > 0).length;
          return `
            <div class="abc-cell ${attention ? "needs-order" : ""}">
              <div class="abc-cell-title">
                <strong>${abcClass}${xyzClass}</strong>
                <span>${escapeHtml(cell.items.length)} поз.</span>
              </div>
              <div class="abc-cell-metrics">
                <span>Свободно: ${escapeHtml(cell.free.toFixed(3))}</span>
                <span>Заказать: ${escapeHtml(cell.recommended.toFixed(3))}</span>
              </div>
              <p>${escapeHtml(abcXyzRecommendation(abcClass, xyzClass))}</p>
            </div>
          `;
        }).join("")}
      `).join("")}
    </div>
  `;
}

function abcXyzScatterPoints(items) {
  const values = items.map((item) => ({
    item,
    consumptionValue: Number(item.consumption_value || 0),
    freeQuantity: Number(item.current_free_quantity || 0),
    recommendedOrder: Number(item.recommended_order_quantity || 0),
  }));
  const maxValue = Math.max(1, ...values.map((point) => point.consumptionValue));
  const maxFree = Math.max(1, ...values.map((point) => point.freeQuantity));
  return values.map((point) => ({
    ...point,
    left: 8 + (point.consumptionValue / maxValue) * 84,
    top: 92 - (point.freeQuantity / maxFree) * 84,
  }));
}

function renderAbcXyzScatter(items) {
  if (!items.length) return `<div class="empty">Карта внимания появится после анализа расхода.</div>`;
  const points = abcXyzScatterPoints(items);
  return `
    <div class="abc-scatter" role="img" aria-label="Карта ABC XYZ по стоимости расхода и свободному остатку">
      <div class="abc-scatter-axis x">Стоимость расхода</div>
      <div class="abc-scatter-axis y">Свободный остаток</div>
      ${points.map((point) => {
        const item = point.item;
        const classes = [
          "abc-scatter-point",
          `abc-${String(item.abc_class || "c").toLowerCase()}`,
          `xyz-${String(item.xyz_class || "z").toLowerCase()}`,
          point.recommendedOrder > 0 ? "needs-order" : "",
        ].filter(Boolean).join(" ");
        const title = `${item.product_name} · ABC ${item.abc_class}/XYZ ${item.xyz_class} · расход ${item.consumption_value} · свободно ${item.current_free_quantity}`;
        return `
          <button
            class="${classes}"
            type="button"
            style="left: ${point.left.toFixed(2)}%; top: ${point.top.toFixed(2)}%;"
            title="${escapeAttr(title)}"
            aria-label="${escapeAttr(title)}"
          >
            <span>${escapeHtml(item.abc_class)}${escapeHtml(item.xyz_class)}</span>
          </button>
        `;
      }).join("")}
    </div>
    <div class="abc-scatter-legend">
      <span><i class="abc-a"></i> A: критично по стоимости</span>
      <span><i class="abc-b"></i> B: средняя важность</span>
      <span><i class="abc-c"></i> C: низкая стоимость</span>
      <span><i class="needs-order"></i> нужен заказ</span>
    </div>
  `;
}

function latestReadingForDevice(deviceId) {
  return state.data.sensorReadings.items.find((reading) => Number(reading.device_id) === Number(deviceId)) || null;
}

function conditionStatusSummary() {
  const readings = state.data.sensorReadings.items || [];
  const latestByDevice = new Map();
  readings.forEach((reading) => {
    if (!latestByDevice.has(reading.device_id)) latestByDevice.set(reading.device_id, reading);
  });
  const latest = [...latestByDevice.values()];
  return {
    devices: state.data.sensorDevices.length,
    readings: readings.length,
    warnings: latest.filter((reading) => reading.status === "warning").length,
    ok: latest.filter((reading) => reading.status === "ok").length,
  };
}

function renderConditionWarningBoard(warnings) {
  if (!warnings.length) return "";
  return `
    <div class="condition-warning-board span-12">
      <div class="toolbar">
        <h2>${t("Нужно проверить условия хранения")}</h2>
        <button class="secondary" data-action="reload">Обновить</button>
      </div>
      <div class="condition-warning-grid">
        ${warnings.slice(0, 5).map((reading) => {
          const details = conditionBreachDetails(reading);
          return `
            <div class="condition-warning-card bad">
              <div>
                <strong>${escapeHtml(reading.device_name || `Датчик #${reading.device_id}`)}</strong>
                <span>${reading.warehouse_name ? escapeHtml(reading.warehouse_name) : nameById("warehouses", reading.warehouse_id)}</span>
              </div>
              <div class="condition-reading">
                <span>${reading.temperature_c === null || reading.temperature_c === undefined ? "—" : `${escapeHtml(reading.temperature_c)} °C`}</span>
                <span>${reading.humidity_percent === null || reading.humidity_percent === undefined ? "—" : `${escapeHtml(reading.humidity_percent)} %`}</span>
                <small>${dateText(reading.recorded_at)}</small>
              </div>
              <ul class="condition-breach-list">
                ${(details.length ? details : ["Показание вне нормы"]).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
              </ul>
              <p class="condition-action">${escapeHtml(conditionActionText(reading))}</p>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  `;
}

function conditionChartPoints(readings, field) {
  const values = readings
    .map((reading) => ({
      reading,
      value: reading[field] === null || reading[field] === undefined ? null : Number(reading[field]),
    }))
    .filter((point) => point.value !== null && !Number.isNaN(point.value));
  if (!values.length) return [];
  const rawMin = Math.min(...values.map((point) => point.value));
  const rawMax = Math.max(...values.map((point) => point.value));
  const min = rawMin === rawMax ? rawMin - 1 : rawMin;
  const max = rawMin === rawMax ? rawMax + 1 : rawMax;
  return values.map((point, index) => ({
    ...point,
    left: values.length === 1 ? 50 : (index / (values.length - 1)) * 100,
    top: 90 - ((point.value - min) / (max - min)) * 80,
  }));
}

function renderConditionChart() {
  const readings = [...(state.data.sensorReadings.items || [])]
    .sort((left, right) => String(left.recorded_at || "").localeCompare(String(right.recorded_at || "")))
    .slice(-20);
  if (!readings.length) return '<div class="empty">График появится после первых показаний датчика.</div>';
  const temperaturePoints = conditionChartPoints(readings, "temperature_c");
  const humidityPoints = conditionChartPoints(readings, "humidity_percent");
  return `
    <div class="condition-chart" role="img" aria-label="График температуры и влажности">
      ${temperaturePoints.map((point) => `
        <span
          class="condition-chart-point temperature"
          style="left: ${point.left.toFixed(2)}%; top: ${point.top.toFixed(2)}%;"
          title="${escapeAttr(`${point.value} °C · ${dateText(point.reading.recorded_at)}`)}"
        ></span>
      `).join("")}
      ${humidityPoints.map((point) => `
        <span
          class="condition-chart-point humidity"
          style="left: ${point.left.toFixed(2)}%; top: ${point.top.toFixed(2)}%;"
          title="${escapeAttr(`${point.value} % · ${dateText(point.reading.recorded_at)}`)}"
        ></span>
      `).join("")}
      <div class="condition-chart-axis x">Последние 20 показаний</div>
      <div class="condition-chart-axis y">Значение</div>
    </div>
    <div class="condition-chart-legend">
      <span><i class="temperature"></i> Температура</span>
      <span><i class="humidity"></i> Влажность</span>
    </div>
  `;
}

function renderConditions() {
  const summary = conditionStatusSummary();
  const warnings = latestConditionWarnings();
  const devices = filteredRows(state.data.sensorDevices, (row) => [
    row.id,
    row.name,
    row.serial_number,
    row.sensor_type,
    rawNameById("warehouses", row.warehouse_id),
  ]);
  const readings = filteredRows(state.data.sensorReadings.items || [], (row) => [
    row.id,
    row.device_name,
    row.warehouse_name,
    row.temperature_c,
    row.humidity_percent,
    row.status,
    row.raw_payload,
    row.recorded_at,
  ]);
  const warehouseUnavailable = state.data.warehouses.length === 0;
  const deviceUnavailable = state.data.sensorDevices.length === 0;
  return `
    <div class="grid">
      ${needsWarehouseNotice("Добавить склад")}
      <div class="panel span-3 metric"><span>Датчики</span><strong>${summary.devices}</strong></div>
      <div class="panel span-3 metric"><span>Показаний</span><strong>${summary.readings}</strong></div>
      <div class="panel span-3 metric"><span>В норме</span><strong>${summary.ok}</strong></div>
      <div class="panel span-3 metric ${summary.warnings ? "condition-alert" : ""}"><span>Требуют внимания</span><strong>${summary.warnings}</strong></div>
      ${renderConditionWarningBoard(warnings)}
      <div class="panel span-12">
        <div class="toolbar">
          <div>
            <h2>${t("График условий хранения")}</h2>
            <span class="helper-text">Последние показания помогают быстро увидеть скачки температуры и влажности.</span>
          </div>
          <button class="secondary" data-action="reload">Обновить</button>
        </div>
        ${renderConditionChart()}
      </div>

      <div class="form-panel span-5">
        <h2>${t("Новый датчик")}</h2>
        ${form("sensor-device-form", [
          { label: "Склад или кабинет", name: "warehouse_id", type: "select", options: optionsFrom("warehouses", "Выберите склад"), required: true },
          { label: "Название", name: "name", value: "Датчик температуры и влажности", required: true },
          { label: "Серийный номер", name: "serial_number", value: "" },
          { label: "Тип", name: "sensor_type", value: "temperature_humidity", required: true },
          { label: "Мин. температура °C", name: "min_temperature_c", type: "number", step: "0.1", value: "2" },
          { label: "Макс. температура °C", name: "max_temperature_c", type: "number", step: "0.1", value: "8" },
          { label: "Мин. влажность %", name: "min_humidity_percent", type: "number", step: "0.1", min: "0", value: "30" },
          { label: "Макс. влажность %", name: "max_humidity_percent", type: "number", step: "0.1", min: "0", value: "70" },
        ], "Добавить датчик", {
          disabledSubmit: warehouseUnavailable,
          submitHint: warehouseUnavailable ? "Сначала добавьте склад или кабинет." : "",
        })}
      </div>

      <div class="form-panel span-7">
        <h2>${t("Внести показание")}</h2>
        ${form("sensor-reading-form", [
          { label: "Датчик", name: "device_id", type: "select", options: optionsFrom("sensorDevices", "Выберите датчик", (device) => `${device.name} · ${rawNameById("warehouses", device.warehouse_id)}`), required: true },
          { label: "Температура °C", name: "temperature_c", type: "number", step: "0.1" },
          { label: "Влажность %", name: "humidity_percent", type: "number", step: "0.1", min: "0" },
          { label: "Источник или заметка", name: "raw_payload", full: true, value: "ручной ввод" },
        ], "Сохранить показание", {
          disabledSubmit: deviceUnavailable,
          submitHint: deviceUnavailable ? "Сначала добавьте датчик слева." : "Заполните температуру или влажность. Система сама сравнит с порогами датчика.",
        })}
      </div>

      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("Датчики хранения")}</h2>
          <button class="secondary" data-action="reload">Обновить</button>
        </div>
        ${table([
          { label: "Номер", key: "id" },
          { label: "Название", key: "name" },
          { label: "Склад", render: (row) => nameById("warehouses", row.warehouse_id) },
          { label: "Порог температуры", render: (row) => `${escapeHtml(row.min_temperature_c ?? "—")} … ${escapeHtml(row.max_temperature_c ?? "—")} °C` },
          { label: "Порог влажности", render: (row) => `${escapeHtml(row.min_humidity_percent ?? "—")} … ${escapeHtml(row.max_humidity_percent ?? "—")} %` },
          { label: "Последнее", render: (row) => {
            const reading = latestReadingForDevice(row.id);
            return reading ? `${escapeHtml(reading.temperature_c ?? "—")} °C · ${escapeHtml(reading.humidity_percent ?? "—")} %` : "—";
          } },
          { label: "Что не так", render: (row) => {
            const reading = latestReadingForDevice(row.id);
            if (!reading) return badge("pending");
            if (reading.status !== "warning") return badge("ok");
            return `<div class="condition-breach-list compact">${conditionBreachDetails(reading).map((item) => `<span>${escapeHtml(item)}</span>`).join("") || "Показание вне нормы"}</div>`;
          } },
        ], devices, "Датчиков пока нет. Добавьте датчик для склада или кабинета.")}
      </div>

      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("Журнал температуры и влажности")}</h2>
          <button class="secondary" data-export-report="sensorReadings">Выгрузить CSV</button>
        </div>
        ${table([
          { label: "Время", render: (row) => dateText(row.recorded_at) },
          { label: "Датчик", render: (row) => escapeHtml(row.device_name || `#${row.device_id}`) },
          { label: "Склад", render: (row) => row.warehouse_name ? escapeHtml(row.warehouse_name) : nameById("warehouses", row.warehouse_id) },
          { label: "Температура", render: (row) => row.temperature_c === null || row.temperature_c === undefined ? "—" : `${escapeHtml(row.temperature_c)} °C` },
          { label: "Влажность", render: (row) => row.humidity_percent === null || row.humidity_percent === undefined ? "—" : `${escapeHtml(row.humidity_percent)} %` },
          { label: "Статус", render: (row) => badge(row.status) },
          { label: "Источник", render: (row) => escapeHtml(row.raw_payload || "—") },
        ], readings, "Показаний пока нет. Внесите первое вручную или запустите мост датчика.")}
      </div>
    </div>
  `;
}

function renderAnalytics() {
  const items = state.data.analytics.items || [];
  const toOrder = items.filter((row) => Number(row.recommended_order_quantity || 0) > 0);
  const important = items.filter((row) => row.abc_class === "A");
  const unstable = items.filter((row) => row.xyz_class === "Z" && Number(row.consumption_quantity || 0) > 0);
  const historyRows = filteredRows(state.data.abcXyzRuns.items || [], (row) => [
    row.id,
    row.warehouse_id,
    row.analysis_days,
    row.period_start,
    row.period_end,
    row.source,
    row.status,
    row.generated_at,
  ]);
  return `
    <div class="grid">
      <div class="panel span-3 metric"><span>Товаров в отчете</span><strong>${items.length}</strong></div>
      <div class="panel span-3 metric"><span>Важные A</span><strong>${important.length}</strong></div>
      <div class="panel span-3 metric"><span>Нужно заказать</span><strong>${toOrder.length}</strong></div>
      <div class="panel span-3 metric"><span>Нестабильный спрос</span><strong>${unstable.length}</strong></div>
      <div class="panel span-12">
        <div class="toolbar">
          <div>
            <h2>${t("Матрица ABC/XYZ")}</h2>
            <span class="helper-text">Матрица показывает важность товара и стабильность расхода. Ячейки с заказом подсвечены.</span>
          </div>
          <button class="primary" data-action="save-abc-xyz-run">Сохранить расчет</button>
          <button class="secondary" data-action="apply-xyz-suggestions" title="Обновить точки заказа на основе XYZ-анализа">Применить XYZ-рекомендации</button>
        </div>
        ${renderAbcXyzMatrix(items)}
      </div>
      <div class="panel span-12">
        <div class="toolbar">
          <div>
            <h2>${t("Карта внимания ABC/XYZ")}</h2>
            <span class="helper-text">Точки справа дают основную стоимость расхода, точки сверху занимают больше свободного остатка.</span>
          </div>
        </div>
        ${renderAbcXyzScatter(items)}
      </div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("ABC/XYZ анализ и заказ")}</h2>
          <div class="row-actions">
            <button class="secondary" data-export-report="analytics">Выгрузить CSV</button>
            <button class="secondary" data-action="reload">Обновить</button>
          </div>
        </div>
        ${table([
          { label: "Товар", render: (row) => `${escapeHtml(row.product_name)}<br><span class="badge">${escapeHtml(row.sku)}</span>` },
          { label: "ABC", render: (row) => analyticsClassBadge(row.abc_class, "abc") },
          { label: "XYZ", render: (row) => analyticsClassBadge(row.xyz_class, "xyz") },
          { label: "Расход", key: "consumption_quantity" },
          { label: "Стоимость расхода", key: "consumption_value" },
          { label: "Свободно", key: "current_free_quantity" },
          { label: "Точка заказа", key: "reorder_point" },
          { label: "Заказать", render: (row) => Number(row.recommended_order_quantity || 0) > 0 ? `<strong>${escapeHtml(row.recommended_order_quantity)}</strong>` : "—" },
          { label: "Рекомендация", key: "recommendation" },
          { label: "Предл. точка заказа", render: (row) => row.suggested_reorder_point && Number(row.suggested_reorder_point) > 0 ? `<span style="color:#2563eb;font-weight:600">${qty(row.suggested_reorder_point)}</span>` : "—" },
        ], filteredRows(items, (row) => [row.product_name, row.sku, row.abc_class, row.xyz_class, row.recommendation, row.recommended_order_quantity]), "Аналитика появится после приемки и расхода товаров.")}
      </div>
      <div class="table-panel span-12">
        <div class="toolbar">
          <h2>${t("История расчетов")}</h2>
          <div class="row-actions">
            <button class="secondary" data-export-report="abcXyzRuns">Выгрузить CSV</button>
            <button class="secondary" data-action="reload">Обновить</button>
          </div>
        </div>
        ${table([
          { label: "Номер", key: "id" },
          { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "Все склады" },
          { label: "Период", render: (row) => `${dateText(row.period_start)} — ${dateText(row.period_end)}` },
          { label: "Дней", key: "analysis_days" },
          { label: "Источник", render: (row) => escapeHtml(row.source === "background" ? "Автоматически" : "Вручную") },
          { label: "Статус", render: (row) => badge(row.status) },
          { label: "Позиций", key: "items_count" },
          { label: "Создан", render: (row) => dateText(row.generated_at) },
        ], historyRows, "Истории расчетов пока нет. Нажмите «Сохранить расчет», чтобы зафиксировать текущий анализ.")}
      </div>
    </div>
  `;
}

function renderAudit() {
  return `
    <div class="table-panel">
      <div class="toolbar"><h2>${t("Журнал действий")}</h2><button class="secondary" data-export-report="audit">${t("Выгрузить CSV")}</button></div>
      ${table([
        { label: "Время", render: (row) => dateText(row.created_at) },
        { label: "Пользователь", key: "actor_id" },
        { label: "Действие", key: "action" },
        { label: "Сущность", render: (row) => `${row.entity_type} #${row.entity_id}` },
        { label: "Склад", render: (row) => row.warehouse_id ? nameById("warehouses", row.warehouse_id) : "—" },
        { label: "IP", render: (row) => escapeHtml(row.ip_address || "—") },
        { label: "Request ID", render: (row) => row.request_id ? `<code style="font-size:.7rem">${escapeHtml(row.request_id.slice(0,12))}…</code>` : "—" },
        { label: "Данные", render: (row) => `<code style="font-size:.7rem;word-break:break-all">${escapeHtml(JSON.stringify(row.payload).slice(0, 120))}${JSON.stringify(row.payload).length > 120 ? "…" : ""}</code>` },
      ], filteredRows(state.data.audit.items, (row) => [row.created_at, row.actor_id, row.action, row.entity_type, row.entity_id, row.warehouse_id, row.ip_address, row.request_id, JSON.stringify(row.payload)]))}
    </div>
  `;
}

function renderUsers() {
  const users = state.data.users || [];
  return `
    <div class="table-panel">
      <div class="toolbar">
        <h2>${t("Пользователи системы")}</h2>
        <button class="primary" data-action="show-create-user">+ Добавить</button>
      </div>
      ${table([
        { label: "#", key: "id" },
        { label: "Логин", key: "username" },
        { label: "Имя", key: "full_name" },
        { label: "Роли", render: (row) => escapeHtml((row.roles || []).join(", ")) },
        { label: "Склады", render: (row) => (row.warehouse_ids && row.warehouse_ids.length ? row.warehouse_ids.join(", ") : "Все") },
        { label: "Отдел", render: (row) => escapeHtml(row.department || "—") },
        { label: "Поставщик", render: (row) => row.supplier_id ? `#${row.supplier_id}` : "—" },
        { label: "Активен", render: (row) => row.is_active ? "✓" : "✗" },
        { label: "Создан", render: (row) => dateText(row.created_at) },
        { label: "", render: (row) => `<button class="secondary" data-action="edit-user" data-user-id="${row.id}">Изменить</button> <button class="secondary danger" data-action="deactivate-user" data-user-id="${row.id}">Деакт.</button>` },
      ], users)}
      <div id="user-form-panel" style="display:none; margin-top:1rem; padding:1rem; border:1px solid #e5e7eb; border-radius:6px; background:#f9fafb">
        <h3 id="user-form-title">Создать пользователя</h3>
        <input type="hidden" id="user-form-id" value="">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem">
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">Логин</label>
            <input id="user-form-username" type="text" placeholder="username" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
          </div>
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">Полное имя</label>
            <input id="user-form-fullname" type="text" placeholder="Иванов Иван" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
          </div>
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">Пароль</label>
            <input id="user-form-password" type="password" placeholder="Пароль (оставьте пустым, чтобы не менять)" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
          </div>
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">Роль</label>
            <select id="user-form-roles" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
              <option value="warehouse_manager">warehouse_manager</option>
              <option value="head_nurse">head_nurse</option>
              <option value="nurse">nurse</option>
              <option value="doctor">doctor</option>
              <option value="other">other</option>
            </select>
          </div>
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">Отдел</label>
            <input id="user-form-department" type="text" placeholder="Необязательно" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
          </div>
          <div>
            <label style="display:block; font-size:.85rem; margin-bottom:.25rem">ID поставщика (для режима «Поставщик»)</label>
            <input id="user-form-supplier-id" type="number" min="1" placeholder="Необязательно" style="width:100%; box-sizing:border-box; padding:.4rem; border:1px solid #ccc; border-radius:4px">
            <span class="helper-text">Если указано — пользователь сможет переключиться в «Режим: Поставщик» с данными этого поставщика.</span>
          </div>
        </div>
        <div style="margin-top:1rem; display:flex; gap:.5rem">
          <button class="primary" data-action="save-user">Сохранить</button>
          <button class="secondary" data-action="cancel-user-form">Отмена</button>
        </div>
        <div id="user-form-error" style="color:red; margin-top:.5rem; font-size:.85rem; display:none"></div>
      </div>
    </div>
    <div class="table-panel" style="margin-top:1rem">
      <div class="toolbar">
        <h2>${t("Модерация отзывов поставщиков")}</h2>
        <button class="secondary" data-action="reload-pending-reviews">Обновить</button>
      </div>
      <div id="pending-reviews-panel">
        ${(state.data.pendingReviews || []).length === 0
          ? '<p style="color:#6b7280;padding:.5rem">Нет отзывов на проверке</p>'
          : (state.data.pendingReviews || []).map(r => `
          <div style="display:flex;align-items:center;gap:.75rem;padding:.6rem;border-bottom:1px solid #e5e7eb;flex-wrap:wrap">
            <span style="color:#f59e0b">${"★".repeat(r.rating)}${"☆".repeat(5-r.rating)}</span>
            <span style="font-size:.85rem"><b>Поставщик #${r.supplier_id}</b> · от ${escapeHtml(r.reviewer_id||"Аноним")} · ${(r.created_at||"").slice(0,10)}</span>
            ${r.comment ? `<span style="font-size:.82rem;color:#374151">"${escapeHtml(r.comment)}"</span>` : ""}
            <button data-action="approve-review" data-review-id="${r.id}" style="padding:.25rem .6rem;background:#16a34a;color:white;border:none;border-radius:4px;cursor:pointer;font-size:.8rem">✓ Одобрить</button>
            <button data-action="reject-review" data-review-id="${r.id}" style="padding:.25rem .6rem;background:#dc2626;color:white;border:none;border-radius:4px;cursor:pointer;font-size:.8rem">✗ Отклонить</button>
          </div>`).join("")
        }
      </div>
    </div>
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>${t("Фоновые задачи")}</h2>
          <span class="helper-text">Выполняются каждый час: просроченные резервы, уведомления, ABC/XYZ снимок</span>
        </div>
        <button class="secondary" data-action="trigger-background-jobs" id="btn-trigger-jobs">Запустить сейчас</button>
      </div>
      ${renderJobStatus()}
    </div>
    ${renderSupplierApplications()}
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>Интеграция с МИС</h2>
          <span class="helper-text">Двусторонняя синхронизация с медицинской информационной системой (mis.qormed.kz). МИС сообщает о завершённой процедуре, sklad сам списывает лекарства по настроенному составу в нужном кабинете.</span>
        </div>
        <button class="secondary" data-action="test-mis-connect" id="btn-test-mis">Проверить соединение</button>
      </div>
      <div id="mis-status-panel" style="padding:.5rem 0;font-size:.85rem;color:#6b7280">Статус не проверялся</div>
      <div style="padding:.5rem 0;font-size:.82rem;color:#6b7280">
        Для настройки на стороне МИС укажите URL вебхука <code>{ваш домен sklad}/api/v1/mis/procedure-event</code>
        и токен из переменной <code>SKLAD_MIS_INBOUND_WEBHOOK_TOKEN</code> на сервере sklad (заголовок <code>Authorization: Bearer &lt;токен&gt;</code>).
        Чтобы кабинет МИС находил свой склад — впишите его ID клиники/кабинета в карточке склада (раздел «Склады»).
      </div>
    </div>
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>Шаблоны расхода по процедурам</h2>
          <span class="helper-text">Что списывается со склада кабинета, когда МИС сообщает о завершении процедуры. Один шаблон на пару (клиника МИС, код процедуры).</span>
        </div>
      </div>
      ${form("procedure-template-form", [
        { label: "ID клиники в МИС", name: "mis_clinic_id", required: true },
        { label: "Код процедуры в МИС", name: "service_code", required: true },
        { label: "Название", name: "name", required: true },
        { label: "Состав (ID товара:количество, по одной позиции на строку)", name: "items_raw", type: "textarea", full: true, required: true },
      ], "Добавить шаблон")}
      ${table([
        { label: "Клиника", render: (row) => escapeHtml(row.mis_clinic_id) },
        { label: "Процедура", render: (row) => escapeHtml(row.service_code) },
        { label: "Название", render: (row) => escapeHtml(row.name) },
        { label: "Состав", render: (row) => escapeHtml((row.items || []).map(i => `${i.product_name || i.product_id} × ${i.quantity}`).join(", ") || "—") },
        { label: "", render: (row) => `<button class="secondary compact-action" type="button" data-delete-procedure-template="${escapeAttr(row.id)}">Удалить</button>` },
      ], state.data.procedureConsumptionTemplates, "Шаблонов пока нет.")}
    </div>
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>Бухгалтерия (1С / webhook)</h2>
          <span class="helper-text">Webhook для передачи приходных и расходных документов в бухгалтерскую систему. Настройте SKLAD_ACCOUNTING_WEBHOOK_URL.</span>
        </div>
        <button class="secondary" data-action="test-accounting" id="btn-test-accounting">Проверить соединение</button>
      </div>
      <div id="accounting-status-panel" style="padding:.5rem 0;font-size:.85rem;color:#6b7280">Статус не проверялся</div>
    </div>
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>ЭДО/ЭЦП (IS-ESF)</h2>
          <span class="helper-text">Интеграция с электронными счетами-фактурами Казахстана. Настройте переменные SKLAD_ESF_USERNAME, SKLAD_ESF_PASSWORD, SKLAD_ESF_SELLER_BIN.</span>
        </div>
        <button class="secondary" data-action="test-esf-connect" id="btn-test-esf">Проверить соединение</button>
      </div>
      <div id="esf-status-panel" style="padding:.5rem 0;font-size:.85rem;color:#6b7280">Статус не проверялся</div>
    </div>
  `;
}

function renderSupplierApplications() {
  const filter = state.ui.supplierApplicationStatusFilter || "pending";
  const apps = pageItems(state.data.supplierApplications);
  const filtered = filter === "all" ? apps : apps.filter((a) => a.status === filter);
  const statusLabels = {
    pending: "На рассмотрении",
    approved: "Одобрена",
    rejected: "Отклонена",
    needs_changes: "Нужны правки",
    suspended: "Приостановлена",
  };
  return `
    <div class="panel" style="margin-top:1rem">
      <div class="toolbar">
        <div>
          <h2>Заявки поставщиков</h2>
          <span class="helper-text">Самостоятельные заявки «Стать поставщиком», отправленные из портала поставщика. После одобрения создаётся поставщик и доступ в портал.</span>
        </div>
        <select id="supplier-application-status-filter" style="padding:.35rem .5rem;border:1px solid var(--line);border-radius:4px">
          ${["pending", "needs_changes", "approved", "rejected", "suspended", "all"].map((value) => `
            <option value="${value}" ${filter === value ? "selected" : ""}>${value === "all" ? "Все" : statusLabels[value]}</option>
          `).join("")}
        </select>
      </div>
      ${table([
        { label: "Компания", render: (row) => escapeHtml(row.name) },
        { label: "БИН", render: (row) => escapeHtml(row.bin || "—") },
        { label: "Email", render: (row) => escapeHtml(row.email) },
        { label: "Телефон", render: (row) => escapeHtml(row.phone || "—") },
        { label: "Город", render: (row) => escapeHtml(row.city || "—") },
        { label: "Статус", render: (row) => {
          const cls = { approved: "ok", rejected: "bad", suspended: "bad", needs_changes: "warn", pending: "warn" }[row.status] || "";
          return `<span class="badge ${cls}">${escapeHtml(statusLabels[row.status] || row.status)}</span>`;
        } },
        { label: "Подана", render: (row) => dateText(row.submitted_at) },
        { label: "Причина решения", render: (row) => escapeHtml((row.review_reason || "").slice(0, 80) || "—") },
        { label: "", render: (row) => ["pending", "needs_changes"].includes(row.status) ? `
          <div class="row-actions">
            <button class="primary" data-supplier-application-review="${escapeAttr(row.id)}" data-supplier-application-next-status="approved">Одобрить</button>
            <button class="secondary" data-supplier-application-review="${escapeAttr(row.id)}" data-supplier-application-next-status="needs_changes">На доработку</button>
            <button class="danger" data-supplier-application-review="${escapeAttr(row.id)}" data-supplier-application-next-status="rejected">Отклонить</button>
          </div>
        ` : (row.status === "approved" ? `<button class="secondary" data-supplier-application-review="${escapeAttr(row.id)}" data-supplier-application-next-status="suspended">Приостановить</button>` : "") },
      ], filtered, "Заявок с таким статусом пока нет.")}
    </div>
  `;
}

function showSupplierApplicationReviewModal(nextStatus, application) {
  const labels = {
    approved: { title: "Одобрить заявку поставщика", confirm: "Одобрить", tone: "primary", reasonRequired: false },
    rejected: { title: "Отклонить заявку поставщика", confirm: "Отклонить", tone: "danger", reasonRequired: true },
    needs_changes: { title: "Вернуть заявку на доработку", confirm: "Отправить на доработку", tone: "primary", reasonRequired: true },
    suspended: { title: "Приостановить поставщика", confirm: "Приостановить", tone: "danger", reasonRequired: true },
  };
  const cfg = labels[nextStatus];
  return new Promise((resolve) => {
    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML = `
      <section class="confirm-modal" role="dialog" aria-modal="true" style="max-width:520px">
        <header><h2>${escapeHtml(cfg.title)}</h2></header>
        <p class="confirm-message">${escapeHtml(application.name)} (${escapeHtml(application.email)})</p>
        <div style="padding:.5rem 0">
          <label style="display:block;font-size:.85rem;margin-bottom:.25rem">Комментарий${cfg.reasonRequired ? ' <span style="color:#dc2626">*</span>' : " (необязательно)"}</label>
          <textarea id="sa-reason" rows="3" style="width:100%;box-sizing:border-box;padding:.4rem;border:1px solid #ccc;border-radius:4px;font-size:.9rem"></textarea>
        </div>
        <footer>
          <button class="secondary" type="button" id="sa-cancel">Отмена</button>
          <button class="${cfg.tone === "danger" ? "danger" : "primary"}" type="button" id="sa-ok">${escapeHtml(cfg.confirm)}</button>
        </footer>
      </section>
    `;
    document.body.appendChild(backdrop);
    const close = (result) => { backdrop.remove(); resolve(result); };
    backdrop.querySelector("#sa-cancel").addEventListener("click", () => close(null));
    backdrop.addEventListener("click", (e) => { if (e.target === backdrop) close(null); });
    backdrop.querySelector("#sa-ok").addEventListener("click", () => {
      const reason = backdrop.querySelector("#sa-reason").value.trim();
      if (cfg.reasonRequired && !reason) {
        backdrop.querySelector("#sa-reason").style.outline = "2px solid red";
        return;
      }
      close({ reason: reason || null });
    });
    backdrop.querySelector("#sa-reason").focus();
  });
}

function showSupplierApprovedNextStepsModal({ email, supplierId }) {
  return new Promise((resolve) => {
    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML = `
      <section class="confirm-modal" role="dialog" aria-modal="true" style="max-width:560px">
        <header><h2>Поставщик одобрен</h2></header>
        <div class="panel" style="background:var(--ok-bg);border-color:var(--ok-border);margin:.5rem 0">
          <strong>Карточка поставщика создана (ID ${escapeHtml(supplierId)}, email ${escapeHtml(email || "—")}).</strong>
          <p style="margin:.5rem 0 0">Доступ выдаётся через tetis1.kz, без пароля:</p>
          <ol style="margin:.4rem 0 0 1.1rem;padding:0">
            <li>Убедитесь, что у поставщика есть аккаунт на tetis1.kz.</li>
            <li>В разделе «Пользователи» этого склада свяжите его пользователя с ID поставщика <strong>${escapeAttr(supplierId)}</strong>.</li>
            <li>Поставщик переключится в «Режим: Поставщик» в верхней панели склада.</li>
          </ol>
        </div>
        <footer><button class="primary" type="button" id="gp-close">Закрыть</button></footer>
      </section>
    `;
    document.body.appendChild(backdrop);
    const close = () => { backdrop.remove(); resolve(); };
    backdrop.querySelector("#gp-close").addEventListener("click", close);
    backdrop.addEventListener("click", (e) => { if (e.target === backdrop) close(); });
  });
}

function renderJobStatus() {
  const js = state.data.jobStatus;
  if (!js) return '<p style="color:#6b7280;padding:.5rem">Нет данных о задачах</p>';
  const last = js.last_result;
  const lastRan = js.last_ran_at ? new Date(js.last_ran_at).toLocaleString("ru-KZ") : "—";
  const statusBadge = (s) => {
    const colors = { done: "#16a34a", running: "#2563eb", failed: "#dc2626", idle: "#6b7280" };
    return `<span style="background:${colors[s]||"#6b7280"};color:white;padding:.1rem .4rem;border-radius:3px;font-size:.75rem">${s}</span>`;
  };
  return `
    <div style="display:flex;gap:2rem;flex-wrap:wrap;padding:.5rem 0;margin-bottom:.75rem">
      <div><span style="color:#6b7280;font-size:.8rem">Статус</span><br>
        ${js.is_running ? statusBadge("running") : statusBadge("idle")}</div>
      <div><span style="color:#6b7280;font-size:.8rem">Последний запуск</span><br>${lastRan}</div>
      ${last ? `
        <div><span style="color:#6b7280;font-size:.8rem">Резервы снято</span><br>${last.expired_reservations}</div>
        <div><span style="color:#6b7280;font-size:.8rem">Уведомления</span><br>${last.low_stock_notifications + last.expiry_notifications}</div>
        <div><span style="color:#6b7280;font-size:.8rem">ABC/XYZ снимков</span><br>${last.abc_xyz_runs}</div>
        ${last.errors && last.errors.length ? `<div style="color:#dc2626"><span style="font-size:.8rem">Ошибки</span><br>${last.errors.join(", ")}</div>` : ""}
      ` : ""}
    </div>
    ${table([
      { label: "#", key: "id" },
      { label: "Статус", render: (r) => statusBadge(r.status) },
      { label: "Начало", render: (r) => new Date(r.started_at).toLocaleString("ru-KZ") },
      { label: "Длит.", render: (r) => r.duration_ms != null ? r.duration_ms + " мс" : "—" },
      { label: "Резервы", render: (r) => r.result_json != null ? r.result_json.expired_reservations : "—" },
      { label: "Увед.", render: (r) => r.result_json != null ? (r.result_json.low_stock_notifications + r.result_json.expiry_notifications) : "—" },
      { label: "Ошибки", render: (r) => r.error_text ? `<span style="color:#dc2626">${escapeHtml(r.error_text.slice(0,60))}</span>` : "—" },
    ], js.history || [])}
  `;
}

function renderMarketplace() {
  const tab = state.ui.marketplaceTab || "catalog";
  const mp = state.data.marketplace || { items: [], total: 0 };
  const categories = state.data.marketplaceCategories || [];
  const filter = state.ui.marketplaceFilter || { search: "", category: "" };
  const suppliers = state.data.marketplaceSuppliers || { items: [], total: 0 };

  const myInquiries = state.data.myInquiries || { items: [], total: 0 };
  const pendingMyCount = (myInquiries.items || []).filter((i) => i.status === "responded").length;
  const cart = state.data.cart || { items: [], total_items: 0, total_amount: 0 };
  const marketplaceItems = [...(mp.items || [])];
  const verifiedCount = marketplaceItems.filter((item) => item.supplier_is_verified).length;
  const bestPrice = marketplaceItems.reduce((min, item) => {
    const price = Number(item.unit_price || 0);
    return price > 0 && (min === null || price < min) ? price : min;
  }, null);
  const fastDeliveryCount = marketplaceItems.filter((item) => Number(item.delivery_days || item.supplier_delivery_days || 99) <= 2).length;

  const tabBar = `
    <div class="marketplace-tabs">
      <button class="${tab === "catalog" ? "active" : "secondary"}" data-mp-tab="catalog">Каталог товаров</button>
      <button class="${tab === "suppliers" ? "active" : "secondary"}" data-mp-tab="suppliers">Поставщики</button>
      <button class="${tab === "cart" ? "active" : "secondary"}" data-mp-tab="cart">Корзина${cart.total_items > 0 ? ` <span class="marketplace-tab-count">${cart.total_items}</span>` : ""}</button>
      <button class="${tab === "my-inquiries" ? "active" : "secondary"}" data-mp-tab="my-inquiries">Мои заказы${pendingMyCount > 0 ? ` <span class="marketplace-tab-count ok">${pendingMyCount}</span>` : ""}</button>
    </div>`;

  if (tab === "suppliers") {
    return tabBar + renderMarketplaceSuppliers(suppliers, filter);
  }
  if (tab === "cart") {
    return tabBar + renderCart(cart);
  }
  if (tab === "my-inquiries") {
    return tabBar + renderMyInquiries(myInquiries.items || []);
  }

  function itemCard(item) {
    const rating = item.supplier_rating != null ? `${"★".repeat(Math.round(item.supplier_rating))}${"☆".repeat(5 - Math.round(item.supplier_rating))}` : "";
    const itemRating = item.avg_rating != null ? `<span class="marketplace-rating">★ ${item.avg_rating} (${item.review_count})</span>` : "";
    const deliveryDays = item.delivery_days || item.supplier_delivery_days;
    const installment = item.unit_price ? Math.ceil(Number(item.unit_price) / 12) : null;
    const isBestPrice = bestPrice != null && Number(item.unit_price) === bestPrice;
    return `
    <div class="panel marketplace-card">
      <div class="marketplace-card-media" data-mp-detail="${item.id}">
        ${item.image_url ? `<img src="${escapeAttr(item.image_url)}" alt="${escapeAttr(item.product_name || "Товар")}" loading="lazy" />` : `<div class="marketplace-card-placeholder">Marqet</div>`}
        <div class="marketplace-card-badges">
          ${isBestPrice ? `<span class="marketplace-pill accent">Лучшая цена</span>` : ""}
          ${item.supplier_is_verified ? `<span class="marketplace-pill ok">Проверен</span>` : ""}
          ${deliveryDays ? `<span class="marketplace-pill">Доставка ${escapeHtml(String(deliveryDays))} дн.</span>` : ""}
        </div>
      </div>
      <div class="marketplace-card-main">
        <div class="marketplace-card-title" data-mp-detail="${item.id}">${escapeHtml(item.product_name)}</div>
        <div class="marketplace-card-meta">
          ${itemRating ? `<div style="margin:2px 0">${itemRating}</div>` : ""}
          ${item.sku ? `<div style="font-size:.78rem;color:var(--muted)">Артикул: ${escapeHtml(item.sku)}</div>` : ""}
          ${item.category ? `<span class="marketplace-pill muted">${escapeHtml(item.category)}</span>` : ""}
        </div>
      </div>
      <div class="marketplace-price-row">
        <div>
          <div class="marketplace-price">${fmtMoneyKzt(item.unit_price)} тг</div>
          <div class="marketplace-unit">за ${escapeHtml(item.unit)}</div>
        </div>
        ${installment ? `<div class="marketplace-installment">≈ ${fmtMoneyKzt(installment)} тг/мес</div>` : ""}
      </div>
      <div class="marketplace-seller-row">
        <div>
          <div class="marketplace-seller-name" data-mp-supplier-profile="${item.supplier_id}">${escapeHtml(item.supplier_name || "")}${item.supplier_is_verified ? ` <span title="Поставщик проверен">✓</span>` : ""}</div>
          <div class="marketplace-seller-meta">${escapeHtml(item.supplier_city || "Казахстан")} ${rating ? `· <span>${rating}</span>` : ""}</div>
        </div>
        <div class="marketplace-stock">
          ${item.stock_qty != null ? `<span>В наличии: <strong>${item.stock_qty}</strong></span>` : ""}
          ${item.min_order_qty > 1 ? `<span>Мин. заказ: <strong>${item.min_order_qty}</strong></span>` : ""}
        </div>
      </div>
      <div class="marketplace-fulfillment">
        ${item.delivery_included ? `<span>Доставка включена</span>` : item.delivery_price ? `<span>Доставка ${fmtMoneyKzt(item.delivery_price)} тг</span>` : `<span>Доставка по договоренности</span>`}
        ${item.condition === "used" ? `<span>Б/У</span>` : item.condition === "refurbished" ? `<span>Восстановлен</span>` : `<span>Новый товар</span>`}
      </div>
      ${item.description ? `<div class="marketplace-card-description">${escapeHtml(item.description)}</div>` : ""}
      <div class="marketplace-card-actions">
        <button class="secondary" data-mp-detail="${item.id}">Подробнее</button>
        <button class="primary" data-mp-cart-add="${item.id}">В корзину</button>
        <button class="primary" data-mp-order="${item.id}" data-supplier-id="${item.supplier_id}">Запросить</button>
        <button class="${(state.ui.compareItems||[]).includes(item.id) ? "primary" : "secondary"}" data-mp-compare="${item.id}">
          ${(state.ui.compareItems||[]).includes(item.id) ? "✓ В сравнении" : "Сравнить"}
        </button>
        ${item.supplier_phone ? `<a href="tel:${escapeAttr(item.supplier_phone)}" class="secondary marketplace-phone-link">Позвонить</a>` : ""}
      </div>
    </div>`;
  }

  const sortVal = filter.sort || "";
  return tabBar + `
    <section class="marketplace-hero">
      <div>
        <p class="eyebrow">marqet.kz marketplace</p>
        <h2>Покупайте у проверенных поставщиков для qpartner и прямых заказов</h2>
        <p>Поиск, сравнение цен, корзина, заявки поставщикам и прозрачные условия доставки в одном рабочем экране.</p>
      </div>
      <div class="marketplace-hero-stats">
        <div><span>Позиций</span><strong>${mp.total || marketplaceItems.length}</strong></div>
        <div><span>Проверенных</span><strong>${verifiedCount}</strong></div>
        <div><span>Быстрая доставка</span><strong>${fastDeliveryCount}</strong></div>
        <div><span>От</span><strong>${bestPrice ? `${fmtMoneyKzt(bestPrice)} тг` : "—"}</strong></div>
      </div>
    </section>
    <div class="marketplace-trust-strip" aria-label="Преимущества marketplace">
      <span>Оплата по счету и условиям договора</span>
      <span>Рассрочка/кредитный сценарий готов к подключению</span>
      <span>Поставщики, отзывы и статусы заявок</span>
      <span>Интеграция с qpartner складом</span>
    </div>
    <div class="marketplace-searchbar">
      <input type="text" id="mp-search" placeholder="Поиск по названию, артикулу, поставщику..." value="${escapeAttr(filter.search)}" />
      <select id="mp-category">
        <option value="">Все категории</option>
        ${(state.data.catalogTaxonomy||[]).length
          ? (state.data.catalogTaxonomy||[]).map((c) => `<option value="${escapeAttr(c.name)}" ${filter.category === c.name ? "selected" : ""}>${c.icon || ""} ${escapeHtml(c.name)}</option>`).join("")
          : categories.map((c) => `<option value="${escapeAttr(c)}" ${filter.category === c ? "selected" : ""}>${escapeHtml(c)}</option>`).join("")}
      </select>
      <select id="mp-sort">
        <option value="">По умолчанию</option>
        <option value="price_asc" ${sortVal === "price_asc" ? "selected" : ""}>Цена ↑</option>
        <option value="price_desc" ${sortVal === "price_desc" ? "selected" : ""}>Цена ↓</option>
        <option value="delivery_asc" ${sortVal === "delivery_asc" ? "selected" : ""}>Быстрее доставка</option>
        <option value="name_asc" ${sortVal === "name_asc" ? "selected" : ""}>По названию</option>
      </select>
      <button class="primary" id="mp-search-btn">Найти</button>
    </div>
    <div class="marketplace-results-row">
      <div style="color:var(--muted);font-size:.85rem">Найдено позиций: ${mp.total}</div>
      ${filter.search ? `<button class="secondary" style="font-size:.82rem" id="mp-bulk-inquire-btn" title="Отправить запрос всем поставщикам у которых есть этот товар">📤 Запросить у всех поставщиков</button>` : ""}
    </div>
    ${(state.data.catalogTaxonomy||[]).length ? `
      <div class="marketplace-category-rail">
        <button class="${!filter.category ? 'active' : 'secondary'}" data-mp-cat="">Все</button>
        ${(state.data.catalogTaxonomy||[]).map((c) => `<button class="${filter.category === c.name ? 'active' : 'secondary'}" data-mp-cat="${escapeAttr(c.name)}">${c.icon||""} ${escapeHtml(c.name)}</button>`).join("")}
      </div>` : ""}
    <div class="marketplace-grid">
      ${mp.items.length ? mp.items.map(itemCard).join("") : `
        <div style="grid-column:1/-1;text-align:center;padding:40px 16px;color:var(--muted)">
          <div style="font-size:2.5rem;margin-bottom:8px">🛒</div>
          <div>Ничего не найдено.<br>Попробуйте изменить запрос.</div>
        </div>`}
    </div>
    ${mp.total > mp.items.length ? `
      <div style="text-align:center;margin-top:16px">
        <button class="secondary" id="mp-load-more" data-offset="${mp.items.length}">
          Загрузить ещё (показано ${mp.items.length} из ${mp.total})
        </button>
      </div>` : ""}
    ${(state.ui.compareItems||[]).length >= 2 ? `
      <div style="position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:var(--accent,#2563eb);color:#fff;border-radius:12px;padding:10px 20px;box-shadow:0 4px 20px rgba(0,0,0,.3);display:flex;align-items:center;gap:12px;z-index:1000;max-width:90vw">
        <span style="font-weight:600">Сравниваем: ${(state.ui.compareItems||[]).length} позиции</span>
        <button id="mp-compare-now-btn" style="background:#fff;color:var(--accent,#2563eb);border:none;border-radius:8px;padding:6px 16px;font-weight:700;cursor:pointer">Сравнить →</button>
        <button id="mp-compare-clear-btn" style="background:rgba(255,255,255,.2);color:#fff;border:none;border-radius:8px;padding:6px 10px;cursor:pointer">✕</button>
      </div>` : ""}`;
}

async function showCompareModal() {
  const ids = state.ui.compareItems || [];
  if (ids.length < 2) return;
  const existing = document.getElementById("compare-modal-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "compare-modal-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:flex-start;justify-content:center;padding:20px;overflow-y:auto";
  overlay.innerHTML = `<div style="background:var(--surface,#fff);border-radius:12px;padding:24px;width:100%;max-width:900px;box-shadow:0 8px 40px rgba(0,0,0,.25)">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h3 style="margin:0">Сравнение предложений</h3>
      <button id="compare-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted)">&times;</button>
    </div>
    <div id="compare-body" style="overflow-x:auto"><div style="color:var(--muted);text-align:center;padding:24px">Загрузка...</div></div>
  </div>`;
  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("compare-close")?.addEventListener("click", () => overlay.remove());
  try {
    const items = await request(`/marketplace/compare?ids=${ids.join(",")}`);
    const fields = [
      ["Поставщик", (i) => escapeHtml(i.supplier_name || "—")],
      ["Город", (i) => escapeHtml(i.supplier_city || "—")],
      ["Рейтинг", (i) => i.supplier_rating != null ? `${i.supplier_rating} ★` : "—"],
      ["Цена", (i) => `<strong style="color:var(--accent)">${fmtMoneyKzt(i.unit_price)} тг</strong>/<span style="font-size:.8rem">${escapeHtml(i.unit)}</span>`],
      ["Мин. заказ", (i) => i.min_order_qty > 1 ? i.min_order_qty : "1"],
      ["В наличии", (i) => i.stock_qty != null ? `${i.stock_qty} ${escapeHtml(i.unit)}` : "—"],
      ["Доставка", (i) => (i.delivery_days || i.supplier_delivery_days) ? `${i.delivery_days || i.supplier_delivery_days} дн.` : "—"],
      ["Описание", (i) => escapeHtml(i.description || "—")],
    ];
    const minPrice = Math.min(...items.map((i) => Number(i.unit_price)));
    const html = `
      <table style="width:100%;border-collapse:collapse;font-size:.88rem;min-width:${items.length * 200}px">
        <thead>
          <tr>
            <th style="text-align:left;padding:8px;border-bottom:2px solid var(--line);width:130px;color:var(--muted);font-weight:500">Параметр</th>
            ${items.map((i) => `<th style="padding:8px;border-bottom:2px solid var(--line);text-align:center">
              <div style="font-weight:700">${escapeHtml(i.product_name)}</div>
              ${Number(i.unit_price) === minPrice ? `<div style="font-size:.72rem;background:#16a34a;color:#fff;border-radius:4px;padding:1px 6px;display:inline-block;margin-top:2px">Лучшая цена</div>` : ""}
            </th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${fields.map(([label, fn], rowIdx) => `
            <tr style="background:${rowIdx % 2 ? "var(--surface-2,#f9f9f9)" : "transparent"}">
              <td style="padding:8px;color:var(--muted);font-weight:500">${label}</td>
              ${items.map((i) => `<td style="padding:8px;text-align:center">${fn(i)}</td>`).join("")}
            </tr>`).join("")}
          <tr>
            <td style="padding:8px"></td>
            ${items.map((i) => `<td style="padding:8px;text-align:center">
              <button class="primary" style="font-size:.82rem;width:100%" data-mp-order="${i.id}">Запросить</button>
            </td>`).join("")}
          </tr>
        </tbody>
      </table>`;
    document.getElementById("compare-body").innerHTML = html;
    document.getElementById("compare-body").querySelectorAll("[data-mp-order]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = items.find((i) => String(i.id) === String(btn.dataset.mpOrder));
        if (item) { overlay.remove(); showInquiryModal(item); }
      });
    });
  } catch (err) {
    document.getElementById("compare-body").innerHTML = `<div style="color:var(--danger);padding:16px">${escapeHtml(err.message || "Ошибка загрузки")}</div>`;
  }
}

function renderMarketplaceSuppliers(suppliers, filter) {
  const items = suppliers.items || [];
  const supplierSearch = filter.supplierSearch || "";
  return `
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;align-items:center">
      <input type="text" id="mp-supplier-search" placeholder="Поиск по названию или контакту..." value="${escapeAttr(supplierSearch)}" style="flex:1;min-width:160px" />
      <button class="primary" id="mp-supplier-search-btn">Найти</button>
      ${supplierSearch ? `<button class="secondary" id="mp-supplier-search-reset">Сбросить</button>` : ""}
    </div>
    <div style="color:var(--muted);font-size:.85rem;margin-bottom:10px">Поставщиков: ${suppliers.total || 0}${supplierSearch ? ` · поиск: ${escapeHtml(supplierSearch)}` : ""}</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px">
      ${items.length ? items.map((s) => {
        const rating = s.rating != null ? Number(s.rating).toFixed(1) : "—";
        const cats = Array.isArray(s.categories) ? s.categories.filter(Boolean).slice(0, 3) : [];
        return `
        <div class="panel" style="display:flex;flex-direction:column;gap:8px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <strong style="font-size:1rem">${escapeHtml(s.name || "")}</strong>
              ${s.is_preferred ? `<span style="font-size:.75rem;color:var(--success,#16a34a);margin-left:6px">⭐ Предпочтительный</span>` : ""}
              <div style="font-size:.82rem;color:var(--muted)">${escapeHtml(s.city || "")}${s.delivery_days ? ` · доставка ${s.delivery_days} дн.` : ""}</div>
            </div>
            ${s.rating != null ? `<div style="text-align:center;background:var(--surface-2,#f5f5f5);padding:4px 8px;border-radius:8px"><div style="font-size:1rem;font-weight:700;color:var(--accent)">${rating}</div><div style="font-size:.7rem;color:var(--muted)">★</div></div>` : ""}
          </div>
          ${cats.length ? `<div style="display:flex;flex-wrap:wrap;gap:4px">${cats.map((c) => `<span style="font-size:.75rem;background:var(--surface-2,#eef);padding:2px 8px;border-radius:10px;color:var(--accent)">${escapeHtml(c)}</span>`).join("")}</div>` : ""}
          <div style="font-size:.85rem;color:var(--muted);display:flex;gap:12px">
            ${s.catalog_items_count ? `<span>🛍️ ${s.catalog_items_count} тов.</span>` : ""}
            ${s.phone ? `<a href="tel:${escapeAttr(s.phone)}" style="color:var(--accent)">📞 ${escapeHtml(s.phone)}</a>` : ""}
          </div>
          ${s.min_price != null ? `<div style="font-size:.82rem;color:var(--muted)">Цены: от ${fmtMoneyKzt(s.min_price)} до ${fmtMoneyKzt(s.max_price)} тг</div>` : ""}
          <button class="secondary" style="font-size:.82rem;margin-top:auto" data-mp-supplier-catalog="${s.id}">Посмотреть каталог →</button>
        </div>`;
      }).join("") : `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--muted)">
        <div style="font-size:2.5rem;margin-bottom:8px">🏢</div>
        <div>Поставщиков не найдено</div>
      </div>`}
    </div>`;
}

function renderCart(cart) {
  const items = cart.items || [];
  const hasInactiveItems = cartHasInactiveItems(items);
  if (!items.length) return `
    <div class="panel" style="text-align:center;padding:40px 16px">
      <div style="font-size:2.5rem;margin-bottom:8px">🛒</div>
      <div style="color:var(--muted)">Корзина пуста.<br>Добавьте товары из каталога.</div>
      <button class="primary" style="margin-top:16px" data-mp-tab="catalog">Перейти в каталог</button>
    </div>`;
  return `
    ${items.map((it) => `
      <div class="panel" style="display:flex;gap:12px;align-items:center;margin-bottom:10px;flex-wrap:wrap" id="cart-item-${it.id}">
        ${it.image_url ? `<img src="${escapeAttr(it.image_url)}" alt="" style="width:64px;height:64px;object-fit:cover;border-radius:6px" />` : `<div style="width:64px;height:64px;border-radius:6px;background:var(--surface-2,#f0f0f0);display:flex;align-items:center;justify-content:center;font-size:1.5rem">🛍️</div>`}
        <div style="flex:1;min-width:160px">
          <div style="font-weight:600">${escapeHtml(it.product_name)}</div>
          <div style="font-size:.82rem;color:var(--muted)">${escapeHtml(it.supplier_name || "")} · ${fmtMoneyKzt(it.unit_price)} тг/${escapeHtml(it.unit)}</div>
          ${!it.is_active ? `<div style="font-size:.78rem;color:var(--danger,#dc2626)">Товар больше не активен</div>` : ""}
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <input type="number" min="${it.min_order_qty || 1}" step="1" value="${it.quantity}" data-cart-qty="${it.id}" style="width:80px" />
        </div>
        <div style="font-weight:700;color:var(--accent);min-width:110px;text-align:right">${fmtMoneyKzt(Number(it.unit_price) * Number(it.quantity))} тг</div>
        <button class="secondary" style="font-size:.82rem" data-cart-remove="${it.id}">✕</button>
      </div>`).join("")}
    ${hasInactiveItems ? `<div class="panel" style="border-color:var(--danger,#dc2626);color:var(--danger,#dc2626);font-size:.88rem;margin-bottom:10px">Удалите неактивные товары из корзины перед оформлением заказа.</div>` : ""}
    <div class="panel" style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
      <div style="font-size:1.05rem">Итого (${cart.total_items} поз.): <strong style="color:var(--accent)">${fmtMoneyKzt(cart.total_amount)} тг</strong></div>
      <button class="primary" id="cart-checkout-btn" ${hasInactiveItems ? `disabled title="Удалите неактивные товары из корзины"` : ""}>Оформить заказ →</button>
    </div>`;
}

function renderSupplierMap() {
  const suppliers = state.data.supplierMap || [];
  const shipments = state.data.shipments?.items || [];

  const statusLabels = { in_transit: "В пути", delivered: "Доставлено", delayed: "Задержка", cancelled: "Отменено" };
  const statusColors = { in_transit: "var(--accent-2)", delivered: "var(--ok)", delayed: "var(--danger)", cancelled: "var(--muted)" };

  return `
<div style="padding:1rem">
  <h2 style="margin:0 0 1rem">Карта поставщиков и логистика</h2>
  <div style="display:grid; grid-template-columns:1fr 340px; gap:1rem; height:600px">
    <div id="supplier-leaflet-map" style="border-radius:8px; overflow:hidden; border:1px solid var(--line)"></div>
    <div style="overflow-y:auto; display:flex; flex-direction:column; gap:.75rem">
      <div style="font-weight:600; font-size:.9rem; color:var(--text)">Активные поставки (${shipments.filter(s=>s.status==='in_transit').length})</div>
      ${shipments.length === 0 ? '<div style="color:var(--muted);font-size:.85rem">Нет активных поставок</div>' : ''}
      ${shipments.map(s => `
        <div class="panel" style="padding:.75rem;font-size:.82rem;box-shadow:none">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.4rem">
            <span style="font-weight:600">${s.reference || 'Поставка #' + s.id}</span>
            <span style="background:${statusColors[s.status]||'var(--muted)'};color:white;padding:2px 8px;border-radius:10px;font-size:.75rem">${statusLabels[s.status]||s.status}</span>
          </div>
          <div style="color:var(--muted)">От: ${s.origin_city || '—'}</div>
          ${s.current_city ? `<div style="color:var(--text)">Сейчас: ${s.current_city}</div>` : ''}
          ${s.estimated_arrival ? `<div style="color:var(--text)">Ожидается: ${s.estimated_arrival}</div>` : ''}
          ${s.notes ? `<div style="color:var(--muted);margin-top:.25rem">${escapeHtml(s.notes)}</div>` : ''}
          <div style="margin-top:.5rem;display:flex;gap:.5rem">
            <select data-shipment-id="${s.id}" data-action="update-shipment-status" style="width:auto;font-size:.78rem;padding:2px 4px">
              <option value="">Изменить статус...</option>
              <option value="in_transit">В пути</option>
              <option value="delivered">Доставлено</option>
              <option value="delayed">Задержка</option>
              <option value="cancelled">Отменено</option>
            </select>
          </div>
        </div>
      `).join('')}
      <div style="margin-top:.5rem">
        <button class="primary" data-action="new-shipment" style="width:100%;font-size:.85rem">+ Новая поставка</button>
      </div>
      <div id="new-shipment-form" class="panel" style="display:none;padding:.75rem;font-size:.82rem;box-shadow:none">
        <div style="font-weight:600;margin-bottom:.5rem">Новая поставка</div>
        <select id="ns-supplier" style="margin-bottom:.4rem;font-size:.82rem">
          <option value="">Поставщик...</option>
          ${state.data.suppliers.map(s=>`<option value="${s.id}">${escapeHtml(s.name)}</option>`).join('')}
        </select>
        <input id="ns-ref" placeholder="Номер заказа" style="margin-bottom:.4rem;font-size:.82rem">
        <input id="ns-origin" placeholder="Город отправки" style="margin-bottom:.4rem;font-size:.82rem">
        <input id="ns-eta" type="date" style="margin-bottom:.4rem;font-size:.82rem">
        <textarea id="ns-notes" placeholder="Примечание" rows="2" style="margin-bottom:.5rem;font-size:.82rem;resize:none"></textarea>
        <div style="display:flex;gap:.5rem">
          <button class="primary" data-action="save-shipment" style="flex:1">Сохранить</button>
          <button class="secondary" data-action="cancel-shipment" style="flex:1">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</div>`;
}

const SHIPMENT_STATUS_LABELS = { planned: "Готовится", in_transit: "В пути", delivered: "Доставлено", delayed: "Задержка", cancelled: "Отменено" };

function orderTrackingSteps(inq) {
  const po = inq.purchase_order;
  const shipment = inq.shipment;
  const delivered = shipment && shipment.status === "delivered";
  const steps = [
    { label: "Запрос отправлен", done: true },
    { label: "Ответ поставщика", done: !!inq.responded_at },
    { label: "Заказ оформлен", done: !!po || inq.status === "ordered" },
    { label: "Поставка", done: !!shipment, note: shipment ? (SHIPMENT_STATUS_LABELS[shipment.status] || shipment.status) : null },
    { label: "Получено", done: delivered || inq.status === "closed" },
  ];
  return `
    <div style="display:flex;align-items:center;flex-wrap:wrap;gap:2px;margin:8px 0;font-size:.78rem">
      ${steps.map((s, i) => `
        <span style="display:flex;align-items:center;gap:4px;color:${s.done ? "var(--success,#16a34a)" : "var(--muted)"}">
          <span style="width:16px;height:16px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:${s.done ? "var(--success,#16a34a)" : "var(--surface-2,#e5e5e5)"};color:#fff;font-size:.65rem">${s.done ? "✓" : i + 1}</span>
          ${s.label}${s.note ? ` (${escapeHtml(s.note)})` : ""}
        </span>
        ${i < steps.length - 1 ? `<span style="width:14px;height:1px;background:var(--line,#ddd)"></span>` : ""}
      `).join("")}
    </div>
    ${shipment && shipment.estimated_arrival ? `<div style="font-size:.78rem;color:var(--muted);margin-bottom:4px">Ожидаемое прибытие: ${escapeHtml(String(shipment.estimated_arrival))}${shipment.current_city ? ` · сейчас в ${escapeHtml(shipment.current_city)}` : ""}</div>` : ""}
    ${po ? `<div style="font-size:.78rem;color:var(--muted);margin-bottom:4px">Заказ ${escapeHtml(po.po_number || "")} · статус: ${escapeHtml(po.status)}</div>` : ""}
  `;
}

function marketplaceInquirySourceMeta(source) {
  const key = source || "marqet";
  return {
    marqet: { label: "marqet.kz", hint: "Публичный маркетплейс", color: "var(--accent,#2563eb)" },
    qpartner: { label: "qpartner", hint: "Складской маркетплейс", color: "var(--success,#16a34a)" },
    api: { label: "API", hint: "Интеграция", color: "var(--muted,#64748b)" },
  }[key] || { label: key, hint: "Источник заявки", color: "var(--muted,#64748b)" };
}

function marketplaceInquirySourceBadge(source) {
  const meta = marketplaceInquirySourceMeta(source);
  return `<span title="${escapeAttr(meta.hint)}" style="display:inline-flex;align-items:center;border:1px solid ${meta.color};color:${meta.color};border-radius:999px;padding:1px 7px;font-size:.72rem;font-weight:600;line-height:1.4;white-space:nowrap">${escapeHtml(meta.label)}</span>`;
}

function marketplaceInquirySourceQuery(source) {
  return source && source !== "all" ? `&source=${encodeURIComponent(source)}` : "";
}

function marketplaceInquiryStatusQuery(status) {
  return status && status !== "all" ? `&status=${encodeURIComponent(status)}` : "";
}

function marketplaceInquiryStatusMeta(status) {
  return {
    pending: "Ожидает ответа",
    responded: "Получен ответ",
    ordered: "Заказано",
    closed: "Закрыт",
  }[status] || status;
}

function marketplaceInquirySourceFilter(value, id) {
  const options = [
    ["all", "Все источники"],
    ["marqet", "marqet.kz"],
    ["qpartner", "qpartner"],
    ["api", "API"],
  ];
  return `
    <label style="display:inline-flex;align-items:center;gap:6px;font-size:.84rem;color:var(--muted);margin-bottom:10px">
      Источник
      <select id="${escapeAttr(id)}" style="padding:4px 8px;border:1px solid var(--line,#ddd);border-radius:6px;background:var(--surface,#fff);font-size:.84rem">
        ${options.map(([key, label]) => `<option value="${key}" ${value === key ? "selected" : ""}>${label}</option>`).join("")}
      </select>
    </label>`;
}

function marketplaceInquiryStatusFilter(value, id) {
  const options = [
    ["all", "Все статусы"],
    ["pending", "Ожидает ответа"],
    ["responded", "Получен ответ"],
    ["ordered", "Заказано"],
    ["closed", "Закрыт"],
  ];
  return `
    <label style="display:inline-flex;align-items:center;gap:6px;font-size:.84rem;color:var(--muted);margin-bottom:10px">
      Статус
      <select id="${escapeAttr(id)}" style="padding:4px 8px;border:1px solid var(--line,#ddd);border-radius:6px;background:var(--surface,#fff);font-size:.84rem">
        ${options.map(([key, label]) => `<option value="${key}" ${value === key ? "selected" : ""}>${label}</option>`).join("")}
      </select>
    </label>`;
}

function marketplaceInquiryFiltersActive(sourceValue, statusValue) {
  return (sourceValue && sourceValue !== "all") || (statusValue && statusValue !== "all");
}

function marketplaceInquiryFilterSummary(sourceValue, statusValue) {
  const parts = [];
  if (sourceValue && sourceValue !== "all") parts.push(`Источник: ${marketplaceInquirySourceMeta(sourceValue).label}`);
  if (statusValue && statusValue !== "all") parts.push(`Статус: ${marketplaceInquiryStatusMeta(statusValue)}`);
  return parts.join(" · ");
}

function marketplaceInquiryFilterBar(sourceValue, sourceId, statusValue, statusId, resetId) {
  const hasActiveFilters = marketplaceInquiryFiltersActive(sourceValue, statusValue);
  const summary = marketplaceInquiryFilterSummary(sourceValue, statusValue);
  return `<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
    ${marketplaceInquirySourceFilter(sourceValue, sourceId)}
    ${marketplaceInquiryStatusFilter(statusValue, statusId)}
    ${hasActiveFilters && resetId ? `<button class="secondary" id="${escapeAttr(resetId)}" style="font-size:.82rem;margin-bottom:10px">Сбросить фильтры</button>` : ""}
    ${summary ? `<span style="font-size:.82rem;color:var(--muted);margin-bottom:10px">${escapeHtml(summary)}</span>` : ""}
  </div>`;
}

function myInquiriesPath() {
  return `/marketplace/my-inquiries?limit=50${marketplaceInquirySourceQuery(state.ui.marketplaceInquirySourceFilter || "all")}${marketplaceInquiryStatusQuery(state.ui.marketplaceInquiryStatusFilter || "all")}`;
}

function supplierInquiriesPath() {
  return `/supplier/inquiries?limit=50${marketplaceInquirySourceQuery(state.ui.supplierInquirySourceFilter || "all")}${marketplaceInquiryStatusQuery(state.ui.supplierInquiryStatusFilter || "all")}`;
}

function focusQpartnerPendingInquiries() {
  state.ui.marketplaceInquirySourceFilter = "qpartner";
  state.ui.marketplaceInquiryStatusFilter = "pending";
}

function marketplaceCreatedInquiryCount(created) {
  if (Array.isArray(created)) return created.length;
  if (created && Array.isArray(created.items)) return created.items.length;
  if (created && Number.isFinite(Number(created.total))) return Number(created.total);
  return 0;
}

function cartHasInactiveItems(items) {
  return (items || []).some((item) => item.is_active === false);
}

function renderMyInquiries(items) {
  const STATUS = {
    pending: { label: "Ожидает ответа", cls: "warning" },
    responded: { label: "Получен ответ", cls: "ok" },
    ordered: { label: "Заказано", cls: "ok" },
    closed: { label: "Закрыт", cls: "" },
  };
  const sourceFilter = state.ui.marketplaceInquirySourceFilter || "all";
  const statusFilter = state.ui.marketplaceInquiryStatusFilter || "all";
  const hasActiveFilters = marketplaceInquiryFiltersActive(sourceFilter, statusFilter);
  const filterBar = marketplaceInquiryFilterBar(sourceFilter, "mp-inquiry-source-filter", statusFilter, "mp-inquiry-status-filter", "mp-inquiry-filter-reset");
  if (!items.length) return `
    ${filterBar}
    <div class="panel" style="text-align:center;padding:40px 16px">
      <div style="font-size:2.5rem;margin-bottom:8px">📋</div>
      <div style="color:var(--muted)">${hasActiveFilters ? "По выбранным фильтрам заявок нет.<br>Сбросьте фильтры или выберите другой источник/статус." : "Вы ещё не отправляли запросы поставщикам.<br>Найдите нужный товар в каталоге и нажмите «Запросить»."}</div>
      ${hasActiveFilters ? `<button class="secondary" style="margin-top:16px" id="mp-inquiry-empty-reset">Сбросить фильтры</button>` : `<button class="primary" style="margin-top:16px" data-mp-tab="catalog">Перейти в каталог</button>`}
    </div>`;
  return filterBar + items.map((inq) => {
    const st = STATUS[inq.status] || { label: inq.status, cls: "" };
    const totalPrice = inq.unit_price ? (inq.quantity * inq.unit_price).toFixed(2) : null;
    return `
    <div class="panel" style="margin-bottom:12px" id="my-inquiry-${inq.id}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:8px">
        <div>
          <strong style="font-size:1rem">${escapeHtml(inq.product_name || "")}</strong>
          ${inq.sku ? `<span style="font-size:.78rem;color:var(--muted);margin-left:6px">(${escapeHtml(inq.sku)})</span>` : ""}
          <div style="font-size:.82rem;color:var(--muted);margin-top:2px">
            Поставщик: <strong>${escapeHtml(inq.supplier_name || "—")}</strong>
            ${inq.supplier_phone ? ` · <a href="tel:${escapeAttr(inq.supplier_phone)}" style="color:var(--accent)">${escapeHtml(inq.supplier_phone)}</a>` : ""}
            ${inq.supplier_email ? ` · ${escapeHtml(inq.supplier_email)}` : ""}
          </div>
          <div style="font-size:.78rem;color:var(--muted)">Запрос от ${String(inq.created_at || "").slice(0, 10)}</div>
        </div>
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;justify-content:flex-end">
          ${marketplaceInquirySourceBadge(inq.source)}
          <span class="badge ${st.cls}" style="white-space:nowrap">${st.label}</span>
        </div>
      </div>
      ${orderTrackingSteps(inq)}
      <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:.88rem;margin-bottom:8px">
        <div>Кол-во: <strong>${inq.quantity} ${escapeHtml(inq.unit || "")}</strong></div>
        ${inq.unit_price ? `<div>Цена: <strong>${fmtMoneyKzt(inq.unit_price)} тг/${escapeHtml(inq.unit || "")}</strong></div>` : ""}
        ${totalPrice ? `<div>Итого: <strong>${fmtMoneyKzt(totalPrice)} тг</strong></div>` : ""}
      </div>
      ${inq.notes ? `<div style="background:var(--surface-2,#f5f5f5);padding:6px 10px;border-radius:6px;font-size:.85rem;margin-bottom:8px;color:var(--muted)">Ваш комментарий: ${escapeHtml(inq.notes)}</div>` : ""}
      ${inq.supplier_response ? `
        <div style="background:var(--surface-2,#f0fff4);border-left:3px solid var(--success,#16a34a);padding:8px 12px;border-radius:0 6px 6px 0;font-size:.88rem;margin-bottom:8px">
          <strong>Ответ поставщика:</strong> ${escapeHtml(inq.supplier_response)}
          ${inq.responded_at ? `<div style="font-size:.75rem;color:var(--muted);margin-top:2px">${String(inq.responded_at).slice(0, 16).replace("T", " ")}</div>` : ""}
        </div>` : ""}
      ${inq.status === "responded" ? `
        <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap">
          <button class="secondary" style="font-size:.82rem" data-inquiry-chat="${inq.id}" data-chat-role="buyer">💬 Переписка</button>
          <button class="primary" style="font-size:.82rem" data-create-po="${inq.id}" data-inquiry-json='${JSON.stringify({product_name:inq.product_name,supplier_name:inq.supplier_name,quantity:inq.quantity,unit:inq.unit,unit_price:inq.unit_price})}'>📄 Заказ (PO)</button>
          <button class="primary" style="font-size:.82rem;background:var(--success,#16a34a)" data-inquiry-mark="${inq.id}" data-status="ordered">✓ Оформить заказ</button>
          <button class="secondary" style="font-size:.82rem" data-inquiry-mark="${inq.id}" data-status="closed">Закрыть</button>
        </div>` : ""}
      ${inq.status === "ordered" ? `
        <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap">
          <button class="secondary" style="font-size:.82rem" data-inquiry-chat="${inq.id}" data-chat-role="buyer">💬 Переписка</button>
          <button class="secondary" style="font-size:.82rem" data-create-po="${inq.id}" data-inquiry-json='${JSON.stringify({product_name:inq.product_name,supplier_name:inq.supplier_name,quantity:inq.quantity,unit:inq.unit,unit_price:inq.unit_price})}'>📄 Заказ (PO)</button>
          <button class="secondary" style="font-size:.82rem" data-escrow-action="${inq.id}" data-action="reserve" title="Зарезервировать средства в escrow">🔒 Escrow резерв</button>
          <button class="primary" style="font-size:.82rem;background:var(--success,#16a34a)" data-escrow-action="${inq.id}" data-action="release" title="Подтвердить получение и освободить escrow">✓ Товар получен</button>
        </div>` : ""}
      ${inq.status === "pending" ? `
        <div style="display:flex;gap:8px;margin-top:4px">
          <button class="secondary" style="font-size:.82rem" data-inquiry-chat="${inq.id}" data-chat-role="buyer">💬 Переписка</button>
          <button class="secondary" style="font-size:.82rem" data-inquiry-mark="${inq.id}" data-status="closed">Отменить запрос</button>
        </div>` : ""}
    </div>`;
  }).join("");
}

function showPOModal(inquiryId, inquiryData) {
  const existing = document.getElementById("po-modal-overlay");
  if (existing) existing.remove();

  const overlay = document.createElement("div");
  overlay.id = "po-modal-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px";

  const qty = inquiryData.quantity || 0;
  const price = inquiryData.unit_price || 0;
  const total = price ? (qty * price).toFixed(2) : null;

  overlay.innerHTML = `<div style="background:var(--surface,#fff);width:100%;max-width:540px;border-radius:12px;max-height:90vh;overflow-y:auto">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid var(--line)">
      <strong>📄 Заказ на поставку</strong>
      <button id="po-modal-close" class="secondary" style="font-size:.82rem">✕</button>
    </div>
    <div style="padding:16px 20px">
      <div style="background:var(--surface-2,#f5f5f5);border-radius:8px;padding:10px 14px;margin-bottom:14px;font-size:.88rem">
        <div><strong>${escapeHtml(inquiryData.product_name||"")}</strong></div>
        <div style="color:var(--muted);margin-top:2px">Поставщик: ${escapeHtml(inquiryData.supplier_name||"—")} · Кол-во: ${qty} ${escapeHtml(inquiryData.unit||"")}${total ? " · Сумма: " + fmtMoneyKzt(total) + " тг" : ""}</div>
      </div>
      <form id="po-create-form" style="display:grid;gap:10px">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <label style="font-size:.85rem">Ваша организация<input type="text" name="buyer_name" placeholder="ТОО «Компания»" /></label>
          <label style="font-size:.85rem">БИН<input type="text" name="buyer_bin" placeholder="000000000000" /></label>
        </div>
        <label style="font-size:.85rem">Ваш адрес<input type="text" name="buyer_address" placeholder="г. Алматы, ул. ..." /></label>
        <label style="font-size:.85rem">Контактное лицо<input type="text" name="buyer_contact" placeholder="Имя Фамилия, тел." /></label>
        <label style="font-size:.85rem">Адрес доставки<input type="text" name="delivery_address" placeholder="Куда доставить" /></label>
        <label style="font-size:.85rem">Условия оплаты<input type="text" name="payment_terms" value="По договорённости" /></label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <label style="font-size:.85rem">Тип доставки<select name="delivery_type">
            <option value="">Не указан</option>
            <option value="courier">Курьер</option>
            <option value="postal">Почта</option>
            <option value="freight">Грузоперевозка</option>
            <option value="pickup">Самовывоз</option>
            <option value="buyer_arranges">Покупатель организует</option>
          </select></label>
          <label style="font-size:.85rem">Стоимость доставки (тг)<input type="number" name="delivery_price" placeholder="0" min="0" step="0.01" /></label>
        </div>
        <label style="font-size:.85rem;display:flex;align-items:center;gap:8px"><input type="checkbox" name="delivery_included" value="true" /> Доставка включена в цену</label>
        <label style="font-size:.85rem">Сумма escrow (тг, необязательно)<input type="number" name="escrow_amount" placeholder="0" min="0" step="0.01" title="Сумма будет зарезервирована до подтверждения доставки" /></label>
        <label style="font-size:.85rem">Примечания<textarea name="notes" rows="2" placeholder="Срок, особые требования..."></textarea></label>
        <div style="display:flex;gap:8px">
          <button type="submit" class="primary" id="po-create-btn">Создать PO</button>
          <button type="button" id="po-modal-close2" class="secondary">Отмена</button>
        </div>
      </form>
    </div>
  </div>`;

  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("po-modal-close").addEventListener("click", () => overlay.remove());
  document.getElementById("po-modal-close2").addEventListener("click", () => overlay.remove());

  document.getElementById("po-create-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = {};
    for (const [k, v] of fd.entries()) { if (v.trim()) body[k] = v.trim(); }
    const btn = document.getElementById("po-create-btn");
    try {
      btn.disabled = true; btn.textContent = "Создание...";
      const po = await request(`/marketplace/my-inquiries/${inquiryId}/purchase-order`, {
        method: "POST",
        body: JSON.stringify(body),
      });
      overlay.remove();
      // Open print form via fetch so auth header is passed
      try {
        const resp = await fetch(`${API}/marketplace/my-inquiries/${inquiryId}/purchase-order/html`, {
          headers: { Authorization: `Bearer ${el("auth-token").value.trim()}` },
        });
        if (resp.ok) {
          const html = await resp.text();
          const blob = new Blob([html], { type: "text/html" });
          window.open(URL.createObjectURL(blob), "_blank");
        } else {
          alert("Не удалось открыть форму PO");
        }
      } catch (_) { alert("Ошибка при загрузке формы PO"); }
    } catch (err) {
      alert(err.message || "Ошибка создания PO");
      btn.disabled = false; btn.textContent = "Создать PO";
    }
  });
}

function showPriceTiersModal(itemId, unit) {
  const existing = document.getElementById("price-tiers-overlay");
  if (existing) existing.remove();

  const overlay = document.createElement("div");
  overlay.id = "price-tiers-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px";
  overlay.innerHTML = `<div style="background:var(--surface,#fff);width:100%;max-width:480px;border-radius:12px;max-height:90vh;overflow-y:auto">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid var(--line)">
      <strong>📊 Объёмные цены</strong>
      <button id="tiers-close" class="secondary" style="font-size:.82rem">✕</button>
    </div>
    <div id="tiers-body" style="padding:14px 16px">
      <div style="color:var(--muted);font-size:.85rem">Загрузка...</div>
    </div>
  </div>`;

  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("tiers-close").addEventListener("click", () => overlay.remove());

  const body = document.getElementById("tiers-body");

  function renderTiers(tiers) {
    body.innerHTML = `
      <div style="font-size:.82rem;color:var(--muted);margin-bottom:10px">Укажите порог (мин. кол-во) и цену за единицу (${escapeHtml(unit||"шт")}). Тиер применяется автоматически при достижении объёма.</div>
      <div id="tiers-list" style="display:grid;gap:8px">
        ${tiers.map((t, i) => `
          <div style="display:flex;gap:8px;align-items:center" id="tier-row-${i}">
            <input type="number" class="tier-qty" value="${t.min_quantity}" min="0.001" step="0.001" placeholder="Мин. кол-во" style="width:110px;font-size:.85rem" />
            <input type="number" class="tier-price" value="${t.unit_price}" min="0.01" step="0.01" placeholder="Цена тг" style="width:110px;font-size:.85rem" />
            <input type="text" class="tier-label" value="${escapeAttr(t.label||"")}" placeholder="Метка (опц.)" style="flex:1;font-size:.85rem" />
            <button class="danger" style="font-size:.78rem;padding:.25rem .6rem" onclick="document.getElementById('tier-row-${i}').remove()">✕</button>
          </div>`).join("")}
      </div>
      <button id="add-tier-btn" class="secondary" style="font-size:.82rem;margin-top:8px">+ Добавить тиер</button>
      <div style="display:flex;gap:8px;margin-top:14px">
        <button id="save-tiers-btn" class="primary" style="font-size:.85rem">Сохранить</button>
        <button id="clear-tiers-btn" class="secondary" style="font-size:.85rem">Очистить все</button>
      </div>`;

    document.getElementById("add-tier-btn").addEventListener("click", () => {
      const list = document.getElementById("tiers-list");
      const idx = list.children.length;
      const row = document.createElement("div");
      row.style.cssText = "display:flex;gap:8px;align-items:center";
      row.id = `tier-row-${idx}`;
      row.innerHTML = `<input type="number" class="tier-qty" min="0.001" step="0.001" placeholder="Мин. кол-во" style="width:110px;font-size:.85rem" /><input type="number" class="tier-price" min="0.01" step="0.01" placeholder="Цена тг" style="width:110px;font-size:.85rem" /><input type="text" class="tier-label" placeholder="Метка (опц.)" style="flex:1;font-size:.85rem" /><button class="danger" style="font-size:.78rem;padding:.25rem .6rem" onclick="this.parentElement.remove()">✕</button>`;
      list.appendChild(row);
    });

    document.getElementById("clear-tiers-btn").addEventListener("click", () => {
      document.getElementById("tiers-list").innerHTML = "";
    });

    document.getElementById("save-tiers-btn").addEventListener("click", async () => {
      const rows = document.querySelectorAll("#tiers-list > div");
      const tiers = [];
      for (const row of rows) {
        const qty = parseFloat(row.querySelector(".tier-qty").value);
        const price = parseFloat(row.querySelector(".tier-price").value);
        const label = row.querySelector(".tier-label").value.trim();
        if (!qty || !price) continue;
        tiers.push({ min_quantity: qty, unit_price: price, label: label || null });
      }
      tiers.sort((a, b) => a.min_quantity - b.min_quantity);
      const btn = document.getElementById("save-tiers-btn");
      try {
        btn.disabled = true; btn.textContent = "Сохранение...";
        const result = await request(`/supplier/catalog/${itemId}/price-tiers`, {
          method: "PUT",
          body: JSON.stringify({ tiers }),
        });
        // Update catalog item in state
        const idx = state.data.supplierPortal.myCatalog.findIndex((i) => String(i.id) === String(itemId));
        if (idx >= 0) state.data.supplierPortal.myCatalog[idx].price_tiers = result;
        renderTiers(result);
        btn.disabled = false; btn.textContent = "Сохранить";
      } catch (err) {
        alert(err.message || "Ошибка сохранения");
        btn.disabled = false; btn.textContent = "Сохранить";
      }
    });
  }

  request(`/supplier/catalog/${itemId}/price-tiers`).then(renderTiers).catch(() => {
    body.innerHTML = '<div style="color:red">Ошибка загрузки</div>';
  });
}

function showBulkInquiryModal(productName) {
  const existing = document.getElementById("bulk-inquiry-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "bulk-inquiry-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px";
  overlay.innerHTML = `
    <div style="background:var(--surface,#fff);border-radius:12px;padding:24px;max-width:440px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.2)">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <h3 style="margin:0">📤 Массовый запрос</h3>
        <button id="bulk-inquiry-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted);padding:0 4px">&times;</button>
      </div>
      <p style="color:var(--muted);font-size:.9rem;margin-bottom:16px">
        Запрос будет отправлен всем поставщикам у которых есть <strong>«${escapeHtml(productName)}»</strong> в каталоге.
        Вы получите ответы от каждого.
      </p>
      <form id="bulk-inquiry-form" style="display:grid;gap:10px">
        <label style="font-size:.88rem">Количество
          <input type="number" name="quantity" value="1" min="1" step="1" required />
        </label>
        <label style="font-size:.88rem">Комментарий
          <textarea name="notes" rows="2" placeholder="Срочно нужно, уточните сроки поставки..."></textarea>
        </label>
        <div id="bulk-inquiry-result" style="display:none;font-size:.88rem;padding:8px 12px;border-radius:6px"></div>
        <div style="display:flex;gap:8px">
          <button type="submit" class="primary" style="flex:1" id="bulk-inquiry-submit">Отправить всем</button>
          <button type="button" class="secondary" id="bulk-inquiry-cancel">Отмена</button>
        </div>
      </form>
    </div>`;
  document.body.appendChild(overlay);
  document.getElementById("bulk-inquiry-close")?.addEventListener("click", () => overlay.remove());
  document.getElementById("bulk-inquiry-cancel")?.addEventListener("click", () => overlay.remove());
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("bulk-inquiry-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = { product_name: productName, quantity: Number(fd.get("quantity")), source: "qpartner" };
    const notes = (fd.get("notes") || "").trim();
    if (notes) body.notes = notes;
    const btn = document.getElementById("bulk-inquiry-submit");
    const result = document.getElementById("bulk-inquiry-result");
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Отправляю..."; }
      const res = await request("/marketplace/bulk-inquire", { method: "POST", body: JSON.stringify(body) });
      const count = res.total || 0;
      result.style.display = "block";
      result.style.background = count > 0 ? "var(--success-bg,#f0fff4)" : "var(--warning-bg,#fffbeb)";
      result.style.color = count > 0 ? "var(--success,#16a34a)" : "var(--warning,#d97706)";
      result.textContent = count > 0
        ? `✓ Запрос отправлен ${count} поставщик${count === 1 ? "у" : count < 5 ? "ам" : "ам"}! Ответы появятся в «Мои запросы».`
        : "Поставщики с таким товаром не найдены в каталоге.";
      if (count > 0) {
        focusQpartnerPendingInquiries();
        request(myInquiriesPath()).then((d) => { state.data.myInquiries = d; }).catch(() => {});
        if (btn) { btn.disabled = true; btn.textContent = "Отправлено"; }
        setTimeout(() => overlay.remove(), 3000);
      } else {
        if (btn) { btn.disabled = false; btn.textContent = "Отправить всем"; }
      }
    } catch (err) {
      result.style.display = "block";
      result.style.background = "var(--danger-bg,#fff0f0)";
      result.style.color = "var(--danger,#dc2626)";
      result.textContent = err.message || "Ошибка";
      if (btn) { btn.disabled = false; btn.textContent = "Отправить всем"; }
    }
  });
}

function showShipmentFromInquiryModal(inquiry) {
  const existing = document.getElementById("ship-from-inq-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "ship-from-inq-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px";
  const today = new Date(); today.setDate(today.getDate() + (inquiry.delivery_days || 3));
  const defaultDate = today.toISOString().slice(0, 10);
  overlay.innerHTML = `
    <div style="background:var(--surface,#fff);border-radius:12px;padding:24px;max-width:440px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.2)">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <h3 style="margin:0">🚚 Создать поставку</h3>
        <button id="ship-inq-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted)">&times;</button>
      </div>
      <div style="background:var(--surface-2,#f5f5f5);padding:10px 12px;border-radius:8px;margin-bottom:14px;font-size:.88rem">
        <strong>${escapeHtml(inquiry.product_name || "")}</strong> · ${inquiry.quantity} ${escapeHtml(inquiry.unit || "")}
        <div style="color:var(--muted);margin-top:2px">Покупатель: ${escapeHtml(inquiry.warehouse_name || inquiry.actor_id || "—")}</div>
      </div>
      <form id="ship-inq-form" style="display:grid;gap:10px">
        <label style="font-size:.88rem">Номер накладной / Референс
          <input type="text" name="reference" placeholder="INQ-${inquiry.id}" />
        </label>
        <label style="font-size:.88rem">Город отправки
          <input type="text" name="origin_city" placeholder="Алматы" />
        </label>
        <label style="font-size:.88rem">Ожидаемая дата доставки
          <input type="date" name="estimated_arrival" value="${defaultDate}" required />
        </label>
        <label style="font-size:.88rem">Примечания
          <textarea name="notes" rows="2" placeholder="Номер трека, особые условия..."></textarea>
        </label>
        <div id="ship-inq-result" style="display:none;font-size:.88rem;padding:8px 12px;border-radius:6px"></div>
        <div style="display:flex;gap:8px">
          <button type="submit" class="primary" style="flex:1" id="ship-inq-submit">Создать поставку</button>
          <button type="button" class="secondary" id="ship-inq-cancel">Отмена</button>
        </div>
      </form>
    </div>`;
  document.body.appendChild(overlay);
  document.getElementById("ship-inq-close")?.addEventListener("click", () => overlay.remove());
  document.getElementById("ship-inq-cancel")?.addEventListener("click", () => overlay.remove());
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("ship-inq-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = {};
    for (const [k, v] of fd.entries()) { if (v) body[k] = String(v).trim(); }
    const btn = document.getElementById("ship-inq-submit");
    const result = document.getElementById("ship-inq-result");
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Создаю..."; }
      const shipment = await request(`/supplier/inquiries/${inquiry.id}/create-shipment`, {
        method: "POST", body: JSON.stringify(body),
      });
      result.style.display = "block";
      result.style.background = "var(--success-bg,#f0fff4)";
      result.style.color = "var(--success,#16a34a)";
      result.textContent = `✓ Поставка #${shipment.id} создана!`;
      const items = state.data.supplierPortal.inquiries || [];
      const idx = items.findIndex((i) => i.id === inquiry.id);
      if (idx >= 0) items[idx] = { ...items[idx], status: "ordered" };
      if (btn) { btn.disabled = true; btn.textContent = "Создано"; }
      setTimeout(() => { overlay.remove(); render(); }, 2000);
    } catch (err) {
      result.style.display = "block";
      result.style.background = "var(--danger-bg,#fff0f0)";
      result.style.color = "var(--danger,#dc2626)";
      result.textContent = err.message || "Ошибка";
      if (btn) { btn.disabled = false; btn.textContent = "Создать поставку"; }
    }
  });
}

function showInquiryModal(item, purchaseRequestId = null) {
  const existing = document.getElementById("inquiry-modal-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "inquiry-modal-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px";
  overlay.innerHTML = `
    <div style="background:var(--surface,#fff);border-radius:12px;padding:24px;max-width:480px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.2)">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">
        <div>
          <h3 style="margin:0 0 4px">${escapeHtml(item.product_name)}</h3>
          <div style="font-size:.9rem;color:var(--muted)">${escapeHtml(item.supplier_name)} · ${escapeHtml(item.supplier_city || "")}</div>
        </div>
        <button id="inquiry-modal-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted);padding:0 4px">&times;</button>
      </div>
      <div style="display:flex;gap:16px;margin-bottom:16px;padding:12px;background:var(--surface-2,#f5f5f5);border-radius:8px">
        <div><div style="font-size:.75rem;color:var(--muted)">Цена</div><div style="font-weight:700;font-size:1.1rem;color:var(--accent)">${fmtMoneyKzt(item.unit_price)} тг/${escapeHtml(item.unit)}</div></div>
        ${item.delivery_days || item.supplier_delivery_days ? `<div><div style="font-size:.75rem;color:var(--muted)">Доставка</div><div style="font-weight:600">${item.delivery_days || item.supplier_delivery_days} дн.</div></div>` : ""}
        ${item.stock_qty != null ? `<div><div style="font-size:.75rem;color:var(--muted)">В наличии</div><div style="font-weight:600">${item.stock_qty} ${escapeHtml(item.unit)}</div></div>` : ""}
      </div>
      <div style="font-size:.85rem;margin-bottom:12px;color:var(--muted)">Контакты: ${escapeHtml(item.supplier_phone || "")} · ${escapeHtml(item.supplier_email || "")}</div>
      ${purchaseRequestId ? `<div style="font-size:.82rem;background:var(--accent-bg,#eff6ff);color:var(--accent,#2563eb);border-radius:6px;padding:6px 10px;margin-bottom:8px">🔗 Привязать к заявке на закупку #${purchaseRequestId}</div>` : ""}
      <form id="inquiry-modal-form" style="display:grid;gap:10px">
        <label style="font-size:.88rem">Количество (${escapeHtml(item.unit)})
          <input type="number" name="quantity" value="${item.min_order_qty || 1}" min="${item.min_order_qty || 1}" step="1" required />
        </label>
        <label style="font-size:.88rem">Комментарий (необязательно)
          <textarea name="notes" rows="2" placeholder="Нужна срочная поставка / конкретный вопрос о товаре..."></textarea>
        </label>
        <div style="display:flex;gap:8px">
          <button type="submit" class="primary" style="flex:1" id="inquiry-submit-btn">Отправить запрос</button>
          <button type="button" class="secondary" id="inquiry-cancel-btn">Отмена</button>
        </div>
        <div id="inquiry-modal-result" style="display:none;font-size:.88rem;padding:8px 12px;border-radius:6px"></div>
      </form>
    </div>`;
  document.body.appendChild(overlay);

  document.getElementById("inquiry-modal-close")?.addEventListener("click", () => overlay.remove());
  document.getElementById("inquiry-cancel-btn")?.addEventListener("click", () => overlay.remove());
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });

  document.getElementById("inquiry-modal-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = { quantity: Number(fd.get("quantity")), source: "qpartner" };
    const notes = (fd.get("notes") || "").trim();
    if (notes) body.notes = notes;
    if (purchaseRequestId) body.purchase_request_id = purchaseRequestId;
    const btn = document.getElementById("inquiry-submit-btn");
    const result = document.getElementById("inquiry-modal-result");
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Отправляю..."; }
      const created = await request(`/marketplace/inquire/${item.id}`, { method: "POST", body: JSON.stringify(body) });
      // Refresh my-inquiries so the new entry appears immediately
      focusQpartnerPendingInquiries();
      request(myInquiriesPath()).then((d) => { state.data.myInquiries = d; }).catch(() => {});
      result.style.display = "block";
      result.style.background = "var(--success-bg,#f0fff4)";
      result.style.color = "var(--success,#16a34a)";
      result.textContent = "✓ Запрос отправлен! Поставщик получит уведомление и свяжется с вами.";
      if (btn) { btn.disabled = true; btn.textContent = "Отправлено"; }
      setTimeout(() => overlay.remove(), 2000);
    } catch (err) {
      result.style.display = "block";
      result.style.background = "var(--danger-bg,#fff0f0)";
      result.style.color = "var(--danger,#dc2626)";
      result.textContent = err.message || "Ошибка при отправке";
      if (btn) { btn.disabled = false; btn.textContent = "Отправить запрос"; }
    }
  });
}

function starRow(value, max = 5) {
  const rounded = Math.round(Number(value) || 0);
  return `${"★".repeat(rounded)}${"☆".repeat(max - rounded)}`;
}

async function showProductDetailModal(itemId) {
  const existing = document.getElementById("product-detail-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "product-detail-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:flex-start;justify-content:center;padding:20px;overflow-y:auto";
  overlay.innerHTML = `<div style="background:var(--surface,#fff);border-radius:12px;padding:24px;width:100%;max-width:640px;box-shadow:0 8px 40px rgba(0,0,0,.25)">
    <div style="display:flex;justify-content:flex-end"><button id="pd-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted)">&times;</button></div>
    <div id="pd-body"><div style="color:var(--muted);text-align:center;padding:24px">Загрузка...</div></div>
  </div>`;
  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("pd-close")?.addEventListener("click", () => overlay.remove());

  async function load() {
    const [item, reviews, tiers] = await Promise.all([
      request(`/marketplace/catalog/${itemId}`),
      request(`/marketplace/catalog/${itemId}/reviews`).catch(() => []),
      request(`/marketplace/catalog/${itemId}/price-tiers`).catch(() => []),
    ]);
    const avg = reviews.length ? (reviews.reduce((s, r) => s + r.rating, 0) / reviews.length) : null;
    document.getElementById("pd-body").innerHTML = `
      ${item.image_url ? `<img src="${escapeAttr(item.image_url)}" alt="" style="width:100%;max-height:280px;object-fit:cover;border-radius:8px;margin-bottom:12px" />` : ""}
      <h2 style="margin:0 0 4px">${escapeHtml(item.product_name)}</h2>
      ${avg != null ? `<div style="margin-bottom:6px"><span style="color:var(--warning,#f59e0b)">${starRow(avg)}</span> <span style="color:var(--muted);font-size:.85rem">${avg.toFixed(1)} (${reviews.length} отзывов)</span></div>` : `<div style="color:var(--muted);font-size:.85rem;margin-bottom:6px">Отзывов пока нет</div>`}
      <div style="font-size:.9rem;color:var(--muted);margin-bottom:10px;cursor:pointer" data-pd-supplier="${item.supplier_id}">
        Поставщик: <strong style="color:var(--accent)">${escapeHtml(item.supplier_name || "")}</strong>${item.supplier_is_verified ? ` <span style="color:var(--success,#16a34a)">✓ проверен</span>` : ""} →
      </div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;padding:12px;background:var(--surface-2,#f5f5f5);border-radius:8px">
        <div><div style="font-size:.75rem;color:var(--muted)">Цена</div><div style="font-weight:700;font-size:1.2rem;color:var(--accent)">${fmtMoneyKzt(item.unit_price)} тг/${escapeHtml(item.unit)}</div></div>
        ${item.stock_qty != null ? `<div><div style="font-size:.75rem;color:var(--muted)">В наличии</div><div style="font-weight:600">${item.stock_qty} ${escapeHtml(item.unit)}</div></div>` : ""}
        ${item.delivery_days || item.supplier_delivery_days ? `<div><div style="font-size:.75rem;color:var(--muted)">Доставка</div><div style="font-weight:600">${item.delivery_days || item.supplier_delivery_days} дн.</div></div>` : ""}
        ${item.min_order_qty > 1 ? `<div><div style="font-size:.75rem;color:var(--muted)">Мин. заказ</div><div style="font-weight:600">${item.min_order_qty} ${escapeHtml(item.unit)}</div></div>` : ""}
      </div>
      ${item.description ? `<p style="color:var(--text);font-size:.92rem">${escapeHtml(item.description)}</p>` : ""}
      ${tiers.length ? `
        <div style="margin:12px 0">
          <div style="font-weight:600;font-size:.88rem;margin-bottom:4px">Цена за объём</div>
          <table style="width:100%;border-collapse:collapse;font-size:.85rem">
            ${tiers.map((t) => `<tr><td style="padding:4px 0;color:var(--muted)">от ${t.min_quantity} ${escapeHtml(item.unit)}${t.label ? ` (${escapeHtml(t.label)})` : ""}</td><td style="padding:4px 0;text-align:right;font-weight:600">${fmtMoneyKzt(t.unit_price)} тг</td></tr>`).join("")}
          </table>
        </div>` : ""}
      <div style="display:flex;gap:8px;margin:12px 0;flex-wrap:wrap">
        <button class="primary" id="pd-cart-add">🛒 В корзину</button>
        <button class="secondary" id="pd-order">Запросить</button>
      </div>
      <hr style="border:none;border-top:1px solid var(--line,#eee);margin:16px 0" />
      <div style="font-weight:600;margin-bottom:8px">Отзывы (${reviews.length})</div>
      <div id="pd-reviews">
        ${reviews.length ? reviews.map((r) => `
          <div style="padding:8px 0;border-bottom:1px solid var(--line,#eee)">
            <div style="color:var(--warning,#f59e0b)">${starRow(r.rating)}</div>
            ${r.comment ? `<div style="font-size:.88rem;margin:2px 0">${escapeHtml(r.comment)}</div>` : ""}
            <div style="font-size:.75rem;color:var(--muted)">${String(r.created_at || "").slice(0, 10)}</div>
          </div>`).join("") : `<div style="color:var(--muted);font-size:.85rem">Будьте первым, кто оставит отзыв.</div>`}
      </div>
      <form id="pd-review-form" style="display:grid;gap:8px;margin-top:12px">
        <label style="font-size:.85rem">Ваша оценка
          <select name="rating" required>
            <option value="">Выберите...</option>
            <option value="5">★★★★★ Отлично</option>
            <option value="4">★★★★☆ Хорошо</option>
            <option value="3">★★★☆☆ Нормально</option>
            <option value="2">★★☆☆☆ Плохо</option>
            <option value="1">★☆☆☆☆ Очень плохо</option>
          </select>
        </label>
        <textarea name="comment" rows="2" placeholder="Комментарий (необязательно)"></textarea>
        <button type="submit" class="secondary">Оставить отзыв</button>
        <div id="pd-review-result" style="display:none;font-size:.85rem;padding:6px 10px;border-radius:6px"></div>
      </form>`;

    document.getElementById("pd-cart-add")?.addEventListener("click", async () => {
      try {
        state.data.cart = await request("/marketplace/cart/items", {
          method: "POST",
          body: JSON.stringify({ catalog_item_id: item.id, quantity: item.min_order_qty || 1 }),
        });
        showAlert("Товар добавлен в корзину");
        if (state.view === "marketplace") render();
      } catch (err) { showAlert(err.message || "Ошибка", "error"); }
    });
    document.getElementById("pd-order")?.addEventListener("click", () => { overlay.remove(); showInquiryModal(item); });
    document.querySelectorAll("[data-pd-supplier]").forEach((el2) => {
      el2.addEventListener("click", () => { overlay.remove(); showSupplierProfileModal(el2.dataset.pdSupplier); });
    });
    document.getElementById("pd-review-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const rating = Number(fd.get("rating"));
      const comment = (fd.get("comment") || "").trim();
      const result = document.getElementById("pd-review-result");
      try {
        await request(`/marketplace/catalog/${itemId}/reviews`, {
          method: "POST",
          body: JSON.stringify({ rating, comment: comment || null }),
        });
        result.style.display = "block";
        result.style.background = "var(--success-bg,#f0fff4)";
        result.style.color = "var(--success,#16a34a)";
        result.textContent = "✓ Спасибо за отзыв!";
        await load();
      } catch (err) {
        result.style.display = "block";
        result.style.background = "var(--danger-bg,#fff0f0)";
        result.style.color = "var(--danger,#dc2626)";
        result.textContent = err.message || "Ошибка";
      }
    });
  }
  try { await load(); } catch (err) {
    document.getElementById("pd-body").innerHTML = `<div style="color:var(--danger);padding:16px">${escapeHtml(err.message || "Ошибка загрузки")}</div>`;
  }
}

async function showSupplierProfileModal(supplierId) {
  const existing = document.getElementById("supplier-profile-overlay");
  if (existing) existing.remove();
  const overlay = document.createElement("div");
  overlay.id = "supplier-profile-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:flex-start;justify-content:center;padding:20px;overflow-y:auto";
  overlay.innerHTML = `<div style="background:var(--surface,#fff);border-radius:12px;padding:24px;width:100%;max-width:760px;box-shadow:0 8px 40px rgba(0,0,0,.25)">
    <div style="display:flex;justify-content:flex-end"><button id="sp-close" style="background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted)">&times;</button></div>
    <div id="sp-body"><div style="color:var(--muted);text-align:center;padding:24px">Загрузка...</div></div>
  </div>`;
  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.getElementById("sp-close")?.addEventListener("click", () => overlay.remove());
  try {
    const s = await request(`/marketplace/suppliers/${supplierId}`);
    document.getElementById("sp-body").innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:12px">
        <div>
          <h2 style="margin:0 0 4px">${escapeHtml(s.name)} ${s.is_verified ? `<span style="font-size:.8rem;background:var(--success,#16a34a);color:#fff;border-radius:10px;padding:2px 10px;vertical-align:middle">✓ Проверенный поставщик</span>` : ""}</h2>
          <div style="color:var(--muted);font-size:.9rem">${escapeHtml(s.city || "")}${s.delivery_days ? ` · доставка ${s.delivery_days} дн.` : ""}${s.is_preferred ? ` · ⭐ предпочтительный` : ""}</div>
        </div>
        ${s.reviews_avg != null ? `<div style="text-align:center;background:var(--surface-2,#f5f5f5);padding:8px 14px;border-radius:10px"><div style="font-size:1.3rem;font-weight:700;color:var(--accent)">${s.reviews_avg}</div><div style="color:var(--warning,#f59e0b)">${starRow(s.reviews_avg)}</div><div style="font-size:.75rem;color:var(--muted)">${s.reviews_count} отзывов</div></div>` : ""}
      </div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px;font-size:.88rem;color:var(--muted)">
        ${s.phone ? `<a href="tel:${escapeAttr(s.phone)}" style="color:var(--accent)">📞 ${escapeHtml(s.phone)}</a>` : ""}
        ${s.email ? `<span>✉️ ${escapeHtml(s.email)}</span>` : ""}
        ${s.address ? `<span>📍 ${escapeHtml(s.address)}</span>` : ""}
        ${s.catalog_items_count != null ? `<span>🛍️ ${s.catalog_items_count} товаров</span>` : ""}
        ${s.min_price != null ? `<span>Цены от ${fmtMoneyKzt(s.min_price)} до ${fmtMoneyKzt(s.max_price)} тг</span>` : ""}
      </div>
      <div style="font-weight:600;margin-bottom:8px">Каталог поставщика</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:16px">
        ${(s.catalog_items || []).map((it) => `
          <div class="panel" style="padding:8px;cursor:pointer" data-sp-item="${it.id}">
            ${it.image_url ? `<img src="${escapeAttr(it.image_url)}" alt="" style="width:100%;height:90px;object-fit:cover;border-radius:6px;margin-bottom:4px" />` : ""}
            <div style="font-size:.82rem;font-weight:600">${escapeHtml(it.product_name)}</div>
            <div style="font-size:.85rem;color:var(--accent);font-weight:700">${fmtMoneyKzt(it.unit_price)} тг</div>
          </div>`).join("") || `<div style="color:var(--muted);grid-column:1/-1">Нет активных товаров</div>`}
      </div>
      <div style="font-weight:600;margin-bottom:8px">Отзывы о поставщике (${s.reviews_count})</div>
      <div style="margin-bottom:12px">
        ${(s.reviews || []).length ? s.reviews.map((r) => `
          <div style="padding:8px 0;border-bottom:1px solid var(--line,#eee)">
            <div style="color:var(--warning,#f59e0b)">${starRow(r.rating)}</div>
            ${r.comment ? `<div style="font-size:.88rem;margin:2px 0">${escapeHtml(r.comment)}</div>` : ""}
            <div style="font-size:.75rem;color:var(--muted)">${String(r.created_at || "").slice(0, 10)}</div>
          </div>`).join("") : `<div style="color:var(--muted);font-size:.85rem">Отзывов пока нет.</div>`}
      </div>
      <form id="sp-review-form" style="display:grid;gap:8px">
        <label style="font-size:.85rem">Оценить поставщика
          <select name="rating" required>
            <option value="">Выберите...</option>
            <option value="5">★★★★★ Отлично</option>
            <option value="4">★★★★☆ Хорошо</option>
            <option value="3">★★★☆☆ Нормально</option>
            <option value="2">★★☆☆☆ Плохо</option>
            <option value="1">★☆☆☆☆ Очень плохо</option>
          </select>
        </label>
        <textarea name="comment" rows="2" placeholder="Комментарий (необязательно)"></textarea>
        <button type="submit" class="secondary">Оставить отзыв</button>
        <div id="sp-review-result" style="display:none;font-size:.85rem;padding:6px 10px;border-radius:6px"></div>
      </form>`;
    document.querySelectorAll("[data-sp-item]").forEach((el2) => {
      el2.addEventListener("click", () => { overlay.remove(); showProductDetailModal(Number(el2.dataset.spItem)); });
    });
    document.getElementById("sp-review-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const result = document.getElementById("sp-review-result");
      try {
        await request(`/suppliers/${supplierId}/reviews`, {
          method: "POST",
          body: JSON.stringify({ rating: Number(fd.get("rating")), comment: (fd.get("comment") || "").trim() || null }),
        });
        result.style.display = "block";
        result.style.background = "var(--success-bg,#f0fff4)";
        result.style.color = "var(--success,#16a34a)";
        result.textContent = "✓ Спасибо! Отзыв отправлен на модерацию.";
        e.target.reset();
      } catch (err) {
        result.style.display = "block";
        result.style.background = "var(--danger-bg,#fff0f0)";
        result.style.color = "var(--danger,#dc2626)";
        result.textContent = err.message || "Ошибка";
      }
    });
  } catch (err) {
    document.getElementById("sp-body").innerHTML = `<div style="color:var(--danger);padding:16px">${escapeHtml(err.message || "Ошибка загрузки")}</div>`;
  }
}

async function initMarketplace() {
  if (!state.ui.marketplaceFilter) state.ui.marketplaceFilter = { search: "", category: "" };

  async function loadMarketplace() {
    const f = state.ui.marketplaceFilter;
    const params = new URLSearchParams({ limit: "60" });
    if (f.search) params.set("search", f.search);
    if (f.category) params.set("category", f.category);
    if (f.sort) params.set("sort", f.sort);
    try {
      state.data.marketplace = await request(`/marketplace/catalog?${params}`);
    } catch (_) { state.data.marketplace = { items: [], total: 0 }; }
    render();
    if (state.view === "marketplace") initMarketplace();
  }

  // Category chip navigation
  document.querySelectorAll("[data-mp-cat]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cat = btn.dataset.mpCat;
      state.ui.marketplaceFilter = { ...(state.ui.marketplaceFilter || {}), category: cat, offset: 0 };
      el("mp-category") && (el("mp-category").value = cat);
      const search = el("mp-search")?.value?.trim() || "";
      const sort = el("mp-sort")?.value || "";
      state.data.marketplace = await request(
        `/marketplace/catalog?limit=50&search=${encodeURIComponent(search)}&category=${encodeURIComponent(cat)}&sort=${encodeURIComponent(sort)}`
      ).catch(() => ({ items: [], total: 0 }));
      render();
    });
  });

  el("mp-search-btn")?.addEventListener("click", async () => {
    const search = el("mp-search")?.value?.trim() || "";
    const category = el("mp-category")?.value || "";
    const sort = el("mp-sort")?.value || "";
    state.ui.marketplaceFilter = { ...state.ui.marketplaceFilter, search, category, sort };
    await loadMarketplace();
  });
  el("mp-search")?.addEventListener("keydown", async (e) => {
    if (e.key === "Enter") el("mp-search-btn")?.click();
  });
  el("mp-category")?.addEventListener("change", async () => {
    el("mp-search-btn")?.click();
  });

  // Request to buy (opens inquiry modal)
  document.querySelectorAll("[data-mp-order]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const itemId = btn.dataset.mpOrder;
      const item = (state.data.marketplace?.items || []).find((i) => String(i.id) === String(itemId));
      if (!item) return;
      showInquiryModal(item);
    });
  });

  // Compare toggle
  document.querySelectorAll("[data-mp-compare]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const itemId = Number(btn.dataset.mpCompare);
      if (!state.ui.compareItems) state.ui.compareItems = [];
      const idx = state.ui.compareItems.indexOf(itemId);
      if (idx >= 0) {
        state.ui.compareItems = state.ui.compareItems.filter((id) => id !== itemId);
      } else {
        if (state.ui.compareItems.length >= 4) {
          showAlert("Можно сравнить не более 4 позиций одновременно");
          return;
        }
        state.ui.compareItems = [...state.ui.compareItems, itemId];
      }
      render();
      if (state.view === "marketplace") initMarketplace();
    });
  });

  // Compare bar buttons
  el("mp-compare-now-btn")?.addEventListener("click", () => showCompareModal());
  el("mp-compare-clear-btn")?.addEventListener("click", () => {
    state.ui.compareItems = [];
    render();
    if (state.view === "marketplace") initMarketplace();
  });

  // "Load more" pagination
  el("mp-load-more")?.addEventListener("click", async () => {
    const btn = el("mp-load-more");
    const offset = Number(btn?.dataset.offset || 0);
    const f = state.ui.marketplaceFilter || {};
    const params = new URLSearchParams({ limit: "30", offset: String(offset) });
    if (f.search) params.set("search", f.search);
    if (f.category) params.set("category", f.category);
    if (f.sort) params.set("sort", f.sort);
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Загружаю..."; }
      const more = await request(`/marketplace/catalog?${params}`);
      state.data.marketplace = {
        items: [...(state.data.marketplace?.items || []), ...(more.items || [])],
        total: more.total,
      };
      render();
      if (state.view === "marketplace") initMarketplace();
    } catch (err) {
      showAlert(err.message || "Ошибка загрузки", "error");
      if (btn) { btn.disabled = false; btn.textContent = "Загрузить ещё"; }
    }
  });

  // Bulk inquiry to all suppliers
  el("mp-bulk-inquire-btn")?.addEventListener("click", () => {
    const searchTerm = (state.ui.marketplaceFilter?.search || "").trim();
    if (!searchTerm) return;
    showBulkInquiryModal(searchTerm);
  });

  // Tab switching
  document.querySelectorAll("[data-mp-tab]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      state.ui.marketplaceTab = btn.dataset.mpTab;
      if (state.ui.marketplaceTab === "suppliers" && !state.data.marketplaceSuppliers) {
        try {
          state.data.marketplaceSuppliers = await request("/marketplace/suppliers?limit=50");
        } catch (_) { state.data.marketplaceSuppliers = { items: [], total: 0 }; }
      }
      if (state.ui.marketplaceTab === "my-inquiries") {
        state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
      }
      if (state.ui.marketplaceTab === "cart") {
        state.data.cart = await request("/marketplace/cart").catch(() => ({ items: [], total_items: 0, total_amount: 0 }));
      }
      render();
      if (state.view === "marketplace") initMarketplace();
    });
  });

  el("mp-inquiry-source-filter")?.addEventListener("change", async (event) => {
    state.ui.marketplaceInquirySourceFilter = event.target.value || "all";
    state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
    render();
    if (state.view === "marketplace") initMarketplace();
  });
  el("mp-inquiry-status-filter")?.addEventListener("change", async (event) => {
    state.ui.marketplaceInquiryStatusFilter = event.target.value || "all";
    state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
    render();
    if (state.view === "marketplace") initMarketplace();
  });
  ["mp-inquiry-filter-reset", "mp-inquiry-empty-reset"].forEach((id) => {
    el(id)?.addEventListener("click", async () => {
      state.ui.marketplaceInquirySourceFilter = "all";
      state.ui.marketplaceInquiryStatusFilter = "all";
      state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
      render();
      if (state.view === "marketplace") initMarketplace();
    });
  });

  // Open product detail modal
  document.querySelectorAll("[data-mp-detail]").forEach((el2) => {
    el2.addEventListener("click", () => showProductDetailModal(Number(el2.dataset.mpDetail)));
  });

  // Open supplier storefront modal
  document.querySelectorAll("[data-mp-supplier-profile]").forEach((el2) => {
    el2.addEventListener("click", () => showSupplierProfileModal(Number(el2.dataset.mpSupplierProfile)));
  });

  // Add to cart from catalog grid
  document.querySelectorAll("[data-mp-cart-add]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const itemId = Number(btn.dataset.mpCartAdd);
      const item = (state.data.marketplace?.items || []).find((i) => i.id === itemId);
      try {
        state.data.cart = await request("/marketplace/cart/items", {
          method: "POST",
          body: JSON.stringify({ catalog_item_id: itemId, quantity: item?.min_order_qty || 1 }),
        });
        showAlert("Товар добавлен в корзину");
        render();
        if (state.view === "marketplace") initMarketplace();
      } catch (err) { showAlert(err.message || "Ошибка", "error"); }
    });
  });

  // Cart: quantity change
  document.querySelectorAll("[data-cart-qty]").forEach((input) => {
    input.addEventListener("change", async () => {
      const cartItemId = Number(input.dataset.cartQty);
      const qty = Number(input.value);
      if (!(qty > 0)) return;
      try {
        state.data.cart = await request(`/marketplace/cart/items/${cartItemId}`, {
          method: "PATCH",
          body: JSON.stringify({ quantity: qty }),
        });
        render();
        if (state.view === "marketplace") initMarketplace();
      } catch (err) { showAlert(err.message || "Ошибка", "error"); }
    });
  });

  // Cart: remove item
  document.querySelectorAll("[data-cart-remove]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cartItemId = Number(btn.dataset.cartRemove);
      try {
        state.data.cart = await request(`/marketplace/cart/items/${cartItemId}`, { method: "DELETE" });
        render();
        if (state.view === "marketplace") initMarketplace();
      } catch (err) { showAlert(err.message || "Ошибка", "error"); }
    });
  });

  // Cart: checkout
  el("cart-checkout-btn")?.addEventListener("click", async () => {
    const btn = el("cart-checkout-btn");
    if (cartHasInactiveItems(state.data.cart?.items || [])) {
      showAlert("Удалите неактивные товары из корзины перед оформлением заказа", "error");
      return;
    }
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Оформляю..."; }
      const created = await request("/marketplace/cart/checkout", { method: "POST", body: JSON.stringify({ source: "qpartner" }) });
      state.data.cart = await request("/marketplace/cart").catch(() => ({ items: [], total_items: 0, total_amount: 0 }));
      focusQpartnerPendingInquiries();
      state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
      state.ui.marketplaceTab = "my-inquiries";
      showAlert(`Заказ оформлен: создано запросов — ${marketplaceCreatedInquiryCount(created)}`);
      render();
      if (state.view === "marketplace") initMarketplace();
    } catch (err) {
      showAlert(err.message || "Ошибка оформления заказа", "error");
      if (btn) { btn.disabled = false; btn.textContent = "Оформить заказ →"; }
    }
  });

  // Mark inquiry as ordered / closed
  document.querySelectorAll("[data-inquiry-chat]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.inquiryChat, 10);
      const role = btn.dataset.chatRole || "buyer";
      showInquiryChatModal(id, role);
    });
  });

  document.querySelectorAll("[data-create-po]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.createPo, 10);
      let inqData = {};
      try { inqData = JSON.parse(btn.dataset.inquiryJson || "{}"); } catch (_) {}
      showPOModal(id, inqData);
    });
  });

  document.querySelectorAll("[data-inquiry-mark]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.inquiryMark;
      const status = btn.dataset.status;
      btn.disabled = true;
      try {
        const updated = await request(`/marketplace/my-inquiries/${id}`, {
          method: "PATCH",
          body: JSON.stringify({ status }),
        });
        const items = state.data.myInquiries?.items || [];
        const idx = items.findIndex((i) => String(i.id) === String(id));
        if (idx >= 0) items[idx] = updated;
        render();
        if (state.view === "marketplace") initMarketplace();
      } catch (err) {
        alert(err.message || "Ошибка");
        btn.disabled = false;
      }
    });
  });

  // Supplier search
  async function refreshMarketplaceSuppliers(search) {
    if (!state.ui.marketplaceFilter) state.ui.marketplaceFilter = {};
    state.ui.marketplaceFilter.supplierSearch = search;
    try {
      state.data.marketplaceSuppliers = await request(`/marketplace/suppliers?limit=50${search ? `&search=${encodeURIComponent(search)}` : ""}`);
    } catch (_) { state.data.marketplaceSuppliers = { items: [], total: 0 }; }
    render();
    if (state.view === "marketplace") initMarketplace();
  }

  document.getElementById("mp-supplier-search-btn")?.addEventListener("click", async () => {
    const s = (document.getElementById("mp-supplier-search")?.value || "").trim();
    await refreshMarketplaceSuppliers(s);
  });
  document.getElementById("mp-supplier-search")?.addEventListener("keydown", async (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    const s = (event.target?.value || "").trim();
    await refreshMarketplaceSuppliers(s);
  });
  document.getElementById("mp-supplier-search-reset")?.addEventListener("click", async () => {
    await refreshMarketplaceSuppliers("");
  });

  // Browse supplier catalog
  document.querySelectorAll("[data-mp-supplier-catalog]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const supplierId = btn.dataset.mpSupplierCatalog;
      if (!state.ui.marketplaceFilter) state.ui.marketplaceFilter = {};
      state.ui.marketplaceFilter.search = "";
      state.ui.marketplaceFilter.category = "";
      state.ui.marketplaceTab = "catalog";
      try {
        state.data.marketplace = await request(`/marketplace/catalog?supplier_id=${supplierId}&limit=60`);
      } catch (_) { state.data.marketplace = { items: [], total: 0 }; }
      render();
      if (state.view === "marketplace") initMarketplace();
    });
  });
}

function initSupplierMap() {
  const container = document.getElementById('supplier-leaflet-map');
  if (!container || !window.L) return;
  if (container._leaflet_id) {
    container._leaflet_id = null;
    container.innerHTML = '';
  }
  const map = L.map('supplier-leaflet-map').setView([48.0, 66.0], 4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18
  }).addTo(map);

  const suppliers = state.data.supplierMap || [];
  suppliers.forEach(s => {
    const marker = L.marker([s.lat, s.lng]).addTo(map);
    const stars = '★'.repeat(s.rating || 0) + '☆'.repeat(5 - (s.rating || 0));
    marker.bindPopup(
      '<b>' + escapeHtml(s.name) + '</b><br>' +
      (s.city ? escapeHtml(s.city) + '<br>' : '') +
      'Рейтинг: ' + stars + '<br>' +
      (s.delivery_days ? 'Срок доставки: ' + s.delivery_days + ' дн.<br>' : '') +
      (s.phone ? 'Тел: ' + escapeHtml(s.phone) : '')
    );
  });

  const shipments = state.data.shipments?.items || [];
  shipments.forEach(sh => {
    if (sh.origin_lat && sh.origin_lng && sh.current_lat && sh.current_lng) {
      const color = sh.status === 'delayed' ? '#b42318' : sh.status === 'delivered' ? '#14745f' : '#0b5c7a';
      L.polyline([[sh.origin_lat, sh.origin_lng], [sh.current_lat, sh.current_lng]], {color, weight: 2, dashArray: '6,4'}).addTo(map);
      L.circleMarker([sh.current_lat, sh.current_lng], {radius: 6, color, fillColor: color, fillOpacity: 0.8}).addTo(map)
        .bindPopup('<b>' + escapeHtml(sh.reference || 'Поставка #' + sh.id) + '</b><br>Статус: ' + sh.status + '<br>Город: ' + (sh.current_city || '—'));
    }
  });
}


function renderAuctions() {
  const auctions = state.data.auctions?.items || [];
  const statusLabel = { draft: "Черновик", active: "Активен", closed: "Закрыт", cancelled: "Отменён" };
  const statusColor = { draft: "var(--muted)", active: "var(--ok)", closed: "var(--accent-2)", cancelled: "var(--danger)" };
  return `<div style="padding:1rem">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
    <h2 style="margin:0">Аукционы на понижение</h2>
    <button class="primary" data-action="new-auction">+ Новый аукцион</button>
  </div>
  <div id="auction-form-block" class="panel" style="display:none;padding:1rem;margin-bottom:1rem;box-shadow:none">
    <h3 style="margin:0 0 .75rem;font-size:.95rem">Создать аукцион</h3>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem">
      <div style="grid-column:1/-1"><label style="font-size:.8rem;color:var(--muted)">Название</label>
        <input id="auc-title" placeholder="Закупка Физраствора" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Товар</label>
        <select id="auc-product" style="font-size:.85rem">
          <option value="">Выберите товар...</option>
          ${(state.data.products||[]).map(p=>`<option value="${p.id}">${escapeHtml(p.name)}</option>`).join("")}
        </select></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Склад</label>
        <select id="auc-warehouse" style="font-size:.85rem">
          <option value="">Выберите склад...</option>
          ${(state.data.warehouses||[]).map(w=>`<option value="${w.id}">${escapeHtml(w.name)}</option>`).join("")}
        </select></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Количество</label>
        <input id="auc-qty" type="number" placeholder="100" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Единица</label>
        <input id="auc-unit" placeholder="шт" value="шт" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Начальная цена (тг)</label>
        <input id="auc-start-price" type="number" placeholder="5000" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Минимальная цена (тг)</label>
        <input id="auc-min-price" type="number" placeholder="1000" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Шаг снижения (тг)</label>
        <input id="auc-step" type="number" placeholder="100" value="100" style="font-size:.85rem"></div>
      <div><label style="font-size:.8rem;color:var(--muted)">Интервал шага (сек)</label>
        <input id="auc-interval" type="number" placeholder="300" value="300" style="font-size:.85rem"></div>
    </div>
    <div id="auction-form-error" style="color:var(--danger);font-size:.82rem;margin-top:.5rem;display:none"></div>
    <div style="display:flex;gap:.5rem;margin-top:.75rem">
      <button class="primary" data-action="save-auction" style="font-size:.85rem">Создать</button>
      <button class="secondary" data-action="cancel-auction-form" style="font-size:.85rem">Отмена</button>
    </div>
  </div>
  ${auctions.length === 0 ? '<div style="color:var(--muted);padding:2rem;text-align:center">Аукционов пока нет</div>' : ""}
  ${auctions.map(a => `
  <div id="auction-${a.id}" class="panel" style="padding:1rem;margin-bottom:.75rem;box-shadow:none">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.5rem">
      <div>
        <span style="font-weight:600;font-size:.95rem">${escapeHtml(a.title)}</span>
        <span style="margin-left:.5rem;background:${statusColor[a.status]||"var(--muted)"};color:white;padding:2px 8px;border-radius:10px;font-size:.75rem">${statusLabel[a.status]||a.status}</span>
      </div>
      <div style="text-align:right">
        <div data-auction-price="${a.id}" style="font-size:1.3rem;font-weight:700;color:${a.status==="active"?"var(--ok)":"var(--text)"}">${Number(a.current_price).toLocaleString("ru-RU")} тг</div>
        <div style="font-size:.75rem;color:var(--muted)">Нач: ${Number(a.start_price).toLocaleString("ru-RU")} → Мин: ${Number(a.min_price).toLocaleString("ru-RU")}</div>
      </div>
    </div>
    <div style="font-size:.82rem;color:var(--muted);margin-bottom:.5rem">
      ${escapeHtml(a.product_name||"")} · ${a.quantity} ${a.unit} · Ставок: ${a.bid_count}
      ${a.winner_supplier_id ? ` · <b>Победитель: поставщик #${a.winner_supplier_id}, ${Number(a.winner_bid).toLocaleString("ru-RU")} тг</b>` : ""}
    </div>
    <div style="display:flex;gap:.5rem;flex-wrap:wrap">
      ${a.status==="draft" ? `<button class="primary" data-action="start-auction" data-id="${a.id}" style="font-size:.82rem">▶ Запустить</button>` : ""}
      ${a.status==="active" ? `<div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">
        <select id="bid-supplier-${a.id}" style="width:auto;padding:.3rem;font-size:.82rem">
          <option value="">Поставщик...</option>
          ${(state.data.suppliers||[]).map(s=>`<option value="${s.id}">${escapeHtml(s.name)}</option>`).join("")}
        </select>
        <input id="bid-amount-${a.id}" type="number" placeholder="Ставка &lt; ${a.current_price}" style="width:130px;padding:.3rem;font-size:.82rem">
        <button class="primary" data-action="place-bid" data-id="${a.id}" style="font-size:.82rem">Ставка</button>
        <button class="danger" data-action="close-auction" data-id="${a.id}" style="font-size:.82rem">Закрыть</button>
      </div>` : ""}
      <button class="secondary" data-action="load-bids" data-id="${a.id}" style="font-size:.82rem">История ставок</button>
    </div>
    <div id="bids-${a.id}" style="display:none;margin-top:.5rem;font-size:.8rem;background:var(--bg);border-radius:4px;padding:.5rem"></div>
  </div>`).join("")}
</div>`;
}

// ── Barcode scanner engine (html5-qrcode, works on iOS Safari + Android + Desktop) ──
let _qrScanner = null;

function _scannerOverlay() { return document.getElementById("barcode-overlay"); }
function _scannerStatus(msg) {
  const el = document.getElementById("barcode-overlay-status");
  if (el) el.textContent = msg;
}

async function startBarcodeScanner() {
  if (typeof Html5Qrcode === "undefined") {
    showAlert("Библиотека сканирования не загружена. Используйте ввод вручную.", "warn");
    return;
  }

  // Show overlay immediately (user gesture context must stay alive for iOS camera)
  const overlay = _scannerOverlay();
  if (!overlay) return;
  overlay.style.display = "flex";
  _scannerStatus("Инициализация камеры…");

  // Stop any running scanner first
  if (_qrScanner) {
    await _qrScanner.stop().catch(() => {});
    _qrScanner = null;
  }

  // Enable every format the library ships with — EAN-13/8, Code-128/39/93, QR, Aztec,
  // DataMatrix, ITF, UPC-A/E, PDF_417, Codabar, MaxiCode, RSS (GS1), etc.
  const allFormats = Object.values(Html5QrcodeSupportedFormats || {}).filter(Number.isFinite);
  _qrScanner = new Html5Qrcode("barcode-reader", {
    verbose: false,
    ...(allFormats.length ? { formatsToSupport: allFormats } : {}),
  });

  // iOS Safari requires facingMode as a plain string (not nested object).
  // Higher resolution + continuous autofocus noticeably improves 1D-barcode reads
  // (default getUserMedia resolution is often 640x480, too coarse for small EAN codes).
  const config = {
    fps: 15,
    qrbox: (w, h) => ({ width: Math.round(Math.min(w, h) * 0.8), height: Math.round(Math.min(w, h) * 0.45) }),
    aspectRatio: 1.7,
    rememberLastUsedCamera: true,
    supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
    experimentalFeatures: { useBarCodeDetectorIfSupported: true },
    videoConstraints: {
      facingMode: "environment",
      width: { ideal: 1920, min: 1280 },
      height: { ideal: 1080, min: 720 },
      advanced: [{ focusMode: "continuous" }],
    },
  };

  try {
    await _qrScanner.start(
      { facingMode: "environment" },
      config,
      (code) => { handleBarcodeScan(code).catch(() => {}); },
      () => { /* per-frame errors — ignore */ },
    );
    state.ui.scannerActive = true;
    const titleEl = document.getElementById("barcode-overlay-title");
    if (titleEl) titleEl.textContent = t("Наведите камеру на штрихкод");
    _scannerStatus(t("EAN-13 · EAN-8 · Code-128 · QR · DataMatrix · PDF417 · и другие"));
    _setupTorchButton();
  } catch (err) {
    overlay.style.display = "none";
    _qrScanner = null;
    const msg = String(err || "").toLowerCase();
    if (msg.includes("permission") || msg.includes("denied") || msg.includes("notallowed")) {
      showAlert("Доступ к камере запрещён. Откройте настройки браузера и разрешите камеру для этого сайта.", "error");
    } else if (msg.includes("notfound") || msg.includes("no camera")) {
      showAlert("Камера не найдена. Используйте поле ввода штрихкода вручную.", "warn");
    } else {
      showAlert("Не удалось запустить сканер: " + err, "error");
    }
  }
}

function _setupTorchButton() {
  const btn = document.getElementById("barcode-overlay-torch");
  if (!btn || !_qrScanner) return;
  btn.style.display = "none";
  btn.classList.remove("active");
  btn.onclick = null;
  let capabilities;
  try { capabilities = _qrScanner.getRunningTrackCapabilities(); } catch (_) { capabilities = null; }
  if (!capabilities || !capabilities.torch) return;
  btn.style.display = "inline-block";
  let torchOn = false;
  btn.onclick = async () => {
    try {
      await _qrScanner.applyVideoConstraints({ advanced: [{ torch: !torchOn }] });
      torchOn = !torchOn;
      btn.classList.toggle("active", torchOn);
    } catch (_) { /* device does not actually support toggling mid-stream */ }
  };
}

async function stopBarcodeScanner() {
  state.ui.scannerActive = false;
  const overlay = _scannerOverlay();
  if (overlay) overlay.style.display = "none";
  const torchBtn = document.getElementById("barcode-overlay-torch");
  if (torchBtn) { torchBtn.style.display = "none"; torchBtn.classList.remove("active"); torchBtn.onclick = null; }
  if (_qrScanner) {
    await _qrScanner.stop().catch(() => {});
    _qrScanner = null;
  }
}

async function handleBarcodeScan(code) {
  const trimmed = code.trim();
  stopBarcodeScanner();
  if (state.ui._scanRawTarget) {
    const sel = document.querySelector(state.ui._scanRawTarget);
    state.ui._scanRawTarget = null;
    if (sel) {
      sel.value = trimmed;
      sel.dispatchEvent(new Event("change", { bubbles: true }));
      showAlert(`Штрихкод ${trimmed} вставлен в поле`, "ok");
    }
    return;
  }
  // Fast path: check already-loaded products first
  let product = state.data.products.find((p) => p.barcode && p.barcode.trim() === trimmed);
  if (!product) {
    // Server lookup handles catalogs with >100 products and freshly added items
    try {
      product = await request(`/products/by-barcode/${encodeURIComponent(trimmed)}`);
      if (product && !state.data.products.find((p) => p.id === product.id)) {
        state.data.products.push(product);
      }
    } catch (_) {
      product = null;
    }
  }
  const target = state.ui.scannerTarget;
  state.ui.scannerTarget = null;
  const batchFilterMode = state.ui._scanForBatchFilter;
  state.ui._scanForBatchFilter = false;
  const inventoryMode = state.ui._scanForInventory;
  state.ui._scanForInventory = false;
  if (batchFilterMode && product) {
    state.ui.batchFilterProductId = product.id;
    showAlert(`Фильтр: ${product.name}`, "ok");
    render();
    return;
  }
  if (inventoryMode) {
    if (product) {
      const session = selectedInventorySession();
      if (session) {
        const matchLine = (session.lines || []).find(l => Number(l.product_id) === Number(product.id));
        if (matchLine) {
          const input = document.querySelector(`[data-actual-line="${matchLine.id}"]`);
          if (input) {
            input.scrollIntoView({ behavior: "smooth", block: "center" });
            input.focus();
            const row = input.closest("tr");
            if (row) { row.style.background = "#fef9c3"; setTimeout(() => { row.style.background = ""; }, 2500); }
            showAlert(`${product.name} — строка найдена`, "ok");
            return;
          }
        }
        showAlert(`Товар "${product.name}" не найден в текущей инвентаризации`, "warn");
      } else {
        showAlert("Нет активной инвентаризации", "warn");
      }
    } else {
      showAlert(`Штрихкод ${trimmed} не найден в справочнике`, "warn");
    }
    return;
  }
  if (target && product) {
    // Fill a specific form field with the product ID
    const sel = document.querySelector(target);
    if (sel) {
      sel.value = String(product.id);
      sel.dispatchEvent(new Event("change", { bubbles: true }));
    }
    showAlert(`${product.name} выбран`, "ok");
    render();
    return;
  }
  if (product) {
    state.ui.barcodeProduct = product;
    showAlert(`Найден: ${product.name}`, "success");
  } else {
    showAlert(`Штрихкод ${trimmed} не найден в справочнике`, "warn");
    state.ui.barcodeProduct = null;
  }
  render();
}

function initBarcodeOverlay() {
  const overlay = _scannerOverlay();
  if (!overlay) return;
  document.getElementById("barcode-overlay-close")?.addEventListener("click", () => {
    stopBarcodeScanner();
    render();
  });
  // Close on backdrop click
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) { stopBarcodeScanner(); render(); }
  });
}

async function renderCameras() {
  el("main").innerHTML = `
    <div style="display:flex;align-items:center;justify-content:center;height:50vh;">
      <div style="text-align:center;">
        <div style="width:2rem;height:2rem;border:3px solid var(--c-border);border-top-color:var(--c-primary,#2563eb);border-radius:50%;animation:spin .7s linear infinite;margin:0 auto 1rem"></div>
        <p style="color:var(--c-muted)">Подключение к системе камер...</p>
      </div>
    </div>`;
  try {
    // Get cameras SSO token from sklad backend
    const sstResp = await request("/cameras-token", { method: "POST" });
    if (!sstResp.ok) {
      const err = await sstResp.json().catch(() => ({}));
      throw new Error(err?.detail?.message || "Система камер не настроена на этом сервере");
    }
    const { access_token: sstToken } = await sstResp.json();
    // Exchange for cameras JWT
    const exchResp = await fetch("/cameras-api/sso/tetis-exchange", {
      method: "POST",
      headers: { "Authorization": `Bearer ${sstToken}` },
    });
    if (!exchResp.ok) {
      throw new Error("Ошибка аутентификации в системе камер");
    }
    const { access_token: camerasToken } = await exchResp.json();
    // Store cameras JWT (cameras SPA reads from localStorage.token)
    try { localStorage.setItem("token", camerasToken); } catch (_) {}
    // Embed cameras SPA
    el("main").innerHTML = `
      <div style="position:relative;height:calc(100vh - 60px);">
        <iframe
          src="/cameras/"
          style="width:100%;height:100%;border:none;display:block;"
          allow="autoplay; fullscreen"
          title="Камеры видеонаблюдения"
        ></iframe>
      </div>`;
  } catch (err) {
    el("main").innerHTML = `
      <div style="padding:2rem;max-width:480px;margin:0 auto;text-align:center;">
        <svg style="width:3rem;height:3rem;color:var(--c-warning,#d97706);margin-bottom:1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <p style="font-weight:600;margin-bottom:.5rem">${err.message}</p>
        <p style="color:var(--c-muted);font-size:.875rem">Обратитесь к администратору для настройки системы камер.</p>
      </div>`;
  }
}

function renderSupport() {
  return `
    <div style="max-width:680px;margin:0 auto">
      <div class="panel" style="text-align:center;padding:32px 20px;margin-bottom:16px">
        <div style="font-size:2.5rem;margin-bottom:8px">🛟</div>
        <h2 style="margin:0 0 6px">Техподдержка</h2>
        <div style="color:var(--muted)">Раздел в разработке. Здесь появятся контакты, форма обращения и база знаний.</div>
      </div>
      <div class="panel" style="margin-bottom:16px">
        <div style="font-weight:600;margin-bottom:10px">Контакты</div>
        <div style="display:grid;gap:8px;color:var(--muted);font-size:.92rem">
          <div>📞 Телефон: <em>будет добавлен</em></div>
          <div>✉️ Email: <em>будет добавлен</em></div>
          <div>💬 Telegram: <em>будет добавлен</em></div>
        </div>
      </div>
      <div class="panel" style="margin-bottom:16px">
        <div style="font-weight:600;margin-bottom:10px">Частые вопросы</div>
        <div style="color:var(--muted);font-size:.92rem">Раздел FAQ скоро появится здесь.</div>
      </div>
      <div class="panel">
        <div style="font-weight:600;margin-bottom:10px">Написать в поддержку</div>
        <form style="display:grid;gap:10px" onsubmit="return false">
          <label style="font-size:.88rem">Тема
            <input type="text" placeholder="Кратко опишите проблему" disabled />
          </label>
          <label style="font-size:.88rem">Сообщение
            <textarea rows="4" placeholder="Подробности..." disabled></textarea>
          </label>
          <button type="submit" class="secondary" disabled title="Форма обращений скоро заработает">Отправить (скоро)</button>
        </form>
      </div>
    </div>`;
}

const renderers = {
  dashboard: renderDashboard,
  "tablet-writeoff": renderTabletWriteoff,
  stock: renderStock,
  catalog: renderCatalog,
  receipts: renderReceipts,
  documents: renderDocuments,
  operations: renderOperations,
  repacking: renderRepacking,
  returns: renderReturns,
  movements: renderMovements,
  reservations: renderReservations,
  "purchase-requests": renderPurchaseRequests,
  inventory: renderInventory,
  conditions: renderConditions,
  analytics: renderAnalytics,
  notifications: renderNotifications,
  audit: renderAudit,
  users: renderUsers,
  "supplier-map": renderSupplierMap,
  auctions: renderAuctions,
  marketplace: renderMarketplace,
  support: renderSupport,
  cameras: renderCameras,
  "my-profile": renderMyProfile,
};


function applyStaticI18n() {
  const map = {
    "eyebrow": "Рабочее место склада",
    "view-title-static": null,
  };
  const eyebrow = document.querySelector(".eyebrow");
  if (eyebrow) eyebrow.textContent = t("Рабочее место склада");
  const workCtxTitle = document.querySelector(".context-title strong");
  if (workCtxTitle) workCtxTitle.textContent = t("Работаем как");
  const langBtn = document.getElementById("lang-toggle");
  if (langBtn) langBtn.textContent = getLang() === "kz" ? "RU" : "KZ";
}

// ── Профиль пользователя ─────────────────────────────────────
function navigateTo(view) {
  state.view = view;
  render();
}

function renderMyProfile() {
  const profile = state.auth.actor || {};
  const isStandalone = state.auth.source === "login";
  const roles = profile.roles || [];
  const isSupplier = roles.includes("supplier");
  const isMgr = roles.includes("warehouse_manager");
  const roleLabel = isSupplier && isMgr ? "Менеджер + Поставщик" :
                    isSupplier ? "Поставщик" : isMgr ? "Менеджер склада" : roles[0] || "—";
  const supplierId = profile.supplier_id;
  const username = profile.actor_id || "";
  const fullName = state.auth.fullName || username;

  return `
    <div style="max-width:680px">
      <h2 style="margin:0 0 1.5rem;font-size:1.3rem">Настройки профиля</h2>

      <!-- Avatar card -->
      <div style="background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:1.5rem;margin-bottom:1.25rem;display:flex;align-items:center;gap:1.25rem">
        <div style="width:64px;height:64px;background:#2563eb;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.6rem;font-weight:700;flex-shrink:0">
          ${escapeHtml((fullName||"?")[0]?.toUpperCase()||"?")}
        </div>
        <div style="flex:1;min-width:0">
          <div style="font-size:1.15rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml(fullName)}</div>
          <div style="font-size:.85rem;color:var(--muted,#6b7280);margin-bottom:.5rem">@${escapeHtml(username)}</div>
          <div style="display:flex;gap:.4rem;flex-wrap:wrap">
            <span style="background:#dbeafe;color:#1d4ed8;border-radius:20px;padding:2px 10px;font-size:.78rem;font-weight:500">${escapeHtml(roleLabel)}</span>
            ${supplierId ? `<span style="background:#d1fae5;color:#065f46;border-radius:20px;padding:2px 10px;font-size:.78rem;font-weight:500">Поставщик #${supplierId}</span>` : ""}
          </div>
        </div>
        <button onclick="(function(){try{localStorage.removeItem('sklad_supplier_token')}catch(e){}; state.auth.loginToken=''; state.auth.source='demo'; location.reload();})()" 
          style="background:none;border:1px solid #d1d5db;border-radius:6px;padding:.4rem .9rem;font-size:.82rem;color:#6b7280;cursor:pointer;white-space:nowrap;flex-shrink:0">
          Выйти
        </button>
      </div>

      ${isStandalone ? `
      <!-- Личные данные -->
      <div style="background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:1.25rem;margin-bottom:1.25rem">
        <h3 style="margin:0 0 1rem;font-size:1rem;font-weight:600">Личные данные</h3>
        <div style="margin-bottom:.75rem">
          <label style="display:block;font-size:.82rem;font-weight:500;color:#374151;margin-bottom:4px">Логин (не изменяется)</label>
          <input type="text" value="${escapeAttr(username)}" disabled
            style="width:100%;box-sizing:border-box;padding:.5rem .75rem;border:1px solid #e5e7eb;border-radius:6px;font-size:.9rem;background:#f9fafb;color:#6b7280"/>
        </div>
        <div style="margin-bottom:.75rem">
          <label style="display:block;font-size:.82rem;font-weight:500;color:#374151;margin-bottom:4px">Полное имя</label>
          <input id="profile-fullname" type="text" value="${escapeAttr(fullName)}"
            style="width:100%;box-sizing:border-box;padding:.5rem .75rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem"/>
        </div>
        <div id="profile-name-msg" style="display:none;margin-bottom:.75rem;padding:8px 12px;border-radius:6px;font-size:.85rem"></div>
        <button data-profile-save-name class="primary" type="button" style="padding:.5rem 1.5rem">Сохранить</button>
      </div>

      <!-- Безопасность -->
      <div style="background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:1.25rem;margin-bottom:1.25rem">
        <h3 style="margin:0 0 1rem;font-size:1rem;font-weight:600">Безопасность</h3>
        <div style="margin-bottom:.75rem">
          <label style="display:block;font-size:.82rem;font-weight:500;color:#374151;margin-bottom:4px">Текущий пароль</label>
          <input id="profile-old-pw" type="password" autocomplete="current-password"
            style="width:100%;box-sizing:border-box;padding:.5rem .75rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem"/>
        </div>
        <div style="margin-bottom:.75rem">
          <label style="display:block;font-size:.82rem;font-weight:500;color:#374151;margin-bottom:4px">Новый пароль <span style="color:#6b7280;font-weight:400">(минимум 8 символов)</span></label>
          <input id="profile-new-pw" type="password" autocomplete="new-password"
            style="width:100%;box-sizing:border-box;padding:.5rem .75rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem"/>
        </div>
        <div style="margin-bottom:.75rem">
          <label style="display:block;font-size:.82rem;font-weight:500;color:#374151;margin-bottom:4px">Повторите новый пароль</label>
          <input id="profile-new-pw2" type="password" autocomplete="new-password"
            style="width:100%;box-sizing:border-box;padding:.5rem .75rem;border:1px solid #d1d5db;border-radius:6px;font-size:.9rem"/>
        </div>
        <div id="profile-pw-msg" style="display:none;margin-bottom:.75rem;padding:8px 12px;border-radius:6px;font-size:.85rem"></div>
        <button data-profile-save-pw class="primary" type="button" style="padding:.5rem 1.5rem">Сменить пароль</button>
      </div>
      ` : `
      <div style="background:#fefce8;border:1px solid #fde047;border-radius:8px;padding:1rem;margin-bottom:1rem;font-size:.9rem;color:#713f12">
        Для редактирования профиля войдите через форму логина на этом сайте.
      </div>
      `}

      ${supplierId || isSupplier ? `
      <!-- Кабинет поставщика -->
      <div style="background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:1.25rem;margin-bottom:1.25rem">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem">
          <div>
            <h3 style="margin:0 0 .25rem;font-size:1rem;font-weight:600">Кабинет поставщика</h3>
            <p style="margin:0;font-size:.85rem;color:var(--muted,#6b7280)">Управление каталогом, заявками и аукционами</p>
          </div>
          <button onclick="el('supplier-mode-toggle')?.click()" class="primary" type="button"
            style="padding:.5rem 1.1rem;white-space:nowrap">Открыть →</button>
        </div>
      </div>
      ` : ""}

    </div>
  `;
}

function bindMyProfileActions() {
  document.querySelector("[data-profile-save-name]")?.addEventListener("click", async () => {
    const btn = document.querySelector("[data-profile-save-name]");
    const msgEl = el("profile-name-msg");
    const fullname = (el("profile-fullname")?.value || "").trim();
    if (!fullname) { 
      if(msgEl){msgEl.textContent="Введите имя";msgEl.style.display="";msgEl.style.background="#fff0f0";msgEl.style.color="#dc2626";}
      return; 
    }
    btn.disabled = true; btn.textContent = "Сохраняем...";
    try {
      const resp = await fetch(API + "/me/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json", "Authorization": "Bearer " + state.auth.loginToken },
        body: JSON.stringify({ full_name: fullname })
      });
      if (resp.ok) {
        state.auth.fullName = fullname;
        if (state.auth.actor) state.auth.actor.full_name = fullname;
        if(msgEl){msgEl.textContent="✓ Имя сохранено";msgEl.style.display="";msgEl.style.background="#f0fdf4";msgEl.style.color="#16a34a";}
        applyActorProfile(state.auth.actor || {});
        render();
      } else {
        if(msgEl){msgEl.textContent="Ошибка сохранения";msgEl.style.display="";msgEl.style.background="#fff0f0";msgEl.style.color="#dc2626";}
      }
    } catch(e) { 
      if(msgEl){msgEl.textContent="Ошибка: "+e.message;msgEl.style.display="";msgEl.style.background="#fff0f0";msgEl.style.color="#dc2626";}
    }
    finally { btn.disabled=false; btn.textContent="Сохранить"; setTimeout(()=>{if(msgEl)msgEl.style.display="none"},3000); }
  });

  document.querySelector("[data-profile-save-pw]")?.addEventListener("click", async () => {
    const btn = document.querySelector("[data-profile-save-pw]");
    const msgEl = el("profile-pw-msg");
    const oldPw = el("profile-old-pw")?.value || "";
    const newPw = el("profile-new-pw")?.value || "";
    const newPw2 = el("profile-new-pw2")?.value || "";
    const showMsg = (text, ok) => {
      msgEl.textContent = text;
      msgEl.style.display = "";
      msgEl.style.background = ok ? "#f0fdf4" : "#fff0f0";
      msgEl.style.color = ok ? "#16a34a" : "#dc2626";
    };
    if (!oldPw || !newPw) return showMsg("Заполните все поля", false);
    if (newPw.length < 8) return showMsg("Новый пароль — минимум 8 символов", false);
    if (newPw !== newPw2) return showMsg("Пароли не совпадают", false);
    btn.disabled = true; btn.textContent = "Меняем...";
    try {
      const resp = await fetch(API + "/me/password", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": "Bearer " + state.auth.loginToken },
        body: JSON.stringify({ current_password: oldPw, new_password: newPw })
      });
      const data = await resp.json().catch(() => ({}));
      if (resp.ok) {
        showMsg("✓ Пароль успешно изменён", true);
        el("profile-old-pw").value = ""; el("profile-new-pw").value = ""; el("profile-new-pw2").value = "";
      } else {
        showMsg(data?.detail?.message || data?.detail || "Ошибка", false);
      }
    } catch(e) { showMsg("Ошибка соединения", false); }
    finally { setTimeout(() => { btn.disabled=false; btn.textContent="Сменить пароль"; }, 2000); }
  });
}

function render() {
  if (state.ui.supplierMode) {
    renderSupplierNav();
    applyStaticI18n();
    const viewTitle = supplierPortalTitles[state.ui.supplierView] || "Режим поставщика";
    el("view-title").textContent = t(viewTitle);
    el("content").innerHTML = renderSupplierContent();
    bindSupplierActions();
    applyDensity();
    // Ensure supplier mode toggle reflects current state
    const tog = el("supplier-mode-toggle");
    if (tog) tog.textContent = state.auth.supplierId ? "Режим: Поставщик ✓" : "← Назад к складу";
    return;
  }
  ensureAccessibleView();
  if (state.ui.scannerActive && state.view !== "stock") stopBarcodeScanner();
  renderNav();
  applyStaticI18n();
  const view = views.find(([id]) => id === state.view);
  el("view-title").textContent = view ? t(view[2]) : "Склад";
  el("content").innerHTML = `${searchNotice()}${renderers[state.view]?.() || renderDashboard()}`;
  bindActions();
  if (state.view === "supplier-map") initSupplierMap();
  if (state.view === "marketplace") initMarketplace();
  if (state.view === "my-profile") bindMyProfileActions();
  applyDensity();
}

// === SUPPLIER MODE (toggle: сотрудник склада ⇄ поставщик) ===

const supplierPortalNav = [
  ["my-applications", "Мои заявки"],
  ["auctions", "Аукционы"],
  ["my-bids", "Мои ставки"],
  ["my-catalog", "Мой каталог"],
  ["inquiries", "Запросы"],
  ["orders", "История заказов"],
  ["price-history", "История цен"],
  ["shipments", "Мои поставки"],
  ["reviews", "Отзывы о нас"],
  ["profile", "Профиль компании"],
];
const supplierPortalTitles = Object.fromEntries(supplierPortalNav);

function renderSupplierNav() {
  const isFullSupplier = !!state.auth.supplierId;
  const visibleNav = isFullSupplier
    ? supplierPortalNav
    : supplierPortalNav.filter(([id]) => ["my-applications", "auctions"].includes(id));
  const pendingInquiries = (state.data.supplierPortal.inquiries || []).filter((i) => i.status === "pending").length;
  el("nav").innerHTML = visibleNav.map(([id, label]) => {
    const badge = id === "inquiries" && pendingInquiries > 0
      ? ` <span style="background:var(--danger,#dc2626);color:#fff;border-radius:10px;padding:0 5px;font-size:.72rem;margin-left:3px">${pendingInquiries}</span>`
      : "";
    return `<button class="${state.ui.supplierView === id ? "active" : ""}" data-supplier-view="${id}">${escapeHtml(t(label))}${badge}</button>`;
  }).join("");
  el("nav").querySelectorAll("[data-supplier-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.ui.supplierView = button.dataset.supplierView;
      document.querySelector(".sidebar")?.classList.remove("nav-open");
      el("nav-toggle")?.setAttribute("aria-expanded", "false");
      render();
    });
  });
}

function fmtMoneyKzt(value) {
  return Number(value || 0).toLocaleString("ru-RU");
}

function renderSupplierAuctions() {
  const auctions = state.data.supplierPortal.auctions;
  const AUCTION_STATUS = { active: { label: "Идёт", cls: "ok" }, closed: { label: "Завершён", cls: "" }, pending: { label: "Ожидает", cls: "warning" }, cancelled: { label: "Отменён", cls: "danger" } };
  function auctionDeadline(endsAt) {
    if (!endsAt) return "";
    const ms = new Date(endsAt) - Date.now();
    if (ms <= 0) return "завершён";
    const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000);
    if (h > 24) return `ещё ${Math.floor(h / 24)} д.`;
    if (h > 0) return `ещё ${h} ч ${m} мин`;
    return `ещё ${m} мин`;
  }
  if (!auctions.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">📋</div>
      <div style="color:var(--muted)">Активных аукционов пока нет.<br>Новые появятся, как только склад разместит закупку.</div>
    </div>`;
  return auctions.map((a) => {
    const st = AUCTION_STATUS[a.status] || { label: a.status, cls: "" };
    const myBids = state.data.supplierPortal.myBids[a.id] || [];
    const myBest = myBids.length ? Math.min(...myBids.map((b) => Number(b.bid_amount))) : null;
    const iWon = a.status === "closed" && a.winner_supplier_id === state.auth.supplierId;
    const deadline = auctionDeadline(a.ends_at);
    return `
    <div class="panel" style="margin-bottom:12px;${iWon ? "border-left:3px solid var(--success,#16a34a)" : ""}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:6px">
        <div>
          <strong style="font-size:1.05rem">${escapeHtml(a.title)}</strong>
          ${iWon ? `<span style="margin-left:8px;font-size:.8rem;color:var(--success,#16a34a);font-weight:600">🏆 Вы выиграли!</span>` : ""}
        </div>
        <span class="badge ${st.cls}" style="white-space:nowrap">${st.label}</span>
      </div>
      <div style="color:var(--muted);font-size:.85rem;margin-bottom:8px">
        ${escapeHtml(a.product_name || "")} · <strong>${escapeHtml(String(a.quantity))} ${escapeHtml(a.unit)}</strong>
        ${a.warehouse_id ? `· Склад #${a.warehouse_id}` : ""}
      </div>
      ${a.description ? `<div style="font-size:.9rem;margin-bottom:8px;color:var(--text-secondary,#555)">${escapeHtml(a.description)}</div>` : ""}
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px">
        <div><div style="font-size:.75rem;color:var(--muted)">Начальная цена</div><div style="font-weight:700;font-size:1.1rem">${fmtMoneyKzt(a.start_price)} тг</div></div>
        <div><div style="font-size:.75rem;color:var(--muted)">Текущая цена</div><div style="font-weight:700;font-size:1.1rem;color:var(--accent)">${fmtMoneyKzt(a.current_price)} тг</div></div>
        ${a.min_price ? `<div><div style="font-size:.75rem;color:var(--muted)">Мин. цена</div><div style="font-weight:600">${fmtMoneyKzt(a.min_price)} тг</div></div>` : ""}
        ${a.step_amount ? `<div><div style="font-size:.75rem;color:var(--muted)">Шаг</div><div style="font-weight:600">${fmtMoneyKzt(a.step_amount)} тг</div></div>` : ""}
      </div>
      ${a.ends_at ? `<div style="font-size:.8rem;color:var(--muted);margin-bottom:8px">⏱ Дедлайн: ${new Date(a.ends_at).toLocaleString("ru-KZ", {day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})} (${deadline})</div>` : ""}
      ${myBest !== null ? `<div style="font-size:.85rem;margin-bottom:8px;padding:6px 10px;background:var(--surface-2,#f0f7ff);border-radius:6px">Ваша лучшая ставка: <strong>${fmtMoneyKzt(myBest)} тг</strong></div>` : ""}
      ${a.status === "active" ? `
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <input type="number" data-supplier-bid-input="${a.id}"
            placeholder="Сумма ставки (тг)"
            style="max-width:180px"
            ${a.min_price ? `min="${a.min_price}"` : ""}
            max="${Number(a.current_price) - (Number(a.step_amount) || 1)}" />
          <button class="primary" data-place-supplier-bid="${a.id}">Сделать ставку</button>
          ${myBest !== null ? `<span style="font-size:.8rem;color:var(--muted)">${myBids.length} ${myBids.length === 1 ? "ставка" : "ставок"}</span>` : ""}
        </div>
      ` : ""}
      ${a.status === "closed" && a.winner_bid ? `<div style="font-size:.85rem;color:var(--muted)">Победная ставка: ${fmtMoneyKzt(a.winner_bid)} тг</div>` : ""}
    </div>`;
  }).join("");
}

function renderSupplierMyBids() {
  const entries = Object.entries(state.data.supplierPortal.myBids);
  const activeBids = entries.filter(([, bids]) => bids.length > 0);
  if (!activeBids.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">🏷️</div>
      <div style="color:var(--muted)">Вы ещё не делали ставок.<br>Перейдите в «Аукционы» и сделайте первую ставку.</div>
    </div>`;
  const auctionMap = Object.fromEntries((state.data.supplierPortal.auctions || []).map((a) => [String(a.id), a]));
  return activeBids.map(([auctionId, bids]) => {
    const auction = auctionMap[auctionId];
    const myBest = Math.min(...bids.map((b) => Number(b.bid_amount)));
    const iWon = auction?.status === "closed" && auction?.winner_supplier_id === state.auth.supplierId;
    const isActive = auction?.status === "active";
    return `
    <div class="panel" style="margin-bottom:12px;${iWon ? "border-left:3px solid var(--success,#16a34a)" : ""}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div>
          <strong>${auction ? escapeHtml(auction.title) : `Аукцион #${auctionId}`}</strong>
          ${auction ? `<div style="font-size:.82rem;color:var(--muted)">${escapeHtml(auction.product_name || "")} · ${escapeHtml(String(auction.quantity))} ${escapeHtml(auction.unit)}</div>` : ""}
        </div>
        ${iWon ? `<span style="color:var(--success,#16a34a);font-weight:700;font-size:.9rem">🏆 Победа!</span>` : (isActive ? `<span class="badge ok">Активен</span>` : `<span class="badge">${auction?.status || "—"}</span>`)}
      </div>
      <div style="display:flex;gap:16px;margin-bottom:8px">
        <div><div style="font-size:.75rem;color:var(--muted)">Лучшая ставка</div><div style="font-weight:700;color:var(--accent)">${fmtMoneyKzt(myBest)} тг</div></div>
        <div><div style="font-size:.75rem;color:var(--muted)">Всего ставок</div><div style="font-weight:600">${bids.length}</div></div>
        ${auction?.current_price ? `<div><div style="font-size:.75rem;color:var(--muted)">Текущая цена</div><div style="font-weight:600">${fmtMoneyKzt(auction.current_price)} тг</div></div>` : ""}
      </div>
      <details>
        <summary style="cursor:pointer;font-size:.85rem;color:var(--muted)">История ставок (${bids.length})</summary>
        <table style="margin-top:6px;width:100%;font-size:.85rem">
          <tr><th>Дата</th><th>Сумма</th></tr>
          ${bids.map((b) => `<tr><td style="color:var(--muted)">${String(b.created_at).slice(0, 16).replace("T", " ")}</td><td><strong>${fmtMoneyKzt(b.bid_amount)} тг</strong></td></tr>`).join("")}
        </table>
      </details>
    </div>`;
  }).join("");
}

function renderSupplierPriceHistory() {
  const rows = state.data.supplierPortal.priceHistory;
  if (!rows.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">💰</div>
      <div style="color:var(--muted)">История цен пока пуста.<br>Она формируется автоматически из принятых поставок.</div>
    </div>`;
  return `
    <div class="table-wrap">
      <table>
        <tr><th>Дата</th><th>Товар</th><th>Партия/Лот</th><th style="text-align:right">Цена за ед.</th></tr>
        ${rows.map((r) => `
          <tr>
            <td style="color:var(--muted);font-size:.85rem">${escapeHtml(String(r.recorded_at).slice(0, 10))}</td>
            <td>${escapeHtml(r.product_name || "—")}</td>
            <td style="color:var(--muted)">${escapeHtml(r.lot || "—")}</td>
            <td style="text-align:right;font-weight:600">${fmtMoneyKzt(r.unit_price)} тг</td>
          </tr>`).join("")}
      </table>
    </div>`;
}

function renderSupplierShipments() {
  const rows = state.data.supplierPortal.shipments;
  const STATUS = {
    in_transit: { label: "В пути", cls: "ok" },
    delivered: { label: "Доставлено", cls: "" },
    delayed: { label: "Задержка", cls: "danger" },
    cancelled: { label: "Отменено", cls: "danger" },
    pending: { label: "Ожидает отправки", cls: "warning" },
  };
  if (!rows.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">🚚</div>
      <div style="color:var(--muted)">Активных поставок нет.<br>Они появятся, когда склад создаст заявку на вашу поставку.</div>
    </div>`;
  return rows.map((s) => {
    const st = STATUS[s.status] || { label: s.status, cls: "" };
    return `
    <div class="panel" style="margin-bottom:12px" id="shipment-card-${s.id}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div>
          <strong>${escapeHtml(s.reference || `Поставка #${s.id}`)}</strong>
          <div style="font-size:.82rem;color:var(--muted);margin-top:2px">Создана: ${String(s.created_at || "").slice(0, 10)}</div>
        </div>
        <span class="badge ${st.cls}">${st.label}</span>
      </div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px;font-size:.9rem">
        ${s.origin_city ? `<div><span style="color:var(--muted)">Откуда:</span> ${escapeHtml(s.origin_city)}</div>` : ""}
        ${s.current_city ? `<div><span style="color:var(--muted)">Сейчас:</span> ${escapeHtml(s.current_city)}</div>` : ""}
        ${s.estimated_arrival ? `<div><span style="color:var(--muted)">ETA:</span> <strong>${escapeHtml(String(s.estimated_arrival))}</strong></div>` : ""}
      </div>
      ${s.notes ? `<div style="font-size:.85rem;background:var(--surface-2,#f5f5f5);padding:6px 10px;border-radius:6px;margin-bottom:10px">${escapeHtml(s.notes)}</div>` : ""}
      <details>
        <summary style="cursor:pointer;font-size:.85rem;color:var(--accent);font-weight:600">Обновить статус поставки</summary>
        <form class="shipment-update-form" data-shipment-id="${s.id}" style="margin-top:10px;display:grid;gap:8px">
          <label style="font-size:.85rem">Статус
            <select name="status">
              <option value="">— не менять —</option>
              <option value="in_transit" ${s.status === "in_transit" ? "selected" : ""}>В пути</option>
              <option value="delayed" ${s.status === "delayed" ? "selected" : ""}>Задержка</option>
              <option value="delivered" ${s.status === "delivered" ? "selected" : ""}>Доставлено</option>
            </select>
          </label>
          <label style="font-size:.85rem">Текущий город
            <input type="text" name="current_city" value="${escapeAttr(s.current_city || "")}" placeholder="Алматы" />
          </label>
          <label style="font-size:.85rem">Ожидаемая дата прибытия
            <input type="date" name="estimated_arrival" value="${escapeAttr(String(s.estimated_arrival || "").slice(0, 10))}" />
          </label>
          <label style="font-size:.85rem">Примечания
            <textarea name="notes" rows="2">${escapeHtml(s.notes || "")}</textarea>
          </label>
          <button type="submit" class="primary" style="max-width:180px">Сохранить</button>
        </form>
      </details>
    </div>`;
  }).join("");
}

function renderSupplierReviews() {
  const rows = state.data.supplierPortal.reviews;
  if (!rows.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">⭐</div>
      <div style="color:var(--muted)">Отзывов пока нет.<br>Они появятся после завершения первых поставок.</div>
    </div>`;
  const avgRating = (rows.reduce((s, r) => s + (r.rating || 0), 0) / rows.length).toFixed(1);
  return `
    <div class="panel" style="margin-bottom:12px;display:flex;align-items:center;gap:16px">
      <div style="font-size:2.5rem;font-weight:700;color:var(--accent)">${avgRating}</div>
      <div>
        <div style="color:var(--warning);font-size:1.2rem">${"★".repeat(Math.round(avgRating))}${"☆".repeat(5 - Math.round(avgRating))}</div>
        <div style="color:var(--muted);font-size:.85rem">${rows.length} ${rows.length === 1 ? "отзыв" : rows.length < 5 ? "отзыва" : "отзывов"}</div>
      </div>
    </div>
    ${rows.map((r) => `
    <div class="panel" style="margin-bottom:10px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
        <span style="color:var(--warning);font-size:1.1rem">${"★".repeat(r.rating || 0)}${"☆".repeat(5 - (r.rating || 0))}</span>
        <span style="font-size:.78rem;color:var(--muted)">${escapeHtml(String(r.created_at).slice(0, 10))}</span>
      </div>
      ${r.comment ? `<div style="margin-top:6px;font-size:.9rem">${escapeHtml(r.comment)}</div>` : `<div style="color:var(--muted);font-size:.85rem;font-style:italic">Без комментария</div>`}
      ${r.supplier_reply ? `
        <div style="margin-top:8px;background:var(--surface-2,#f0f9ff);border-left:3px solid var(--accent,#2563eb);padding:8px 12px;border-radius:0 6px 6px 0;font-size:.85rem">
          <strong>Ответ компании:</strong> ${escapeHtml(r.supplier_reply)}
          <div style="font-size:.75rem;color:var(--muted);margin-top:2px">${String(r.replied_at || "").slice(0, 10)}</div>
        </div>` : (r.status === "approved" ? `
        <details style="margin-top:6px">
          <summary style="cursor:pointer;font-size:.8rem;color:var(--accent)">Ответить на отзыв</summary>
          <form class="review-reply-form" data-review-id="${r.id}" style="margin-top:6px;display:grid;gap:6px">
            <textarea name="reply_text" rows="2" placeholder="Благодарим за обратную связь..." required style="font-size:.85rem"></textarea>
            <button type="submit" class="primary" style="font-size:.82rem;max-width:160px">Отправить ответ</button>
          </form>
        </details>` : "")}
    </div>`).join("")}`;
}

function renderSupplierOrders() {
  const orders = state.data.supplierPortal.orders || { items: [], total: 0 };
  const items = orders.items || [];
  const STATUS = {
    ordered: { label: "Заказано", cls: "ok" },
    closed: { label: "Завершён", cls: "" },
  };
  if (!items.length) return `
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">📋</div>
      <div style="color:var(--muted)">Нет завершённых заказов.<br>Здесь появятся запросы со статусом «Заказано» или «Завершён».</div>
    </div>`;
  const totalRevenue = items.reduce((s, o) => s + Number(o.total_amount || 0), 0);
  return `
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin-bottom:12px">
      <div class="panel" style="text-align:center;padding:10px">
        <div style="font-size:1.3rem;font-weight:700;color:var(--accent)">${items.length}</div>
        <div style="font-size:.75rem;color:var(--muted)">Всего заказов</div>
      </div>
      <div class="panel" style="text-align:center;padding:10px">
        <div style="font-size:1.1rem;font-weight:700;color:var(--accent)">${fmtMoneyKzt(totalRevenue)} тг</div>
        <div style="font-size:.75rem;color:var(--muted)">Выручка</div>
      </div>
      <div class="panel" style="text-align:center;padding:10px">
        <div style="font-size:1.3rem;font-weight:700;color:var(--accent)">${items.filter(o => o.status === "ordered").length}</div>
        <div style="font-size:.75rem;color:var(--muted)">Активных</div>
      </div>
    </div>
    ${items.map((o) => {
      const st = STATUS[o.status] || { label: o.status, cls: "" };
      return `
      <div class="panel" style="margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <strong>${escapeHtml(o.product_name || "")}</strong>
            ${o.sku ? `<span style="font-size:.78rem;color:var(--muted);margin-left:6px">(${escapeHtml(o.sku)})</span>` : ""}
            <div style="font-size:.82rem;color:var(--muted);margin-top:2px">
              ${escapeHtml(o.warehouse_name || o.actor_id || "—")} · ${String(o.created_at || "").slice(0, 10)}
            </div>
          </div>
          <span class="badge ${st.cls}">${st.label}</span>
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:.88rem;margin-top:6px">
          <span>Кол-во: <strong>${o.quantity} ${escapeHtml(o.unit || "")}</strong></span>
          ${o.unit_price ? `<span>Цена: <strong>${fmtMoneyKzt(o.unit_price)} тг</strong></span>` : ""}
          ${o.total_amount ? `<span>Итого: <strong style="color:var(--accent)">${fmtMoneyKzt(o.total_amount)} тг</strong></span>` : ""}
        </div>
        ${o.notes ? `<div style="font-size:.82rem;color:var(--muted);margin-top:4px">${escapeHtml(o.notes)}</div>` : ""}
      </div>`;
    }).join("")}
    ${orders.total > items.length ? `<div style="text-align:center;padding:12px;color:var(--muted);font-size:.85rem">Показано ${items.length} из ${orders.total}</div>` : ""}`;
}

const supplierPortalRenderers = {
  "my-applications": renderSupplierMyApplications,
  auctions: renderSupplierAuctions,
  "my-bids": renderSupplierMyBids,
  "my-catalog": renderSupplierMyCatalog,
  inquiries: renderSupplierInquiries,
  orders: renderSupplierOrders,
  "price-history": renderSupplierPriceHistory,
  shipments: renderSupplierShipments,
  reviews: renderSupplierReviews,
  profile: renderSupplierProfile,
};

function renderSupplierMyApplications() {
  const apps = state.data.supplierPortal.myApplications;
  const STATUS_LABELS = {
    pending: { label: "На проверке", cls: "warning" },
    approved: { label: "Одобрена", cls: "ok" },
    rejected: { label: "Отклонена", cls: "danger" },
    needs_changes: { label: "Требуются изменения", cls: "warning" },
  };
  if (!apps.length) return `
    <div class="panel">
      <p style="color:var(--muted)">Вы ещё не подавали заявку на статус поставщика.</p>
      <button class="primary" id="goto-become-supplier">Подать заявку</button>
    </div>`;
  return apps.map((app) => {
    const s = STATUS_LABELS[app.status] || { label: app.status, cls: "" };
    const isNeedsChanges = app.status === "needs_changes";
    return `
    <div class="panel" style="margin-bottom:12px" id="supplier-app-card-${app.id}">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <strong>Заявка №${app.id}</strong>
        <span class="badge ${s.cls}">${s.label}</span>
      </div>
      <div style="font-size:.85rem;color:var(--muted);margin-bottom:4px">Подана: ${escapeHtml(String(app.submitted_at||"").slice(0,10))}</div>
      ${app.review_reason ? `<div style="background:var(--surface-2,#f5f5f5);border-left:3px solid var(--warning,#f59e0b);padding:8px 12px;border-radius:0 4px 4px 0;margin:8px 0;font-size:.9rem">
        <strong>Комментарий модератора:</strong><br>${escapeHtml(app.review_reason)}
      </div>` : ""}
      ${isNeedsChanges ? `
        <details style="margin-top:12px">
          <summary style="cursor:pointer;font-weight:600;color:var(--accent)">Исправить и повторно отправить</summary>
          <form id="resubmit-form-${app.id}" style="margin-top:10px;display:grid;gap:8px">
            <label>Название компании<input type="text" name="name" value="${escapeAttr(app.name||"")}" required /></label>
            <label>БИН<input type="text" name="bin" value="${escapeAttr(app.bin||"")}" /></label>
            <label>Email<input type="email" name="email" value="${escapeAttr(app.email||"")}" /></label>
            <label>Телефон<input type="text" name="phone" value="${escapeAttr(app.phone||"")}" /></label>
            <label>Контактное лицо<input type="text" name="contact_person" value="${escapeAttr(app.contact_person||"")}" /></label>
            <label>Город<input type="text" name="city" value="${escapeAttr(app.city||"")}" /></label>
            <label>Адрес<input type="text" name="address" value="${escapeAttr(app.address||"")}" /></label>
            <label>Срок доставки (дней)<input type="number" name="delivery_days" value="${escapeAttr(String(app.delivery_days||""))}" min="0" /></label>
            <label>Примечания<textarea name="notes" rows="2">${escapeHtml(app.notes||"")}</textarea></label>
            <button type="submit" class="primary" data-resubmit-id="${app.id}">Отправить повторно</button>
          </form>
        </details>
      ` : ""}
    </div>`;
  }).join("");
}

function renderSupplierInquiries() {
  const items = state.data.supplierPortal.inquiries || [];
  const STATUS = {
    pending: { label: "Ожидает ответа", cls: "warning" },
    responded: { label: "Отвечено", cls: "ok" },
    ordered: { label: "Заказано", cls: "ok" },
    closed: { label: "Закрыт", cls: "" },
  };
  const sourceFilter = state.ui.supplierInquirySourceFilter || "all";
  const statusFilter = state.ui.supplierInquiryStatusFilter || "all";
  const hasActiveFilters = marketplaceInquiryFiltersActive(sourceFilter, statusFilter);
  const filterBar = marketplaceInquiryFilterBar(sourceFilter, "supplier-inquiry-source-filter", statusFilter, "supplier-inquiry-status-filter", "supplier-inquiry-filter-reset");
  if (!items.length) return `
    ${filterBar}
    <div class="panel" style="text-align:center;padding:32px 16px">
      <div style="font-size:2rem;margin-bottom:8px">📨</div>
      <div style="color:var(--muted)">${hasActiveFilters ? "По выбранным фильтрам входящих запросов нет.<br>Сбросьте фильтры или выберите другой источник/статус." : "Входящих запросов нет.<br>Они появятся, когда склад запросит ваш товар из каталога."}</div>
      ${hasActiveFilters ? `<button class="secondary" style="margin-top:16px" id="supplier-inquiry-empty-reset">Сбросить фильтры</button>` : ""}
    </div>`;
  return filterBar + items.map((inq) => {
    const st = STATUS[inq.status] || { label: inq.status, cls: "" };
    return `
    <div class="panel" style="margin-bottom:12px" id="inquiry-card-${inq.id}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div>
          <strong>${escapeHtml(inq.product_name || "")}</strong>
          ${inq.sku ? `<span style="font-size:.8rem;color:var(--muted);margin-left:6px">(${escapeHtml(inq.sku)})</span>` : ""}
          <div style="font-size:.82rem;color:var(--muted);margin-top:2px">
            Запрос от: <strong>${escapeHtml(inq.warehouse_name || inq.actor_id || "—")}</strong>
            · ${String(inq.created_at || "").slice(0, 10)}
          </div>
        </div>
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;justify-content:flex-end">
          ${marketplaceInquirySourceBadge(inq.source)}
          <span class="badge ${st.cls}">${st.label}</span>
        </div>
      </div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:.9rem;margin-bottom:8px">
        <div>Количество: <strong>${inq.quantity} ${escapeHtml(inq.unit || "")}</strong></div>
        ${inq.unit_price ? `<div>Цена: <strong>${fmtMoneyKzt(inq.unit_price)} тг/${escapeHtml(inq.unit || "")}</strong></div>` : ""}
        ${inq.warehouse_name ? `<div>Склад: <strong>${escapeHtml(inq.warehouse_name)}</strong></div>` : ""}
      </div>
      ${inq.notes ? `<div style="background:var(--surface-2,#f5f5f5);padding:8px 12px;border-radius:6px;font-size:.88rem;margin-bottom:8px">${escapeHtml(inq.notes)}</div>` : ""}
      ${inq.supplier_response ? `
        <div style="background:var(--surface-2,#f0fff4);border-left:3px solid var(--success,#16a34a);padding:8px 12px;border-radius:0 6px 6px 0;font-size:.88rem;margin-bottom:8px">
          <strong>Ваш ответ:</strong> ${escapeHtml(inq.supplier_response)}
        </div>` : ""}
      <div style="display:flex;gap:8px;margin-top:8px">
        <button class="secondary" style="font-size:.82rem" data-inquiry-chat="${inq.id}" data-chat-role="supplier">💬 Переписка</button>
      </div>
      ${inq.status === "pending" ? `
        <details style="margin-top:8px">
          <summary style="cursor:pointer;font-size:.85rem;color:var(--accent);font-weight:600">Ответить</summary>
          <form class="inquiry-respond-form" data-inquiry-id="${inq.id}" style="margin-top:8px;display:grid;gap:8px">
            <textarea name="response_text" rows="3" placeholder="Подтверждаем наличие, готовы отгрузить в течение 3 дней..." required style="font-size:.88rem"></textarea>
            <button type="submit" class="primary" style="max-width:160px;font-size:.85rem">Отправить ответ</button>
          </form>
        </details>` : ""}
      ${inq.status === "responded" ? `
        <div style="margin-top:8px">
          <button class="primary" style="font-size:.82rem" data-create-shipment-inq='${JSON.stringify({id:inq.id, product_name:inq.product_name, quantity:inq.quantity, unit:inq.unit, warehouse_name:inq.warehouse_name, actor_id:inq.actor_id})}'>
            🚚 Создать поставку
          </button>
        </div>` : ""}
    </div>`;
  }).join("");
}

function renderSupplierMyCatalog() {
  const catalogTab = state.ui.catalogSubTab || "items";
  if (catalogTab === "analytics") return renderCatalogAnalytics();

  const allItems = state.data.supplierPortal.myCatalog;
  const catalogSearch = (state.ui.catalogSearch || "").toLowerCase();
  const catalogStatusFilter = state.ui.catalogStatusFilter || "all";
  const items = allItems.filter((item) => {
    if (catalogSearch && !item.product_name.toLowerCase().includes(catalogSearch) && !(item.sku || "").toLowerCase().includes(catalogSearch) && !(item.category || "").toLowerCase().includes(catalogSearch)) return false;
    if (catalogStatusFilter === "active" && !item.is_active) return false;
    if (catalogStatusFilter === "hidden" && item.is_active) return false;
    return true;
  });
  const filteredItems = items;
  const UNITS = ["шт", "уп", "кг", "л", "мл", "рулон", "ампула", "флакон", "бут", "коробка", "пачка"];

  function itemCard(item) {
    return `
    <div class="panel" style="margin-bottom:10px" id="catalog-item-${item.id}">
      ${item.image_url ? `<div style="position:relative;margin-bottom:8px"><img src="${escapeAttr(item.image_url)}" alt="" style="width:100%;height:180px;object-fit:cover;border-radius:6px" loading="lazy" /><button class="danger" style="position:absolute;top:6px;right:6px;font-size:.75rem;padding:3px 8px;opacity:.85" data-catalog-del-image="${item.id}">✕ Удалить фото</button></div>` : ""}
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">
        <div style="flex:1">
          <div style="font-weight:700;font-size:1rem">${escapeHtml(item.product_name)}</div>
          ${item.sku ? `<div style="font-size:.8rem;color:var(--muted)">Артикул: ${escapeHtml(item.sku)}</div>` : ""}
          ${item.category ? `<span style="font-size:.78rem;background:var(--surface-2,#eef);padding:1px 7px;border-radius:10px;color:var(--accent)">${escapeHtml(item.category)}</span>` : ""}
        </div>
        <div style="text-align:right;white-space:nowrap">
          <div style="font-size:1.2rem;font-weight:700;color:var(--accent)">${fmtMoneyKzt(item.unit_price)} тг</div>
          <div style="font-size:.8rem;color:var(--muted)">за ${escapeHtml(item.unit)}</div>
        </div>
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;font-size:.85rem;margin-top:8px;color:var(--muted)">
        ${item.min_order_qty > 1 ? `<span>Мин. заказ: <strong>${item.min_order_qty}</strong></span>` : ""}
        ${item.stock_qty != null ? `<span>В наличии: <strong>${item.stock_qty} ${escapeHtml(item.unit)}</strong></span>` : ""}
        ${item.delivery_days ? `<span>Доставка: <strong>${item.delivery_days} дн.</strong></span>` : ""}
        ${item.valid_until ? `<span style="color:${new Date(item.valid_until) < new Date() ? "var(--danger,#dc2626)" : "var(--success,#16a34a)"}">До: <strong>${item.valid_until}</strong></span>` : ""}
        ${item.condition === "used" ? `<span class="badge warning">Б/У</span>` : item.condition === "refurbished" ? `<span class="badge">Восстановлен</span>` : `<span class="badge ok">Новый</span>`}
        ${item.delivery_type && item.delivery_type !== "buyer_arranges" ? `<span style="font-size:.78rem;color:var(--muted)">${{"courier":"Курьер","postal":"Почта","freight":"Груз","pickup":"Самовывоз"}[item.delivery_type]||item.delivery_type}${item.delivery_price ? " · " + fmtMoneyKzt(item.delivery_price) + " тг" : item.delivery_included ? " (включена)" : ""}</span>` : ""}
        <span class="badge ${item.is_active ? "ok" : "danger"}">${item.is_active ? "Активен" : "Скрыт"}</span>
      </div>
      ${item.description ? `<div style="font-size:.85rem;color:var(--muted);margin-top:6px">${escapeHtml(item.description)}</div>` : ""}
      <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="secondary" style="font-size:.82rem" data-catalog-edit="${item.id}">Редактировать</button>
        <button class="${item.is_active ? "secondary" : "primary"}" style="font-size:.82rem" data-catalog-toggle="${item.id}" data-catalog-active="${item.is_active}">
          ${item.is_active ? "Скрыть" : "Опубликовать"}
        </button>
        ${item.image_url ? "" : `<label class="secondary" style="font-size:.82rem;padding:.35rem .9rem;border-radius:6px;cursor:pointer;border:1px solid var(--line)">📷 Фото<input type="file" accept="image/*" style="display:none" data-catalog-upload-image="${item.id}" /></label>`}
        <button class="secondary" style="font-size:.82rem" data-catalog-tiers="${item.id}" data-catalog-unit="${escapeAttr(item.unit||"")}">📊 Объём</button>
        <button class="danger" style="font-size:.82rem" data-catalog-delete="${item.id}">Удалить</button>
      </div>
      <div id="catalog-edit-form-${item.id}" style="display:none;margin-top:12px">
        <form class="catalog-edit-form" data-item-id="${item.id}" style="display:grid;gap:8px">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <label style="font-size:.85rem">Название<input type="text" name="product_name" value="${escapeAttr(item.product_name)}" required /></label>
            <label style="font-size:.85rem">Артикул<input type="text" name="sku" value="${escapeAttr(item.sku||"")}" /></label>
            <label style="font-size:.85rem">Цена (тг)<input type="number" name="unit_price" value="${item.unit_price}" min="0" step="0.01" required /></label>
            <label style="font-size:.85rem">Единица<select name="unit">
              ${UNITS.map((u) => `<option ${u === item.unit ? "selected" : ""}>${escapeHtml(u)}</option>`).join("")}
            </select></label>
            <label style="font-size:.85rem">Мин. заказ<input type="number" name="min_order_qty" value="${item.min_order_qty}" min="0.001" step="0.001" /></label>
            <label style="font-size:.85rem">В наличии<input type="number" name="stock_qty" value="${item.stock_qty ?? ""}" min="0" step="0.001" /></label>
            <label style="font-size:.85rem">Доставка (дней)<input type="number" name="delivery_days" value="${item.delivery_days ?? ""}" min="0" /></label>
            <label style="font-size:.85rem">Категория<input type="text" name="category" value="${escapeAttr(item.category||"")}" list="catalog-categories-list" /></label>
            <label style="font-size:.85rem">Действует до<input type="date" name="valid_until" value="${escapeAttr(item.valid_until||"")}" title="Срок действия цены" /></label>
            <label style="font-size:.85rem">Состояние<select name="condition">
              <option value="new" ${item.condition === "new" || !item.condition ? "selected" : ""}>Новый</option>
              <option value="used" ${item.condition === "used" ? "selected" : ""}>Б/У</option>
              <option value="refurbished" ${item.condition === "refurbished" ? "selected" : ""}>Восстановленный</option>
            </select></label>
            <label style="font-size:.85rem">Тип доставки<select name="delivery_type">
              <option value="buyer_arranges" ${!item.delivery_type || item.delivery_type === "buyer_arranges" ? "selected" : ""}>Покупатель организует</option>
              <option value="courier" ${item.delivery_type === "courier" ? "selected" : ""}>Курьер</option>
              <option value="postal" ${item.delivery_type === "postal" ? "selected" : ""}>Почта</option>
              <option value="freight" ${item.delivery_type === "freight" ? "selected" : ""}>Грузоперевозка</option>
              <option value="pickup" ${item.delivery_type === "pickup" ? "selected" : ""}>Самовывоз</option>
            </select></label>
            <label style="font-size:.85rem">Стоимость доставки (тг)<input type="number" name="delivery_price" value="${item.delivery_price ?? ""}" min="0" step="0.01" /></label>
          </div>
          <label style="font-size:.85rem;display:flex;align-items:center;gap:8px">
            <input type="checkbox" name="delivery_included" value="true" ${item.delivery_included ? "checked" : ""} />
            Доставка включена в цену товара
          </label>
          <label style="font-size:.85rem">Регионы доставки<input type="text" name="delivery_regions" value="${escapeAttr(item.delivery_regions||"")}" placeholder="Алматы, Астана..." /></label>
          <label style="font-size:.85rem">Описание<textarea name="description" rows="2">${escapeHtml(item.description||"")}</textarea></label>
          <div style="display:flex;gap:8px">
            <button type="submit" class="primary" style="font-size:.82rem">Сохранить</button>
            <button type="button" class="secondary" style="font-size:.82rem" data-catalog-cancel="${item.id}">Отмена</button>
          </div>
        </form>
      </div>
    </div>`;
  }

  const categories = [...new Set(items.map((i) => i.category).filter(Boolean))];
  // Build product name suggestions from marketplace catalog items (items others have published) + any linked product names
  const mpNames = (state.data.marketplace?.items || []).map((i) => i.product_name).filter(Boolean);
  const uniqueProductSuggestions = [...new Set([...mpNames])].slice(0, 200);
  return `
    <datalist id="catalog-categories-list">
      ${categories.map((c) => `<option value="${escapeAttr(c)}">`).join("")}
    </datalist>
    <datalist id="mp-product-suggestions">
      ${uniqueProductSuggestions.map((n) => `<option value="${escapeAttr(n)}">`).join("")}
    </datalist>
    <div style="display:flex;gap:6px;margin-bottom:12px;border-bottom:2px solid var(--border,#e2e8f0);padding-bottom:0">
      <button class="${catalogTab === "items" ? "primary" : "secondary"}" style="font-size:.82rem;border-radius:6px 6px 0 0;border-bottom:none" id="catalog-tab-items">Товары (${allItems.length})</button>
      <button class="${catalogTab === "analytics" ? "primary" : "secondary"}" style="font-size:.82rem;border-radius:6px 6px 0 0;border-bottom:none" id="catalog-tab-analytics">Аналитика</button>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;align-items:center">
      <input id="catalog-search-input" type="search" placeholder="Поиск по названию, артикулу..." value="${escapeAttr(state.ui.catalogSearch || "")}" style="flex:1;min-width:160px;font-size:.88rem;padding:6px 10px" />
      <select id="catalog-status-filter" style="font-size:.85rem;padding:6px 8px">
        <option value="all" ${catalogStatusFilter === "all" ? "selected" : ""}>Все</option>
        <option value="active" ${catalogStatusFilter === "active" ? "selected" : ""}>Только активные</option>
        <option value="hidden" ${catalogStatusFilter === "hidden" ? "selected" : ""}>Только скрытые</option>
      </select>
      <button class="secondary" style="font-size:.82rem" id="catalog-bulk-price-btn">% Цены</button>
      <button class="secondary" style="font-size:.82rem" id="catalog-import-btn">📥 CSV</button>
      <button class="primary" id="catalog-add-btn">+ Добавить</button>
    </div>
    <div id="catalog-bulk-price-panel" style="display:none;margin-bottom:12px">
      <div class="panel" style="background:var(--surface-2,#f5f5f5)">
        <strong style="display:block;margin-bottom:8px">Изменение цен в процентах</strong>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <label style="font-size:.85rem;display:flex;align-items:center;gap:6px">
            Изменить цены на
            <input type="number" id="bulk-price-pct" value="0" step="0.1" style="width:80px;font-size:.9rem" />
            %
          </label>
          <span style="font-size:.8rem;color:var(--muted)">(применится ко всем товарам в каталоге)</span>
          <button class="primary" style="font-size:.85rem" id="bulk-price-apply">Применить</button>
          <button class="secondary" style="font-size:.85rem" id="bulk-price-cancel">Отмена</button>
        </div>
        <div id="bulk-price-result" style="display:none;margin-top:8px;font-size:.85rem;padding:6px 10px;border-radius:6px"></div>
      </div>
    </div>
    <div id="catalog-import-panel" style="display:none;margin-bottom:12px">
      <div class="panel" style="background:var(--surface-2,#f5f5f5)">
        <strong style="display:block;margin-bottom:8px">Импорт прайс-листа из CSV</strong>
        <div style="font-size:.82rem;color:var(--muted);margin-bottom:10px">
          Колонки: <code>product_name</code> (обязательно), <code>unit_price</code> (обязательно), <code>unit</code>, <code>sku</code>, <code>stock_qty</code>, <code>delivery_days</code>, <code>category</code>, <code>description</code>, <code>min_order_qty</code>
          <br>Первая строка — заголовки. Кодировка UTF-8.
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <input type="file" id="catalog-csv-file" accept=".csv" style="font-size:.85rem" />
          <button class="primary" style="font-size:.85rem" id="catalog-csv-upload">Загрузить</button>
          <button class="secondary" style="font-size:.85rem" id="catalog-import-cancel">Отмена</button>
        </div>
        <div id="catalog-import-result" style="display:none;margin-top:10px;font-size:.85rem;padding:8px 12px;border-radius:6px"></div>
      </div>
    </div>
    <div id="catalog-add-form" style="display:none;margin-bottom:16px">
      <div class="panel">
        <strong style="display:block;margin-bottom:10px">Новая позиция</strong>
        <form id="catalog-new-form" style="display:grid;gap:8px">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <label style="font-size:.85rem">Название<input type="text" name="product_name" placeholder="Шприц 5мл" required list="mp-product-suggestions" autocomplete="off" /></label>
            <label style="font-size:.85rem">Артикул<input type="text" name="sku" placeholder="SHR-005" /></label>
            <label style="font-size:.85rem">Цена (тг)<input type="number" name="unit_price" placeholder="45" min="0" step="0.01" required /></label>
            <label style="font-size:.85rem">Единица<select name="unit">
              ${UNITS.map((u) => `<option>${escapeHtml(u)}</option>`).join("")}
            </select></label>
            <label style="font-size:.85rem">Мин. заказ<input type="number" name="min_order_qty" value="1" min="1" step="1" /></label>
            <label style="font-size:.85rem">В наличии<input type="number" name="stock_qty" placeholder="1000" min="0" step="0.001" /></label>
            <label style="font-size:.85rem">Доставка (дней)<input type="number" name="delivery_days" placeholder="3" min="0" /></label>
            <label style="font-size:.85rem">Категория<input type="text" name="category" placeholder="Расходники" list="catalog-categories-list" /></label>
            <label style="font-size:.85rem">Действует до<input type="date" name="valid_until" title="Срок действия цены" /></label>
            <label style="font-size:.85rem">Состояние<select name="condition">
              <option value="new" selected>Новый</option>
              <option value="used">Б/У</option>
              <option value="refurbished">Восстановленный</option>
            </select></label>
            <label style="font-size:.85rem">Тип доставки<select name="delivery_type">
              <option value="buyer_arranges" selected>Покупатель организует</option>
              <option value="courier">Курьер</option>
              <option value="postal">Почта</option>
              <option value="freight">Грузоперевозка</option>
              <option value="pickup">Самовывоз</option>
            </select></label>
            <label style="font-size:.85rem">Стоимость доставки (тг)<input type="number" name="delivery_price" placeholder="0" min="0" step="0.01" /></label>
          </div>
          <label style="font-size:.85rem;display:flex;align-items:center;gap:8px">
            <input type="checkbox" name="delivery_included" value="true" />
            Доставка включена в цену товара
          </label>
          <label style="font-size:.85rem">Регионы доставки<input type="text" name="delivery_regions" placeholder="Алматы, Астана..." /></label>
          <label style="font-size:.85rem">Описание<textarea name="description" rows="2" placeholder="Краткое описание товара"></textarea></label>
          <div style="display:flex;gap:8px">
            <button type="submit" class="primary">Добавить</button>
            <button type="button" class="secondary" id="catalog-add-cancel">Отмена</button>
          </div>
        </form>
      </div>
    </div>
    ${filteredItems.length ? filteredItems.map(itemCard).join("") : `
      <div class="panel" style="text-align:center;padding:32px 16px">
        <div style="font-size:2.5rem;margin-bottom:8px">${items.length ? "🔍" : "🛍️"}</div>
        <div style="color:var(--muted)">${items.length ? "Ничего не найдено по вашему поиску." : "Ваш каталог пуст.<br>Нажмите «+ Добавить товар», чтобы опубликовать первую позицию."}</div>
      </div>`}`;
}

function renderCatalogAnalytics() {
  const analytics = state.data.supplierPortal.catalogAnalytics || [];
  if (!analytics.length) return `<div class="panel" style="text-align:center;padding:32px"><div style="color:var(--muted)">Нет данных. Аналитика появится когда на ваши товары начнут поступать запросы.</div></div>`;
  const maxInq = Math.max(...analytics.map((a) => a.inquiries_total || 0), 1);
  return `
    <div class="panel" style="margin-bottom:12px">
      <div style="font-weight:600;margin-bottom:8px">Спрос по позициям каталога</div>
      ${analytics.map((a) => `
        <div style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <span style="font-size:.88rem;font-weight:500">${escapeHtml(a.product_name)}</span>
            <span style="font-size:.82rem;color:var(--muted)">${a.inquiries_total} запр.</span>
          </div>
          <div style="background:var(--surface-2,#f0f0f0);border-radius:4px;height:8px;overflow:hidden">
            <div style="height:100%;background:var(--accent,#2563eb);border-radius:4px;width:${Math.round(100*(a.inquiries_total||0)/maxInq)}%;transition:width .3s"></div>
          </div>
          <div style="display:flex;gap:10px;margin-top:3px;font-size:.75rem;color:var(--muted)">
            <span>Ожидают: <strong style="color:var(--warning,#d97706)">${a.inquiries_pending}</strong></span>
            <span>Заказано: <strong style="color:var(--success,#16a34a)">${a.inquiries_ordered}</strong></span>
            <span class="badge ${a.is_active ? "ok" : "danger"}" style="font-size:.7rem">${a.is_active ? "Активен" : "Скрыт"}</span>
          </div>
        </div>`).join("")}
    </div>`;
}

function renderSupplierProfile() {
  const p = state.data.supplierPortal.profile;
  if (!p) return `<div class="panel"><p style="color:var(--muted)">Загрузка...</p></div>`;
  const field = (label, val) => val ? `<div style="margin-bottom:6px"><span style="color:var(--muted);font-size:.82rem">${label}</span><div style="font-weight:500">${escapeHtml(String(val))}</div></div>` : "";
  const fieldHtml = (label, html) => html ? `<div style="margin-bottom:6px"><span style="color:var(--muted);font-size:.82rem">${label}</span><div style="font-weight:500">${html}</div></div>` : "";
  const stats = state.data.supplierPortal.stats;
  const statsCard = stats ? `
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin-bottom:12px">
      ${[
        ["🛍️", stats.catalog_active, "Товаров в каталоге"],
        ["📨", stats.inquiries_pending, "Новых запросов"],
        ["🚚", stats.shipments_active, "Поставок в пути"],
        ["🏆", stats.auctions_won, "Выиграно аукционов"],
        ["⭐", stats.reviews_avg != null ? Number(stats.reviews_avg).toFixed(1) : "—", "Рейтинг"],
      ].map(([icon, val, label]) => `
        <div class="panel" style="text-align:center;padding:12px 8px">
          <div style="font-size:1.4rem">${icon}</div>
          <div style="font-size:1.3rem;font-weight:700;color:var(--accent)">${val}</div>
          <div style="font-size:.72rem;color:var(--muted);margin-top:2px">${label}</div>
        </div>`).join("")}
    </div>` : "";
  return `${statsCard}
    <div class="panel" style="margin-bottom:12px">
      <h3 style="margin:0 0 12px">${escapeHtml(p.name||"")}</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px">
        ${field("БИН", p.bin)}
        ${field("ИНН", p.inn)}
        ${field("Рейтинг", p.rating != null ? `${p.rating} ★` : null)}
        ${field("Email", p.email)}
        ${field("Телефон", p.phone)}
        ${field("Контактное лицо", p.contact_person)}
        ${field("Город", p.city)}
        ${field("Адрес", p.address)}
        ${fieldHtml("Сайт", p.website ? `<a href="${escapeAttr(p.website)}" target="_blank" rel="noopener">${escapeHtml(p.website)}</a>` : null)}
        ${field("Срок доставки", p.delivery_days != null ? `${p.delivery_days} дней` : null)}
      </div>
      ${p.bank_details ? `<div style="background:var(--surface-2,#f5f5f5);border-radius:6px;padding:10px 12px;font-size:.88rem;white-space:pre-wrap;margin-bottom:10px"><span style="color:var(--muted);display:block;font-size:.78rem;margin-bottom:4px">Банковские реквизиты</span>${escapeHtml(p.bank_details)}</div>` : ""}
      ${p.notes ? `<div style="font-size:.9rem;color:var(--muted)">${escapeHtml(p.notes)}</div>` : ""}
      <hr style="margin:16px 0">
      ${p.is_verified ? `<div style="background:#f0fff4;border:1px solid #16a34a;border-radius:8px;padding:10px 14px;margin-bottom:12px;display:flex;align-items:center;gap:8px"><span style="font-size:1.2rem">✅</span><div><strong style="color:#16a34a">Поставщик верифицирован</strong>${p.verified_at ? `<div style="font-size:.78rem;color:var(--muted)">${String(p.verified_at).slice(0,10)}</div>` : ""}</div></div>` : `<div style="background:#fffbeb;border:1px solid #f59e0b;border-radius:8px;padding:10px 14px;margin-bottom:12px;display:flex;align-items:center;gap:10px"><span style="font-size:1.2rem">⏳</span><div><strong style="color:#92400e">Верификация не пройдена</strong><div style="font-size:.8rem;color:var(--muted);margin-top:2px">Загрузите документы ниже чтобы получить значок верифицированного поставщика</div></div></div>`}
      <details>
        <summary style="cursor:pointer;font-weight:600;color:var(--accent)">Редактировать контактную информацию</summary>
        <form id="supplier-profile-edit-form" style="margin-top:10px;display:grid;gap:8px">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <label>Email<input type="email" name="email" value="${escapeAttr(p.email||"")}" /></label>
            <label>Телефон<input type="text" name="phone" value="${escapeAttr(p.phone||"")}" /></label>
            <label>Контактное лицо<input type="text" name="contact_person" value="${escapeAttr(p.contact_person||"")}" /></label>
            <label>Город<input type="text" name="city" value="${escapeAttr(p.city||"")}" /></label>
            <label>Срок доставки (дней)<input type="number" name="delivery_days" value="${escapeAttr(String(p.delivery_days||""))}" min="0" /></label>
            <label>ИНН<input type="text" name="inn" value="${escapeAttr(p.inn||"")}" placeholder="Введите ИНН" /></label>
          </div>
          <label>Адрес<input type="text" name="address" value="${escapeAttr(p.address||"")}" /></label>
          <label>Сайт<input type="url" name="website" value="${escapeAttr(p.website||"")}" placeholder="https://example.com" /></label>
          <label>Банковские реквизиты
            <textarea name="bank_details" rows="3" placeholder="Наименование банка, ИИК, БИК, КБЕ...">${escapeHtml(p.bank_details||"")}</textarea>
          </label>
          <label>Примечания<textarea name="notes" rows="2">${escapeHtml(p.notes||"")}</textarea></label>
          <button type="submit" class="primary" id="save-supplier-profile-btn">Сохранить</button>
        </form>
      </details>
    </div>
    <div class="panel" style="margin-bottom:12px">
      <h4 style="margin:0 0 10px">📋 Документы для верификации</h4>
      ${(state.data.supplierPortal.verificationDocs||[]).length ? (state.data.supplierPortal.verificationDocs||[]).map((d) => `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--line)">
          <div>
            <a href="${escapeAttr(d.file_url)}" target="_blank" style="color:var(--accent);font-size:.9rem">${escapeHtml(d.original_name||d.file_url)}</a>
            <div style="font-size:.75rem;color:var(--muted)">${escapeHtml(d.doc_type)} · ${String(d.uploaded_at||"").slice(0,10)}</div>
          </div>
          <button class="danger" style="font-size:.78rem;padding:.25rem .7rem" data-del-vdoc="${d.id}">✕</button>
        </div>`).join("") : `<div style="color:var(--muted);font-size:.88rem">Документы ещё не загружены</div>`}
      <div style="margin-top:14px;display:grid;gap:8px">
        <div style="font-size:.82rem;color:var(--muted)">Загрузить документ:</div>
        <select id="vdoc-type" style="font-size:.88rem">
          <option value="registration">Свидетельство о регистрации</option>
          <option value="license">Лицензия / Разрешение</option>
          <option value="certificate">Сертификат качества</option>
          <option value="bank">Банковские реквизиты</option>
          <option value="other">Другое</option>
        </select>
        <label class="primary" style="cursor:pointer;display:inline-block;padding:.5rem 1rem;border-radius:6px;font-size:.88rem;text-align:center">
          📎 Выбрать файл
          <input type="file" id="vdoc-file-input" style="display:none" accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" />
        </label>
      </div>
    </div>`;
}

function renderSupplierContent() {
  return supplierPortalRenderers[state.ui.supplierView]?.() || renderSupplierAuctions();
}

function bindSupplierActions() {
  document.querySelectorAll("[data-place-supplier-bid]").forEach((button) => {
    button.addEventListener("click", () => placeSupplierBid(button.dataset.placeSupplierBid));
  });

  // Resubmit application
  document.querySelectorAll("[data-resubmit-id]").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const id = btn.dataset.resubmitId;
      const form = document.getElementById(`resubmit-form-${id}`);
      if (!form) return;
      const fd = new FormData(form);
      const body = {};
      for (const [k, v] of fd.entries()) { if (v.trim()) body[k] = v.trim(); }
      try {
        btn.disabled = true;
        btn.textContent = "Отправка...";
        await request(`/supplier/my-applications/${id}/resubmit`, { method: "POST", body: JSON.stringify(body) });
        state.data.supplierPortal.myApplications = await request(`/supplier/my-applications`).catch(() => []);
        render();
      } catch (err) {
        alert(err.message || "Ошибка при отправке");
        btn.disabled = false;
        btn.textContent = "Отправить повторно";
      }
    });
  });

  // Save profile
  // Price tiers modal
  document.querySelectorAll("[data-catalog-tiers]").forEach((btn) => {
    btn.addEventListener("click", () => {
      showPriceTiersModal(btn.dataset.catalogTiers, btn.dataset.catalogUnit);
    });
  });

  // Verification docs are loaded in loadSupplierPortalData() to avoid render loops

  // Delete verification doc
  document.querySelectorAll("[data-del-vdoc]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Удалить этот документ?")) return;
      const id = btn.dataset.delVdoc;
      try {
        await request(`/supplier/verification-docs/${id}`, { method: "DELETE" });
        state.data.supplierPortal.verificationDocs = state.data.supplierPortal.verificationDocs.filter((d) => String(d.id) !== String(id));
        render();
      } catch (err) { alert(err.message || "Ошибка"); }
    });
  });

  // Upload verification doc
  document.getElementById("vdoc-file-input")?.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const docType = document.getElementById("vdoc-type")?.value || "other";
    const formData = new FormData();
    formData.append("file", file);
    const label = e.target.closest("label");
    if (label) label.textContent = "Загрузка...";
    try {
      const result = await fetch(`${API}/supplier/verification-docs/upload?doc_type=${encodeURIComponent(docType)}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${el("auth-token").value.trim()}` },
        body: formData,
      });
      if (!result.ok) {
        const err = await result.json().catch(() => ({}));
        throw new Error(err?.detail?.message || "Ошибка загрузки");
      }
      const doc = await result.json();
      state.data.supplierPortal.verificationDocs = [...(state.data.supplierPortal.verificationDocs || []), doc];
      render();
    } catch (err) {
      alert(err.message || "Ошибка при загрузке");
      if (label) label.textContent = "📎 Выбрать файл";
    }
  });

  document.getElementById("supplier-profile-edit-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);
    const body = {};
    for (const [k, v] of fd.entries()) { if (v.trim()) body[k] = v; }
    const btn = document.getElementById("save-supplier-profile-btn");
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Сохраняю..."; }
      const updated = await request(`/supplier/me`, { method: "PATCH", body: JSON.stringify(body) });
      state.data.supplierPortal.profile = updated;
      render();
    } catch (err) {
      alert(err.message || "Ошибка при сохранении");
      if (btn) { btn.disabled = false; btn.textContent = "Сохранить"; }
    }
  });

  // Go to become-supplier from my-applications
  document.getElementById("goto-become-supplier")?.addEventListener("click", () => {
    state.ui.supplierMode = false;
    render();
    setTimeout(() => el("become-supplier-button")?.click(), 100);
  });

  // Shipment status update by supplier
  document.querySelectorAll(".shipment-update-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const shipmentId = form.dataset.shipmentId;
      const fd = new FormData(form);
      const body = {};
      const status = fd.get("status");
      if (status) body.status = status;
      const city = (fd.get("current_city") || "").trim();
      if (city) body.current_city = city;
      const eta = (fd.get("estimated_arrival") || "").trim();
      if (eta) body.estimated_arrival = eta;
      const notes = (fd.get("notes") || "").trim();
      if (notes !== undefined) body.notes = notes || null;
      if (!Object.keys(body).length) return;
      const btn = form.querySelector("button[type=submit]");
      try {
        if (btn) { btn.disabled = true; btn.textContent = "Сохраняю..."; }
        const updated = await request(`/shipments/${shipmentId}`, { method: "PATCH", body: JSON.stringify(body) });
        const idx = state.data.supplierPortal.shipments.findIndex((s) => String(s.id) === String(shipmentId));
        if (idx >= 0) state.data.supplierPortal.shipments[idx] = updated;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при обновлении поставки");
        if (btn) { btn.disabled = false; btn.textContent = "Сохранить"; }
      }
    });
  });

  // ── Catalog management ──────────────────────────────────────────────────

  // Tab switching
  el("catalog-tab-items")?.addEventListener("click", () => { state.ui.catalogSubTab = "items"; render(); });
  el("catalog-tab-analytics")?.addEventListener("click", () => { state.ui.catalogSubTab = "analytics"; render(); });

  // Search & filter
  el("catalog-search-input")?.addEventListener("input", (e) => {
    state.ui.catalogSearch = e.target.value;
    render();
  });
  el("catalog-status-filter")?.addEventListener("change", (e) => {
    state.ui.catalogStatusFilter = e.target.value;
    render();
  });

  el("catalog-add-btn")?.addEventListener("click", () => {
    const f = el("catalog-add-form");
    if (f) f.style.display = f.style.display === "none" ? "" : "none";
  });
  el("catalog-add-cancel")?.addEventListener("click", () => {
    el("catalog-add-form").style.display = "none";
  });

  // Bulk price panel toggle
  el("catalog-bulk-price-btn")?.addEventListener("click", () => {
    const p = el("catalog-bulk-price-panel");
    if (p) p.style.display = p.style.display === "none" ? "" : "none";
  });
  el("bulk-price-cancel")?.addEventListener("click", () => {
    if (el("catalog-bulk-price-panel")) el("catalog-bulk-price-panel").style.display = "none";
  });
  el("bulk-price-apply")?.addEventListener("click", async () => {
    const pctInput = el("bulk-price-pct");
    const pct = Number(pctInput?.value);
    if (isNaN(pct) || pct === 0) { alert("Введите ненулевой процент"); return; }
    if (!confirm(`Изменить цены на ${pct > 0 ? "+" : ""}${pct}% для всех товаров в каталоге?`)) return;
    const btn = el("bulk-price-apply");
    const resultDiv = el("bulk-price-result");
    try {
      btn.disabled = true; btn.textContent = "Применяю...";
      const res = await request("/supplier/catalog/bulk-price", { method: "POST", body: JSON.stringify({ percent_change: pct }) });
      state.data.supplierPortal.myCatalog = (await request("/supplier/catalog").catch(() => ({ items: [] }))).items || [];
      if (resultDiv) {
        resultDiv.style.display = "block";
        resultDiv.style.background = "var(--success-bg,#f0fff4)";
        resultDiv.style.color = "var(--success,#16a34a)";
        resultDiv.textContent = `Цены обновлены: ${res.updated || 0} позиций`;
      }
      setTimeout(() => render(), 1500);
    } catch (err) {
      if (resultDiv) {
        resultDiv.style.display = "block";
        resultDiv.style.background = "var(--danger-bg,#fff0f0)";
        resultDiv.style.color = "var(--danger,#dc2626)";
        resultDiv.textContent = err.message || "Ошибка";
      }
    } finally {
      btn.disabled = false; btn.textContent = "Применить";
    }
  });

  // CSV import panel toggle
  el("catalog-import-btn")?.addEventListener("click", () => {
    const p = el("catalog-import-panel");
    if (p) p.style.display = p.style.display === "none" ? "" : "none";
  });
  el("catalog-import-cancel")?.addEventListener("click", () => {
    if (el("catalog-import-panel")) el("catalog-import-panel").style.display = "none";
  });

  // CSV upload handler
  el("catalog-csv-upload")?.addEventListener("click", async () => {
    const fileInput = el("catalog-csv-file");
    const resultDiv = el("catalog-import-result");
    if (!fileInput?.files?.length) {
      alert("Выберите CSV-файл");
      return;
    }
    const btn = el("catalog-csv-upload");
    try {
      btn.disabled = true; btn.textContent = "Загружаю...";
      const fd = new FormData();
      fd.append("file", fileInput.files[0]);
      const res = await request("/supplier/catalog/import-csv", { method: "POST", body: fd, isFormData: true });
      resultDiv.style.display = "block";
      resultDiv.style.background = res.inserted > 0 ? "var(--success-bg,#f0fff4)" : "var(--warning-bg,#fffbeb)";
      resultDiv.style.color = res.inserted > 0 ? "var(--success,#16a34a)" : "var(--warning,#d97706)";
      resultDiv.innerHTML = `Добавлено: <strong>${res.inserted}</strong> · Пропущено: <strong>${res.skipped}</strong>`
        + (res.errors?.length ? `<div style="margin-top:4px;font-size:.78rem">${res.errors.slice(0, 5).map(escapeHtml).join("<br>")}</div>` : "");
      if (res.inserted > 0) {
        // Refresh catalog
        state.data.supplierPortal.myCatalog = (await request("/supplier/catalog").catch(() => ({ items: [] }))).items || [];
        setTimeout(() => render(), 1500);
      }
    } catch (err) {
      resultDiv.style.display = "block";
      resultDiv.style.background = "var(--danger-bg,#fff0f0)";
      resultDiv.style.color = "var(--danger,#dc2626)";
      resultDiv.textContent = err.message || "Ошибка загрузки";
    } finally {
      btn.disabled = false; btn.textContent = "Загрузить";
    }
  });

  el("catalog-new-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = {};
    for (const [k, v] of fd.entries()) {
      if (v.trim() === "") continue;
      if (k === "delivery_included") { body[k] = true; continue; }
      body[k] = ["unit_price", "min_order_qty", "stock_qty", "delivery_days", "delivery_price"].includes(k) ? Number(v) : v.trim();
    }
    const btn = e.target.querySelector("button[type=submit]");
    try {
      if (btn) { btn.disabled = true; btn.textContent = "Добавляю..."; }
      const created = await request("/supplier/catalog", { method: "POST", body: JSON.stringify(body) });
      state.data.supplierPortal.myCatalog.unshift(created);
      el("catalog-add-form").style.display = "none";
      e.target.reset();
      render();
    } catch (err) {
      alert(err.message || "Ошибка при добавлении");
      if (btn) { btn.disabled = false; btn.textContent = "Добавить"; }
    }
  });

  // Edit toggle
  document.querySelectorAll("[data-catalog-edit]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.catalogEdit;
      const form = el(`catalog-edit-form-${id}`);
      if (form) form.style.display = form.style.display === "none" ? "" : "none";
    });
  });
  document.querySelectorAll("[data-catalog-cancel]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.catalogCancel;
      const form = el(`catalog-edit-form-${id}`);
      if (form) form.style.display = "none";
    });
  });

  // Edit submit
  document.querySelectorAll(".catalog-edit-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const itemId = form.dataset.itemId;
      const fd = new FormData(form);
      const body = {};
      for (const [k, v] of fd.entries()) {
        if (k === "delivery_included") { body[k] = true; continue; }
        body[k] = ["unit_price", "min_order_qty", "stock_qty", "delivery_days", "delivery_price"].includes(k) ? (v ? Number(v) : null) : v || null;
      }
      if (!("delivery_included" in body)) body.delivery_included = false;
      const btn = form.querySelector("button[type=submit]");
      try {
        if (btn) { btn.disabled = true; btn.textContent = "Сохраняю..."; }
        const updated = await request(`/supplier/catalog/${itemId}`, { method: "PATCH", body: JSON.stringify(body) });
        const idx = state.data.supplierPortal.myCatalog.findIndex((i) => String(i.id) === String(itemId));
        if (idx >= 0) state.data.supplierPortal.myCatalog[idx] = updated;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при сохранении");
        if (btn) { btn.disabled = false; btn.textContent = "Сохранить"; }
      }
    });
  });

  // Toggle active
  document.querySelectorAll("[data-catalog-toggle]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.catalogToggle;
      const newActive = btn.dataset.catalogActive !== "true";
      try {
        btn.disabled = true;
        const updated = await request(`/supplier/catalog/${id}`, { method: "PATCH", body: JSON.stringify({ is_active: newActive }) });
        const idx = state.data.supplierPortal.myCatalog.findIndex((i) => String(i.id) === String(id));
        if (idx >= 0) state.data.supplierPortal.myCatalog[idx] = updated;
        render();
      } catch (err) {
        alert(err.message || "Ошибка");
        btn.disabled = false;
      }
    });
  });

  // Delete
  document.querySelectorAll("[data-catalog-delete]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Удалить позицию из каталога?")) return;
      const id = btn.dataset.catalogDelete;
      try {
        btn.disabled = true;
        await request(`/supplier/catalog/${id}`, { method: "DELETE" });
        state.data.supplierPortal.myCatalog = state.data.supplierPortal.myCatalog.filter((i) => String(i.id) !== String(id));
        render();
      } catch (err) {
        alert(err.message || "Ошибка при удалении");
        btn.disabled = false;
      }
    });
  });

  // Catalog item photo upload
  document.querySelectorAll("[data-catalog-upload-image]").forEach((input) => {
    input.addEventListener("change", async (e) => {
      const id = input.dataset.catalogUploadImage;
      const file = e.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("file", file);
      try {
        const label = input.closest("label");
        if (label) label.textContent = "Загрузка...";
        const result = await fetch(`${API}/supplier/catalog/${id}/image/upload`, {
          method: "POST",
          headers: { Authorization: `Bearer ${el("auth-token").value.trim()}` },
          body: formData,
        });
        if (!result.ok) {
          const err = await result.json().catch(() => ({}));
          throw new Error(err?.detail?.message || "Ошибка загрузки");
        }
        const data = await result.json();
        const idx = state.data.supplierPortal.myCatalog.findIndex((i) => String(i.id) === String(id));
        if (idx >= 0) state.data.supplierPortal.myCatalog[idx].image_url = data.image_url;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при загрузке фото");
      }
    });
  });

  // Catalog item photo delete
  document.querySelectorAll("[data-catalog-del-image]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Удалить фото этого товара?")) return;
      const id = btn.dataset.catalogDelImage;
      try {
        btn.disabled = true;
        await request(`/supplier/catalog/${id}/image`, { method: "DELETE" });
        const idx = state.data.supplierPortal.myCatalog.findIndex((i) => String(i.id) === String(id));
        if (idx >= 0) state.data.supplierPortal.myCatalog[idx].image_url = null;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при удалении фото");
        btn.disabled = false;
      }
    });
  });

  // Respond to marketplace inquiries
  el("supplier-inquiry-source-filter")?.addEventListener("change", async (event) => {
    state.ui.supplierInquirySourceFilter = event.target.value || "all";
    state.data.supplierPortal.inquiries = (await request(supplierInquiriesPath()).catch(() => ({ items: [] }))).items || [];
    render();
  });
  el("supplier-inquiry-status-filter")?.addEventListener("change", async (event) => {
    state.ui.supplierInquiryStatusFilter = event.target.value || "all";
    state.data.supplierPortal.inquiries = (await request(supplierInquiriesPath()).catch(() => ({ items: [] }))).items || [];
    render();
  });
  ["supplier-inquiry-filter-reset", "supplier-inquiry-empty-reset"].forEach((id) => {
    el(id)?.addEventListener("click", async () => {
      state.ui.supplierInquirySourceFilter = "all";
      state.ui.supplierInquiryStatusFilter = "all";
      state.data.supplierPortal.inquiries = (await request(supplierInquiriesPath()).catch(() => ({ items: [] }))).items || [];
      render();
    });
  });

  document.querySelectorAll(".inquiry-respond-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = form.dataset.inquiryId;
      const text = (form.querySelector("textarea").value || "").trim();
      if (!text) return;
      const btn = form.querySelector("button[type=submit]");
      try {
        if (btn) { btn.disabled = true; btn.textContent = "Отправляю..."; }
        const updated = await request(`/supplier/inquiries/${id}/respond`, {
          method: "POST",
          body: JSON.stringify({ response_text: text }),
        });
        const idx = state.data.supplierPortal.inquiries.findIndex((i) => String(i.id) === String(id));
        if (idx >= 0) state.data.supplierPortal.inquiries[idx] = updated;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при отправке ответа");
        if (btn) { btn.disabled = false; btn.textContent = "Отправить ответ"; }
      }
    });
  });

  // Create shipment from inquiry button
  document.querySelectorAll("[data-create-shipment-inq]").forEach((btn) => {
    btn.addEventListener("click", () => {
      try {
        const inq = JSON.parse(btn.dataset.createShipmentInq);
        showShipmentFromInquiryModal(inq);
      } catch (_) {}
    });
  });

  // Review reply forms
  document.querySelectorAll(".review-reply-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const reviewId = form.dataset.reviewId;
      const text = (form.querySelector("textarea").value || "").trim();
      if (!text) return;
      const btn = form.querySelector("button[type=submit]");
      try {
        if (btn) { btn.disabled = true; btn.textContent = "Отправляю..."; }
        const updated = await request(`/supplier/reviews/${reviewId}/reply`, {
          method: "POST",
          body: JSON.stringify({ reply_text: text }),
        });
        const idx = (state.data.supplierPortal.reviews || []).findIndex((r) => String(r.id) === String(reviewId));
        if (idx >= 0) state.data.supplierPortal.reviews[idx] = updated;
        render();
      } catch (err) {
        alert(err.message || "Ошибка при отправке ответа");
        if (btn) { btn.disabled = false; btn.textContent = "Отправить ответ"; }
      }
    });
  });
}

async function placeSupplierBid(auctionId) {
  const input = document.querySelector(`[data-supplier-bid-input="${auctionId}"]`);
  const amount = Number(input?.value);
  if (!amount || amount <= 0) return;
  try {
    await request(`/auctions/${auctionId}/bids`, {
      method: "POST",
      body: JSON.stringify({ supplier_id: state.auth.supplierId, bid_amount: amount }),
    });
    await loadSupplierAuctions();
    await loadSupplierBids(auctionId);
    render();
  } catch (err) {
    showAlert(err.message);
  }
}

async function loadSupplierAuctions() {
  const data = await request("/auctions").catch(() => ({ items: [] }));
  state.data.supplierPortal.auctions = data.items || data || [];
}

async function loadSupplierBids(auctionId) {
  const bids = await request(`/auctions/${auctionId}/bids`).catch(() => []);
  state.data.supplierPortal.myBids[auctionId] = bids;
}

async function loadSupplierPortalData() {
  const supplierId = state.auth.supplierId;
  const auctions = await request(`/auctions?status=active&limit=50`).catch(() => ({ items: [] }));
  state.data.supplierPortal.auctions = auctions.items || [];
  if (supplierId && state.data.supplierPortal.auctions.length) {
    for (const a of state.data.supplierPortal.auctions) {
      await loadSupplierBids(a.id);
    }
  }
  if (supplierId) {
    state.data.supplierPortal.priceHistory = (await request(`/suppliers/${supplierId}/price-history?limit=50`).catch(() => ({ items: [] }))).items || [];
    state.data.supplierPortal.shipments = (await request(`/shipments?supplier_id=${supplierId}`).catch(() => ({ items: [] }))).items || [];
    state.data.supplierPortal.reviews = await request(`/suppliers/${supplierId}/reviews`).catch(() => []);
    state.data.supplierPortal.profile = await request(`/supplier/me`).catch(() => null);
    state.data.supplierPortal.myCatalog = (await request(`/supplier/catalog`).catch(() => ({ items: [] }))).items || [];
    state.data.supplierPortal.inquiries = (await request(supplierInquiriesPath()).catch(() => ({ items: [] }))).items || [];
    state.data.supplierPortal.stats = await request(`/supplier/stats`).catch(() => null);
    state.data.supplierPortal.orders = await request(`/supplier/orders?limit=100`).catch(() => ({ items: [], total: 0 }));
    state.data.supplierPortal.catalogAnalytics = await request(`/supplier/catalog/analytics`).catch(() => []);
    state.data.supplierPortal.verificationDocs = await request(`/supplier/verification-docs`).catch(() => []);
  }
  state.data.supplierPortal.myApplications = await request(`/supplier/my-applications`).catch(() => []);
  updateBecomeSupplierButton();
}

function updateBecomeSupplierButton() {
  const btn = el("become-supplier-button");
  if (!btn || btn.style.display === "none") return;
  const apps = state.data.supplierPortal.myApplications || [];
  const latest = apps[0];
  if (!latest) return;
  const STATUS_LABELS = {
    pending: "⏳ Заявка на рассмотрении",
    needs_changes: "✏️ Требуются исправления",
    rejected: "❌ Заявка отклонена",
    approved: null,
  };
  const label = STATUS_LABELS[latest.status];
  if (!label) return;
  btn.textContent = label;
  btn.classList.remove("primary");
  btn.classList.add(latest.status === "rejected" ? "danger" : "secondary");
}

async function toggleSupplierMode() {
  state.ui.supplierMode = !state.ui.supplierMode;
  if (state.ui.supplierMode) {
    // Supplier access requires Tetis SSO — no separate login
    if (state.auth.source !== "tetis" && state.auth.source !== "login") {
      state.ui.supplierMode = false;
      return;
    }
    // Default to "profile" (shows dashboard stats) for approved suppliers, "my-applications" for applicants
    const pendingInq = (state.data.supplierPortal.inquiries || []).filter((i) => i.status === "pending").length;
    state.ui.supplierView = state.auth.supplierId
      ? (pendingInq > 0 ? "inquiries" : "profile")
      : "my-applications";
    render();
    await loadSupplierPortalData();
  }
  render();
}

function renderAuthBlocked() {
  return `
    <div class="panel span-12 auth-blocked" role="status">
      <h2>${t("Доступ временно ограничен")}</h2>
      <p>${escapeHtml(state.auth.blockedMessage)}</p>
      <button class="secondary" type="button" data-action="reload">Проверить снова</button>
    </div>
  `;
}

function applyDensity() {
  document.body.classList.toggle("compact", state.ui.density === "compact");
  const densityButton = el("density-button");
  densityButton.textContent = state.ui.density === "compact" ? "Обычный вид" : "Компактный вид";
  densityButton.setAttribute(
    "aria-pressed",
    state.ui.density === "compact" ? "true" : "false",
  );
}

async function loadAll() {
  // Standalone (non-tetis, non-/sklad) требует логин перед загрузкой
  const _isStandaloneGuard = !(
    window.location.pathname.startsWith("/sklad") ||
    window.location.hostname === "tetis1.kz" ||
    window.location.hostname === "www.tetis1.kz"
  );
  if (_isStandaloneGuard && state.auth.source !== "login") {
    await showLoginScreen();
    return;
  }
  try {
    console.log("[SKLAD_DBG]",{src:state.auth.source,hasLogin:!!state.auth.loginToken,hasAuthTok:!!el("auth-token").value.trim(),qormed:!!localStorage.getItem("qormed_token"),supToken:!!localStorage.getItem("sklad_supplier_token")});
    state.loadWarnings = [];
    state.auth.blockedMessage = "";
    if (state.auth.source === "login" && state.auth.loginToken) {
      el("auth-token").value = state.auth.loginToken;
    } else if (!el("auth-token").value.trim()) {
      // Restore cached sklad JWT from session (avoids re-exchange when Qtrix access token has expired)
      try {
        const _cached = sessionStorage.getItem("sklad_tetis_session");
        if (_cached) {
          const _pb64 = _cached.split(".")[1];
          const _p = JSON.parse(atob(_pb64.replace(/-/g,"+").replace(/_/g,"/")));
          if (_p.exp && _p.exp > Math.floor(Date.now() / 1000) + 60) {
            el("auth-token").value = _cached;
            state.auth.source = "tetis";
          } else {
            sessionStorage.removeItem("sklad_tetis_session");
          }
        }
      } catch(_) {}
      if (!el("auth-token").value.trim()) {
        await requestSkladTokenFromTetis();
        // If exchange failed, continue — /me will 401 and we'll show a banner
      }
    }
    let profile = await request("/me");
    // If supplier access was approved since last login, silently re-exchange the tetis token
    // so the new JWT reflects the updated supplier_id without requiring manual re-login
    if (profile.access_needs_refresh && state.auth.source === "tetis") {
      const ok = await requestSkladTokenFromTetis();
      if (ok) profile = await request("/me");
    }
    applyActorProfile(profile);
    const [health, readiness, categories, suppliers, warehouses, productUnits, products] = await Promise.all([
      request("/health"),
      request("/health/ready"),
      request("/categories"),
      request("/suppliers"),
      request("/warehouses"),
      loadOptional("Единицы измерения", request("/product-units"), ["шт", "уп", "рулон", "флакон", "бут", "ампула"]),
      request("/products?limit=5000"),
    ]);
    state.data.health = health;
    state.data.readiness = readiness;
    state.data.categories = categories;
    state.data.suppliers = suppliers;
    state.data.warehouses = warehouses;
    state.data.productUnits = productUnits;
    state.data.products = products;
    reconcileWarehouseScope();
    const wf = warehouseFilterParam();
    const query = wf ? `?${wf}` : "";

    const [balances, batches, batchRecalls, reservations, quarantineReviews, purchaseRequests, notifications, audit, documents, inventorySessions, movements, repackings, analytics, abcXyzRuns, sensorDevices, sensorReadings, repackTemplates, procedureConsumptionTemplates, supplierApplications] = await Promise.all([
      request(`/balances${query ? `${query}&limit=100` : "?limit=100"}`),
      request(`/batches${query ? `${query}&limit=100` : "?limit=100"}`),
      loadOptional("Отзывы партий", request("/batch-recalls?limit=200"), { items: [], total: 0 }),
      loadOptional("Бронирование", request(`/reservations${query ? `${query}&limit=100` : "?limit=100"}`), []),
      loadOptional("Карантинные проверки", request(`/quarantine-reviews${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Заявки на закупку", request(`/purchase-requests${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      request(`/notifications${query ? `${query}&limit=100` : "?limit=100"}`),
      hasPermission("audit:read")
        ? loadOptional("Журнал действий", request(`/audit-log${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 })
        : Promise.resolve({ items: [], total: 0 }),
      loadOptional("Документы", request(`/stock-documents${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Инвентаризация", request(`/inventory-sessions${query ? `${query}&limit=100` : "?limit=100"}`), []),
      loadOptional("Движения", request(`/stock-movements${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Журнал фасовки", request(`/batch-transformations${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Аналитика", request(`/analytics/abc-xyz${query ? `${query}&days=90` : "?days=90"}`), { items: [], analysis_days: 90, warehouse_id: null, generated_at: null }),
      loadOptional("История ABC/XYZ", request(`/analytics/abc-xyz/history${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Датчики условий хранения", request(`/sensor-devices${query ? `${query}&limit=100` : "?limit=100"}`), []),
      loadOptional("Журнал условий хранения", request(`/sensor-readings${query ? `${query}&limit=100` : "?limit=100"}`), { items: [], total: 0 }),
      loadOptional("Шаблоны фасовки", request("/repack-templates"), []),
      loadOptional("Шаблоны расхода по процедурам", request("/procedure-consumption-templates"), []),
      hasPermission("admin:users")
        ? loadOptional("Заявки поставщиков", request("/tetis/supplier-applications?limit=200"), { items: [], total: 0 })
        : Promise.resolve({ items: [], total: 0 }),
    ]);
    state.data.balances = balances;
    state.data.batches = batches;
    state.data.batchRecalls = batchRecalls;
    try {
      state.data.recallStats = await request("/recalls/stats");
    } catch (_) { state.data.recallStats = null; }
    state.data.reservations = reservations;
    state.data.quarantineReviews = quarantineReviews;
    state.data.purchaseRequests = pageItems(purchaseRequests);
    state.data.notifications = notifications;
    state.data.audit = audit;
    state.data.documents = pageItems(documents);
    state.data.inventorySessions = inventorySessions;
    state.data.movements = pageItems(movements);
    state.data.repackings = repackings;
    state.data.analytics = analytics;
    state.data.abcXyzRuns = abcXyzRuns;
    state.data.sensorDevices = sensorDevices;
    state.data.sensorReadings = sensorReadings;
    state.data.repackTemplates = repackTemplates;
    state.data.procedureConsumptionTemplates = procedureConsumptionTemplates;
    state.data.supplierApplications = supplierApplications;
    // Load supplier map data
    if (hasPermission("audit:read")) {
      try {
        state.data.supplierMap = await request("/suppliers/map");
      } catch (_) { state.data.supplierMap = []; }
      try {
        state.data.shipments = await request("/shipments?limit=20");
      } catch (_) { state.data.shipments = { items: [], total: 0 }; }
    }
    // Load marketplace catalog (available to all)
    try {
      state.data.marketplace = await request("/marketplace/catalog?limit=50");
      state.data.marketplaceCategories = await request("/marketplace/catalog/categories");
      state.data.catalogTaxonomy = await request("/catalog-categories").catch(() => []);
    } catch (_) {
      state.data.marketplace = { items: [], total: 0 };
      state.data.marketplaceCategories = [];
    }
    // Load my sent inquiries
    state.data.myInquiries = await request(myInquiriesPath()).catch(() => ({ items: [], total: 0 }));
    // Load cart
    state.data.cart = await request("/marketplace/cart").catch(() => ({ items: [], total_items: 0, total_amount: 0 }));
    // Load users if manager
    if (hasPermission("admin:users")) {
      try {
        state.data.users = await request("/users");
      } catch (_) {
        state.data.users = [];
      }
    }
    // Load auctions if manager
    if (hasPermission("audit:read")) {
      try {
        state.data.auctions = await request("/auctions?limit=50");
      } catch (_) { state.data.auctions = { items: [], total: 0 }; }
    }
    // Load pending supplier reviews for moderation
    if (hasPermission("admin:users")) {
      try {
        state.data.pendingReviews = await request("/supplier-reviews?status=pending");
      } catch (_) { state.data.pendingReviews = []; }
      try {
        state.data.jobStatus = await request("/admin/jobs");
      } catch (_) { state.data.jobStatus = null; }
    }
    // Load pending controlled writeoffs (ПКУ двойная подпись)
    try {
      state.data.pendingControlledWriteoffs = await request(`/controlled-writeoffs/pending${query ? query + "&limit=200" : "?limit=200"}`);
    } catch (_) { state.data.pendingControlledWriteoffs = []; }
    // Load controlled substance limits and violations for selected warehouse
    {
      const wfPku = warehouseFilterParam();
      const wIdPku = wfPku ? new URLSearchParams(wfPku).get("warehouse_id") : null;
      if (wIdPku) {
        try { state.data.controlledLimits = await request(`/controlled-substances/limits?warehouse_id=${wIdPku}`); } catch (_) { state.data.controlledLimits = []; }
        try { state.data.controlledViolations = await request(`/controlled-substances/limits/violations?warehouse_id=${wIdPku}`); } catch (_) { state.data.controlledViolations = []; }
      }
    }
    el("api-status").className = "status-dot ok";
    el("api-status").textContent = t("Система доступна");
  } catch (error) {
    if (error instanceof AuthRequiredError) {
      state.auth.blockedMessage = error.message || "Сервер требует вход";
      el("api-status").className = "status-dot bad";
      el("api-status").textContent = "Ошибка входа";
      if (state.auth.source === "login") {
        try { localStorage.removeItem("sklad_supplier_token"); } catch(_) {}
        state.auth.loginToken = "";
        state.auth.source = "demo";
        el("auth-token").value = "";
      }
      await showLoginScreen();
    } else {
      el("api-status").className = "status-dot bad";
      el("api-status").textContent = t("Нет связи с сервером");
      showAlert(error.message, "error");
    }
  }
  render();
  if (!state.auth.blockedMessage) {
    connectRealtime();
  }
}

function scheduleRealtimeRefresh() {
  if (realtimeRefreshTimer) return;
  realtimeRefreshTimer = window.setTimeout(async () => {
    realtimeRefreshTimer = null;
    await loadAll();
  }, 350);
}

function connectRealtime() {
  const wf = warehouseFilterParam();
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const authToken = el("auth-token").value.trim();
  const params = new URLSearchParams(wf);
  if (authToken) params.set("access_token", authToken);
  const query = params.toString();
  const targetUrl = `${protocol}//${window.location.host}${API}/ws/balances${query ? `?${query}` : ""}`;
  if (balanceSocket && balanceSocket.url === targetUrl && balanceSocket.readyState <= WebSocket.OPEN) return;
  if (balanceSocket) balanceSocket.close();

  state.realtime = "connecting";
  const socket = new WebSocket(targetUrl);
  balanceSocket = socket;
  socket.addEventListener("open", () => {
    if (balanceSocket !== socket) return;
    state.realtime = "online";
    render();
  });
  socket.addEventListener("message", (event) => {
    const payload = parseJson(event.data, {});
    if ([
      "stock.balance.updated",
      "stock.transfer.posted",
      "stock.return.posted",
      "inventory.posted",
      "batch.recalled",
      "batch.status.updated",
      "sensor.reading.created",
      "notifications.updated",
    ].includes(payload.event_type)) {
      scheduleRealtimeRefresh();
    }
    if (["auction_bid", "auction_started", "auction_closed"].includes(payload.event_type)) {
      const auctionId = payload.data && payload.data.auction_id;
      if (state.view === "auctions") {
        if (payload.event_type === "auction_bid" && auctionId) {
          // update current price in-place without full reload
          const priceEl = document.querySelector(`[data-auction-price="${auctionId}"]`);
          if (priceEl && payload.data.bid_amount != null) {
            priceEl.textContent = Number(payload.data.bid_amount).toLocaleString("ru-RU", {minimumFractionDigits:2}) + " ₸";
            priceEl.classList.add("realtime-flash");
            setTimeout(() => priceEl.classList.remove("realtime-flash"), 1200);
          }
        }
        scheduleRealtimeRefresh();
      }
    }
  });
  socket.addEventListener("close", () => {
    if (balanceSocket !== socket) return;
    state.realtime = "offline";
    render();
  });
  socket.addEventListener("error", () => {
    if (balanceSocket !== socket) return;
    state.realtime = "offline";
    render();
  });
}

function bindSubmit(id, handler, confirmMessage = null) {
  const node = document.getElementById(id);
  if (!node) return;
  node.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (node.dataset.pending === "true") return;
    const submitButton = node.querySelector('button[type="submit"]');
    try {
      clearFormError(node);
      const payload = collect(node);
      const controlledIssues = node.querySelector("input[name='patient_id'], input[name='doctor_id'], input[name='medical_record_no']")
        ? applyControlledWriteoffRequirements(node, payload)
        : [];
      if (controlledIssues.length) {
        showFormError(node, controlledWriteoffMessage());
        return;
      }
      const message = typeof confirmMessage === "function" ? confirmMessage(payload) : confirmMessage;
      if (message && !(await confirmAction(message))) return;
      node.dataset.pending = "true";
      setPending(submitButton, true);
      await handler(payload);
      showAlert("Операция выполнена");
      await loadAll();
    } catch (error) {
      showFormError(node, error.message);
      showAlert(error.message, "error");
    } finally {
      delete node.dataset.pending;
      setPending(submitButton, false);
    }
  });
}

function updateBatchAwareForm(formElement, { autofill = false } = {}) {
  const batchId = formElement.elements.batch_id?.value;
  const warehouseField = formElement.querySelector("[data-batch-warehouse-field]");
  if (autofill && batchId && warehouseField) {
    const balance = balanceForBatch(batchId);
    if (balance) warehouseField.value = String(balance.warehouse_id);
  }
  const warehouseId = warehouseField?.value || null;
  const summary = formElement.querySelector("[data-selected-batch-summary]");
  if (summary) summary.innerHTML = selectedBatchSummaryHtml(batchId, warehouseId);
  applyControlledWriteoffRequirements(formElement);
}

function bindBatchAwareForms() {
  document.querySelectorAll("form[data-batch-aware]").forEach((formElement) => {
    updateBatchAwareForm(formElement);
    formElement.querySelectorAll("select[name='batch_id'], [data-batch-warehouse-field]").forEach((input) => {
      input.addEventListener("change", () => {
        updateBatchAwareForm(formElement, { autofill: input.name === "batch_id" });
      });
    });
  });
}

function bindControlledWriteoffForms() {
  ["writeoff-form", "tablet-writeoff-form", "fefo-form"].forEach((id) => {
    const formElement = document.getElementById(id);
    if (!formElement) return;
    applyControlledWriteoffRequirements(formElement);
    formElement.querySelectorAll("select[name='batch_id'], select[name='product_id'], input[name='patient_id'], input[name='doctor_id'], input[name='medical_record_no'], input[name='second_approver_id']").forEach((input) => {
      input.addEventListener("change", () => applyControlledWriteoffRequirements(formElement));
      input.addEventListener("input", () => applyControlledWriteoffRequirements(formElement));
    });
  });
}

function bindActions() {
  document.querySelectorAll("[data-clear-search]").forEach((button) => {
    button.addEventListener("click", () => {
      state.ui.search = "";
      el("global-search").value = "";
      render();
    });
  });

  document.querySelectorAll("[data-go-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = safeViewTarget(button.dataset.goView);
      render();
    });
  });

  document.querySelectorAll("[data-batch-detail]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        setPending(button, true, "Открываем");
        await showBatchTraceability(button.dataset.batchDetail);
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });

  document.querySelectorAll("[data-export-report]").forEach((button) => {
    button.addEventListener("click", () => {
      exportReport(button.dataset.exportReport);
    });
  });
  document.querySelectorAll("[data-print-product-label]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Готовим");
        const pid = Number(button.dataset.printProductLabel);
        const result = await request("/products/barcode-labels", {
          method: "POST",
          body: JSON.stringify({ product_ids: [pid] }),
        });
        downloadText(`sklad-product-${pid}-label.zpl`, result.zpl);
        // Mark reprinted
        try { await request(`/products/${pid}/mark-reprinted`, { method: "POST" }); } catch (_) {}
        const prod = state.data.products.find(p => p.id === pid);
        if (prod) prod.label_needs_reprint = false;
        showAlert("Этикетка подготовлена (ZPL)");
        render();
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-show-barcode]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Загрузка");
        const pid = button.dataset.showBarcode;
        const result = await request(`/products/${pid}/barcode-label`);
        const overlay = document.createElement("div");
        overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;display:flex;align-items:center;justify-content:center";
        overlay.innerHTML = `<div style="background:white;border-radius:8px;padding:1.5rem;max-width:420px;width:90%;box-shadow:0 20px 40px rgba(0,0,0,.3)">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.75rem">
            <div><b style="font-size:.95rem">${escapeHtml(result.name)}</b><br>
            <span style="font-size:.82rem;color:#6b7280">${escapeHtml(result.sku)} · ${escapeHtml(result.barcode)}</span></div>
            <button id="close-barcode-overlay" style="background:none;border:none;font-size:1.2rem;cursor:pointer;padding:0 .25rem">✕</button>
          </div>
          <div style="text-align:center;border:1px solid #e5e7eb;border-radius:4px;padding:.5rem;background:#fafafa">
            ${result.svg || `<span style="font-size:.85rem;color:#6b7280">${escapeHtml(result.barcode)}</span>`}
          </div>
          <div style="display:flex;gap:.5rem;margin-top:.75rem">
            <button id="download-zpl-btn" style="flex:1;padding:.4rem;background:#2563eb;color:white;border:none;border-radius:4px;cursor:pointer;font-size:.85rem">Скачать ZPL</button>
            <button id="close-barcode-btn" style="flex:1;padding:.4rem;background:#f3f4f6;border:1px solid #d1d5db;border-radius:4px;cursor:pointer;font-size:.85rem">Закрыть</button>
          </div>
        </div>`;
        document.body.appendChild(overlay);
        overlay.querySelector("#close-barcode-overlay")?.addEventListener("click", () => overlay.remove());
        overlay.querySelector("#close-barcode-btn")?.addEventListener("click", () => overlay.remove());
        overlay.querySelector("#download-zpl-btn")?.addEventListener("click", () => {
          downloadText(`sklad-product-${pid}-label.zpl`, result.zpl);
        });
        overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-print-batch-price-label]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Готовим");
        const result = await request(`/batches/${button.dataset.printBatchPriceLabel}/price-label?symbology=ean13`);
        downloadText(`sklad-batch-${button.dataset.printBatchPriceLabel}-price-label.zpl`, result.zpl);
        showAlert("Ценник подготовлен");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-print-receipt-batch]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const batchId = btn.dataset.printReceiptBatch;
      setPending(btn, true, "...");
      try {
        const form = await request(`/batches/${batchId}/receipt-print-form`);
        const w = window.open("", "_blank", "width=800,height=600");
        w.document.write(receiptPrintHtml(form));
        w.document.close();
        w.focus();
        setTimeout(() => w.print(), 300);
      } catch(e) { showAlert(e.message, "error"); }
      setPending(btn, false);
    });
  });
  document.querySelectorAll("[data-export-price-history]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Выгружаем");
        const result = await request(`/suppliers/${button.dataset.exportPriceHistory}/price-history?limit=500`);
        if (!result.items.length) {
          showAlert("История цен поставщика пока пустая", "error");
          return;
        }
        downloadCsv("sklad-supplier-price-history.csv", [
          { label: "Дата", value: (row) => dateText(row.recorded_at) },
          { label: "Поставщик", key: "supplier_name" },
          { label: "Товар", key: "product_name" },
          { label: "SKU", key: "sku" },
          { label: "Партия", value: (row) => row.lot || "" },
          { label: "Цена", key: "unit_price" },
          { label: "Источник", key: "source" },
        ], result.items);
        showAlert("История цен выгружена");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-supplier-card]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Открываем");
        await showSupplierCard(button.dataset.supplierCard);
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-download-controlled-ledger]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Выгружаем");
        const query = warehouseFilterParam();
        const result = await request(`/controlled-substances/ledger/export${query ? `?${query}` : ""}`);
        downloadText(result.filename, result.csv, "text/csv;charset=utf-8");
        showAlert("Журнал ПКУ выгружен");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-download-repack-form]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Выгружаем");
        const result = await request(`/stock-documents/${button.dataset.downloadRepackForm}/repack-print-form`);
        downloadText(`sklad-repack-document-${button.dataset.downloadRepackForm}.csv`, result.csv, "text/csv;charset=utf-8");
        showAlert("Печатная форма фасовки выгружена");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-download-transfer-form]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Выгружаем");
        const result = await request(`/stock-documents/${button.dataset.downloadTransferForm}/transfer-print-form`);
        downloadText(`sklad-transfer-document-${button.dataset.downloadTransferForm}.csv`, result.csv, "text/csv;charset=utf-8");
        showAlert("Печатная форма перемещения выгружена");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-download-quarantine-protocol]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        setPending(button, true, "Выгружаем");
        const result = await request(`/quarantine-reviews/${button.dataset.downloadQuarantineProtocol}/protocol`);
        downloadText(`sklad-quarantine-review-${button.dataset.downloadQuarantineProtocol}.csv`, result.csv, "text/csv;charset=utf-8");
        showAlert("Протокол карантинной проверки выгружен");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-print-inventory]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        const session = selectedInventorySession();
        if (!session) return;
        setPending(button, true, "Готовим");
        const form = await request(`/inventory-sessions/${session.id}/print-form`);
        downloadText(`sklad-inventory-${session.id}-count-sheet.csv`, form.count_sheet_csv, "text/csv;charset=utf-8");
        showAlert("Печатная ведомость выгружена");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });
  document.querySelectorAll("[data-print-inventory-reconciliation]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        const session = selectedInventorySession();
        if (!session) return;
        setPending(button, true, "Готовим");
        const form = await request(`/inventory-sessions/${session.id}/print-form`);
        downloadText(`sklad-inventory-${session.id}-reconciliation.csv`, form.reconciliation_csv, "text/csv;charset=utf-8");
        showAlert("Сличительная ведомость выгружена");
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });

  document.querySelectorAll("[data-print-inventory-pdf]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        const sessionId = button.dataset.sessionId;
        if (!sessionId) return;
        setPending(button, true, "Готовим PDF");
        const query = warehouseFilterParam();
        const url = `${API}/inventory-sessions/${sessionId}/pdf${query ? "?" + query : ""}`;
        const resp = await fetch(url, { headers: headers() });
        if (!resp.ok) throw new Error(`Ошибка ${resp.status}`);
        const blob = await resp.blob();
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `inventory-${sessionId}.pdf`;
        a.click();
        URL.revokeObjectURL(a.href);
        showAlert("PDF ведомость скачана");
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });

  document.querySelectorAll("[data-approve-document]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        const document = state.data.documents.find((entry) => Number(entry.id) === Number(button.dataset.approveDocument));
        const title = document ? documentTitle(document) : `Документ #${button.dataset.approveDocument}`;
        if (!(await confirmAction(`Утвердить ${title}? После утверждения документ можно провести.`, { confirmText: "Утвердить" }))) return;
        setPending(button, true, "Утверждаем");
        await mutate(`/stock-documents/${button.dataset.approveDocument}/approve`, {
          document_id: Number(button.dataset.approveDocument),
        });
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(button, false);
      }
    });
  });

  document.querySelectorAll("[data-edit-catalog]").forEach((button) => {
    button.addEventListener("click", () => {
      showCatalogEditModal(button.dataset.editCatalog, button.dataset.editId);
    });
  });

  document.querySelectorAll("[data-delete-catalog]").forEach((button) => {
    button.addEventListener("click", () => {
      deleteCatalogEntry(button.dataset.deleteCatalog, button.dataset.deleteId, button);
    });
  });

  bindSubmit("product-form", (payload) => mutate("/products", normalizeProductPayload(payload)));
  bindSubmit("procedure-template-form", (payload) => {
    const items = (payload.items_raw || "")
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const [productId, quantity] = line.split(":").map((part) => part.trim());
        return { product_id: Number(productId), quantity };
      });
    return mutate("/procedure-consumption-templates", {
      mis_clinic_id: payload.mis_clinic_id,
      service_code: payload.service_code,
      name: payload.name,
      items,
    });
  });
  bindSubmit("category-form", (payload) => mutate("/categories", payload));
  bindSubmit("supplier-form", (payload) => mutate("/suppliers", normalizeSupplierPayload(payload)));
  bindSubmit("warehouse-form", (payload) => mutate("/warehouses", {
    ...payload,
    department: payload.department || null,
    tetis_org_id: payload.tetis_org_id || null,
    external_tetis_id: payload.external_tetis_id || null,
    mis_clinic_id: payload.mis_clinic_id || null,
    mis_room_id: payload.mis_room_id || null,
    storage_zone: payload.storage_zone || null,
    capacity_limit: payload.capacity_limit ? Number(payload.capacity_limit) : null,
    storage_conditions: payload.storage_conditions || null,
    responsible_person: payload.responsible_person || null,
  }));
  bindSubmit("receipt-form", (payload) => mutate("/receipts", { ...payload, quarantine: true }));
  bindSubmit("receipt-doc-form", async (payload) => {
    const { supplier_id, warehouse_id, external_ref, notes } = payload;
    const body = { supplier_id, warehouse_id, lines: receiptDocumentLinesPayload() };
    if (external_ref && external_ref.trim()) body.external_ref = external_ref.trim();
    if (notes && notes.trim()) body.notes = notes.trim();
    await mutate("/stock-documents/receipts", body);
    resetDocumentLines("receipt");
  });
  bindSubmit("writeoff-doc-form", async (payload) => {
    const { warehouse_id } = payload;
    await mutate("/stock-documents/write-offs", {
      warehouse_id,
      lines: writeoffDocumentLinesPayload(),
    });
    resetDocumentLines("writeoff");
  }, () => `Создать черновик списания на ${state.documentForms.writeoff.lines.length} строк?`);
  bindSubmit("fefo-form", (payload) => mutate("/write-offs/fefo", payload), (payload) => `Списать ${payload.quantity} по ближайшему сроку годности? Остатки на выбранном складе уменьшатся.`);
  bindSubmit("writeoff-form", (payload) => mutate("/write-offs", payload), (payload) => operationPreview("writeoff", payload));
  bindSubmit("tablet-writeoff-form", (payload) => mutate("/write-offs", payload), (payload) => operationPreview("writeoff", payload));
  bindSubmit("transfer-form", (payload) => mutate("/transfers", payload), (payload) => operationPreview("transfer", payload));

  // Repack template handlers
  document.querySelectorAll("[data-action='apply-repack-template']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sel = document.getElementById("repack-template-select");
      if (!sel || !sel.value) return;
      const tpl = state.data.repackTemplates.find((t) => String(t.id) === sel.value);
      if (!tpl) return;
      const form = document.getElementById("repacking-form");
      if (!form) return;
      const setField = (name, val) => {
        const el = form.querySelector(`[name="${name}"]`);
        if (el && val !== null && val !== undefined) { el.value = val; el.dispatchEvent(new Event("change")); }
      };
      setField("target_product_id", tpl.target_product_id);
      if (tpl.target_unit_price) setField("target_unit_price", tpl.target_unit_price);
      if (tpl.reason) setField("reason", tpl.reason);
      // Store conversion factors for quantity auto-calc when source quantity changes
      form.dataset.tplQtyFactor = tpl.quantity_factor;
      form.dataset.tplLossFactor = tpl.loss_factor;
      showAlert("Шаблон применён. Введите исходное количество — поля пересчитаются.", "ok");
    });
  });

  // Auto-calc target_quantity and loss_quantity from template factors
  document.querySelectorAll("#repacking-form [name='quantity']").forEach((input) => {
    input.addEventListener("input", () => {
      const form = document.getElementById("repacking-form");
      if (!form || !form.dataset.tplQtyFactor) return;
      const qty = parseFloat(input.value) || 0;
      const factor = parseFloat(form.dataset.tplQtyFactor) || 1;
      const lossFactor = parseFloat(form.dataset.tplLossFactor) || 0;
      const tgt = form.querySelector("[name='target_quantity']");
      const loss = form.querySelector("[name='loss_quantity']");
      if (tgt) tgt.value = (qty * factor).toFixed(3);
      if (loss) loss.value = (qty * lossFactor).toFixed(3);
    });
  });

  document.querySelectorAll("[data-action='save-repack-template']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const form = document.getElementById("repacking-form");
      if (!form) return;
      const get = (name) => form.querySelector(`[name="${name}"]`)?.value || "";
      const targetProductId = get("target_product_id");
      if (!targetProductId) { showAlert("Выберите товар результата перед сохранением шаблона.", "error"); return; }
      const srcQty = parseFloat(get("quantity")) || 1;
      const tgtQty = parseFloat(get("target_quantity")) || 1;
      const lossQty = parseFloat(get("loss_quantity")) || 0;
      const factor = srcQty > 0 ? (tgtQty / srcQty).toFixed(6) : "1";
      const lossFactor = srcQty > 0 ? (lossQty / srcQty).toFixed(6) : "0";
      const name = prompt(t("Название шаблона") + ":");
      if (!name || !name.trim()) return;
      try {
        const tpl = await request("/repack-templates", {
          method: "POST",
          body: JSON.stringify({
            name: name.trim(),
            target_product_id: parseInt(targetProductId),
            quantity_factor: parseFloat(factor),
            loss_factor: parseFloat(lossFactor),
            target_unit_price: get("target_unit_price") ? parseFloat(get("target_unit_price")) : null,
            reason: get("reason") || null,
          }),
        });
        state.data.repackTemplates = [...state.data.repackTemplates, tpl];
        showAlert(`Шаблон «${name}» сохранён.`, "ok");
        render();
      } catch (err) {
        showAlert("Не удалось сохранить шаблон: " + (err.message || err), "error");
      }
    });
  });

  bindSubmit("repacking-form", (payload) => mutate("/stock-documents/repack", normalizeRepackingPayload(payload)), (payload) => repackingPreview(payload));
  bindSubmit("department-return-form", (payload) => mutate("/returns/from-department", payload), (payload) => operationPreview("department-return", payload));
  bindSubmit("supplier-return-form", (payload) => mutate("/returns/to-supplier", payload), (payload) => operationPreview("supplier-return", payload));
  bindSubmit("batch-status-form", (payload) => {
    const batchId = payload.batch_id;
    delete payload.batch_id;
    return mutate(`/batches/${batchId}/status`, payload, "PATCH");
  }, (payload) => `Изменить статус партии #${payload.batch_id} на “${humanStatus(payload.status)}”?`);
  bindSubmit("batch-recall-form", (payload) => {
    const batchId = payload.batch_id;
    return mutate(`/batches/${batchId}/recall`, {
      reason: payload.reason,
      source: payload.source || "manual",
      reference: payload.reference || null,
    });
  }, (payload) => recallPreview(payload));

  document.querySelectorAll("[data-action='unblock-batch']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const batchId = btn.dataset.batchId;
      const reason = prompt("Причина снятия блокировки:");
      if (reason === null) return;
      try {
        setPending(btn, true, "...");
        await request(`/batches/${batchId}/unblock`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ reason }),
        });
        showAlert(`Партия #${batchId} разблокирована`, "success");
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  bindSubmit("reservation-form", (payload) => mutate("/reservations", payload), (payload) => `Зарезервировать партию #${payload.batch_id} в количестве ${payload.quantity}?`);
  bindSubmit("purchase-request-form", (payload) => mutate("/purchase-requests", payload), (payload) => `Создать заявку на закупку товара #${payload.product_id} в количестве ${payload.quantity}?`);
  bindSubmit("inventory-form", (payload) => {
    const prepared = {
      warehouse_id: payload.warehouse_id,
      category_ids: payload.category_id ? [Number(payload.category_id)] : [],
      responsible_ids: String(payload.responsible_ids || "")
        .split(",")
        .map((value) => value.trim())
        .filter(Boolean),
    };
    return mutate("/inventory-sessions", prepared);
  }, (payload) => `Начать инвентаризацию склада #${payload.warehouse_id} и заблокировать движения?`);
  bindSubmit("inventory-action-form", (payload) => mutate(`/inventory-sessions/${payload.session_id}/post`, { session_id: payload.session_id }), (payload) => inventoryCompletionPreview(payload.session_id));
  bindSubmit("sensor-device-form", (payload) => mutate("/sensor-devices", {
    ...payload,
    serial_number: payload.serial_number || null,
    min_temperature_c: payload.min_temperature_c || null,
    max_temperature_c: payload.max_temperature_c || null,
    min_humidity_percent: payload.min_humidity_percent || null,
    max_humidity_percent: payload.max_humidity_percent || null,
  }));
  bindSubmit("sensor-reading-form", (payload) => {
    if (!payload.temperature_c && !payload.humidity_percent) {
      throw new Error("Введите температуру или влажность.");
    }
    return mutate("/sensor-readings", {
      ...payload,
      temperature_c: payload.temperature_c || null,
      humidity_percent: payload.humidity_percent || null,
      raw_payload: payload.raw_payload || "ручной ввод",
    });
  }, (payload) => `Сохранить показание датчика #${payload.device_id}?`);

  bindBatchAwareForms();
  bindControlledWriteoffForms();

  document.querySelectorAll("[data-doc-header-field]").forEach((input) => {
    input.addEventListener("change", () => {
      state.documentForms[input.dataset.docLineKind][input.dataset.docHeaderField] = input.value;
    });
  });
  document.querySelectorAll("[data-doc-line-field]").forEach((input) => {
    input.addEventListener("input", () => {
      const index = Number(input.dataset.docLineIndex);
      const lines = state.documentForms[input.dataset.docLineKind].lines;
      lines[index][input.dataset.docLineField] = input.value;
    });
    input.addEventListener("change", () => {
      const index = Number(input.dataset.docLineIndex);
      const lines = state.documentForms[input.dataset.docLineKind].lines;
      lines[index][input.dataset.docLineField] = input.value;
    });
  });
  document.querySelectorAll("[data-doc-line-add]").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.docLineAdd === "receipt") {
        state.documentForms.receipt.lines.push(newReceiptDocumentLine());
      }
      if (button.dataset.docLineAdd === "writeoff") {
        state.documentForms.writeoff.lines.push(newWriteoffDocumentLine());
      }
      render();
    });
  });
  document.querySelectorAll("[data-doc-line-remove]").forEach((button) => {
    button.addEventListener("click", () => {
      const kind = button.dataset.docLineRemove;
      const lines = state.documentForms[kind].lines;
      if (lines.length <= 1) return;
      lines.splice(Number(button.dataset.docLineIndex), 1);
      render();
    });
  });

  document.querySelectorAll("[data-release]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        if (!(await confirmAction(`Снять бронь #${button.dataset.release}? Товар снова станет доступным для выдачи.`))) return;
        setPending(button, true);
        await mutate(`/reservations/${button.dataset.release}/release`, { reservation_id: Number(button.dataset.release) });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-use-reservation]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        if (!(await confirmAction(`Использовать резерв #${button.dataset.useReservation}? Зарезервированное количество будет выдано со склада.`))) return;
        setPending(button, true, "Используем");
        await mutate(`/reservations/${button.dataset.useReservation}/use`, {
          reservation_id: Number(button.dataset.useReservation),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-purchase-status]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      const nextStatus = button.dataset.purchaseNextStatus;
      const statusText = nextStatus === "ordered" ? "пометить как заказанную" : "отменить";
      try {
        if (!(await confirmAction(`Заявку #${button.dataset.purchaseStatus} ${statusText}?`))) return;
        setPending(button, true);
        await request(`/purchase-requests/${button.dataset.purchaseStatus}`, {
          method: "PATCH",
          body: JSON.stringify({ status: nextStatus }),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });

  // Gov procurement advance
  document.querySelectorAll("[data-gov-advance]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (btn.disabled) return;
      const reqId = btn.dataset.govAdvance;
      const status = btn.dataset.govStatus;
      if (status === "closed") {
        const text = prompt("Введите текст фидбэка (оценка поставщика):");
        if (!text) return;
        const rating = parseInt(prompt("Оценка (1-5):") || "5", 10);
        try {
          setPending(btn, true);
          await request(`/purchase-requests/${reqId}/gov-feedback`, {
            method: "POST",
            body: JSON.stringify({ feedback_text: text, rating: Math.max(1, Math.min(5, rating || 5)) }),
          });
          state.data.purchaseRequests = await request("/purchase-requests").catch(() => state.data.purchaseRequests);
          render();
        } catch (err) { showAlert(err.message, "error"); }
        finally { setPending(btn, false); }
      } else {
        const labels = { demand: "перевести в приём", accepting: "закрыть" };
        if (!(await confirmAction(`Гос. закупка #${reqId}: ${labels[status] || "продвинуть"}?`))) return;
        try {
          setPending(btn, true);
          await request(`/purchase-requests/${reqId}/gov-advance`, { method: "POST" });
          state.data.purchaseRequests = await request("/purchase-requests").catch(() => state.data.purchaseRequests);
          render();
        } catch (err) { showAlert(err.message, "error"); }
        finally { setPending(btn, false); }
      }
    });
  });

  // Escrow actions (reserve / release / refund) from my-inquiries (buyer side)
  document.querySelectorAll("[data-escrow-action]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (btn.disabled) return;
      const inquiryId = btn.dataset.escrowAction;
      const action = btn.dataset.action;
      const labels = { reserve: "зарезервировать средства (escrow)", release: "подтвердить получение и освободить escrow", refund: "вернуть средства (refund)" };
      if (!(await confirmAction(`Escrow: ${labels[action] || action}?`))) return;
      try {
        setPending(btn, true);
        await request(`/marketplace/my-inquiries/${inquiryId}/purchase-order/escrow`, {
          method: "POST",
          body: JSON.stringify({ action }),
        });
        showAlert(action === "release" ? "Escrow освобождён. Средства перечислены поставщику." : action === "reserve" ? "Средства зарезервированы." : "Средства возвращены.", "ok");
        state.data.myInquiries = await request(myInquiriesPath()).catch(() => state.data.myInquiries);
        render();
      } catch (err) { showAlert(err.message, "error"); }
      finally { setPending(btn, false); }
    });
  });

  // Show marketplace offers for a product from the purchase requests table
  document.querySelectorAll("[data-show-pr-offers]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const productId = Number(btn.dataset.showPrOffers);
      const purchaseRequestId = btn.dataset.prId ? Number(btn.dataset.prId) : null;
      // Find the nearest offers panel — in purchase-requests, balances, or recommendations
      const panel = document.getElementById("pr-offers-panel") || document.getElementById("pr-offers-panel-balances");
      if (!panel) return;
      const offers = findMarketplaceOffersForProduct(productId);
      const productName = rawNameById("products", productId);
      if (!offers.length) {
        panel.style.display = "none";
        return;
      }
      panel.style.display = "block";
      panel.innerHTML = `
        <div class="panel">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <strong>📦 Предложения поставщиков: «${escapeHtml(productName)}»</strong>
            <button class="secondary" style="font-size:.78rem" id="pr-offers-close">✕ Закрыть</button>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px">
            ${offers.map((item) => `
              <div style="border:1px solid var(--line,#eee);border-radius:8px;padding:12px">
                <div style="font-weight:600;margin-bottom:4px">${escapeHtml(item.supplier_name)}</div>
                <div style="font-size:.82rem;color:var(--muted)">${escapeHtml(item.supplier_city || "")} ${item.supplier_phone ? `· ${escapeHtml(item.supplier_phone)}` : ""}</div>
                <div style="margin:8px 0;font-size:1.1rem;font-weight:700;color:var(--accent)">${fmtMoneyKzt(item.unit_price)} тг<span style="font-size:.8rem;font-weight:400;color:var(--muted)">/${escapeHtml(item.unit)}</span></div>
                <div style="font-size:.8rem;color:var(--muted);margin-bottom:8px">
                  ${item.stock_qty != null ? `В наличии: ${item.stock_qty} · ` : ""}
                  ${item.delivery_days || item.supplier_delivery_days ? `Доставка: ${item.delivery_days || item.supplier_delivery_days} дн.` : ""}
                </div>
                <button class="primary" style="font-size:.82rem;width:100%" data-mp-order="${item.id}" data-supplier-id="${item.supplier_id}">Запросить</button>
              </div>`).join("")}
          </div>
        </div>`;
      document.getElementById("pr-offers-close")?.addEventListener("click", () => { panel.style.display = "none"; });
      // Wire "Запросить" buttons inside the panel
      panel.querySelectorAll("[data-mp-order]").forEach((ob) => {
        ob.addEventListener("click", () => {
          const itemId = ob.dataset.mpOrder;
          const item = (state.data.marketplace?.items || []).find((i) => String(i.id) === String(itemId));
          if (item) showInquiryModal(item, purchaseRequestId);
        });
      });
    });
  });

  // "Find in marketplace" for purchase requests with no offers yet
  document.querySelectorAll("[data-goto-marketplace]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const name = btn.dataset.gotoMarketplace || "";
      state.view = "marketplace";
      state.ui.marketplaceTab = "catalog";
      if (!state.ui.marketplaceFilter) state.ui.marketplaceFilter = {};
      state.ui.marketplaceFilter.search = name;
      state.ui.marketplaceFilter.category = "";
      render();
      if (state.view === "marketplace") initMarketplace();
      // Trigger search
      setTimeout(() => el("mp-search-btn")?.click(), 100);
    });
  });
  document.querySelectorAll("[data-quarantine-review]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      const nextStatus = button.dataset.quarantineNextStatus;
      try {
        let payload;
        if (nextStatus === "in_review") {
          if (!(await confirmAction(`Начать карантинную проверку #${button.dataset.quarantineReview}?`, {
            tone: "normal", confirmText: "Начать",
          }))) return;
          payload = { status: "in_review", responsible_id: currentActorId() || null, decision_reason: null };
        } else {
          const result = await showQuarantineDecisionModal(nextStatus);
          if (!result) return;
          payload = {
            status: nextStatus,
            responsible_id: currentActorId() || null,
            decision_reason: result.reason,
            commission_members: result.commission,
            resolution_type: result.resolution,
            disposal_quantity: result.disposalQty,
          };
        }
        setPending(button, true);
        await request(`/quarantine-reviews/${button.dataset.quarantineReview}`, {
          method: "PATCH",
          body: JSON.stringify(payload),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-read]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        setPending(button, true);
        await request(`/notifications/${button.dataset.read}/read`, {
          method: "PATCH",
          body: JSON.stringify({ is_read: true }),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-post-document]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        const document = state.data.documents.find((entry) => Number(entry.id) === Number(button.dataset.postDocument));
        const documentIssues = controlledWriteoffDocumentIssues(document);
        if (documentIssues.length) {
          showAlert(`Провести документ нельзя. ${controlledWriteoffMessage()}`, "error");
          return;
        }
        if (!(await confirmAction(`Провести документ #${button.dataset.postDocument}? После этого остатки на складе изменятся.`))) return;
        setPending(button, true);
        await mutate(`/stock-documents/${button.dataset.postDocument}/post`, {
          document_id: Number(button.dataset.postDocument),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-cancel-document]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        if (!(await confirmAction(`Отменить черновик документа #${button.dataset.cancelDocument}? Остатки на складе не изменятся.`))) return;
        setPending(button, true);
        await mutate(`/stock-documents/${button.dataset.cancelDocument}/cancel`, {
          document_id: Number(button.dataset.cancelDocument),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-lock-warehouse]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      const locked = button.dataset.lockValue === "true";
      try {
        if (!(await confirmAction(`${locked ? "Заблокировать складские операции" : "Разблокировать складские операции"} для склада #${button.dataset.lockWarehouse}?`))) return;
        setPending(button, true);
        await mutate(`/warehouses/${button.dataset.lockWarehouse}/inventory-lock`, { inventory_lock: locked }, "PATCH");
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-save-inventory-line]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      const lineId = button.dataset.saveInventoryLine;
      const sessionId = button.dataset.session;
      const input = document.querySelector(`[data-actual-line="${lineId}"]`);
      try {
        if (!input.value) {
          showAlert("Введите фактическое количество по строке инвентаризации", "error");
          input.focus();
          return;
        }
        setPending(button, true);
        await request(`/inventory-sessions/${sessionId}/lines/${lineId}`, {
          method: "PATCH",
          body: JSON.stringify({ actual_quantity: String(input.value) }),
        });
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;
      try {
        setPending(button, true);
        if (button.dataset.action === "reload") await loadAll();
        if (button.dataset.action === "load-more-balances") {
          const wf = warehouseFilterParam();
          const offset = state.data.balances.items.length;
          const url = `/balances?limit=100&offset=${offset}${wf ? '&' + wf : ''}`;
          const more = await request(url);
          state.data.balances.items.push(...more.items);
          state.data.balances.total = more.total;
          render();
          setPending(button, false); return;
        }
        if (button.dataset.action === "generate-low-stock") {
          const wf = warehouseFilterParam();
          await request(`/notifications/generate-low-stock${wf ? `?${wf}` : ""}`, { method: "POST" });
          await loadAll();
        }
        if (button.dataset.action === "generate-expiry") {
          const wf = warehouseFilterParam();
          await request(`/notifications/generate-expiry${wf ? `?${wf}&days=30` : "?days=30"}`, { method: "POST" });
          await loadAll();
        }
        if (button.dataset.action === "generate-quarantine") {
          const wf = warehouseFilterParam();
          await request(`/notifications/generate-quarantine${wf ? `?${wf}&days=3` : "?days=3"}`, { method: "POST" });
          await loadAll();
        }
        if (button.dataset.action === "generate-supplier-contracts") {
          await request("/notifications/generate-supplier-contracts?days=30", { method: "POST" });
          await loadAll();
        }
        if (button.dataset.action === "reload-controlled-limits") {
          const wf = warehouseFilterParam();
          const warehouseId = wf ? new URLSearchParams(wf).get("warehouse_id") : null;
          if (warehouseId) {
            try {
              state.data.controlledLimits = await request(`/controlled-substances/limits?warehouse_id=${warehouseId}`);
            } catch (_) { state.data.controlledLimits = []; }
            try {
              state.data.controlledViolations = await request(`/controlled-substances/limits/violations?warehouse_id=${warehouseId}`);
            } catch (_) { state.data.controlledViolations = []; }
          }
          render();
          setPending(button, false); return;
        }
        if (button.dataset.action === "check-violations") {
          const wf = warehouseFilterParam();
          const warehouseId = wf ? new URLSearchParams(wf).get("warehouse_id") : null;
          if (!warehouseId) { showAlert("Выберите склад для проверки нарушений", "warn"); setPending(button, false); return; }
          try {
            state.data.controlledViolations = await request(`/controlled-substances/limits/violations?warehouse_id=${warehouseId}`);
            if (state.data.controlledViolations.length === 0) {
              showAlert("Нарушений лимитов ПКУ не обнаружено", "ok");
            } else {
              showAlert(`Обнаружено нарушений: ${state.data.controlledViolations.length}`, "warn");
            }
          } catch (_) { state.data.controlledViolations = []; }
          render();
          setPending(button, false); return;
        }
        if (button.dataset.action === "download-purchase-pdf") {
          try {
            const wf = warehouseFilterParam();
            const url = `${API}/purchase-requests/pdf${wf ? "?" + wf : ""}`;
            const resp = await fetch(url, { headers: headers() });
            if (!resp.ok) throw new Error(`Ошибка ${resp.status}`);
            const blob = await resp.blob();
            const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
            a.download = "purchase-requests.pdf"; a.click(); URL.revokeObjectURL(a.href);
            showAlert("PDF заявок скачан");
          } catch (err) { showAlert(err.message, "error"); }
          setPending(button, false); return;
        }
        if (button.dataset.action === "generate-purchase-requests") {
          const wf = warehouseFilterParam();
          await mutate(`/purchase-requests/generate-auto${wf ? `?${wf}` : ""}`, {
            source: "abc_xyz",
            analytics_days: state.data.analytics.analysis_days || 90,
          });
          await loadAll();
        }
        if (button.dataset.action === "save-abc-xyz-run") {
          const wf = warehouseFilterParam();
          await request(`/analytics/abc-xyz/runs${wf ? `?${wf}&days=90` : "?days=90"}`, {
            method: "POST",
            body: JSON.stringify({}),
          });
          await loadAll();
        }
        if (button.dataset.action === "apply-xyz-suggestions") {
          setPending(button, false);
          if (!(await confirmAction("Применить XYZ-рекомендации? Точки заказа товаров будут обновлены на основе расчётного потребления."))) return;
          setPending(button, true);
          const wf = warehouseFilterParam();
          const result = await request(`/analytics/abc-xyz/apply-suggestions${wf ? `?${wf}&days=90` : "?days=90"}`, { method: "POST" });
          showAlert(`Обновлено точек заказа: ${result.updated}`, "ok");
          await loadAll();
        }
        if (button.dataset.action === "expire-reservations") {
          setPending(button, false);
          if (!(await confirmAction("Снять всю просроченную бронь в выбранном складе? Товары снова станут доступными."))) return;
          setPending(button, true);
          const wf = warehouseFilterParam();
          await mutate(`/reservations/expire${wf ? `?${wf}` : ""}`, {});
          await loadAll();
        }
        if (button.dataset.action === "cancel-inventory") {
          const formNode = document.getElementById("inventory-action-form");
          const payload = collect(formNode);
          setPending(button, false);
          if (!(await confirmAction(`Отменить инвентаризацию #${payload.session_id}? Складские операции снова будут доступны.`))) return;
          setPending(button, true);
          await mutate(`/inventory-sessions/${payload.session_id}/cancel`, payload);
          await loadAll();
        }
        if (button.dataset.action === "show-create-user") {
          const panel = document.getElementById("user-form-panel");
          const title = document.getElementById("user-form-title");
          if (panel) {
            document.getElementById("user-form-id").value = "";
            document.getElementById("user-form-username").value = "";
            document.getElementById("user-form-fullname").value = "";
            document.getElementById("user-form-password").value = "";
            document.getElementById("user-form-roles").value = "warehouse_manager";
            document.getElementById("user-form-department").value = "";
            document.getElementById("user-form-supplier-id").value = "";
            if (title) title.textContent = "Создать пользователя";
            panel.style.display = "block";
            setPending(button, false);
          }
        }
        if (button.dataset.action === "cancel-user-form") {
          const panel = document.getElementById("user-form-panel");
          if (panel) panel.style.display = "none";
          setPending(button, false);
        }
        if (button.dataset.action === "save-user") {
          const userId = document.getElementById("user-form-id")?.value;
          const username = document.getElementById("user-form-username")?.value?.trim();
          const fullName = document.getElementById("user-form-fullname")?.value?.trim();
          const password = document.getElementById("user-form-password")?.value;
          const roles = [document.getElementById("user-form-roles")?.value || "warehouse_manager"];
          const department = document.getElementById("user-form-department")?.value?.trim() || null;
          const supplierIdRaw = document.getElementById("user-form-supplier-id")?.value?.trim();
          const supplierId = supplierIdRaw ? Number(supplierIdRaw) : null;
          const errEl = document.getElementById("user-form-error");
          if (!fullName) {
            if (errEl) { errEl.textContent = "Введите имя"; errEl.style.display = "block"; }
            setPending(button, false);
            return;
          }
          const body = { full_name: fullName, roles, department, supplier_id: supplierId };
          if (password) body.password = password;
          let result;
          if (userId) {
            result = await request(`/users/${userId}`, { method: "PATCH", body: JSON.stringify(body) });
          } else {
            if (!username) {
              if (errEl) { errEl.textContent = "Введите логин"; errEl.style.display = "block"; }
              setPending(button, false);
              return;
            }
            if (!password) {
              if (errEl) { errEl.textContent = "Введите пароль для нового пользователя"; errEl.style.display = "block"; }
              setPending(button, false);
              return;
            }
            body.username = username;
            result = await request("/users", { method: "POST", body: JSON.stringify(body) });
          }
          await loadAll();
          showAlert("Пользователь сохранён");
        }
        if (button.dataset.action === "deactivate-user") {
          const userId = button.dataset.userId;
          if (!(await confirmAction("Деактивировать пользователя?"))) { setPending(button, false); return; }
          await request(`/users/${userId}`, { method: "DELETE" });
          await loadAll();
          showAlert("Пользователь деактивирован");
        }
        if (button.dataset.action === "edit-user") {
          const userId = button.dataset.userId;
          const user = (state.data.users || []).find(u => String(u.id) === String(userId));
          if (!user) { setPending(button, false); return; }
          const panel = document.getElementById("user-form-panel");
          const title = document.getElementById("user-form-title");
          if (panel) {
            document.getElementById("user-form-id").value = user.id;
            document.getElementById("user-form-username").value = user.username;
            document.getElementById("user-form-fullname").value = user.full_name;
            document.getElementById("user-form-password").value = "";
            document.getElementById("user-form-roles").value = (user.roles || [])[0] || "warehouse_manager";
            document.getElementById("user-form-department").value = user.department || "";
            document.getElementById("user-form-supplier-id").value = user.supplier_id || "";
            if (title) title.textContent = `Редактировать: ${user.username}`;
            panel.style.display = "block";
            setPending(button, false);
          }
        }
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });
  // Supplier map actions
  document.querySelectorAll("[data-action='new-shipment']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const form = document.getElementById("new-shipment-form");
      if (form) form.style.display = form.style.display === "none" ? "block" : "none";
    });
  });
  document.querySelectorAll("[data-action='cancel-shipment']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const form = document.getElementById("new-shipment-form");
      if (form) form.style.display = "none";
    });
  });
  document.querySelectorAll("[data-action='save-shipment']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const supplierId = document.getElementById("ns-supplier")?.value;
        if (!supplierId) { showAlert("Выберите поставщика", "error"); return; }
        const body = {
          supplier_id: Number(supplierId),
          reference: document.getElementById("ns-ref")?.value || null,
          origin_city: document.getElementById("ns-origin")?.value || null,
          estimated_arrival: document.getElementById("ns-eta")?.value || null,
          notes: document.getElementById("ns-notes")?.value || null,
          status: "in_transit",
        };
        setPending(btn, true, "Сохраняем");
        await request("/shipments", { method: "POST", body: JSON.stringify(body) });
        state.data.shipments = await request("/shipments?limit=20");
        showAlert("Поставка создана");
        render();
      } catch (error) {
        showAlert(error.message, "error");
      } finally {
        setPending(btn, false);
      }
    });
  });
  document.querySelectorAll("[data-action='update-shipment-status']").forEach((sel) => {
    sel.addEventListener("change", async () => {
      const shipmentId = sel.dataset.shipmentId;
      const newStatus = sel.value;
      if (!newStatus || !shipmentId) return;
      try {
        await request(`/shipments/${shipmentId}`, { method: "PATCH", body: JSON.stringify({ status: newStatus }) });
        state.data.shipments = await request("/shipments?limit=20");
        showAlert("Статус обновлён");
        render();
      } catch (error) {
        showAlert(error.message, "error");
      }
    });
  });
  document.querySelectorAll("[data-download-pku-pdf]").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const query = warehouseFilterParam();
      const url = `${API}/controlled-substances/ledger/pdf${query ? "?" + query : ""}`;
      window.open(url, "_blank");
    });
  });
  // AI analyze purchases
  document.querySelectorAll("[data-action='ai-analyze-purchases']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const resultEl = document.getElementById("ai-analysis-result");
      try {
        setPending(btn, true, "Анализирую");
        if (resultEl) { resultEl.style.display = "block"; resultEl.innerHTML = "⏳ ИИ анализирует заявки..."; }
        const wf = warehouseFilterParam();
        const warehouseId = wf ? Number(new URLSearchParams(wf).get("warehouse_id")) || null : null;
        const result = await request("/ai/analyze-purchases", {
          method: "POST",
          body: JSON.stringify({ warehouse_id: warehouseId }),
        });
        const decisionColor = { "Одобрить": "#16a34a", "Требует проверки": "#d97706", "Отклонить": "#dc2626" };
        const rows = (result.items || []).map(r =>
          `<tr><td style="padding:4px">${escapeHtml(r.product_name||"")}</td>` +
          `<td style="padding:4px;color:${decisionColor[r.decision]||"#374151"};font-weight:600">${escapeHtml(r.decision||"")}</td>` +
          `<td style="padding:4px;font-size:.82rem;color:#6b7280">${escapeHtml(r.reason||"")}</td></tr>`
        ).join("");
        const html = `<b>🤖 AI анализ закупок</b>` +
          (result.summary ? `<p style="margin:.5rem 0;color:#374151">${escapeHtml(result.summary)}</p>` : "") +
          (rows ? `<table style="width:100%;border-collapse:collapse;margin-top:.5rem">` +
            `<thead><tr style="border-bottom:1px solid #bae6fd">` +
            `<th style="text-align:left;padding:4px">Товар</th><th style="text-align:left;padding:4px">Решение</th><th style="text-align:left;padding:4px">Причина</th></tr></thead>` +
            `<tbody>${rows}</tbody></table>` : "<p>Заявок для анализа не найдено</p>");
        if (resultEl) resultEl.innerHTML = html;
      } catch (error) {
        if (resultEl) resultEl.innerHTML = `<span style="color:red">Ошибка: ${escapeHtml(error.message)}</span>`;
        showAlert(error.message, "error");
      }
      finally { setPending(btn, false); }
    });
  });
  // Auction actions
  document.querySelectorAll("[data-action='new-auction']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fb = document.getElementById("auction-form-block");
      if (fb) fb.style.display = fb.style.display === "none" ? "block" : "none";
    });
  });
  document.querySelectorAll("[data-action='cancel-auction-form']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fb = document.getElementById("auction-form-block");
      if (fb) fb.style.display = "none";
    });
  });
  bindSubmit("controlled-limit-form", async (payload) => {
    const wf = warehouseFilterParam();
    const warehouseId = wf ? new URLSearchParams(wf).get("warehouse_id") : null;
    if (!warehouseId) { showAlert("Выберите кабинет в фильтре склада", "error"); return; }
    await request("/controlled-substances/limits", {
      method: "PUT",
      body: JSON.stringify({ ...payload, warehouse_id: Number(warehouseId), max_quantity: Number(payload.max_quantity) }),
    });
    try { state.data.controlledLimits = await request(`/controlled-substances/limits?warehouse_id=${warehouseId}`); } catch(_) {}
  });
  bindPendingControlledWriteoffHandlers();
  document.querySelectorAll("[data-delete-controlled-limit]").forEach((button) => {
    button.addEventListener("click", async () => {
      const limitId = button.dataset.deleteControlledLimit;
      if (!(await confirmAction("Удалить лимит ПКУ?", {}))) return;
      await request(`/controlled-substances/limits/${limitId}`, { method: "DELETE" });
      const wf2 = warehouseFilterParam();
      const wid2 = wf2 ? new URLSearchParams(wf2).get("warehouse_id") : null;
      if (wid2) { try { state.data.controlledLimits = await request(`/controlled-substances/limits?warehouse_id=${wid2}`); } catch(_) {} }
      render();
    });
  });

  document.querySelectorAll("[data-action='save-auction']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const title = document.getElementById("auc-title")?.value?.trim();
        const productId = document.getElementById("auc-product")?.value;
        const warehouseId = document.getElementById("auc-warehouse")?.value;
        const qty = document.getElementById("auc-qty")?.value;
        const unit = document.getElementById("auc-unit")?.value || "шт";
        const startPrice = document.getElementById("auc-start-price")?.value;
        const minPrice = document.getElementById("auc-min-price")?.value;
        const step = document.getElementById("auc-step")?.value || "100";
        const interval = document.getElementById("auc-interval")?.value || "300";
        const errEl = document.getElementById("auction-form-error");
        if (!title || !productId || !qty || !startPrice || !minPrice) {
          if (errEl) { errEl.textContent = "Заполните все обязательные поля"; errEl.style.display = "block"; }
          return;
        }
        if (errEl) errEl.style.display = "none";
        setPending(btn, true, "Создаём");
        await request("/auctions", {
          method: "POST",
          body: JSON.stringify({
            title, product_id: Number(productId), warehouse_id: warehouseId ? Number(warehouseId) : null,
            quantity: Number(qty), unit, start_price: Number(startPrice), min_price: Number(minPrice),
            step_amount: Number(step), step_interval_seconds: Number(interval),
          }),
        });
        state.data.auctions = await request("/auctions?limit=50");
        showAlert("Аукцион создан");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  document.querySelectorAll("[data-action='start-auction']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        setPending(btn, true, "Запускаем");
        await request(`/auctions/${btn.dataset.id}/start`, { method: "POST" });
        state.data.auctions = await request("/auctions?limit=50");
        showAlert("Аукцион запущен");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  document.querySelectorAll("[data-action='close-auction']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!(await confirmAction("Закрыть аукцион и определить победителя?"))) return;
      try {
        setPending(btn, true, "Закрываем");
        await request(`/auctions/${btn.dataset.id}/close`, { method: "POST" });
        state.data.auctions = await request("/auctions?limit=50");
        showAlert("Аукцион закрыт");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  document.querySelectorAll("[data-action='place-bid']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const aId = btn.dataset.id;
        const supplierId = document.getElementById(`bid-supplier-${aId}`)?.value;
        const amount = document.getElementById(`bid-amount-${aId}`)?.value;
        if (!supplierId || !amount) { showAlert("Выберите поставщика и укажите ставку", "error"); return; }
        setPending(btn, true, "Ставим");
        await request(`/auctions/${aId}/bids`, {
          method: "POST",
          body: JSON.stringify({ supplier_id: Number(supplierId), bid_amount: Number(amount) }),
        });
        state.data.auctions = await request("/auctions?limit=50");
        showAlert("Ставка принята");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  document.querySelectorAll("[data-action='load-bids']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const aId = btn.dataset.id;
        const container = document.getElementById(`bids-${aId}`);
        if (!container) return;
        if (container.style.display !== "none") { container.style.display = "none"; return; }
        setPending(btn, true, "Загрузка");
        const bids = await request(`/auctions/${aId}/bids`);
        if (!bids.length) {
          container.innerHTML = "Ставок ещё нет";
        } else {
          container.innerHTML = `<table style="width:100%;border-collapse:collapse"><thead><tr><th style="text-align:left;padding:3px">Поставщик</th><th style="text-align:right;padding:3px">Ставка</th><th style="text-align:left;padding:3px">Время</th></tr></thead><tbody>${
            bids.map(b=>`<tr><td style="padding:3px">${escapeHtml(b.supplier_name||"#"+b.supplier_id)}</td><td style="padding:3px;text-align:right">${Number(b.bid_amount).toLocaleString("ru-RU")} тг</td><td style="padding:3px;color:#6b7280">${b.created_at||""}</td></tr>`).join("")
          }</tbody></table>`;
        }
        container.style.display = "block";
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  // Reprint filter checkbox
  const reprintCb = document.getElementById("filter-reprint-only");
  if (reprintCb) {
    reprintCb.addEventListener("change", () => {
      if (!state.ui) state.ui = {};
      state.ui.reprintFilterOn = reprintCb.checked;
      render();
    });
  }

  // Mass barcode reprint
  document.querySelectorAll("[data-action='mass-reprint-labels']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const needReprint = state.data.products.filter(p => p.label_needs_reprint);
        if (!needReprint.length) { showAlert("Нет товаров, требующих перепечатки"); return; }
        setPending(btn, true, "Готовим");
        const result = await request("/products/barcode-labels", {
          method: "POST",
          body: JSON.stringify({ product_ids: needReprint.map(p => p.id) }),
        });
        downloadText(`sklad-reprint-labels-${needReprint.length}.zpl`, result.zpl);
        // Mark all reprinted
        await Promise.allSettled(needReprint.map(p =>
          request(`/products/${p.id}/mark-reprinted`, { method: "POST" })
        ));
        needReprint.forEach(p => { p.label_needs_reprint = false; });
        showAlert(`Подготовлено ${needReprint.length} этикеток (ZPL)`);
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  // Review moderation
  document.querySelectorAll("[data-action='approve-review'],[data-action='reject-review']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        setPending(btn, true);
        const action = btn.dataset.action === "approve-review" ? "approve" : "reject";
        await request(`/supplier-reviews/${btn.dataset.reviewId}`, {
          method: "PATCH", body: JSON.stringify({ action }),
        });
        state.data.pendingReviews = await request("/supplier-reviews?status=pending");
        state.data.suppliers = await request("/suppliers");
        showAlert(action === "approve" ? "Отзыв одобрен — рейтинг обновлён" : "Отзыв отклонён");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });
  document.querySelectorAll("[data-action='reload-pending-reviews']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        setPending(btn, true, "Загрузка");
        state.data.pendingReviews = await request("/supplier-reviews?status=pending");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });

  document.querySelectorAll("[data-action='test-esf-connect']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      setPending(btn, true, 'Подключение...');
      try {
        const result = await request('/esf/status');
        if (result.configured) {
          await request('/esf/connect', { method: 'POST' });
          const panel = document.getElementById('esf-status-panel');
          if (panel) panel.textContent = '✓ Соединение с IS-ESF установлено. BIN поставщика: ' + (result.seller_bin || '—');
        } else {
          const panel = document.getElementById('esf-status-panel');
          if (panel) panel.textContent = '⚠ ESF не настроен. Укажите SKLAD_ESF_USERNAME, SKLAD_ESF_PASSWORD, SKLAD_ESF_SELLER_BIN в .env';
        }
      } catch(e) {
        const panel = document.getElementById('esf-status-panel');
        if (panel) panel.textContent = '✗ Ошибка: ' + e.message;
      }
      setPending(btn, false);
    });
  });

  document.querySelectorAll("[data-action='trigger-background-jobs']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        setPending(btn, true, "Запуск...");
        await request("/admin/jobs/trigger", { method: "POST" });
        showAlert("Фоновые задачи запущены", "success");
        await new Promise(r => setTimeout(r, 2000));
        state.data.jobStatus = await request("/admin/jobs");
        render();
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(btn, false); }
    });
  });

  document.querySelectorAll("[data-action='test-mis-connect']").forEach((button) => {
    button.addEventListener("click", async () => {
      setPending(button, true, 'Проверка...');
      try {
        const st = await request('/mis/status');
        const parts = [];
        parts.push(st.inbound_configured ? `✓ Входящий webhook настроен (${st.mapped_warehouses} складов сопоставлено, ${st.procedure_templates} шаблонов)` : '⚠ Входящий webhook не настроен (SKLAD_MIS_INBOUND_WEBHOOK_TOKEN)');
        if (st.configured) {
          const res = await request('/mis/test', { method: 'POST' });
          parts.push('✓ Исходящий webhook: ' + res.message);
        } else {
          parts.push('⚠ Исходящий webhook не настроен (SKLAD_MIS_WEBHOOK_URL)');
        }
        document.getElementById('mis-status-panel').innerHTML = parts.join('<br>');
      } catch(e) { document.getElementById('mis-status-panel').textContent = '✗ ' + e.message; }
      setPending(button, false);
    });
  });

  document.querySelectorAll("[data-delete-procedure-template]").forEach((button) => {
    button.addEventListener("click", async () => {
      const templateId = button.dataset.deleteProcedureTemplate;
      if (!(await confirmAction("Удалить шаблон расхода?", {}))) return;
      try {
        await request(`/procedure-consumption-templates/${templateId}`, { method: "DELETE" });
        showAlert("Шаблон удалён", "ok");
        await loadAll();
      } catch (error) { showAlert(error.message, "error"); }
    });
  });

  document.getElementById("supplier-application-status-filter")?.addEventListener("change", (event) => {
    state.ui.supplierApplicationStatusFilter = event.target.value;
    render();
  });

  document.querySelectorAll("[data-supplier-application-review]").forEach((button) => {
    button.addEventListener("click", async () => {
      const applicationId = button.dataset.supplierApplicationReview;
      const nextStatus = button.dataset.supplierApplicationNextStatus;
      const application = pageItems(state.data.supplierApplications).find(
        (a) => String(a.id) === String(applicationId)
      );
      if (!application) return;
      const result = await showSupplierApplicationReviewModal(nextStatus, application);
      if (!result) return;
      try {
        setPending(button, true);
        const response = await request(`/tetis/supplier-applications/${applicationId}/review`, {
          method: "POST",
          body: JSON.stringify({ status: nextStatus, reason: result.reason }),
        });
        if (nextStatus === "approved" && response.supplier_id) {
          await loadAll();
          await showSupplierApprovedNextStepsModal({
            email: response.email || application.email,
            supplierId: response.supplier_id,
          });
        } else {
          showAlert("Заявка обновлена", "ok");
          await loadAll();
        }
      } catch (error) { showAlert(error.message, "error"); }
      finally { setPending(button, false); }
    });
  });

  document.querySelectorAll("[data-action='test-accounting']").forEach((button) => {
    button.addEventListener("click", async () => {
      setPending(button, true, 'Проверка...');
      try {
        const st = await request('/accounting/status');
        if (st.configured) {
          const res = await request('/accounting/test', { method: 'POST' });
          document.getElementById('accounting-status-panel').textContent = '✓ ' + res.message;
        } else {
          document.getElementById('accounting-status-panel').textContent = '⚠ Не настроено. Укажите SKLAD_ACCOUNTING_WEBHOOK_URL в .env';
        }
      } catch(e) { document.getElementById('accounting-status-panel').textContent = '✗ ' + e.message; }
      setPending(button, false);
    });
  });

  // ── Barcode scanner ─────────────────────────────────────────────────────
  document.querySelectorAll("[data-action='toggle-scanner']").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (state.ui.scannerActive) {
        stopBarcodeScanner();
      } else {
        startBarcodeScanner();
      }
    });
  });

  document.querySelectorAll("[data-action='scan-for-barcode-field']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const field = btn.closest("form")?.querySelector(`[name="${btn.dataset.targetField}"]`);
      if (!field) return;
      state.ui.scannerTarget = null;
      state.ui._scanRawTarget = `#${field.closest("form").id} [name="${btn.dataset.targetField}"]`;
      startBarcodeScanner();
    });
  });

  document.querySelectorAll("[data-action='generate-barcode-field']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const field = btn.closest("form")?.querySelector(`[name="${btn.dataset.targetField}"]`);
      if (!field) return;
      field.value = generateEan13();
      field.dispatchEvent(new Event("change", { bubbles: true }));
      showAlert(`Сгенерирован штрихкод ${field.value}`, "ok");
    });
  });

  document.querySelectorAll("[data-action='scan-for-receipt']").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.ui.scannerTarget = "#receipt-form [name='product_id']";
      startBarcodeScanner();
    });
  });

  document.querySelectorAll("[data-action='scan-for-fefo']").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.ui.scannerTarget = "#fefo-form [name='product_id']";
      startBarcodeScanner();
    });
  });

  document.querySelectorAll("[data-action='scan-for-batch-filter']").forEach((btn) => {
    btn.addEventListener("click", async () => {
      // Override handleBarcodeScan to set batchFilterProductId instead of navigating to stock
      state.ui.scannerTarget = null;
      state.ui._scanForBatchFilter = true;
      startBarcodeScanner();
    });
  });

  document.querySelectorAll("[data-action='scan-for-inventory']").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.ui._scanForInventory = true;
      state.ui.scannerTarget = null;
      state.ui._scanForBatchFilter = false;
      startBarcodeScanner();
    });
  });

    document.querySelectorAll("[data-action='clear-batch-filter']").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.ui.batchFilterProductId = null;
      render();
    });
  });

  document.querySelectorAll("[data-action='barcode-manual-search']").forEach(() => {
    const input = el("barcode-manual");
    if (!input) return;
    const doSearch = () => {
      const code = input.value.trim();
      if (!code) return;
      const product = state.data.products.find((p) => p.barcode && p.barcode.trim() === code);
      if (product) {
        state.ui.barcodeProduct = product;
        render();
      } else {
        showAlert(`Товар со штрихкодом ${escapeHtml(code)} не найден`, "warn");
      }
    };
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") doSearch(); });
    document.querySelector("[data-action='barcode-manual-search']")?.addEventListener("click", doSearch);
  });

  document.querySelectorAll("[data-action='barcode-clear']").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.ui.barcodeProduct = null;
      render();
    });
  });
}

["actor-id", "actor-role", "actor-warehouses", "warehouse-filter", "auth-token"].forEach((id) => {
  el(id).addEventListener("change", loadAll);
});
el("refresh-button").addEventListener("click", loadAll);
el("global-search").addEventListener("input", (event) => {
  state.ui.search = event.target.value;
  render();
});

el("global-search").addEventListener("keydown", async (event) => {
  if (event.key !== "Enter") return;
  const query = event.target.value.trim();
  // Barcode pattern: 8–14 digits (EAN-8, EAN-13, Code-128 numeric, etc.)
  if (!/^\d{8,14}$/.test(query)) return;
  event.preventDefault();
  let product = state.data.products.find((p) => p.barcode && p.barcode.trim() === query);
  if (!product) {
    try { product = await request(`/products/by-barcode/${encodeURIComponent(query)}`); } catch (_) { product = null; }
    if (product && !state.data.products.find((p) => p.id === product.id)) state.data.products.push(product);
  }
  if (product) {
    state.ui.barcodeProduct = product;
    state.ui.search = "";
    event.target.value = "";
    state.view = "stock";
    showAlert(`${product.name} найден по штрихкоду`, "ok");
    render();
  } else {
    showAlert(`Штрихкод ${query} не найден в справочнике`, "warn");
  }
});
el("lang-toggle")?.addEventListener("click", () => {
    setLang(getLang() === "ru" ? "kz" : "ru");
  });
  el("density-button").addEventListener("click", () => {
  state.ui.density = state.ui.density === "compact" ? "comfortable" : "compact";
  applyDensity();
});

render();
loadAll();
initBarcodeOverlay();

el("nav-toggle")?.addEventListener("click", () => {
  const sidebar = document.querySelector(".sidebar");
  const open = sidebar?.classList.toggle("nav-open");
  el("nav-toggle")?.setAttribute("aria-expanded", open ? "true" : "false");
});

el("show-supplier-application")?.addEventListener("click", () => {
  const _isTetis = window.location.hostname === "tetis1.kz" || window.location.hostname === "www.tetis1.kz";
  if (!_isTetis) {
    const loginScreen = el("login-screen");
    if (loginScreen) loginScreen.style.display = "flex";
    const directBlock = document.getElementById("login-direct-block");
    if (directBlock) directBlock.style.display = "";
    const tetisBlock = document.getElementById("login-tetis-block");
    if (tetisBlock) tetisBlock.style.display = "none";
    document.getElementById("tab-register")?.click();
    const roleEl = document.getElementById("reg-role");
    if (roleEl) { roleEl.value = "supplier"; roleEl.dispatchEvent(new Event("change")); }
    setTimeout(() => document.getElementById("reg-username")?.focus(), 80);
  } else {
    showSupplierApplicationScreen();
  }
});
el("become-supplier-button")?.addEventListener("click", async () => {
  if (state.auth.source === "login") { navigateTo("my-profile"); return; }
  const apps = state.data.supplierPortal.myApplications || [];
  const hasActiveApp = apps.some((a) => ["pending", "needs_changes"].includes(a.status));
  if (hasActiveApp) {
    state.ui.supplierMode = true;
    state.ui.supplierView = "my-applications";
    render();
    if (!apps.length || state.data.supplierPortal.auctions.length === 0) {
      await loadSupplierPortalData();
      render();
    }
    return;
  }
  showSupplierApplicationScreen();
});
el("hide-supplier-application")?.addEventListener("click", () => {
  hideSupplierApplicationScreen();
});
el("supplier-application-form")?.addEventListener("submit", submitSupplierApplication);

el("supplier-login-button")?.addEventListener("click", () => showSupplierLoginModal());
el("supplier-logout-button")?.addEventListener("click", () => supplierLogout());
el("supplier-mode-toggle")?.addEventListener("click", async () => {
  await toggleSupplierMode();
  const btn = el("supplier-mode-toggle");
  if (btn) {
    btn.textContent = state.ui.supplierMode ? "← Режим склада" : "Кабинет поставщика";
    btn.style.background = state.ui.supplierMode ? "" : "#2563eb";
    btn.style.color = state.ui.supplierMode ? "" : "#fff";
  }
});

// === ПКУ PENDING WRITEOFFS UI ===

function statusBadgePending(status) {
  const map = { pending: "Ожидает подтверждения", confirmed: "Подтверждено", rejected: "Отклонено" };
  const cls = { pending: "badge-amber", confirmed: "badge-green", rejected: "badge-red" };
  return `<span class="badge ${cls[status] || ""}">${map[status] || escapeHtml(status)}</span>`;
}

function renderPendingControlledWriteoffs() {
  const items = state.data.pendingControlledWriteoffs || [];
  const pendingOnly = items.filter((r) => r.status === "pending");
  const other = items.filter((r) => r.status !== "pending");
  const canApprove = isManagerRole() || hasPermission("stock:write");

  const cols = [
    { label: "ID", key: "id" },
    { label: "Партия", render: (row) => batchDetailLabel(row.batch_id) },
    { label: "Склад", render: (row) => escapeHtml(row.warehouse_name || "") },
    { label: "Кол-во", render: (row) => qty(row.quantity) },
    { label: "Пациент", render: (row) => escapeHtml(row.patient_id || "—") },
    { label: "Врач", render: (row) => escapeHtml(row.doctor_id || "—") },
    { label: "Ист. болезни", render: (row) => escapeHtml(row.medical_record_no || "—") },
    { label: "Запросил", render: (row) => escapeHtml(row.requested_by || "—") },
    { label: "Дата", render: (row) => dateText(row.requested_at) },
    { label: "Статус", render: (row) => statusBadgePending(row.status) },
    { label: "2-й подтверждающий", render: (row) => escapeHtml(row.second_approver_id || "—") },
    { label: "Причина отклонения", render: (row) => escapeHtml(row.rejected_reason || "—") },
  ];
  const actionCols = canApprove ? [...cols, {
    label: "Действия",
    render: (row) => row.status !== "pending" ? "" : `
      <button class="btn-sm compact-action" data-confirm-pending-writeoff="${escapeAttr(row.id)}">Подтвердить</button>
      <button class="danger compact-action" data-reject-pending-writeoff="${escapeAttr(row.id)}">Отклонить</button>
    `,
  }] : cols;

  return `
    <div class="table-panel span-12">
      <div class="toolbar">
        <h2>${t("Заявки на списание ПКУ (двойная подпись)")}</h2>
        <button class="secondary" data-action="reload-pending-controlled-writeoffs">Обновить</button>
      </div>
      ${pendingOnly.length === 0 && other.length === 0
        ? "<p class=\"empty-state\">Заявок на списание ПКУ нет.</p>"
        : ""}
      ${pendingOnly.length > 0 ? `
        <p style="font-size:.82rem;color:#b45309;font-weight:600;margin:.25rem 0 .5rem">Ожидают подтверждения: ${pendingOnly.length}</p>
        ${table(actionCols, pendingOnly, "Нет ожидающих заявок")}
      ` : ""}
      ${other.length > 0 ? `
        <details style="margin-top:.75rem">
          <summary style="cursor:pointer;font-size:.82rem;color:#6b7280">Архив заявок (${other.length})</summary>
          ${table(cols, other, "")}
        </details>
      ` : ""}
      ${canApprove ? `
        <div id="confirm-pending-writeoff-modal" style="display:none;border:1px solid #d97706;background:#fffbeb;padding:1rem;border-radius:.5rem;margin-top:1rem">
          <h3 style="margin:0 0 .5rem;font-size:.95rem">Подтверждение списания ПКУ</h3>
          <input type="hidden" id="cpw-pending-id">
          <label style="display:block;margin:.25rem 0 .1rem;font-size:.82rem">Ваш ID (второй подтверждающий)</label>
          <input id="cpw-approver-id" class="form-input" style="width:100%;margin-bottom:.5rem" placeholder="Ваш ID пользователя" value="${escapeHtml(currentActorId())}">
          <label style="display:block;margin:.25rem 0 .1rem;font-size:.82rem">Комментарий (необязательно)</label>
          <input id="cpw-note" class="form-input" style="width:100%;margin-bottom:.75rem" placeholder="Примечание">
          <button id="cpw-confirm-btn" class="primary">Подтвердить списание</button>
          <button id="cpw-cancel-btn" class="secondary" style="margin-left:.5rem">Отмена</button>
        </div>
        <div id="reject-pending-writeoff-modal" style="display:none;border:1px solid #dc2626;background:#fef2f2;padding:1rem;border-radius:.5rem;margin-top:1rem">
          <h3 style="margin:0 0 .5rem;font-size:.95rem">Отклонение заявки ПКУ</h3>
          <input type="hidden" id="rpw-pending-id">
          <label style="display:block;margin:.25rem 0 .1rem;font-size:.82rem">Причина отклонения</label>
          <input id="rpw-reason" class="form-input" style="width:100%;margin-bottom:.75rem" placeholder="Укажите причину отклонения">
          <button id="rpw-reject-btn" class="danger">Отклонить заявку</button>
          <button id="rpw-cancel-btn" class="secondary" style="margin-left:.5rem">Отмена</button>
        </div>
      ` : ""}
    </div>
  `;
}

function bindPendingControlledWriteoffHandlers() {
  document.querySelectorAll("[data-action=reload-pending-controlled-writeoffs]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      setPending(btn, true, "Загрузка...");
      try {
        const wf = warehouseFilterParam();
        const url = `/controlled-writeoffs/pending${wf ? "?" + wf : ""}`;
        state.data.pendingControlledWriteoffs = await request(url);
      } catch (_) { state.data.pendingControlledWriteoffs = []; }
      render();
      setPending(btn, false);
    });
  });

  document.querySelectorAll("[data-confirm-pending-writeoff]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pendingId = btn.dataset.confirmPendingWriteoff;
      document.getElementById("cpw-pending-id").value = pendingId;
      document.getElementById("cpw-approver-id").value = currentActorId();
      document.getElementById("cpw-note").value = "";
      document.getElementById("confirm-pending-writeoff-modal").style.display = "block";
      document.getElementById("reject-pending-writeoff-modal").style.display = "none";
      document.getElementById("confirm-pending-writeoff-modal").scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });

  document.querySelectorAll("[data-reject-pending-writeoff]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pendingId = btn.dataset.rejectPendingWriteoff;
      document.getElementById("rpw-pending-id").value = pendingId;
      document.getElementById("rpw-reason").value = "";
      document.getElementById("reject-pending-writeoff-modal").style.display = "block";
      document.getElementById("confirm-pending-writeoff-modal").style.display = "none";
      document.getElementById("reject-pending-writeoff-modal").scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });

  const cpwConfirmBtn = document.getElementById("cpw-confirm-btn");
  if (cpwConfirmBtn) {
    cpwConfirmBtn.addEventListener("click", async () => {
      const pendingId = document.getElementById("cpw-pending-id").value;
      const approverId = document.getElementById("cpw-approver-id").value.trim();
      const note = document.getElementById("cpw-note").value.trim();
      if (!approverId) { showAlert("Укажите ID второго подтверждающего", "error"); return; }
      setPending(cpwConfirmBtn, true, "Подтверждение...");
      try {
        await request(`/controlled-writeoffs/pending/${pendingId}/confirm`, {
          method: "POST",
          body: JSON.stringify({ second_approver_id: approverId, note: note || null }),
        });
        document.getElementById("confirm-pending-writeoff-modal").style.display = "none";
        showAlert("Заявка подтверждена, списание выполнено");
        const wf = warehouseFilterParam();
        state.data.pendingControlledWriteoffs = await request(`/controlled-writeoffs/pending${wf ? "?" + wf : ""}`);
        await loadAll();
      } catch (err) { showAlert(err.message, "error"); }
      setPending(cpwConfirmBtn, false);
    });
  }

  const cpwCancelBtn = document.getElementById("cpw-cancel-btn");
  if (cpwCancelBtn) {
    cpwCancelBtn.addEventListener("click", () => {
      document.getElementById("confirm-pending-writeoff-modal").style.display = "none";
    });
  }

  const rpwRejectBtn = document.getElementById("rpw-reject-btn");
  if (rpwRejectBtn) {
    rpwRejectBtn.addEventListener("click", async () => {
      const pendingId = document.getElementById("rpw-pending-id").value;
      const reason = document.getElementById("rpw-reason").value.trim();
      if (!reason) { showAlert("Укажите причину отклонения", "error"); return; }
      setPending(rpwRejectBtn, true, "Отклонение...");
      try {
        await request(`/controlled-writeoffs/pending/${pendingId}/reject`, {
          method: "POST",
          body: JSON.stringify({ rejected_reason: reason }),
        });
        document.getElementById("reject-pending-writeoff-modal").style.display = "none";
        showAlert("Заявка отклонена");
        const wf = warehouseFilterParam();
        state.data.pendingControlledWriteoffs = await request(`/controlled-writeoffs/pending${wf ? "?" + wf : ""}`);
        render();
      } catch (err) { showAlert(err.message, "error"); }
      setPending(rpwRejectBtn, false);
    });
  }

  const rpwCancelBtn = document.getElementById("rpw-cancel-btn");
  if (rpwCancelBtn) {
    rpwCancelBtn.addEventListener("click", () => {
      document.getElementById("reject-pending-writeoff-modal").style.display = "none";
    });
  }
}
