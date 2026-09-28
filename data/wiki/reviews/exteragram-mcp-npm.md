---
type: review
source_id: exteragram-mcp-npm
reviewer: /root/review_exteragram_mcp_npm
requested_model: gpt-6-luna
verdict: accepted-with-gaps
fact_count: 10
---

# Независимая проверка npm-публикации ExteraGram MCP

## Область и snapshot

Проверен только `@catalystdev/exteragram-mcp@1.0.0` как registry package и его сравнение с GitHub snapshot `cataIystdev/exteragram-mcp@ad824092ae60d785d0f0f21f1897b74118a186b1`. Входы: `raw/exteragram-mcp-npm/{capture.json,packument.json,file-inventory.json,exteragram-mcp-1.0.0.tgz}`; GitHub-контекст: `raw/exteragram-mcp/{repository.json,snapshot.json,tree.json,file-manifest.json,files/package.json,files/README.md}`. В `tree.json` — 59 blobs: 24 `src/`, 22 `docs/`, 7 `tests/` и 6 корневых файлов. Source snapshot использован для идентификации, сравнения manifest/README и наличия source/test files; полный повторный review всех API не входил в этот scope.

Пакет и исходники читались как данные. Архив не устанавливался и ничего из него не запускалось.

## Независимые проверки

- Свежий запрос к официальному version packument подтвердил версию `1.0.0`, время публикации `2026-04-25T14:52:28.882Z`, SRI и SHA-1, `fileCount: 99`, `unpackedSize: 434341`, repository URL и один объект подписи. Эти значения совпали с сохранённым `packument.json`.
- Независимый пересчёт локального raw tarball: SHA-512 `H1BonRlPIu78bvMXKNe+Bv+jB9zWg/Kq1scabrieK+PU1CNw8vz6hnFGXfeD03dL6+Vrkp5fesabixLcUb2EzA==`; SHA-1 `be7558ecd720c6c4d6d836e5e64deca4622533b5`; SHA-256 `151c790cf61d4e8b3066f8c408433fa7926442379b8c33b6a85e6c409bab052f`. SHA-512 SRI и SHA-1 совпали с registry.
- Архив содержит 99 regular files, сумма размеров — 434341 байт. Независимо построенные path/size pairs полностью совпали с `file-inventory.json` и registry `fileCount/unpackedSize`; расхождений и повторов путей нет. Top-level entries: `LICENSE`, `README.md`, `package.json`, `dist/`; в `dist/` 96 файлов.
- Tarball `package.json` и `README.md` побайтно совпадают с соответствующими файлами snapshot. Их SHA-256: `fad6e49ba059a92cf390549df263caf4dcc2f118296f25d9df2459fadf1c5892` и `466a9fc281d996ea7b9bf6690a4ff7dd47bbea36680c273f82476e7ffa04b6ea`.
- README говорит 76 tools и 18 groups. Статический подсчёт `server.registerTool(` в опубликованных `dist/tools/*.js` даёт 81 вызов; `dist/server.js` подключает 18 регистрационных функций A–R. Это подтверждённое текстовое расхождение, не проверка фактически возвращаемого списка по MCP.
- Manifest задаёт ESM, `main`/`bin` на `dist/index.js` и Node `>=20`; `exports` и `types` отсутствуют, а `dist/index.d.ts` содержит `export {}`. Entry script статически импортирует MCP stdio transport и имеет Node shebang. Это описание файлов, не запуск CLI.
- `prepublishOnly` объявляет `npm run build && npm test`. Официальная npm lifecycle документация относит его к `npm publish`; само наличие команды не доказывает её фактический запуск/успех. Ни тесты, ни установка, ни runtime не запускались.

## Найденные и исправленные проблемы

1. Исходное описание создавало впечатление, что разница `CataIystDev`/`cataIystdev` — только регистр. Зафиксировано существенное визуально похожее различие символов: npm scope/publisher `catalystdev` содержит латинскую `l`, GitHub login `cataIystdev` — латинскую заглавную `I`. GitHub account ID `151609278` и npm publisher name `catalystdev` — разные реестровые идентификаторы; общность владельца ими не доказана. Repository URL из packument указывает на GitHub repository, но это заявление metadata, не подтверждение контроля одного аккаунта.
2. «Экспортируемая поверхность» уточнена: нет manifest `exports`/`types`, корневая декларация пустая, хотя 24 `.d.ts` входят в архив. `main`/`bin` описаны без заявления о runtime-успехе.
3. Добавлено, что уникальные npm-факты не дублируют каноническое описание реализации на странице `exteragram-mcp`; у них отдельный provenance и IDs.
4. Добавлена packageable ссылка `../facts/exteragram-mcp-npm.json`; ссылки `/work` и несуществующий JSON-артефакт не используются.
5. Уточнено значение `prepublishOnly` и добавлена ссылка на официальную npm lifecycle документацию.

## Проверка фактов и доказательств

В `work/exteragram-mcp-npm-facts.json` — 10 уникальных записей, IDs `exteragram-mcp-npm-001`–`exteragram-mcp-npm-010`, без дублирующих ID или повторов claim. Исправлены точные evidence paths и статическая/документальная границы для artifact digests, inventory, export surface, owner mismatch, 81/76 и lifecycle. Портируемые evidence URLs ведут на official npm registry/tarball, pinned GitHub SHA и npm docs.

## Остаточные gaps и verdict

- `dist.signatures` содержит signature metadata; cryptographic signature verification не проводилась.
- Нет подтверждённого provenance/attestation и побайтной воспроизводимой сборки всего `dist/` из указанного commit. Package/README match подтверждает только эти два файла.
- Связь между npm namespace/publisher и GitHub owner не установлена на уровне account control.
- Причина разницы README 76 и 81 статических регистраций неизвестна; runtime tool listing не получен.
- `prepublishOnly` не рассматривается как подтверждение successful build/tests для публикации; CI job result не проверялся.
- API и поведение инструментов, совместимость с реальным ExteraGram, установка, MCP handshake, ADB/device behavior не проверялись в рамках этого npm review.

**Вердикт: `accepted-with-gaps`.** Артефактно-проверяемые claims подтверждены; supply-chain provenance, account ownership и runtime claims остаются gaps.
