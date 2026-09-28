---
type: review
source_id: televip
reviewer: /root/review_televip
collector: /root/collect_televip
model: gpt-6-luna
verdict: unavailable-verified
date: 2026-09-28
accepted_facts: 9
---

# Независимая проверка TeleVip

## Область и снимок

Проверена только назначенная цель `Xposed-Modules-Repo/com.my.televip`, snapshot `ebb10ec44719a516177f525e70ab19d686e3d288`. Репозиторий/коммит отдельной ссылки `mustafa1dev/TeleVip-Lsposed` не использован как замена кода или доказательство реализации release APK.

Сверены `raw/televip/snapshot.json`, весь `tree.json`, `file-manifest.json`, `repository.json`, `radar-context.md`, пустой `radar-urls.json` и полные файлы README/SUMMARY. В исходном capture README уже был, но README-документированный `SUMMARY` был пропущен из локальных файлов/manifest; я повторно получил `SUMMARY` командой acquisition для той же цели и SHA. Сейчас tree содержит ровно `README.md` и `SUMMARY`, `truncated=false`, а SHA-256 обоих файлов совпадает с `file-manifest.json`. Источники: [зафиксированный tree](https://api.github.com/repos/Xposed-Modules-Repo/com.my.televip/git/trees/ebb10ec44719a516177f525e70ab19d686e3d288?recursive=1), [README permalink](https://github.com/Xposed-Modules-Repo/com.my.televip/blob/ebb10ec44719a516177f525e70ab19d686e3d288/README.md), [SUMMARY permalink](https://github.com/Xposed-Modules-Repo/com.my.televip/blob/ebb10ec44719a516177f525e70ab19d686e3d288/SUMMARY).

## Независимые проверки distribution и ссылок

GitHub REST API проверен live 2026-09-28. [`GET /releases?per_page=100`](https://api.github.com/repos/Xposed-Modules-Repo/com.my.televip/releases?per_page=100) возвращает `330-3.6.2` первым из 20 релизов; его [release endpoint](https://api.github.com/repos/Xposed-Modules-Repo/com.my.televip/releases/tags/330-3.6.2) показывает `TeleVip.apk`. Это подтверждает публикацию asset, но я не загружал и не декодировал APK, поэтому его содержимое, соответствие исходникам и безопасность не подтверждены.

Исторический [tag 315-3.5](https://api.github.com/repos/Xposed-Modules-Repo/com.my.televip/git/ref/tags/315-3.5) указывает на annotated tag `dcc53932126c6c7e131e9958f4fece4b7bf807d9`; [tag object](https://api.github.com/repos/Xposed-Modules-Repo/com.my.televip/git/tags/dcc53932126c6c7e131e9958f4fece4b7bf807d9) разрешается в commit `73d168b941470c6c86ed4a13dc67c4770b893bcc`. У commit нет parent, сообщение `315-3.5`, а tree SHA — canonical empty-tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`; GitHub tree endpoint для этого SHA возвращает 404. При этом [release tag page](https://github.com/Xposed-Modules-Repo/com.my.televip/releases/tag/315-3.5) и releases API перечисляют `app-release.apk`. Это согласуется с раздельным наличием бинарного asset и отсутствием файлов в Git tree коммита.

README links проверены на предмет идентичности и цели. `mustafa1dev/TeleVip-Lsposed` доступен как отдельный GitHub repo (API возвращает `full_name=mustafa1dev/TeleVip-LSPosed`, ID `900002599`, default branch `main`); его code tree не изучался и его контракт не переносился на точную цель. README credit link `Sakion-Team/Re-Telegram` API разрешает в `Nep-Timeline/Re-Telegram` (ID `663325586`), что я отразил только как README provenance/credit, не как доказанный заимствованный код. Относительная ссылка [README `./LICENSE`](https://github.com/Xposed-Modules-Repo/com.my.televip/blob/ebb10ec44719a516177f525e70ab19d686e3d288/LICENSE) не имеет цели в pinned tree; contents endpoint для `LICENSE` возвращает 404. Поэтому README GPL-3.0 badge/text — опубликованное утверждение, не проверка license file. В `radar-urls.json` нет дополнительных закреплённых URL.

## Facts, исправления и дубликаты

Все **9** machine facts имеют уникальные ID; точных повторов внутри источника нет. Проверены уровни доказательств: README claims остаются `secondary`, GitHub release/ref/tree metadata не объявляется кодом, отсутствие кода и отсутствие runtime/build evidence не выдается за runtime test. Факт о TeleVip destination связывает только проектную ссылку; он отдельно оговаривает, что code-level provenance release не установлена.

Исправлены capture и описания: добавлен недостающий `SUMMARY`; уточнено, что 3.6.2 — первый/latest listed release на дату проверки и что APK не инспектировался; для `315-3.5` доказательства уточнены как tag-object → commit → canonical empty tree при наличии release asset; feature fact сообщает, что сам README говорит о не перечисленных дополнительных функциях; license fact отмечает отсутствующий `LICENSE`; добавлен README warning о риске проблем/блокировки аккаунта Telegram с явной пометкой, что предупреждение не является воспроизведённым runtime-эффектом. Source page и facts содержат эти же границы. Канонические темы на будущее: Xposed/LSPosed availability and asset-vs-source provenance; опубликованные README claims о клиентской совместимости; README warnings/licensing. Общие topic/index страницы не менялись.

## Остаточные пробелы и verdict

В exact snapshot нет исходного кода, build-конфигурации, tests или license file. APK 3.6.2 и `app-release.apk` 3.5 не скачивались/не проверялись; связь каждого release asset с source commit не установлена. Матрица клиентов и функции README не проверялись на устройствах или в конкретных клиентах; сборка, hook API, lifecycle/thread behavior и runtime не исследовались. Прочитан весь релевантный материал, который доступен в точном snapshot, но невозможно утверждать полноту по отсутствующему коду или заявлению README об omitted features.

**Verdict: `unavailable-verified`.** Публикация release assets проверена, а отсутствие исходников именно в закреплённом snapshot и пустое дерево исторического tag независимо подтверждены. Принято **9 фактов** с ограничениями выше.
