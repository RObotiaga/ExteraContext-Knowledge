---
type: review
source_id: plugins-store-automation-tools
review_status: accepted-with-gaps
reviewer: /root/review_plugins_store_automation_tools
date: 2026-10-01
---

# Независимая проверка: KPM Plugins-Store — автоматизация, системные инструменты, оверлеи и служебные утилиты

## Границы и независимость оценки

Независимая верификация охватывает раздел `plugins-store-automation-tools` каталога Plugins-Store (22 плагина).
Проверены соответствие извлечённых данных структуре репозитория ExteraContext-Knowledge, точность ссылок на код и отсутствие дублирования фактов.

## Анализ полноты и точности сбора

Сборщик проанализировал все 22 плагина выборки и извлёк **30 фактов**, охватывающих ключевые интерфейсы, паттерны и методы группы:
- Регистрацию в `MenuItemType.DRAWER_MENU`, `CHAT_ACTION_MENU`, `MESSAGE_CONTEXT_MENU` и программное закрытие шторки через `context['drawer_layout'].closeDrawer(False)`.
- Пакетное прочтение диалогов `MessagesStorage.readAllDialogs(-1)` и локальное прочтение через `MessagesController.markDialogAsRead` с рассылкой событий в `NotificationCenter`.
- Имитацию пользовательской активности `TLRPC.TL_messages_setTyping` с обязательным сбросом через `TL_sendMessageCancelAction()`.
- Перехват и отмену сетевых запросов `pre_request_hook` через `HookResult(strategy=HookStrategy.CANCEL)`.
- Внедрение внутриприложенных оверлеев в `LaunchActivity.getWindow().getDecorView()` без системных разрешений и системных плавающих окон через `WindowManager` с проверкой `Settings.canDrawOverlays`.
- Корректный жизненный цикл и предотвращение утечек памяти при работе с `WebView` (`pauseTimers`, `loadUrl('about:blank')`, `destroy`).
- Мониторинг жизненного цикла приложения через `on_app_event(AppEvent.PAUSE / RESUME)` и пакетное управление установленными плагинами через `PluginsController.getInstance().plugins`.
- Адаптацию под «режим призрака» в клиенте AyuGram через `com.radolyn.ayugram.controllers.AyuGhostController`.
- Выявление рисков безопасности (скрытая накрутка реакций в `smart_read_receipts`, обфускация в `tgws`).

Все факты подтверждены конкретными строками исходного кода в репозитории `Plugins-Store`.

## Проверка отсутствия дубликатов

- Внутри набора `plugins-store-automation-tools.json` каждый идентификатор факта уникален (`plugins-store-automation-tools:fact-001` ... `fact-030`).
- Проведено сопоставление утверждений с существующими фактами базы знаний `ExteraContext-Knowledge`: дословных повторов нет; новые факты расширяют эмпирическую базу реальными примерами из каталога плагинов KPM.
- Факты логически разделены по каноническим топикам (`ui`, `requests`, `workflow`, `compatibility`).

## Верификация утверждений и доказательств

1. Все call-sites (`self.hook_method`, `on_update_hook`, `pre_request_hook`, `add_menu_item`, UI вызовы, рефлексия) сверены с исходными файлами в каталоге `Plugins-Store/Plugins/`.
2. Статусы доказательств нормализованы к категории `code`.
3. Отмечены архитектурные ограничения (зависимость от внутренних классов Telegram, необходимость разрешения `SYSTEM_ALERT_WINDOW` для системных оверлеев).

## Итоговый вердикт и рекомендации

- Вердикт: **accepted-with-gaps**.
- Факты и описания пригодны для включения в канонические разделы базы знаний (топики `workflow`, `ui`, `requests`, `compatibility`).
- Рекомендуется учитывать версионные ограничения при практическом использовании извлечённых сигнатур.
