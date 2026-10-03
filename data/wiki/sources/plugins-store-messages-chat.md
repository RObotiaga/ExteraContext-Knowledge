---
type: source
source_id: plugins-store-messages-chat
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-messages-chat.md
date: 2026-10-01
---

# Plugins-Store: Раздел сообщений и чатов (Messages & Chat)

Источник: 150 плагинов каталога [Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store) (`Plugins/`), отобранных по функционалу перехвата и модификации сообщений, работы со стилями текста, спойлерами, форматированием, автоответами, черновиками, а также хуками на `on_send_message_hook`, `SendMessagesHelper`, `ChatActivity`, `ChatActivityEnterView` и `ChatMessageCell`. Срез зафиксирован в неизменяемом манифесте `data/plugins-manifest.json`.

## Роль и границы источника

Данный раздел представляет собой практический срез реальных реализаций плагинов для Android-клиентов Telegram с поддержкой плагинов (ExteraGram, AyuGram). Исходный код плагинов демонстрирует актуальные конвенции расширения мессенджера через Chaquopy (Python/JVM bridge), рефлексию над Android/Telegram классами и встроенную подсистему перехвата сообщений.

**Границы применимости:**
* Реализации используют API хост-клиента на базе Android и Telegram v11.x–v12.x.
* Ни один из плагинов не сопровождается формальными модульными тестами; статус подтверждения — `code` (исследованный и верифицированный исходный код), статус рецензирования — `accepted-with-gaps`.
* Часть плагинов обращается к недокументированным полям через приватную рефлексию Java (`getDeclaredField`, `setAccessible(True)`), что требует осторожности при миграции между минорными версиями клиента.

## Покрытие

| Область / Путь | Исследованные компоненты | Извлеченные механизмы | Пробелы и специфика |
|---|---|---|---|
| `on_send_message_hook` (95 плагинов) | `Gos_censorship`, `CompactText`, `dont65textreplacer`, `photoQuote`, `all_mention`, `auto_delete`, `SendSound`, `Shtrix` | Приоритеты вызовов (`priority`), мутация `params.message`, `params.entities`, `params.path`, отмена отправки (`CANCEL`), завершение цепочки (`MODIFY_FINAL`) | Различия в сигнатурах (`(self, account, params)` vs `(self, account: int, params: Any) -> HookResult`) |
| `ChatActivityEnterView` (16 плагинов) | `always_send_button`, `TextReplacement`, `enhanced_text_toolbar`, `clawd_pet`, `QuickReplies` | Доступ к `getEditField()`, управление кнопками отправки/записи, методы `makeSelectedSpoiler()`, `makeSelectedBold()`, `setFieldText("")` | Приватные поля UI зависят от обфускации базового Telegram |
| `ChatActivity` & меню (61 плагин) | `OldBottomForward`, `tdesktop_copy`, `hide_pinned_messages`, `quick_note2`, `AegisGuard`, `SearchIt` | `MenuItemType.CHAT_ACTION_MENU`, `MenuItemType.MESSAGE_CONTEXT_MENU`, `getMessageContent`, `openForward`, скрытие закрепленных сообщений | Обработка клика передает разные структуры `context` в зависимости от типа меню |
| `SendMessagesHelper` (10 плагинов) | `big_reactions`, `caption_fix`, `rounder`, `rounds_manager`, `auto_delete`, `QPS` | `prepareSendingDocument`, принудительные большие реакции (`args[3] = True`), восстановление потерянных подписей `caption` | Требует экземпляра `SendMessagesHelper.getInstance(account)` |
| `ChatActivityAdapter` & Cells (10 плагинов) | `hide_system_notifications`, `nodisturb`, `anti_spoiler` | Подмена `getItemViewType` на отрицательный ID, локальное обновление `cell.invalidate()`, динамическая подгрузка DEX | Модификация ячеек в реальном времени может вызывать мерцание при скролле без ViewHolder-заглушки |

---

## Технические факты

### 1. Жизненный цикл и конвейер `on_send_message_hook`

Перехват исходящих сообщений регистрируется в методе `on_plugin_load()` базового класса плагина:
* **Регистрация:** `self.add_on_send_message_hook(priority=int)`. Приоритет определяет порядок плагинов в конвейере. По умолчанию `priority=0`. Плагины используют значения `100` (`murintranslator.plugin:84`, `metadata_stripper_pro.plugin:50`), `200` (`dont65textreplacer.plugin:195`), `1000` (`CompactText.plugin:58`) и `Integer.MAX_VALUE` (`sender.plugin:590`).
* **Сигнатура:**
  ```python
  def on_send_message_hook(self, account: int, params: Any) -> HookResult:
  ```
