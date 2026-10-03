---
type: recipe
date: 2026-09-27
---

# Регистрация хуков с проверяемой очисткой

Точка вмешательства выбирается по событию, которое нужно изменить. SDK request/update/message hook, Xposed-style method hook и MethodReplacement имеют разные контракты.

1. Найдите метод и точную перегрузку в целевой версии; запишите типы параметров и семантику before/after или replacement.
2. Сохраните возвращенные handles сразу после регистрации. При ошибке показывайте причину и состояние частично установленной группы.
3. При unload снимите каждую успешно зарегистрированную операцию и освободите связанные listeners/tasks. Для временного replacement поставьте освобождение в finally.
4. Проверьте disable/enable/reload и число регистраций. Пустой список cleanup не подтверждает, что перехват снят.

## Доказательства и варианты

- [official-sdk](../sources/official-sdk.md): точные методы, версии и ограничения.
- [for-vibecoders](../sources/for-vibecoders.md): точные методы, версии и ограничения.
- [altylib](../sources/altylib.md): точные методы, версии и ограничения.
- [exteralib](../sources/exteralib.md): точные методы, версии и ограничения.
- [plugins-store-hooks-reflection](../sources/plugins-store-hooks-reflection.md): фильтры HookFilter (Condition, ArgumentNotNull), hook_all_methods и безопасный unhooking в 40 плагинах каталога KPM.

[Каталог рецептов](index.md) · [Справочник вызовов](../apis/index.md) · [Пробелы](../gaps.md)
