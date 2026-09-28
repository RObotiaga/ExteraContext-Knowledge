---
type: entity
entity_id: desktop-plengine
date: 2026-09-27
---

# AyuGram Desktop PLEngine

Изучайте интерфейс native-плагина и ABI вместе с движком и примером. Потоки, фильтрация HistoryItem и Qt-объекты относятся к Desktop; сигнатуры Android BasePlugin не устанавливают связь совместимости.

## Проверенные материалы

| Источник | Сведения для применения | Доказательства и проверка |
|---|---|---|
| [ayugram-plengine](../sources/ayugram-plengine.md) | PLEngine запускается из main() после создания Core::Launcher и до launcher->exec().<br>Автозагрузчик ждет 5 секунд и затем периодически проверяет Core::App().wasRan перед загрузкой найденных файлов.<br>AyuPlugin ABI содержит wchar_t массивы фиксированной длины, uintptr_t адреса и указатель на std::function callback; это зависит от ABI C++ toolchain и не является переносимым бинарным C ABI. | [первичный материал](https://github.com/MrCheatEugene/AyuGramDesktop-PLEngine/blob/55feefdb6abd702e368b12431de97313441362a0/Telegram/SourceFiles/main.cpp), [первичный материал](https://github.com/MrCheatEugene/AyuGramDesktop-PLEngine/blob/55feefdb6abd702e368b12431de97313441362a0/Telegram/SourceFiles/plengine/PLEMains.cpp), [первичный материал](https://github.com/MrCheatEugene/AyuGramDesktop-PLEngine/blob/55feefdb6abd702e368b12431de97313441362a0/Telegram/SourceFiles/AyuPlugin.h) · [проверка](../reviews/ayugram-plengine.md) |
| [ayugram-sample](../sources/ayugram-sample.md) | README говорит, что DllMain должен вернуть TRUE, иначе плагин не загрузится; реализация возвращает TRUE для всех четырёх причин вызова DLL.<br>AyuPlugin.h объявляет типы callback для setup, loop, фильтрации HistoryItem, исключения удаления, preprocess текста, popup, GUI, online-hook и pluginInfo; GUI получает оба builder и PLEPlugins.<br>README утверждает, что каждый плагин выполняется в отдельном потоке; это заявление документации, конкретное создание потока находится за пределами AyuSamplePlugin. | [первичный материал](https://github.com/MrCheatEugene/AyuSamplePlugin/blob/76d0514da1210e5f913c8c239713c2532d42cfea/dllmain.cpp#L211-L227), [первичный материал](https://github.com/MrCheatEugene/AyuSamplePlugin/blob/76d0514da1210e5f913c8c239713c2532d42cfea/AyuPlugin.h#L41-L56), [первичный материал](https://github.com/MrCheatEugene/AyuSamplePlugin/blob/76d0514da1210e5f913c8c239713c2532d42cfea/README.md#L8-L10) · [проверка](../reviews/ayugram-sample.md) |
| [ayugram-desktop](../sources/ayugram-desktop.md) | Plugin description UI обрабатывает `**bold**` и markdown-подобные `[label](url)` ссылки, проверяя URL через Ui::InputField::IsValidMarkdownLink; полный Markdown контракт этим не заявлен.<br>AyuSectionBuilder::addToggle инициализирует UI из getter, передаёт reactive toggle changes setter'у только если значение отличается от getter, и привязывает подписку к button->lifetime(). | [первичный материал](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/boxes/plugin_info_box.cpp), [первичный материал](https://github.com/AyuGram/AyuGramDesktop/blob/db3b9891cb0b04ebb7d8c0e71ada3bcc669b910a/Telegram/SourceFiles/ayu/ui/settings/ayu_builder.cpp) · [проверка](../reviews/ayugram-desktop.md) |
| [ayugram-desktop-plus](../sources/ayugram-desktop-plus.md) | AyuGram Desktop Plus описан как Desktop-клиент для Windows, Linux и macOS на базе Telegram Desktop; README помечает проект C++20 и Qt.<br>Новый feature помещается в Telegram/SourceFiles/ayu/features/<name>/, а его исходники перечисляются в ayugram_files в Telegram/CMakeLists.txt.<br>AyuInfra::init() запускает язык, БД, UI settings, icon, worker, remote config, translator и debug server именно в таком порядке. | [первичный материал](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/README.md#L8), [первичный материал](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/AGENTS.md#L119), [первичный материал](https://github.com/Kindness-Kismet/AyuGramDesktop-Plus/blob/b59475e090b64fd5c8bc4124535c515050b70ef0/Telegram/SourceFiles/ayu/ayu_infra.cpp#L71) · [проверка](../reviews/ayugram-desktop-plus.md) |

## Связанные понятия

- [hooks](../topics/hooks.md)
- [lifecycle](../topics/lifecycle.md)
- [threading](../topics/threading.md)
- [ui](../topics/ui.md)
- [build](../topics/build.md)
- [portability](../topics/portability.md)

[Все сущности](index.md) · [Наблюдаемые вызовы](../apis/index.md) · [Рецепты](../recipes/index.md) · [Пробелы и версии](../gaps.md)