* **Стратегии возврата (`HookStrategy`):**
  1. `HookResult()` или `None` — сообщение пропускается дальше без изменений (`HookStrategy.DEFAULT`).
  2. `HookResult(strategy=HookStrategy.CANCEL)` — полная отмена отправки сообщения. Сетевой запрос к серверам Telegram блокируется (`CompactText.plugin:206`, `Crypter.plugin:178`, `auto_delete.plugin:459`).
  3. `HookResult(strategy=HookStrategy.MODIFY, params=params)` — замена параметров сообщения и передача управления следующему плагину в цепочке (`Gos_censorship.plugin:1331`, `Shtrix.Plugin:196`).
  4. `HookResult(strategy=HookStrategy.MODIFY_FINAL, params=params)` — терминальная фиксация параметров. Последующие плагины в конвейере отправки игнорируются, сообщение немедленно уходит на отправку (`dont65textreplacer.plugin:232`, `comlist.plugin:1001`).

### 2. Структура и мутация объекта `params`

Объект `params` инкапсулирует параметры отправки (`org.telegram.messenger.SendMessagesHelper$SendMessageParams`):
* `params.message`: строка с текстом отправляемого сообщения. Изменение этого поля переопределяет отправляемый текст (`Gos_censorship.plugin:1330`).
* `params.peer`: целочисленный идентификатор диалога (ID чата, пользователя или канала).
* `params.entities`: список сущностей оформления (`TLRPC$MessageEntity`). Может быть представлен как `java.util.ArrayList` или Python `list` (`comlist.plugin:982`, `long_quote_auto.plugin:76`).
* `params.replyToMsg`: объект сообщения (`TLRPC$Message` или `MessageObject`), на которое формируется ответ (`quoteReply.plugin:162`, `sender.plugin:627`).
* `params.replyToTopMsg`: сообщение корня ветки обсуждения или темы форума (`sender.plugin:628`, `CompactText.plugin:706`).
* `params.replyQuote`: блок цитирования (`TLRPC$TL_inputReplyToQuote`). Присвоение этого поля преобразует обычный ответ в точечную цитату (`quoteReply.plugin:170`).
* `params.disable_web_page_preview`: логический флаг отключения предпросмотра ссылок (`hidelink_preview_1.0.0r.plugin:136`).
* `params.path`, `params.videoPath`, `params.imagePath`: пути к медиафайлам на локальной файловой системе устройства (`metadata_stripper_pro.plugin:54-68`).
* `params.document`: объект документа при отправке файлов/стикеров (`auto_delete.plugin:426`).
* Поле `notify`: приватное поле Java-класса параметров, отвечающее за отправку без звука. Сбрасывается рефлексивно: `params.getClass().getDeclaredField("notify").set(params, False)` (`AegisGuard.plugin:511`).

### 3. Сущности Telegram, спойлеры и расчет UTF-16 смещений

* **Расчет UTF-16 Code Units:** Telegram требует, чтобы `offset` и `length` сущностей (`MessageEntity`) считались в 16-битных единицах UTF-16, а не в символах Python (`len(str)`). Для корректного учета эмодзи и суррогатных пар используется:
  ```python
  entity.length = len(text.encode('utf_16_le')) // 2
  ```
  Код подтвержден в `comlist.plugin:1035`.
* **Сворачиваемые цитаты:** создаются через экземпляр `TLRPC.TL_messageEntityBlockquote`:
  ```python
  quote = TLRPC.TL_messageEntityBlockquote()
  quote.offset = 0
  quote.length = len(text.encode('utf_16_le')) // 2
  quote.flags = 1
  quote.collapsed = True
  params.entities.add(0, quote)
  ```
  Код подтвержден в `long_quote_auto.plugin:67-76` и `comlist.plugin:1032-1036`.
* **Скрытый предпросмотр веб-страниц:** добавление невидимого символа `\u200b` (нулевая ширина) с прикреплением сущности `TL_messageEntityTextUrl` длиной 1 позволяет сгенерировать карточку сайта без отображения ссылки в тексте (`hidelink_preview_1.0.0r.plugin:100-115`).
* **Markdown-парсер клиента:** плагины парсят форматированный текст через `markdown_utils.parse_markdown(text)` и конвертируют спаны через `entity.to_tlrpc_object()`, добавляя их в `params.entities` (`comlist.plugin:1041`, `all_mention.plugin:193`).

