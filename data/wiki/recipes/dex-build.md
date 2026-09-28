---
type: recipe
date: 2026-09-27
---

# Проверка конвейера Kotlin/Java → DEX

Шаблоны могут производить разные артефакты: classes.dex, Python-loader, EAF или JAR с metadata. Команды одного инструмента не переносятся по названию задачи.

1. Сверьте фактический DSL и task names в выбранном SHA. Укажите plugin ID, entry class, клиентские зависимости и минимум версии.
2. Проверьте, какие классы хоста исключены из output, как исправляется compile classpath, какие зависимости перемещаются и что сохраняет R8.
3. Разделите debug/release и optional signing. Посмотрите архив как набор файлов: присутствуют entry, metadata и ожидаемый DEX; лишние host classes отсутствуют.
4. Для проверки incremental/cache behavior сравните implementation annotations и README, затем выполните собственный consumer build. Если такого опыта нет, оставьте его непроверенным.

## Доказательства и варианты

- [gradle-plugin](../sources/gradle-plugin.md): точные методы, версии и ограничения.
- [template-n08](../sources/template-n08.md): точные методы, версии и ограничения.
- [template-robotiaga](../sources/template-robotiaga.md): точные методы, версии и ограничения.

[Каталог рецептов](index.md) · [Справочник вызовов](../apis/index.md) · [Пробелы](../gaps.md)
