---
type: source
source_id: televip
platform: Android
review_status: unavailable-verified
review: ../reviews/televip.md
date: 2026-09-28
---

# TeleVip — `Xposed-Modules-Repo/com.my.televip`

## Идентичность и состояние материалов

Точная цель радара — [публичный репозиторий `Xposed-Modules-Repo/com.my.televip`](https://github.com/Xposed-Modules-Repo/com.my.televip), snapshot `ebb10ec44719a516177f525e70ab19d686e3d288` (`main`, 2026-09-27). Зафиксированное неполное дерево содержит ровно `README.md` и `SUMMARY`; исходного кода в snapshot нет. Это независимо сверено с Git Trees API 2026-09-28. Восстановленный `SUMMARY` сохранён в `raw/televip/files/SUMMARY` и добавлен в manifest; его текст — “TeleVip A module for modifying Telegram”.

Тег [315-3.5](https://github.com/Xposed-Modules-Repo/com.my.televip/releases/tag/315-3.5) разрешается через annotated tag `dcc53932126c6c7e131e9958f4fece4b7bf807d9` к коммиту `73d168b941470c6c86ed4a13dc67c4770b893bcc` с canonical empty tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`; релиз при этом прикладывает `app-release.apk`. GitHub Releases API на 2026-09-28 показывает 3.6.2 как самый новый релиз в списке и его asset `TeleVip.apk`. Asset не загружался и не анализировался.

README точного repo говорит “Move to TeleVip” и ссылается на отдельный [mustafa1dev/TeleVip-Lsposed](https://github.com/mustafa1dev/TeleVip-Lsposed), указывая на проектное продолжение. Это отдельный repository destination со своей историей кода. Его код здесь не рассматривается как source для release APK из `Xposed-Modules-Repo/com.my.televip`: ссылка README не устанавливает соответствие между конкретным бинарным релизом и конкретным commit destination repo. Следовательно, доступность: **release/APK — да; source code в точном радарном repo/snapshot — нет**.

`radar-urls.json` пуст; исторических закреплённых ссылок для этого источника в радарном контексте нет. Кода и APK не запускал, runtime-проверки нет.

## Покрытие

| Путь / материал точного источника | Извлечено | Ограничение |
|---|---|---|
| `snapshot.json`, `tree.json`, `file-manifest.json`, `repository.json` | SHA, состав дерева, публичная доступность и repo metadata; SHA-256 обоих сохранённых документов совпадают с manifest | Текущий snapshot содержит только документационные файлы |
| `README.md` и `SUMMARY` на snapshot `ebb10ec…` | Авторское описание проекта, заявленные функции и клиенты, destination link, предупреждение, сведения об авторе и лицензии | README/summary — заявления документации, не доказательство реализации или runtime; README ссылается на `LICENSE`, которого нет в tree |
| GitHub Releases API, Git refs/tags/commit/tree APIs (live, 2026-09-28) | Новейший listed release 3.6.2 и asset `TeleVip.apk`; tag 3.5, target commit `73d168b…` и canonical empty tree | APK не загружался и не инспектировался; commit release tag не содержит файлов |
| `radar-urls.json` | Проверено отсутствие сохранённых исторических permalinks | Дополнительные исторические URL радара отсутствуют |

## Подтверждённые сведения и границы

README описывает модуль для Telegram-клиентов, перечисляет функции приватности, медиа/историй, UI-модификаций, ускорения загрузок и local premium, а также матрицу клиентов и версий. README прямо говорит, что некоторые функции не перечислены, и предупреждает о возможных проблемах Telegram-аккаунта, включая бан/приостановку; это авторские заявления/предупреждение, не независимо установленный runtime-эффект. README ссылается на Telegram `t_l0_e`, указывает автора `@mustafa1dev` и заявляет GPL-3.0. При этом `LICENSE` в зафиксированном tree отсутствует, поэтому ссылку README на `./LICENSE` нельзя подтвердить содержимым лицензии. `SUMMARY` формулирует назначение как модуль для модификации Telegram. Ни публичные API, ни сигнатуры hook-ов, ни threading/lifecycle или рецепты реализации в доступном snapshot не обнаружены.

Отдельный README destination — важный идентификационный сигнал, но не замена исходников точной цели; его технические утверждения не переносятся на release-ы этого repo. Для этого источника закрыты identity, опубликованные документационные claims и состояние distribution; реализация, сборка и runtime остаются недоступными. [Независимый review](../reviews/televip.md).