### 4. Взаимодействие с полем ввода и `ChatActivityEnterView`

* **Встроенные методы стилизации текста:** объект поля ввода `ChatActivityEnterView.getEditField()` предоставляет готовые нативные методы для выделенного фрагмента (`text_field.setSelection(0, length)`):
  * `makeSelectedBold()` — жирный шрифт
  * `makeSelectedItalic()` — курсив
  * `makeSelectedMono()` — моноширинный шрифт
  * `makeSelectedQuote(collapsed: bool)` — цитата (включая свернутую)
  * `makeSelectedSpoiler()` — спойлер (скрытый текст)
  Код подтвержден в `TextReplacement.plugin:176-189`.
* **Программная очистка поля ввода:**
  ```python
  fragment = get_last_fragment()
  enter_view = fragment.getChatActivityEnterView()
  enter_view.setFieldText("")
  ```
  Код подтвержден в `CompactText.plugin:1391`.
* **Фиксация кнопки отправки (`always_send_button`):** предотвращение переключения кнопки отправки на голосовое/видео-сообщение достигается перехватом `checkSendButton`, `updateAudioVideoButton` и `updateRecordInterface` в `ChatActivityEnterView` со сбросом приватного поля `set_private_field(ev, "recordingAudioVideo", False)` и установкой `sendButton.setVisibility(View.VISIBLE)` (`always_send_button.plugin:54-66, 168`).

### 5. Архитектура `ChatActivity` и адаптера сообщений

* **Меню чата и контекстное меню сообщений (`MenuItemData`):**
  * `MenuItemType.CHAT_ACTION_MENU` — меню «три точки» на панели инструментов чата (`AegisGuard.plugin:82`, `Crypter.plugin:115`).
  * `MenuItemType.MESSAGE_CONTEXT_MENU` — меню действий над конкретным сообщением (`Crypter.plugin:109`, `SearchIt.plugin:2725`). В функцию `on_click(context)` передается словарь, содержащий `context.get("message")` (`MessageObject`) и `context.get("fragment")` (`ChatActivity`).
* **Локальная модификация текста ячейки без сети:**
  ```python
  message.applyNewText(text)
  message.forceUpdate = True
  cell = fragment.findMessageCell(msg_id, False)
  if cell:
      cell.getMessageObject().applyNewText(text)
      cell.invalidate()
  ```
  Код подтвержден в `Shtrix.Plugin:164-173`.
* **Скрытие системных сервисных сообщений:** перехват метода `ChatActivity$ChatActivityAdapter.getItemViewType(int position)` позволяет вернуть отрицательный ID типа ячейки (`-1000`), а в `onCreateViewHolder` вернуть пустой невидимый `View` с нулевой высотой, полностью исключая системное сообщение из списка (`hide_system_notifications.plugin:415-434, 521`).
* **Модификация копируемого текста:** перехват `ChatActivity.getMessageContent(MessageObject)` позволяет дополнять копируемый текст датой и временем в стиле TDesktop (`tdesktop_copy.plugin:22-38, 50`).

### 6. Контракты `SendMessagesHelper` и медиа-функций

* **Программная отправка документов:** статический метод `SendMessagesHelper.prepareSendingDocument(account, path, path, None, None, mime, dialog_id, reply_to_msg, reply_to_top_msg, None, None, None, True, 0, None, None, 0, False)` отправляет файл напрямую в чат (`CompactText.plugin:709`).
* **Принудительные большие реакции:** перехват метода `SendMessagesHelper.sendReaction` с установкой аргумента `args[3] = True` активирует полноэкранную анимацию для всех реакций (`big_reactions.plugin:22-25, 36`).
* **Асинхронная отправка через перехватчик сообщений:**
  ```python
  # В хуке on_send_message_hook:
  self._pending_params = params
  self._pending_account = account
  return HookResult(strategy=HookStrategy.CANCEL)

  # Позже в UI-обработчике:
  smh = SendMessagesHelper.getInstance(self._pending_account)
  smh.sendMessage(self._pending_params)
  ```
  Код подтвержден в `auto_delete.plugin:452-459, 641-643`.

---

