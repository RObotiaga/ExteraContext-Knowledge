---
type: source
source_id: plugins-store-accounts-storage
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-accounts-storage.md
date: 2026-10-01
---

# Kangel-Plugins/Plugins-Store — Мультиаккаунтность, AccountInstance, UserConfig и подсистемы хранилища

Источник: репозиторий [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), ветка `main`, снимок дерева и репозитория `513e29a07858e5dec3a8dcdc6a860fe4296f1d43`. Локальные файлы плагинов расположены в `Plugins-Store/Plugins/`. Тематический раздел `plugins-store-accounts-storage` включает 127 плагинов, реализующих механизмы работы с учетными записями Telegram, многопользовательскую маршрутизацию, управление сессиями, прямое манипулирование базами данных SQLite (`MessagesStorage`), файловую персистентность, Android `SharedPreferences` и встроенный механизм настроек плагинов.

## Роль и границы источника

Этот источник документирует реальные архитектурные решения и call-site контракты, используемые разработчиками плагинов для ExteraGram и AyuGram на платформе Android. В фокусе раздела — взаимодействие с ключевыми подсистемами Telegram: `UserConfig`, `AccountInstance`, `ConnectionsManager`, `MessagesController`, `MessagesStorage` и `NotificationCenter`.

Все приведённые сведения получены методом статического анализа исходного кода Python-плагинов (.plugin). Анализ раскрывает реальные сигнатуры Java reflection, структуру внутреннего бинарного и XML-хранилища сессий Telegram, транзакционную работу с локальными таблицами SQLite, паттерны изолированного кэширования и приёмы предотвращения конфликтов состояния между несколькими активными аккаунтами. Доказательства имеют статус `code` (подтверждены реализацией в кодовой базе, но не верифицированы динамическим стендовым тестированием на устройстве).

## Покрытие

