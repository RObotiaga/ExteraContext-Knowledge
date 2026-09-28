---
source_id: official-sdk
review_status: accepted-with-gaps
review: ../reviews/official-sdk.md
---

# Официальная документация exteraGram Plugin SDK

Источник: [официальный раздел SDK](https://plugins.exteragram.app/docs). Ниже сведения сведены по задачам разработчика; URL первоисточника указан в заголовке каждого раздела. Полученные серверные HTML-ответы сохранены без преобразований в [`raw/official-sdk/`](../../raw/official-sdk/), а [`manifest.json`](../../raw/official-sdk/manifest.json) фиксирует адрес, дату снимка и назначение каждой страницы.

## Версии и пределы подтверждения

Главная страница указывает версию SDK дерева `1.4.4.3`, Python `3.11` и рекомендуемую нижнюю версию приложения `12.5.1+` ([Introduction](https://plugins.exteragram.app/docs)). `12.5.1+` также стоит в Setup и примерах обычного плагина. При этом дочерние страницы документации уже описывают API новее этого baseline: multi-account требует `__sdk_version__ >= 1.4.5.0`, Elyx Quick Start/Metadata — `>= 1.4.5.3`, а intents доступны на приложении с version code `66999` (`12.6.4`) и выше ([Multi-account](https://plugins.exteragram.app/docs/multi-account), [Elyx Metadata](https://plugins.exteragram.app/docs/elyx/metadata), [Intents](https://plugins.exteragram.app/docs/intents)). Class Proxy отдельно отмечает app version code `>= 66690` для описанной функциональности ([Class Proxy](https://plugins.exteragram.app/docs/class-proxy)).

Поэтому версия 1.4.4.3 — baseline, который заявляет индексная страница, а не доказательство того, что все опубликованные подстраницы или установленные клиенты относятся к одному дереву. В сравнении с PySDK `1.4.5.5`, указанным для проектов в [экспортированном радаре](../../raw/radar-export-text.md), документация содержит признаки более нового API, но сама по себе не доказывает, что конкретный runtime 1.4.5.5 реализует каждую описанную сигнатуру. Для переносимого плагина задавайте `__sdk_version__`/`sdk_version` не ниже минимальной версии нужных методов и проверяйте на целевой сборке. Это статическое исследование страниц; ни runtime, ни скачанный SDK-код здесь не запускались.

## Начало работы и форма плагина

Источники: [Setup](https://plugins.exteragram.app/docs/setup), [First Plugin](https://plugins.exteragram.app/docs/first-plugin), [Plugin Class](https://plugins.exteragram.app/docs/plugin-class).

Обычный плагин — Python-файл с топ-level метаданными и классом `BasePlugin`. Loader извлекает метаданные AST-разбором, поэтому держите их литералами, а не вычисляйте динамически. Обязательны только `__id__` и `__name__`; ID — 2–32 символа, начинается с латинской буквы, затем допускает латинские буквы, цифры, `_` и `-`. `__version__` по умолчанию `1.0`; `__min_version__` поддержан как legacy alias для `__app_version__ = ">=..."`.

```python
from base_plugin import BasePlugin

__id__ = "hello_world"
__name__ = "Hello World"
__description__ = "Example plugin"
__author__ = "Your Name"
__version__ = "1.0.0"
__icon__ = "exteraPlugins/1"
__app_version__ = ">=12.5.1"
__sdk_version__ = ">=1.4.4.3"
__requirements__ = ["tinydb>=4"]

class HelloWorldPlugin(BasePlugin):
    pass
```

Setup советует держать имя файла равным ID (`hello_world.py`), добавить `src/` SDK в IDE для импорта и autocomplete, включить plugin engine и developer mode в exteraGram Preferences → Plugins. На телефоне single-file плагин обычно расположен в `/data/user/0/com.exteragram.messenger/files/plugins/<plugin_id>.py`; разработку можно вести копированием файла или через DevServer. Метаданные в виде plain constants — требование загрузчика, а не только стиль.

## Жизненный цикл, hooks и результаты

Источник: [Plugin Class](https://plugins.exteragram.app/docs/plugin-class), примеры также в [First Plugin](https://plugins.exteragram.app/docs/first-plugin).

- `on_plugin_load(self)` вызывается при включении плагина и восстановлении при старте приложения; здесь регистрируют hooks/listeners и запускают фоновые работы.
- `on_plugin_unload(self)` вызывается при выключении или завершении приложения; здесь останавливают созданные плагином worker-ы и освобождают собственные ресурсы. Xposed hooks и menu items SDK снимает автоматически, но сторонние listeners, потоки и глобальные monkey patch требуют явной очистки.
- `on_app_event(self, event_type: AppEvent)` получает `AppEvent.START`, `STOP`, `PAUSE`, `RESUME`.
- `create_settings(self) -> List[Any]` возвращает строки из `ui.settings`.

Событийные методы сами по себе не подписываются: вызовите регистрацию при загрузке. Основные регистрации: `self.add_hook(name, match_substring=False, priority=0)` для TL-запроса/события и `self.add_on_send_message_hook(priority=0)` для параметров исходящего сообщения.

```python
from base_plugin import BasePlugin, HookResult, HookStrategy

class Plugin(BasePlugin):
    def on_plugin_load(self):
        self.add_hook("TL_account_updateStatus")
        self.add_on_send_message_hook()

    def pre_request_hook(self, request_name: str, account: int, request):
        if request_name == "TL_account_updateStatus":
            request.offline = True
            return HookResult(strategy=HookStrategy.MODIFY, request=request)
        return HookResult()

    def post_request_hook(self, request_name: str, account: int, response, error):
        if request_name == "TL_messages_sendMessage" and not error:
            self.log("sent")
        return HookResult()

    def on_update_hook(self, update_name: str, account: int, update):
        return HookResult()

    def on_updates_hook(self, container_name: str, account: int, updates):
        return HookResult()

    def on_send_message_hook(self, account: int, params):
        return HookResult()
```

`HookResult()` оставляет событие без изменения; `HookStrategy.CANCEL` прекращает операцию; `MODIFY` возвращает изменённый объект; `MODIFY_FINAL` прекращает дальнейшую обработку плагинами с изменённым объектом. В зависимости от hook-типа объект передаётся через `HookResult.request`, `.response`, `.update`, `.updates` или `.params`. Для отправки достаточно проверить наличие `params.message`: медиа-сообщение может не иметь строкового текста. Перед долгой сетью/файлами не блокируйте hook на UI-потоке.

Пример из документации для преобразования `.hello Alice`: разобрать текст, изменить `params.message`, вернуть `HookResult(strategy=HookStrategy.MODIFY, params=params)`; отсутствие имени можно обработать изменением на usage-текст. Этот паттерн годится для команды, но на странице не специфицированы все возможные типы `params` и гарантии повторной доставки.

## Мультиаккаунт и поток выполнения

Источники: [Multi-account](https://plugins.exteragram.app/docs/multi-account), [Client Utilities](https://plugins.exteragram.app/docs/client-utils), [Android Utilities](https://plugins.exteragram.app/docs/android-utils).

Все залогиненные аккаунты остаются подключёнными, включая аккаунты вне UI; hooks могут прийти от фонового аккаунта. Сигнатуры hooks содержат `account: int`. Для ответа на событие используйте этот же аккаунт: `self.client(account)` или `send_text(peer, text, account=account)`, `get_messages_controller(account)` и другие account-scoped helpers. Вызов без аккаунта использует выбранный в UI аккаунт. Документация говорит, что SDK пишет предупреждение один раз на helper, когда callback текущего account scope и UI-selected account расходятся.

`get_hook_account()` возвращает текущий scope (или `None` вне callback); `self.client()` без аргумента внутри callback следует scope. Scope устанавливается в hook callback, `run_on_queue(...)`, запланированном из него, и `send_request` callbacks. `NotificationCenterDelegate.didReceivedNotification(id, account, args)` получает аккаунт, но автоматически в scope не помещается. `get_media_controller()` — документированное исключение: один общий MediaController без account parameter. Страница требует SDK `>=1.4.5.0`; не считать это частью baseline 1.4.4.3.

`run_on_queue(func, queue=PLUGINS_QUEUE, delay=0)` переносит сеть, дисковый ввод-вывод, тяжёлый разбор и вычисления с UI thread; задержка задаётся в миллисекундах. Константы: `STAGE_QUEUE`, `GLOBAL_QUEUE`, `CACHE_CLEAR_QUEUE`, `SEARCH_QUEUE`, `PHONE_BOOK_QUEUE`, `THEME_QUEUE`, `EXTERNAL_NETWORK_QUEUE`, `PLUGINS_QUEUE`. Для UI есть `run_on_ui_thread(func, delay=0)`. Она принимает обычный Python callable. `R(fn)` нужен только если Java API отдельно ожидает `Runnable`. `OnClickListener(fn)` передаёт Python callback нажатый View; `OnLongClickListener(fn)` должен вернуть bool (true потребляет событие).

## Клиентские запросы, ответы и сообщения

Источник: [Client Utilities](https://plugins.exteragram.app/docs/client-utils).

- `send_request(request, fn, account=...)` отправляет TLObject через ConnectionsManager; `fn(response, error)` — обычная Python-функция, которую SDK оборачивает в `RequestDelegate`. Возврат — request ID. Пример строит `TLRPC.TL_messages_readMessageContents()`, добавляет `Integer(12345)` в `req.id`, отправляет и в callback проверяет `error`, затем ожидаемый тип `TLRPC.TL_messages_affectedMessages` и поля `pts`, `pts_count`.
- Текст и медиа отправляются специализированными helper-ами; `send_text`, `send_photo`, `send_document`, `send_video`, `send_audio` принимают необязательные `parse_mode="HTML"` либо `"Markdown"`. Примеры: `send_text(peer_id, "Hello", replyToMsg=9876)`, `send_photo(peer_id, path, caption="...", high_quality=True)`, `send_document(peer_id, path, caption=...)`.
- Для низкоуровневой отправки есть `send_message(params, parse_mode=None)`; `params` — dict, поля сопоставляются с `SendMessagesHelper.SendMessageParams`; документированы, среди прочих, `peer`, `message`, `caption`, `photo`, `document`, `path`, `replyToMsg`, `replyMarkup`, `params`, `notify`, `scheduleDate`, `ttl`, `hasMediaSpoilers`, `sendingHighQuality`.
- `edit_message(message_obj, text=..., file_path=..., with_spoiler=..., parse_mode=...)` изменяет реальный `org.telegram.messenger.MessageObject`; `text` заменяет текст/подпись, `file_path` заменяет медиа; неподдерживаемый parse mode вызывает `ValueError`.
- Для `parse_mode` регистр не важен; поддержаны только HTML и Markdown. Когда он передан, парсер заполняет `message` либо `caption` и entities.

Контроллеры/состояние доступны через `get_last_fragment`, `get_account_instance`, `get_messages_controller`, `get_contacts_controller`, `get_media_data_controller`, `get_connections_manager`, `get_location_controller`, `get_notifications_controller`, `get_messages_storage`, `get_send_messages_helper`, `get_file_loader`, `get_secret_chat_helper`, `get_download_controller`, `get_notifications_settings`, `get_notification_center`, `get_media_controller`, `get_user_config`; account-scoped функции принимают account. `NotificationCenterDelegate` можно наследовать напрямую, он уже Python base class для Telegram delegate — `dynamic_proxy(...)` не требуется.

## Настройки и пользовательский интерфейс

Источники: [Plugin Settings](https://plugins.exteragram.app/docs/plugin-settings), [Alert Dialog Builder](https://plugins.exteragram.app/docs/alert-dialog-builder), [Bulletin Helper](https://plugins.exteragram.app/docs/bulletin-helper), [Android Utilities](https://plugins.exteragram.app/docs/android-utils).

Базовый интерфейс строится в `create_settings() -> List[Any]`. Типы из `ui.settings`: `Header`, `Divider`, `Switch`, `Selector`, `Input`, `Text`, `EditText`, `Custom`. Ряд с persisted value получает стабильный `key`, `default`, опционально `subtext`, `icon`, callbacks и `link_alias`. `Selector` задаёт `items` и integer index; `EditText` требует `hint` и может включать `multiline`, `max_length`, `mask`. `Text` может иметь click/long-click, создавать подстраницу через `create_sub_fragment`, иметь `accent`/`red`.

Из кода читать/писать через `self.get_setting(key, default=None)` и `self.set_setting(key, value, reload_settings=False)`. `reload_settings=True` нужно, если запись меняет состав/вид строк. `export_settings()`/`import_settings(settings, reload_settings=True)` позволяют выгрузить или восстановить словарь настроек.

Для `Custom` страница рекомендует `SimpleSettingFactory`: `create_view(context, list_view, current_account, class_guid, resources_provider) -> View`, `bind_view(view, item, divider, adapter, list_view)`, опциональные `create_item(plugin, setting, args)`, `on_click(plugin, item, view)`, `on_long_click(plugin, item, view)`, `attached_view`, `equals`, `content_equals`; фабрика задаёт `is_clickable`, `is_shadow`. Разделяйте создание каркаса view и bind данных, поскольку строки могут переиспользоваться. Низкоуровневая альтернатива — готовый `UItem`, Android `View` или собственный Java `CustomSetting.Factory` через Class Proxy.

Диалоги: `AlertDialogBuilder(activity, progress_style=ALERT_TYPE_MESSAGE, resources_provider=None)`, дальше `set_title`, `set_message`, `set_view`, `set_items`, `set_positive_button`/`set_negative_button`/`set_neutral_button`, `create`, `show`, `dismiss`, `get_dialog`, `get_button`. Listener получает `(builder, which)`. Типы — message, loading с `set_progress(0..100)`, spinner. Создание, показ и изменение диалога должны происходить на UI thread; `set_cancelable` и touch-outside лучше настраивать после `create()` или `show()`.

`BulletinHelper.show_info/error/success(text, fragment=None)` и более специальные методы `show_simple`, `show_two_line`, `show_with_button`, `show_undo` показывают короткие нижние уведомления; если fragment не задан, helper ищет безопасный текущий фрагмент и fallback. Эти `show_...` сами переключаются на UI thread. Длительности документированы как 1500/2750/5000 мс (`DURATION_SHORT/LONG/PROLONG`).

## Java reflection, hooks и proxy-классы

Источники: [Hook Utilities](https://plugins.exteragram.app/docs/hook-utils), [Xposed Method Hooking](https://plugins.exteragram.app/docs/xposed-hooking), [Class Proxy](https://plugins.exteragram.app/docs/class-proxy).

Для reflection `find_class("org.telegram.ui.ActionBar.ActionBar")` возвращает Java Class или `None`; вызывать reflection надо непосредственно на нём, не делать `getClass()` для Class object. В Xposed-примере сигнатура метода находится явно: `ActionBarClass.getDeclaredMethod("setTitle", CharSequenceClass)`; constructor аналогично ищется через `getDeclaredConstructor(ContextClass)`, после чего вызывается `setAccessible(True)`. Private instance/static поля: `get_private_field`, `set_private_field`, `get_static_private_field`, `set_static_private_field`. Reflection fragилен к изменению приложения — проверять `None` и оборачивать доступ в обработку ошибок.

В Xposed hooks доступны `MethodHook.before_hooked_method(param)`/`after_hooked_method(param)`, `MethodReplacement.replace_hooked_method(param)` и краткий `self.hook_method(method, before=..., after=..., before_filters=..., after_filters=...)`. `param.thisObject`, `param.args`, `param.method`, `param.getResult()`, `param.setResult(...)`: изменение args меняет аргументы; `setResult` в before пропускает оригинальную реализацию; в after заменяет результат. Возвращаемое значение `MethodReplacement` должно быть совместимо с Java return type. Фильтры включают `RESULT_IS_NULL/TRUE/FALSE/NOT_NULL`, `ResultIsInstanceOf`, `ResultEqual/NotEqual`, `ArgumentIsNull/NotNull/IsFalse/IsTrue/IsInstanceOf/Equal/NotEqual`, `Condition`, `Or`; применять через `HookFilter`/`@hook_filters`.

Найти target и подписать класс hook можно на обычный app method или constructor; `self.hook_all_methods(clazz, name, hook)` и `hook_all_constructors(clazz, hook)` возвращают список unhook handles. SDK автоматически снимает hooks при unload; для досрочного снятия — `self.unhook_method(handle)`. Кодовый пример показывает также `hook_method(method, handler_instance, priority=10)`.

Class Proxy строит реальный Java class на базе DexMaker. Основной DSL: `Base`, `@java_subclass(JavaClass, Interface...)`, `@joverride`, `@joverload(name, arg_types)`, `@jmethod`, `jfield`, `@jconstructor`, `@jpreconstructor`, `jgetmethod`, `jsetmethod`, `@jclassbuilder`, `jMVELmethod`, `jMVELoverride`. Для перегруженных Java методов выбирайте точную сигнатуру `@joverload`, не неявный overload. `super()` в override вызывает Java parent implementation.

```python
from extera_utils.classes import Base, java_subclass, joverload, jfield
from java.util import ArrayList

@java_subclass(ArrayList)
class CountingList(Base):
    added_count = jfield("int", default=0)

    @joverload("add", ["java.lang.Object"])
    def add_item(self, value):
        self.added_count += 1
        return super().add_item(value)

peer = CountingList.new_instance()  # Python peer
peer.add("hello")
java_object = peer.java            # raw Java object
```

`new_instance(...)` возвращает Python peer; передавайте `.java` туда, где требуется собственно Java object. Для Java constructor arguments используйте позиционные параметры; `init_args=[...]` предназначен `__init__` на стороне Python. `new_java_instance(...)` создаёт raw object, `from_java(existing)` возвращает Python peer. Документация указывает app version code `>=66690` для части Class Proxy API; точная матрица версий отдельных декораторов не дана.

## Форматирование текста

Источник: [Text Formatting](https://plugins.exteragram.app/docs/text-formatting).

`extera_utils.text_formatting.parse_text(text, parse_mode='HTML', is_caption=False)` возвращает dict с plain `message` (или `caption`) и списком `TLRPC.MessageEntity`. Поддерживает HTML tags `b/strong`, `i/em`, `u`, `s/del/strike`, `a href`, `code`, `pre language`, `spoiler/tg-spoiler`, `blockquote` (в т.ч. expandable/collapsed), `emoji id`. Markdown-вариант: `*bold*`, `_italic_`, `__underline__`, `~strike~`, `||spoiler||`, backticks для code, `[text](url)`, `![alt](tg://emoji?id=...)`, `>`/`**>` для quote. Для стандартной отправки вручную вызывать parser обычно не нужно: `client_utils` принимает `parse_mode`.

## Файлы и intents

Источники: [File Utilities](https://plugins.exteragram.app/docs/file-utils), [Intents](https://plugins.exteragram.app/docs/intents).

Для путей используйте `get_plugins_dir`, `get_cache_dir`, `get_files_dir`, `get_images_dir`, `get_videos_dir`, `get_audios_dir`, `get_documents_dir`; `ensure_dir_exists(path)`, `list_dir(path, recursive=False, include_files=True, include_dirs=False, extensions=None)`, `read_file`/`write_file`, binary `read_file_bytes`/`write_file_bytes`, `delete_file`. Ошибки чтения возвращают `None` и логируются; delete возвращает bool.

`FilesController.register(FileInfo(ext, on_click, whitelist_places=[], blacklist_places=[], get_icon=None))` перехватывает открытие расширения и возвращает secret для `unregister(ext, secret)`. whitelist и blacklist вместе запрещены; `get_icon` разрешён только если `FilesController.SUPPORT_ICONS`. В callback `OnClickArgs` доступны `place`, `file`, `file_name`, `message`, `activity`, `parent_fragment`. Регистрация дублирующего extension/неверный secret дают документированные exceptions.

`IntentsManager` (`from intents import IntentsManager as IM`) регистрирует global before/after обработчики через `new_global_before_handler(callback, **filters)` / `new_global_after_handler(...)`; фильтры: `scheme`, `host`, `path` с `{path_var}`, `required_path_args_names` (несмотря на имя, это обязательные query argument names), `action`, `whitelist_flags`, `blacklist_flags`, `type`, `categories`, `priority`. Callback получает только именованные значения, которые объявлены в signature: `intent`, `scheme`, `host`, `path`, `query_args`, `action`, `flags`, `type`, `categories`, плюс query/path vars; `**kwargs` принимает весь named context, `*args` — стандартный позиционный набор. Меньшее число `priority` исполняется раньше. Возврат именно `True` у before-handler останавливает последующие Python handlers и оригинальную обработку; after-handler остановить её не может. `HandlerHandle.unhandle()` либо `IM.unhandle(handler_id)` снимают регистрацию; `IM.parse(url)` разбирает URL. Минимум приложения: version code 66999 / 12.6.4. Страница не описывает разрешения Android или модель permission grant.

## Elyx: структурированный формат

Источники: [Elyx](https://plugins.exteragram.app/docs/elyx), [Quick Start](https://plugins.exteragram.app/docs/elyx/quick-start), [Project Structure](https://plugins.exteragram.app/docs/elyx/project-structure), [Metadata](https://plugins.exteragram.app/docs/elyx/metadata), [Modules and Imports](https://plugins.exteragram.app/docs/elyx/modules-and-imports), [Public API](https://plugins.exteragram.app/docs/elyx/public-api).

Elyx — ZIP-compatible `.elyx`/`.eaf`, который оставляет тот же `BasePlugin`, но добавляет многофайловую структуру, ресурсы, locale files, bundled wheels и desktop sync. В корне архива лежит `refmap.yml`/`.yaml`/`.json`; архивировать надо содержимое проекта так, чтобы `refmap` был именно в archive root, без внешней обёртки-папки. Пример:

```yaml
metainfo: plugin/meta.yml
main: plugin/src/main.py
assets: plugin/res
strings: plugin/locales
wheels: wheels
```

`main` указывает entry module; первый найденный `BasePlugin` subclass из entry module будет создан, поэтому держите там один plugin class. При пропуске ключа берутся `main.py` и `metainfo.yml` в корне; assets/metadata discovery также документированы для root-level paths. Пути case-sensitive на Android. Неизвестные builder keys в refmap игнорируются runtime, но доступны плагину как `elyx.refmap`.

Metadata YAML: `id`, `name` обязательны; опционально `description`, `author`, `version`, `icon`, `app_version`, `sdk_version`, `requirements`, `requires`. Elyx Metadata задаёт ID из 2–32 ASCII букв/цифр/underscore (без дефиса — расходится с правилом ID single-file plugin, где дефис допускается). `requires` — карта plugin ID → URL, минимум версии указывается в скобках; требуется, чтобы целевой плагин был установлен и включён. Для нового проекта сохраняйте version constraint в quoted YAML string, например `sdk_version: ">=1.4.5.3"`.

Локальные imports изолированы на plugin namespace. Обычный `from helpers import ...` или relative import разрешается в файлы того же plugin. Для runtime-вычисленного имени есть `elyx.import_module(name, package=None)`; обычный `importlib.import_module(...)` не имеет plugin context и может пропустить локальный модуль. Поддерживаются `.py`, `.pyc` (только ABI magic Python 3.11), пакеты и namespace dirs. JSON/YAML/YML/TXT могут импортироваться как data modules; рекомендуют `__init__.py` для tooling. Не используйте зарезервированные корни вроде `elyx`, `ui`, `java`, `android`.

`from elyx import assets, metainfo, refmap, settings, strings` — стабильный plugin-facing импорт, но values `assets`, `metainfo`, `refmap`, `strings` динамичны и доступны только когда соответствующая структура обнаружена/успешно загружена. `get_environment()` возвращает environment конкретного caller plugin и вызывает `RuntimeError` вне Elyx-кода. `elyx.__all__` перечисляет поддерживаемые экспорты; engine/importer/installer/внутренние model modules не являются публичным API.

Assets: `assets.logo`, `assets["logo.svg"]`, `assets.get("logo")`; атрибут нормализует stem, вложенные папки доступны через `/` или атрибут. Для чтения — `.content_bytes()`, `.content_string()`, `.content_json()`, `.content_yaml()`, `.content()`. Для Android есть `to_drawable`, `to_image_location`, `to_bitmap_drawable`, `to_svg_drawable`, `to_svg_bitmap`, `to_svg_thumb`, `to_lottie_drawable`. Путь bundled asset read-only; пользовательские данные храните через file helpers. `Asset.temp_asset_from_url(url, filename)` делает синхронную сеть и запись — вызывать на background queue.

Локализация: `strings_en.yml`, `strings_ru.yml`; suffix после последнего `_` задаёт locale; поддержаны `.yaml`, `.yml`, `.json`, `.py` (Python localization file исполняется при загрузке). Разрешение строки: выбранная locale → English → ключ; есть `strings(key, name=value)`, `.get(key, default)`, `.get_with_locale(key, locale)`, `.pluralize(count, key)`. Pluralize реализует только три Slavic-style формы, это не CLDR. English-файл нужен для fallback.

Settings Elyx обёрнуты `SettingsController`: `settings.get/get_setting(key, default)`, `settings.set/set_setting(key, value, reload_settings=False)`, `settings[key]`, `settings.get_settings()`, `settings.clear_settings()`. Хранилище общее с `BasePlugin` settings, привязано к plugin ID и переживает reload/update. Рекомендуются небольшие prefs и лёгкое состояние; большие данные/cache — файлы/БД, секреты — dedicated secure storage. `reload_settings=True` нужен для перестроения открытой settings page.

## Зависимости Python

Источники: [PIP & Dependencies](https://plugins.exteragram.app/docs/pip), [Available Libraries](https://plugins.exteragram.app/docs/available-libraries), [Elyx Dependencies](https://plugins.exteragram.app/docs/elyx/dependencies).

Single-file метаданные задают `__requirements__ = ["mpmath", "tinydb"]`; Elyx — PEP 508 comma-separated `requirements`. Встроенный package manager скачивает только universal wheels с `-none-any.whl`, требует сеть к PyPI и поддерживает ограниченный набор environment markers. Нативные расширения (`numpy`, `pandas`, `scipy`, `cryptography`, OpenCV и др.) не устанавливаются обычным этим путём. Пакеты разделяются между plugins, поэтому конфликтующие pinned versions могут блокировать установку.

Заявленный Python runtime — 3.11. В preinstalled packages перечислены beautifulsoup4, debugpy, lxml, packaging, pillow, requests, PyYAML. Elyx может включать wheels в `refmap.wheels`; runtime извлекает direct children `.whl` в plugin-specific storage, использует wheel filename stem как идентификатор извлечённой версии и удаляет устаревшие каталоги; изменив wheel content, меняйте version/filename. Есть и локальные source packages в проекте. Требуемые другие плагины объявляются в `requires`, но docs подчёркивают, что это availability dependency, не стабильный cross-plugin Python API.

## DevServer и сборка

Источники: [Development Server](https://plugins.exteragram.app/docs/dev-server), [Elyx Development and Build](https://plugins.exteragram.app/docs/elyx/development), [ElyxBuilder](https://plugins.exteragram.app/docs/elyx/elyxbuilder).

TCP DevServer слушает loopback `127.0.0.1:42690`; с телефона пробрасывается `adb forward tcp:42690 tcp:42690`. Протокол — соседние UTF-8 JSON objects. Запрос содержит `"@": command` и уникальный in-flight `"#": request_id`; ответ возвращает тот же `#`. Для single-file: `ping`, `get_plugins`, `enable_plugin`, `disable_plugin`, `reload_plugin`, `write_plugin(plugin_id, content)`, `remove_plugin`, `start_debugger(host, port, platform)`, `stop_debugger(platform)`. `write_plugin` передаёт полный исходник. Для Elyx: `elyx_ping`, `get_elyx_plugins`, `elyx_compare_folder`, `elyx_changes`. Изменения кодируются base64 полем `data`, внутри zlib-compressed JSON; `elyx_changes` содержит `plugin_id` и изменения created/modified/deleted/moved, относительные к корню пути и base64 bytes для содержимого. После применения плагин выгружается, модули очищаются и проект перезагружается.

Сервер опасен как dev интерфейс: docs прямо говорят, что команды могут установить, перезаписать, включить, выключить, reload и удалить код плагина; включать только во время разработки. Для debugger IDE отдельный порт (пример 5678), поддержанные `platform`: `vscode`, `pycharm`; ADB rule зависит от направления подключения. Внутри App пример remote path `/data/user/0/com.exteragram.messenger/files/plugins`.

Перед Elyx live sync архив нужно хотя бы раз установить и включить, чтобы running Elyx узнал plugin ID. ElyxBuilder — необязательный CLI (архив допустимо собрать вручную); он требует Python >=3.10, а компиляция `.pyc` — именно Python 3.11. Установите его командой `python -m pip install --upgrade ElyxBuilder`; типовые команды `elyb new`, `elyb new -g -n "My Plugin" -a myname`, `elyb build --ast --verbose --no-folder`, `elyb build --compile 2 --verbose --no-folder`, `elyb watch 10 --args "--ast -v -nf"`. `--ast` и `--compile` вместе не используются; Python bytecode должен собираться Python 3.11. Сам `elyx_dev_client.py` не входит в SDK и CLI зависит от своей версии — сначала смотрите `--help`.

## Диагностика Elyx и Android helpers

Источники: [Elyx Troubleshooting](https://plugins.exteragram.app/docs/elyx/troubleshooting), [Android Utilities](https://plugins.exteragram.app/docs/android-utils), [Common Telegram Classes](https://plugins.exteragram.app/docs/common-source-classes).

Troubleshooting рекомендует начинать с ошибки на странице плагина и логов приложения; подробные Elyx debug logs включать только на время диагностики. Для «archive not recognized» проверяйте расширение `.elyx`/`.eaf` (включая `.zip` варианты), полноту загрузки, доступность plugin/Elyx engines, ZIP-формат и пароль зашифрованного архива. «Metainfo not found» обычно требует metadata в корне или корректный `metainfo` path из `refmap`; YAML/JSON должны разбираться в непустую map. Важное расхождение: текущий Elyx validator принимает 2–32 ASCII letters/digits/underscore и отвергает дефис, хотя правило single-file `__id__` допускает дефис.

Для проблем imports/resources/localization проверяйте регистр путей, reserved roots (`elyx`, `ui`, `java`, `android`), наличие настроенной папки ресурсов/переводов, поддерживаемые расширения, UTF-8 и обязательный English catalog. Live reload требует установленный и загруженный archive с тем же plugin ID и активный forwarding `42690`; старое поведение после reload может быть вызвано внешними listeners, потоками, monkey patches или process-global cache. Архив релиза отдельно проверяйте на наличие всех configured entry files, assets, locale files, modules и wheels. Для диагностики docs просят указать версии app/SDK/Elyx, Android/ABI, metadata/refmap, минимальную структуру проекта и полный traceback; перед передачей логов удалить секреты и личные данные.

`android_utils.log(data)` отправляет простые значения как текст, сложные объекты — в Java-side object inspector; `copy_to_clipboard(text)` копирует строку и при успехе показывает bulletin. Common Telegram Classes — указатель на upstream классы и их роли/пути (`LaunchActivity`, `ProfileActivity`, `ChatActivity`, `MessageObject`, `AndroidUtilities`, controllers/storage/helpers, `TLRPC`), а не доказательство контракта Python SDK. Эти ссылки полезны для исследования деталей, но читать upstream код и запускать клиент в рамках этого review не выполнялось.

## Permissions, unknown и проверка фактов

В перечисленных 33 страницах нет описанной plugin permission declaration/grant API или списка разрешений. Это означает «не задокументировано в исследованном navigation tree», а не доказательство отсутствия permissions в приложении или в другом SDK разделе. Также не подтверждены запуск на эмуляторе/телефоне, compatibility каждого API с конкретным app build и поведение hooks при исключениях/параллельных callback-ах. Для таких вопросов см. [work/official-sdk-facts.json](../facts/official-sdk.json): документированные контракты отделены от версионных расхождений и runtime-unverified замечаний.

## Покрытие навигации

Все 33 страницы корневой навигации просмотрены и сохранены как raw HTTP HTML. Сокращённые заголовки в первом столбце ведут к первоисточнику; все полученные URL, timestamp UTC, HTTP статус, размер и назначение также перечислены в manifest.

| Раздел | Охваченные страницы |
|---|---|
| Начало | [Introduction](https://plugins.exteragram.app/docs), [Setup](https://plugins.exteragram.app/docs/setup), [First Plugin](https://plugins.exteragram.app/docs/first-plugin) |
| Elyx | [Overview](https://plugins.exteragram.app/docs/elyx), [Quick Start](https://plugins.exteragram.app/docs/elyx/quick-start), [ElyxBuilder](https://plugins.exteragram.app/docs/elyx/elyxbuilder), [Project Structure](https://plugins.exteragram.app/docs/elyx/project-structure), [Metadata](https://plugins.exteragram.app/docs/elyx/metadata), [Modules and Imports](https://plugins.exteragram.app/docs/elyx/modules-and-imports), [Assets](https://plugins.exteragram.app/docs/elyx/assets), [Localization](https://plugins.exteragram.app/docs/elyx/localization), [Settings Storage](https://plugins.exteragram.app/docs/elyx/settings), [Dependencies](https://plugins.exteragram.app/docs/elyx/dependencies), [Development and Build](https://plugins.exteragram.app/docs/elyx/development), [Public API](https://plugins.exteragram.app/docs/elyx/public-api), [Troubleshooting](https://plugins.exteragram.app/docs/elyx/troubleshooting) |
| База SDK | [Plugin Class](https://plugins.exteragram.app/docs/plugin-class), [Multi-account](https://plugins.exteragram.app/docs/multi-account), [Plugin Settings](https://plugins.exteragram.app/docs/plugin-settings), [Class Proxy](https://plugins.exteragram.app/docs/class-proxy), [Xposed Hooking](https://plugins.exteragram.app/docs/xposed-hooking) |
| Утилиты | [Android Utilities](https://plugins.exteragram.app/docs/android-utils), [Client Utilities](https://plugins.exteragram.app/docs/client-utils), [Text Formatting](https://plugins.exteragram.app/docs/text-formatting), [Hook Utilities](https://plugins.exteragram.app/docs/hook-utils), [File Utilities](https://plugins.exteragram.app/docs/file-utils), [Intents](https://plugins.exteragram.app/docs/intents), [Alert Dialog Builder](https://plugins.exteragram.app/docs/alert-dialog-builder), [Bulletin Helper](https://plugins.exteragram.app/docs/bulletin-helper) |
| Остальное | [Development Server](https://plugins.exteragram.app/docs/dev-server), [PIP & Dependencies](https://plugins.exteragram.app/docs/pip), [Available Libraries](https://plugins.exteragram.app/docs/available-libraries), [Common Telegram Classes](https://plugins.exteragram.app/docs/common-source-classes) |

### Первичные ссылки на Telegram code, перечисленные в SDK docs

`Common Telegram Classes` ведёт к upstream источникам класса, а не к реализации Python SDK: [LaunchActivity](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java), [ChatActivity](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java), [MessageObject](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/MessageObject.java), [MessagesController](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java), [MessagesStorage](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/MessagesStorage.java), [SendMessagesHelper](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/SendMessagesHelper.java), [AlertDialog](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/ui/ActionBar/AlertDialog.java). Для TL-схемы docs отдельно ссылаются на [corefork.telegram.org/schema](https://corefork.telegram.org/schema) и предупреждают, что список не всегда актуален. Эти Telegram источники объясняют underlying classes, но не подтверждают Python wrapper поведение.