## Вызовы и наблюдаемые контракты

| Класс / Интерфейс | Метод / Член | Сигнатура / Типы | Назначение | Доказательство |
|---|---|---|---|---|
| `BasePlugin` | `add_on_send_message_hook` | `(priority: int = 0) -> None` | Регистрация перехватчика исходящих сообщений с приоритетом | `CompactText.plugin:58` |
| `BasePlugin` | `on_send_message_hook` | `(account: int, params: Any) -> HookResult` | Точка перехвата исходящего сообщения перед отправкой в сеть | `Gos_censorship.plugin:1290` |
| `HookResult` | конструктор | `(strategy=HookStrategy.*, params=None)` | Управление поведением сообщения (CANCEL, MODIFY, MODIFY_FINAL) | `dont65textreplacer.plugin:232` |
| `BasePlugin` | `add_menu_item` | `(item: MenuItemData) -> int` | Регистрация пункта в меню чата или контекстном меню сообщения | `Crypter.plugin:108` |
| `BasePlugin` | `remove_menu_item` | `(item_id: int) -> None` | Динамическое удаление ранее зарегистрированного пункта меню | `SearchIt.plugin:2745` |
| `ChatActivity.ReplyQuote` | `from` | `(msg: MessageObject) -> ReplyQuote` | Создание объекта цитаты из сообщения (вызывается через `getattr`) | `quoteReply.plugin:169` |
| `ChatActivityEnterView` | `setFieldText` | `(text: CharSequence) -> None` | Установка текста в поле ввода сообщения | `CompactText.plugin:1391` |
| `ChatActivityEnterView` | `getEditField` | `() -> EditTextCaption` | Получение нативного виджета поля ввода текста | `TextReplacement.plugin:144` |
| `EditTextCaption` | `makeSelectedSpoiler` | `() -> None` | Обертывание выделенного текста в поле ввода в спойлер | `TextReplacement.plugin:184` |
| `SendMessagesHelper` | `prepareSendingDocument` | `(account, path, path, ..., dialog_id, ...)` | Отправка произвольного файла без открытия диалоговых окон | `CompactText.plugin:709` |
| `SendMessagesHelper` | `sendMessage` | `(params: SendMessageParams) -> None` | Отправка подготовленного объекта сообщения через ядро мессенджера | `auto_delete.plugin:643` |
| `SendMessagesHelper` | `sendReaction` | `(..., boolean big, ...) -> None` | Отправка реакции на сообщение (args[3] отвечает за большой эффект) | `big_reactions.plugin:25` |
| `ChatActivity` | `getMessageContent` | `(msg: MessageObject, ...) -> CharSequence` | Формирование текста при копировании одного или нескольких сообщений | `tdesktop_copy.plugin:50` |
| `ChatActivity` | `openForward` | `(boolean oldStyle) -> None` | Открытие диалога выбора чатов для пересылки сообщения | `OldBottomForward.plugin:30` |
| `ChatActivity` | `openVideoEditor` | `(videoPath: str, outputPath: str) -> None` | Вызов встроенного видеоредактора для кружков | `rounds_manager.plugin:53` |
| `PhotoViewer` | `sendPressed` | `(..., ...) -> None` | Нажатие кнопки отправки в просмотрщике фото/видео | `caption_fix.plugin:81` |
| `dalvik.system.InMemoryDexClassLoader` | конструктор | `(ByteBuffer dex, ClassLoader parent)` | Динамическая загрузка байткода DEX из памяти устройства | `anti_spoiler.plugin:79` |

---

## Практические приёмы и рецепты

### Рецепт 1: Перехват и замена текста с защитой от искажения суррогатных пар
```python
from base_plugin import BasePlugin, HookResult, HookStrategy
from java.util import ArrayList
from org.telegram.tgnet import TLRPC

class TextModifierPlugin(BasePlugin):
    def on_plugin_load(self):
        self.add_on_send_message_hook(priority=100)

    def on_send_message_hook(self, account: int, params) -> HookResult:
        if not hasattr(params, "message") or not params.message:
            return HookResult()

        text = str(params.message)
        if text.startswith(".shrug"):
            params.message = text.replace(".shrug", "¯\_(ツ)_/¯")
            return HookResult(strategy=HookStrategy.MODIFY_FINAL, params=params)

        return HookResult()
```