| Файл плагина | Реализованные механизмы и компоненты | Границы и специфические детали |
|---|---|---|
| [`16 Accounts.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/16%20Accounts.plugin) | Перехват `UserConfig.hasPremiumOnAccounts()`, инспекция стектрейса Java (`Thread.currentThread().getStackTrace()`), снятие лимита аккаунтов до 16 | Точечный хук по стеку вызовов; не проверялся с новыми версиями Telegram |
| [`SessionManager.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin) | Сканирование всех слотов (`UserConfig.MAX_ACCOUNT_COUNT`), генерация `userconfig<slot>.xml`, удаление и переключение слотов, парсинг tdata, MTProto криптография (AES-256 IGE), валидация сессий | Монолитный модуль инъекции сессий (1954 строки); без runtime-тестов на всех версиях DC |
| [`panic_passcode_pro.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/panic_passcode_pro.plugin) | Хук `SharedConfig.checkPasscode`, очистка баз данных `MessagesStorage.cleanUp` по всем слотам `UserConfig.getActivatedAccountsCount()`, single-flight guard, экстренный логаут | Деструктивный сценарий очистки; код содержит защитный флаг от повторного входа |
| [`account_stats.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/account_stats.plugin) | Системные настройки `get_setting` / `set_setting`, перехват `.stats` в `on_send_message_hook`, пагинация диалогов через `TLRPC.TL_messages_getDialogs` | Потокобезопасная пакетная вычитка диалогов через `run_on_queue` |
| [`local_pin.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/local_pin.plugin) | Локальное закрепление в обход RPC через `MessagesStorage.updatePinnedMessages`, открытие экрана памяти `CacheControlActivity`, нотификации интерфейса | Требует ручной очистки БД перед удалением плагина |
| [`archive_folder_fix.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/archive_folder_fix.plugin) | Хук `MessagesController$DialogFilter.includesDialog` с аргументом `AccountInstance`, фильтр `HookFilter.RESULT_IS_TRUE`, кэширование поля `folder_id` | Оптимизированный хук без reflection внутри вызова |
| [`in-app-notifications.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/in-app-notifications.plugin) | Маршрутизация контроллеров по `message_object.currentAccount`, получение менеджеров через `AccountInstance.getInstance(account_id)`, межсессионные всплытия | Покрывает различия фонового аккаунта и `UserConfig.selectedAccount` |
| [`bot.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/bot.plugin) | Открытие `ChatActivity` под другим аккаунтом через `setCurrentAccount`, изолированный резолв пиров через `ConnectionsManager` выбранного слота | Замещение текущего фрагмента через `presentFragment(fragment, True)` |
| [`re_extera.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin) | Прямой доступ к внутренней SQLite БД `MessagesStorage.database`, таблица `messages_v2`, транзакции `beginTransaction`/`commitTransaction`, хуки подавления удаления | Низкоуровневая бинарная правка TL-буфера флагов сообщения на лету |
| [`ASC.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/ASC.plugin) | Локальное переименование через SQLite (`REPLACE INTO`), сохранение в `Mandre.Data.write_persistent_json`, подавление перезаписи кэша через `putUser`/`putChat` | Требует наличия библиотеки `mandre_lib` |
| [`unlimited_pins.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/unlimited_pins.plugin) | Патчинг полей лимитов `MessagesController` по всем активным слотам, сохранение и восстановление состояния из JSON-файла в `PluginsController.pluginsDir/cache` | Многопоточный дебаунс сохранения и поколенческий откат восстановления |
| [`mute_account.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/mute_account.plugin) | Поаккаунтная изоляция настроек через ключи `f"mute_acc_{current}"`, чтение `currentAccount` из `param.thisObject` | Хук на регистрацию push-устройств `TL_account_registerDevice` |
| [`custom_recent_reactions.plugin`, `gif_folders.plugin`, `proxy_pill.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/custom_recent_reactions.plugin) | Прямая работа с Android `SharedPreferences` (`ApplicationLoader.applicationContext.getSharedPreferences`), чтение Telegram `mainconfig`, сопоставление `.apply()` и `.commit()` | Выход за рамки стандартного хранилища BasePlugin для низкоуровневых флагов |
| [`hideChats.plugin`, `copy_profile.plugin`, `meow_reply.plugin`](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hideChats.plugin) | Сохранение JSON в `filesDir`, сложная сериализация структур данных в настройки, бинарное резервное копирование аватаров | Разные подходы к хранению: файл в каталоге приложения vs сериализованная JSON-строка |
| Остальные 112 плагинов выборки | Использование `UserConfig.selectedAccount`, базовые настройки `get_setting`, чтение пользовательских профилей | Типовые потребители синглтонов текущего аккаунта |

## Технические факты

### 1. Ядро UserConfig и лимиты учетных записей

В Telegram для Android класс `org.telegram.messenger.UserConfig` управляет состоянием профилей. Внутри процесса поддерживается пул аккаунтов, ограниченный статической константой `UserConfig.MAX_ACCOUNT_COUNT` (традиционно равной 3, а с Premium или в форках — 4 или более).

* **Снятие ограничения на число аккаунтов**:
  Плагин `16 Accounts` демонстрирует технику расширения лимита через перехват метода `UserConfig.hasPremiumOnAccounts` ([16 Accounts.plugin:15-68](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/16%20Accounts.plugin#L15-L68)). Когда клиент определяет доступность добавления новой учетной записи, он опрашивает `hasPremiumOnAccounts()`. Хук с приоритетом 10000 возвращает `Boolean(True)`.
* **Контекстная фильтрация по стектрейсу**:
  Чтобы не ломать логику проверки Premium в других компонентах приложения, плагин анализирует стек вызовов Java через `Thread.currentThread().getStackTrace()` ([16 Accounts.plugin:18-23, 83-93](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/16%20Accounts.plugin#L18-L23)). Лимит разблокируется только тогда, когда в стеке присутствуют целевые экраны:
  - `org.telegram.ui.MainTabsActivity`
  - `org.telegram.ui.UserInfoActivity`
  - `org.telegram.ui.LogoutActivity`
  - `com.exteragram.messenger.drawer.DrawerAccountPickerView`
* **Полное сканирование слотов аккаунтов**:
  В `SessionManager.plugin` ([SessionManager.plugin:876-923](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L876-L923)) реализован алгоритм аудита всех аккаунтов устройства:
  ```python
  for i in range(UserConfig.MAX_ACCOUNT_COUNT):
      uc = UserConfig.getInstance(i)
      user = uc.getCurrentUser()
      is_activated = uc.isClientActivated()
      user_id = uc.getClientUserId()
      is_active = (UserConfig.selectedAccount == i)
      cm = ConnectionsManager.getInstance(i)
      dc_id = cm.getCurrentDatacenterId()
  ```
  Слот считается занятым, если `isClientActivated() == True` или `clientUserId != 0` или объект `getCurrentUser()` не равен `None`.

### 2. Маршрутизация через AccountInstance и контроллеры слотов

Ключевая ошибка неопытных разработчиков плагинов — использование синглтонов `client_utils.get_messages_controller()` или `MessagesController.getInstance(0)`. Они всегда привязаны либо к слоту 0, либо к текущему отображаемому аккаунту (`UserConfig.selectedAccount`). При многопоточном поступлении событий или фоновых уведомлениях это приводит к загрязнению кэша или отправке сообщений не из того аккаунта.

* **Паттерн явной маршрутизации контроллера**:
  В `in-app-notifications.plugin` ([in-app-notifications.plugin:318-326](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/in-app-notifications.plugin#L318-L326)) зафиксирован канонический хелпер:
  ```python
  def get_messages_controller2(account_id: int | None = None):
      if account_id is None or account_id == get_user_config().currentAccount:
          return get_messages_controller()
      return AccountInstance.getInstance(account_id).getMessagesController()
  ```
* **Привязка сущностей к `currentAccount`**:
  Каждый объект `MessageObject` несёт в себе целочисленное поле `currentAccount` ([in-app-notifications.plugin:358-415](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/in-app-notifications.plugin#L358-L415)). Любые связанные операции (скачивание медиа через `MediaDataController`, отправка через `SendMessagesHelper`, отметка прочтения `markDialogAsRead`) должны извлекать инстанс строго по номеру аккаунта сообщения:
  `AccountInstance.getInstance(message_object.currentAccount).getMediaDataController()`.
* **Переключение активного профиля на лету**:
  В `SessionManager.plugin` ([SessionManager.plugin:775-796](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L775-L796)) показан безопасный двухэтапный переход между аккаунтами:
  1. `LaunchActivity.instance.switchToAccount(slot, True)` в основном UI-потоке через `run_on_ui_thread`. Это перестраивает все фрагменты, боковое меню и навигационный стек.
  2. Запасной fallback (если ссылка на `LaunchActivity.instance` отсутствует): `AccountInstance.getInstance(slot).switchToAccount(slot, True)`.
* **Безопасное удаление активного слота**:
  Если удаляется аккаунт, который в данный момент выбран (`slot == UserConfig.selectedAccount`), прямое удаление данных вызовет краш клиента. В `SessionManager.plugin` ([SessionManager.plugin:1158-1215](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L1158-L1215)) реализован алгоритм:
  1. Поиск альтернативного активированного слота `i != slot`.
  2. Смена активного слота: `UserConfig.selectedAccount = i; uc.saveConfig(True)`.
  3. Очистка конфигурации удаляемого слота: `UserConfig.getInstance(slot).clearConfig()`.
  4. Удаление дисковых файлов (`tgnet.dat`, `user.xml`, `config.xml`, `shared_prefs/userconfing{slot}.xml`) и каталога `account{slot}`.
* **Изолированный запуск чата под другим аккаунтом**:
  В `bot.plugin` ([bot.plugin:39-50, 440-465](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/bot.plugin#L39-L50)) продемонстрировано открытие отдельного диалога под другим аккаунтом без переключения всего клиента:
  - Создаётся экземпляр `ChatActivity(args)`.
  - У фрагмента явно вызывается `fragment.setCurrentAccount(slot)`.
  - Текущий фрагмент заменяется через `source.presentFragment(fragment, True)`.
  - Пользователи и чаты резолвятся через `AccountInstance.getInstance(slot).getConnectionsManager()` и помещаются в `AccountInstance.getInstance(slot).getMessagesController().putUsers(...)`.

### 3. Нативные SharedPreferences и конфигурация Telegram

Telegram использует механизм Android `SharedPreferences` для хранения параметров приложения и сессионных данных.

* **Прямой доступ к префам**:
  Плагины получают контекст через `ApplicationLoader.applicationContext` и открывают системные файлы префов:
  `prefs = ApplicationLoader.applicationContext.getSharedPreferences(NAME, 0)` ([custom_recent_reactions.plugin:104-125](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/custom_recent_reactions.plugin#L104-L125)).
* **Синхронный `commit()` против асинхронного `apply()`**:
  - `custom_recent_reactions.plugin` использует `_prefs().edit().putString(...).apply()` для фоновой неблокирующей записи реакций.
  - `gif_folders.plugin` ([gif_folders.plugin:86-105](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/gif_folders.plugin#L86-L105)) использует `_prefs().edit().putString(...).commit()`. Синхронная запись критична, если сохранённые данные должны быть немедленно перечитаны другим процессом или перед перезапуском приложения.
* **Чтение глобальной конфигурации `"mainconfig"`**:
  В `proxy_pill.plugin` ([proxy_pill.plugin:666-675](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/proxy_pill.plugin#L666-L675)) показано чтение глобальных флагов Telegram из системных префов:
  `ApplicationLoader.applicationContext.getSharedPreferences("mainconfig", 0).getBoolean("proxy_enabled", False)`.
* **Формат XML-хранилища сессий Telegram**:
  В `SessionManager.plugin` ([SessionManager.plugin:343-395, 1180-1230](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L343-L395)) задокументирована внутренняя структура файлов `userconfing.xml` (для слота 0, обратите внимание на историческую опечатку `userconfing` в кодовой базе Telegram) и `userconfing{slot}.xml` (для слотов `> 0`):
  ```xml
  <?xml version='1.0' encoding='utf-8' standalone='yes' ?>
  <map>
      <string name="user">{base64_tl_user}</string>
      <int name="dc_id" value="{dc}" />
      <long name="clientUserId" value="{uid}" />
      <int name="currentAccount" value="{slot}" />
  </map>
  ```
  Поле `user` содержит base64-сериализованную бинарную структуру `TLRPC.User` (конструктор `0x20b1422` с флагами `0x1c7e`).

### 4. Внутренняя база данных SQLite Telegram (`MessagesStorage`)

Класс `org.telegram.messenger.MessagesStorage` отвечает за хранение сообщений, диалогов и контактов в локальной SQLite БД. Каждый аккаунт имеет собственный экземпляр `MessagesStorage.getInstance(account)`.

* **Прямой доступ к экземпляру SQLiteDatabase**:
  Плагин `re_extera.plugin` ([re_extera.plugin:214-260](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin#L214-L260)) извлекает внутренний объект базы через рефлексию:
  ```python
  db = get_private_field(MessagesStorage.getInstance(account), "database")
  cursor = db.queryFinalized("SELECT data FROM messages_v2 WHERE uid = ? AND mid = ?", dialog_id, message_id)
  ```
* **Схема таблицы `messages_v2` и TL-буферы**:
  Таблица `messages_v2` содержит поля `uid` (идентификатор диалога / пира), `mid` (идентификатор сообщения) и `data` (сырой бинарный BLOB сообщения).
  `re_extera.plugin` модифицирует флаги сообщения напрямую в памяти:
  ```python
  data = cursor.byteBufferValue(0)
  data.position(8)
  flags2 = data.readInt32(True)
  flags2 |= FLAG_DELETED  # установка битовой маски удаления
  data.position(8)
  data.writeInt32(flags2)
  ```
* **Транзакционные пакетные операции**:
  Для предотвращения блокировок диска и повреждения базы операции оборачиваются в транзакции ([re_extera.plugin:270-320](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin#L270-L320)):
  ```python
  db.beginTransaction()
  try:
      updateStatement.bindByteBuffer(1, data)
      updateStatement.bindLong(2, dialogId)
      updateStatement.bindInteger(3, msg_id)
      updateStatement.step()
      db.commitTransaction()
  finally:
      pass
  ```
* **Подавление удаления сообщений (Anti-Recall)**:
  В `re_extera.plugin` ([re_extera.plugin:884-950](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin#L884-L950)) перехватываются внутренние методы `MessagesStorage`:
  - `markMessagesAsDeletedInternal(Long.TYPE, ArrayList, Boolean.TYPE, Integer.TYPE, Integer.TYPE)`
  - `updateDialogsWithDeletedMessages(Long.TYPE, Long.TYPE, ArrayList, ArrayList, Boolean.TYPE)`
  - `updateDialogsWithDeletedMessagesInternal(Long.TYPE, Long.TYPE, ArrayList, ArrayList)`
  Установка `param.setResult(None)` отменяет удаление сообщений из базы данных.
* **Локальное закрепление сообщений без RPC**:
  В `local_pin.plugin` ([local_pin.plugin:617-645, 1206-1215](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/local_pin.plugin#L617-L645)) показана запись закрепления прямо в локальную базу:
  `storage.updatePinnedMessages(dialog_id, ids, True, -1, 0, False, None)` с последующим оповещением UI через `NotificationCenter.getInstance(account).postNotificationName(NotificationCenter.updateInterfaces, Integer(0))`.
* **Экстренная очистка баз данных**:
  В `panic_passcode_pro.plugin` ([panic_passcode_pro.plugin:402-417](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/panic_passcode_pro.plugin#L402-L417)) для каждого активированного аккаунта вызывается:
  `ms = MessagesStorage.getInstance(aid); ms.cleanUp(True); ms.clearMediaDatabase()`.

### 5. Персистентность настроек плагинов и файловые хранилища

Плагины используют три уровня персистентности:
1. **Встроенное KV-хранилище настроек плагина**:
   Предоставляется методами `self.get_setting(key, default)` и `self.set_setting(key, value, [immediate])` базового класса `BasePlugin` ([account_stats.plugin:42-65](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/account_stats.plugin#L42-L65)).
   - Примитивные типы (`bool`, `int`, `str`) сохраняются напрямую.
   - Сложные структуры данных сериализуются в JSON-строки через `json.dumps()` перед вызовом `set_setting` и десериализуются через `json.loads(self.get_setting(key, "{}"))` ([meow_reply.plugin:155-171](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/meow_reply.plugin#L155-L171); [copy_profile.plugin:1351-1377](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/copy_profile.plugin#L1351-L1377)).
2. **Изолированный кэш-каталог плагинов**:
   В `unlimited_pins.plugin` ([unlimited_pins.plugin:80-100](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/unlimited_pins.plugin#L80-L100)) путь к хранилищу определяется динамически через контроллер плагинов:
   `cache_dir = os.path.join(PluginsController.getInstance().pluginsDir.getAbsolutePath(), "cache")`.
   Файлы сохраняются в атомарном режиме через `json.dump(data, f, ensure_ascii=False)`.
3. **Каталог файлов приложения Android**:
   В `hideChats.plugin` ([hideChats.plugin:35-45](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hideChats.plugin#L35-L45)) путь берётся напрямую из Android Context:
   `os.path.join(ApplicationLoader.applicationContext.getFilesDir().getAbsolutePath(), "hidechats_data.json")`.

### 6. Синхронизация состояния, скрытие сессий и безопасность

* **Поаккаунтная изоляция настроек**:
  Плагин `mute_account.plugin` ([mute_account.plugin:18-25](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/mute_account.plugin#L18-L25)) формирует динамические ключи настроек с суффиксом текущего слота: `self.get_setting(f"mute_acc_{current}", False)`. Это исключает взаимное влияние конфигураций разных аккаунтов.
* **Скрытие диалогов и подавление уведомлений**:
  `hideChats.plugin` ([hideChats.plugin:80-140](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/hideChats.plugin#L80-L140)) фильтрует списки чатов в `after_hooked_method` у `MessagesController.getDialogs()`, удаляя скрытые диалоги через `dialogs.removeAll(to_remove)`, а также отсекает входящие пуши перехватом диспетчера нотификаций.
* **Аварийный сброс и паник-код**:
  `panic_passcode_pro.plugin` ([panic_passcode_pro.plugin:104-128, 477-525](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/panic_passcode_pro.plugin#L104-L128)) реализует паттерн защиты от повторного входа (single-flight guard) через `with self.logout_lock: if self.logout_in_progress: return`. Поток выполняет очистку баз данных, сброс `SharedConfig.passcodeHash = ""`, вызов `AccountInstance.getInstance(i).cleanup()` и форсированный перезапуск процесса.
* **Патчинг лимитов на экземплярах контроллеров**:
  `unlimited_pins.plugin` ([unlimited_pins.plugin:29-36, 800-870](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/unlimited_pins.plugin#L29-L36)) обходит все активные аккаунты и динамически переопределяет числовые поля в `MessagesController`:
  - `maxPinnedDialogsCountDefault`
  - `maxPinnedDialogsCountPremium`
  - `maxFolderPinnedDialogsCountDefault`
  - `maxFolderPinnedDialogsCountPremium`
  - `dialogFiltersPinnedLimitDefault`
  - `dialogFiltersPinnedLimitPremium`
  При выгрузке исходные значения восстанавливаются из словаря `self._original_limits`.

## Вызовы и наблюдаемые контракты

| Класс / модуль | Метод / сигнатура вызова | Назначение и контекст | Доказательство в коде |
|---|---|---|---|
| `UserConfig` | `UserConfig.getInstance(int account)` | Получение конфигурации конкретного слота аккаунта | [SessionManager.plugin#L880](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L880) |
| `UserConfig` | `UserConfig.selectedAccount` | Статическое целочисленное поле текущего активного UI-слота | [SessionManager.plugin#L898](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L898) |
| `UserConfig` | `uc.isClientActivated() -> bool` | Проверка авторизованности клиента в данном слоте | [SessionManager.plugin#L882](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L882) |
| `UserConfig` | `uc.getClientUserId() -> long` | Получение Telegram User ID авторизованного аккаунта | [SessionManager.plugin#L883](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L883) |
| `UserConfig` | `UserConfig.hasPremiumOnAccounts() -> boolean` | Проверка наличия Premium для расширения слотов | [16 Accounts.plugin#L16-L59](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/16%20Accounts.plugin#L16-L59) |
| `UserConfig` | `UserConfig.getActivatedAccountsCount() -> int` | Получение общего числа активных учетных записей | [panic_passcode_pro.plugin#L407](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/panic_passcode_pro.plugin#L407) |
| `AccountInstance` | `AccountInstance.getInstance(int account)` | Получение контейнера зависимостей для конкретного аккаунта | [bot.plugin#L53](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/bot.plugin#L53) |
| `AccountInstance` | `acc.switchToAccount(int slot, boolean reset)` | Программное переключение активного аккаунта приложения | [SessionManager.plugin#L790](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L790) |
| `AccountInstance` | `acc.getMessagesController()` | Получение `MessagesController` конкретного аккаунта | [in-app-notifications.plugin#L325](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/in-app-notifications.plugin#L325) |
| `AccountInstance` | `acc.getConnectionsManager()` | Получение `ConnectionsManager` конкретного аккаунта | [bot.plugin#L398](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/bot.plugin#L398) |
| `LaunchActivity` | `LaunchActivity.instance.switchToAccount(slot, True)` | Переключение активного аккаунта через главный UI-компонент | [SessionManager.plugin#L784](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/SessionManager.plugin#L784) |
| `ChatActivity` | `fragment.setCurrentAccount(int account)` | Установка рабочего аккаунта для отдельного экрана чата | [bot.plugin#L48](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/bot.plugin#L48) |
| `MessagesStorage` | `MessagesStorage.getInstance(int account)` | Получение менеджера SQLite-хранилища для слота | [local_pin.plugin#L623](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/local_pin.plugin#L623) |
| `MessagesStorage` | `storage.updatePinnedMessages(long did, ArrayList ids, boolean pin, int mid, int unpin, boolean notify, ...)` | Запись закрепления сообщений прямо в базу SQLite | [local_pin.plugin#L636](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/local_pin.plugin#L636) |
| `MessagesStorage` | `storage.cleanUp(boolean isLogout)` | Полная очистка локальной базы данных сообщений | [panic_passcode_pro.plugin#L411](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/panic_passcode_pro.plugin#L411) |
| `SQLiteDatabase` | `db.queryFinalized(String sql, Object... args) -> SQLiteCursor` | Выполнение SELECT-запроса к SQLite базе Telegram | [re_extera.plugin#L223](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin#L223) |
| `SQLiteDatabase` | `db.executeFast(String sql) -> SQLitePreparedStatement` | Подготовка компилированного SQL-запроса | [re_extera.plugin#L250](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/re_extera.plugin#L250) |
| `BasePlugin` | `self.get_setting(str key, default=None)` | Чтение параметра из изолированного хранилища плагина | [account_stats.plugin#L64](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/account_stats.plugin#L64) |
| `BasePlugin` | `self.set_setting(str key, value, immediate=False)` | Сохранение параметра в изолированное хранилище плагина | [account_stats.plugin#L60](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/account_stats.plugin#L60) |
| `SharedPreferences` | `ctx.getSharedPreferences(String name, int mode)` | Получение Android SharedPreferences по имени | [custom_recent_reactions.plugin#L104](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/custom_recent_reactions.plugin#L104) |
| `SharedPreferences.Editor`| `editor.putString(k, v).apply()` | Асинхронная неблокирующая фиксация изменений | [custom_recent_reactions.plugin#L109](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/custom_recent_reactions.plugin#L109) |
| `SharedPreferences.Editor`| `editor.putString(k, v).commit()` | Синхронная блокирующая фиксация изменений на диск | [gif_folders.plugin#L98](https://github.com/Kangel-Plugins/Plugins-Store/blob/00de67026419f9dbe3a2787bb1236e8aaead8f76/Plugins/gif_folders.plugin#L98) |

## Практические приёмы и рецепты

### 1. Расширение лимита аккаунтов через UserConfig.hasPremiumOnAccounts

```python
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class
from java.lang import Boolean, Thread

USER_CONFIG_CLASS = "org.telegram.messenger.UserConfig"
PREMIUM_CHECK_METHOD = "hasPremiumOnAccounts"
ACCOUNT_LIMIT_CALLERS = (
    "org.telegram.ui.MainTabsActivity",
    "org.telegram.ui.UserInfoActivity",
    "org.telegram.ui.LogoutActivity",
    "com.exteragram.messenger.drawer.DrawerAccountPickerView",
)

class AccountLimitHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        try:
            stack = Thread.currentThread().getStackTrace()
            for element in stack:
                cls_name = str(element.getClassName())
                if any(cls_name == c or cls_name.startswith(c + "$") for c in ACCOUNT_LIMIT_CALLERS):
                    param.setResult(Boolean(True))
                    return
        except Exception:
            pass
```

### 2. Полный обход и сканирование доступных аккаунтов

```python
from org.telegram.messenger import UserConfig, ConnectionsManager

def get_all_active_accounts():
    accounts = []
    for slot in range(UserConfig.MAX_ACCOUNT_COUNT):
        try:
            uc = UserConfig.getInstance(slot)
            if not uc.isClientActivated() and uc.getClientUserId() == 0:
                continue
            user = uc.getCurrentUser()
            cm = ConnectionsManager.getInstance(slot)
            accounts.append({
                "slot": slot,
                "user_id": uc.getClientUserId(),
                "is_current": (slot == UserConfig.selectedAccount),
                "first_name": user.first_name if user else "",
                "dc_id": cm.getCurrentDatacenterId() if cm else 0
            })
        except Exception:
            continue
    return accounts
```

### 3. Маршрутизация контроллера сообщений по номеру аккаунта

```python
from client_utils import get_messages_controller, get_user_config
from org.telegram.messenger import AccountInstance

def resolve_messages_controller(account_id: int | None = None):
    if account_id is None or account_id == get_user_config().currentAccount:
        return get_messages_controller()
    return AccountInstance.getInstance(account_id).getMessagesController()
```

### 4. Открытие изолированного чата под альтернативным аккаунтом

```python
from client_utils import get_last_fragment
from android.os import Bundle
from org.telegram.ui import ChatActivity

def open_chat_under_account(user_id: int, target_account_slot: int):
    fragment = get_last_fragment()
    if not fragment:
        return
    args = Bundle()
    args.putLong("user_id", int(user_id))
    chat_activity = ChatActivity(args)
    chat_activity.setCurrentAccount(int(target_account_slot))
    fragment.presentFragment(chat_activity, True)
```

### 5. Сериализация сложных структур данных в настройки плагина

```python
import json

def load_dict_setting(plugin, key: str, default: dict) -> dict:
    raw = plugin.get_setting(key, None)
    if not raw:
        return dict(default)
    try:
        data = json.loads(str(raw))
        return data if isinstance(data, dict) else dict(default)
    except Exception:
        return dict(default)

def save_dict_setting(plugin, key: str, data: dict, immediate: bool = False):
    plugin.set_setting(key, json.dumps(data, ensure_ascii=False), immediate)
```

### 6. Локальное закрепление сообщений в базе данных без RPC

```python
from org.telegram.messenger import UserConfig, MessagesStorage, NotificationCenter
from java.lang import Integer, Long
from java.util import ArrayList

def pin_message_locally(dialog_id: int, message_id: int, account: int | None = None):
    acc = UserConfig.selectedAccount if account is None else account
    storage = MessagesStorage.getInstance(acc)
    notif_center = NotificationCenter.getInstance(acc)
    
    ids = ArrayList()
    ids.add(Integer(message_id))
    
    # Прямая запись в SQLite без обращения к серверам Telegram
    storage.updatePinnedMessages(dialog_id, ids, True, -1, 0, False, None)
    notif_center.postNotificationName(NotificationCenter.updateInterfaces, Integer(0))
    notif_center.postNotificationName(NotificationCenter.didLoadPinnedMessages, Long(dialog_id), ids, False, -1, 0, 0, 0)
```

### 7. Прямой доступ к таблице messages_v2 во внутренней базе данных Telegram

```python
from hook_utils import get_private_field
from org.telegram.messenger import MessagesStorage

def get_message_blob(account: int, dialog_id: int, message_id: int):
    storage = MessagesStorage.getInstance(account)
    db = get_private_field(storage, "database")
    if not db:
        return None
    cursor = None
    try:
        cursor = db.queryFinalized("SELECT data FROM messages_v2 WHERE uid = ? AND mid = ?", dialog_id, message_id)
        if cursor.next():
            return cursor.byteBufferValue(0)
    finally:
        if cursor:
            cursor.dispose()
    return None
```

### 8. Изоляция кэш-файлов плагина в служебном каталоге

```python
import os, json
from com.exteragram.messenger.plugins import PluginsController

def get_plugin_cache_file(filename: str) -> str:
    plugins_dir = PluginsController.getInstance().pluginsDir.getAbsolutePath()
    cache_dir = os.path.join(plugins_dir, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, filename)
```

## Ограничения и противоречия

1. **Разрыв между UI-состоянием и фоновыми менеджерами**:
   Глобальный `UserConfig.selectedAccount` отражает состояние активного UI-слота. При получении уведомлений или фоновом выполнении RPC для других аккаунтов вызовы функций без явного указания `account_id` обращаются к контроллеру активного пользователя, вызывая порчу данных или некорректное обновление счетчиков непрочитанного.
2. **Блокировки UI-потока при работе с SQLite**:
   Методы `MessagesStorage` выполняются на выделенном внутреннем потоке `StorageQueue`. Прямое извлечение `database` через рефлексию и синхронные вызовы `executeFast` / `queryFinalized` из UI-потока могут приводить к зависаниям (ANR), если в этот момент база заблокирована транзакцией `MessagesStorage`. Все прямые SQL-операции должны оборачиваться в `run_on_queue` или запускаться в демоническом потоке.
3. **Особенности очистки кэша `putUser` / `putChat`**:
   При локальном изменении свойств пользователя или группы (как в `ASC.plugin`) Telegram перезаписывает кэш в памяти при любом входящем обновлении через сетевые хендлеры `processUpdateArray`. Для сохранения локальных изменений требуется непрерывный перехват методов `MessagesController.putUser` и `putChat`.
4. **Формат SharedPreferences `userconfing`**:
   Файл префов слота 0 имеет опечатку в коде Telegram: `userconfing.xml` (вместо `userconfig.xml`). При парсинге и манипулировании файлами конфигураций на диске необходимо учитывать эту особенность, иначе удаление или инъекция профиля слота 0 потерпит неудачу.
5. **Атомарность `commit()` и производительность `apply()`**:
   В плагинах зафиксировано расхождение: частая запись через `.commit()` в цикле или UI-потоке вызывает микрофризы интерфейса из-за синхронного ввода-вывода. Напротив, вызов `.apply()` перед немедленным `Process.killProcess(Process.myPid())` или экстренным логаутом может привести к потере данных, так как Android не успеет сбросить префы из памяти на диск.