### Рецепт 2: Добавление свернутой цитаты (Collapsible Blockquote)
```python
def wrap_in_collapsed_quote(params, text: str):
    params.message = text
    if not hasattr(params, "entities") or params.entities is None:
        params.entities = ArrayList()
    else:
        params.entities.clear()

    quote = TLRPC.TL_messageEntityBlockquote()
    quote.offset = 0
    # Telegram требует UTF-16 code units:
    quote.length = len(text.encode("utf_16_le")) // 2
    quote.flags = 1
    quote.collapsed = True
    params.entities.add(quote)
```

### Рецепт 3: Преобразование обычного ответа в цитату с обходом ключевого слова Python
```python
from org.telegram.ui import ChatActivity

def convert_reply_to_quote(params):
    if getattr(params, "replyToMsg", None) and params.replyQuote is None:
        # ChatActivity.ReplyQuote.from() недоступен напрямую из-за 'from' в Python:
        create_quote = getattr(ChatActivity.ReplyQuote, "from")
        params.replyQuote = create_quote(params.replyToMsg)
```

### Рецепт 4: Асинхронный диалог подтверждения перед отправкой сообщения
```python
class ConfirmSendPlugin(BasePlugin):
    def on_send_message_hook(self, account: int, params) -> HookResult:
        if getattr(self, "_in_progress", False):
            return HookResult()

        self._pending_params = params
        self._pending_account = account
        self._in_progress = True

        run_on_ui_thread(self._show_confirm_dialog)
        return HookResult(strategy=HookStrategy.CANCEL)

    def _show_confirm_dialog(self):
        # Показать диалог AlertDialogBuilder...
        # При подтверждении пользователя:
        smh = SendMessagesHelper.getInstance(self._pending_account)
        smh.sendMessage(self._pending_params)
        self._in_progress = False
```

### Рецепт 5: Контекстное меню сообщения с чтением текста
```python
def on_plugin_load(self):
    self.add_menu_item(MenuItemData(
        menu_type=MenuItemType.MESSAGE_CONTEXT_MENU,
        text="Действие плагина",
        icon="msg_edit",
        on_click=self._on_message_action
    ))

def _on_message_action(self, context: dict):
    msg_obj = context.get("message")
    if not msg_obj:
        return
    raw_text = getattr(msg_obj, "messageText", getattr(msg_obj, "text", ""))
    fragment = context.get("fragment") or get_last_fragment()
```

---

## Ограничения и противоречия

1. **Конфликт ключевого слова `from` в Python:** статический Java-метод `ChatActivity.ReplyQuote.from(...)` синтаксически не может быть вызван через точку в Python. Единственный рабочий способ вызова — через `getattr(ChatActivity.ReplyQuote, "from")(msg)`. Попытка прямого вызова приводит к `SyntaxError`.
2. **Аномалии с сообщениями AyuGram Anti-Delete:** удаленные собеседником сообщения, сохраненные локально AyuGram, имеют поле `messageOwner.ayuDeleted = True`. Попытка ответить на такое сообщение цитатой или переслать его серверу Telegram завершается сетевой ошибкой `RPCError: MESSAGE_ID_INVALID`, так как на сервере этого ID больше не существует. Плагины обязаны проверять `getattr(msg.messageOwner, "ayuDeleted", None)`.
3. **Рассинхронизация длины строк UTF-16 и Python:** многие авторы плагинов используют `len(text)` для расчета `entity.length`. Для символов за пределами Basic Multilingual Plane (эмодзи, некоторые математические знаки), где символ кодируется суррогатной парой в UTF-16, `len(str) == 1`, но Telegram ожидает `length == 2`. Это приводит к визуальному сдвигу форматирования или ошибкам парсинга на клиентах получателей.
4. **Утечки хуков при `on_plugin_unload()`:** исследование показало, что некоторые плагины (`nodisturb.plugin:1215`, `always_send_button.plugin:208`) накапливают зарегистрированные дескрипторы `MethodHook` в списках, но забывают вызвать `self.unhook_method(h)` в `on_plugin_unload()`, что приводит к утечкам памяти и накоплению паразитных перехватов в рантайме.
5. **Хрупкость рефлексии приватных полей:** использование `set_private_field(ev, "recordingAudioVideo", False)` и `getDeclaredField("notify")` завязано на непубличные имена внутренних полей Telegram. При сборках клиента с агрессивным обфусцированием R8/ProGuard эти имена могут отсутствовать или иметь другие идентификаторы.
