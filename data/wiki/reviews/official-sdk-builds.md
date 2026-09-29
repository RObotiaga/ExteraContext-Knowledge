---
type: review
source_id: official-sdk-builds
date: 2026-09-29
verdict: accepted-with-gaps
---

# Проверка official-sdk-builds

## Проверено

- официальный repository `exteraSquad/plugins-pysdk-builds`;
- полный доступный release list на 2026-09-29: 14 releases;
- для каждого release нормализованы SDK version, channel, build, tag, full commit SHA, publication date и asset metadata;
- каждый captured release содержит `stubs.zip` с size и SHA-256 digest;
- 1.4.3.9, 1.4.4.1 и 1.4.5.0 имеют несколько builds и разные stubs digests;
- GitHub `prerelease` не отражает beta-channel для этих releases.

## Вердикт

**accepted-with-gaps** как первичный источник version/build/artifact provenance.

Можно использовать для точной identity SDK snapshot и проверки artifact bytes по digest. Нельзя использовать для утверждения конкретного symbol/signature/introduced/removed boundary или runtime behavior.

## Остаточный gap

`stubs.zip` binaries не разобраны в этом capture. Следующий этап — скачать assets, проверить digest, нормализовать Python symbols и построить pairwise diff. До этого symbol-level compatibility остаётся unknown/version-uncertain, если нет другого прямого evidence.

Этот source создан после legacy prompt archive и не получает фиктивный legacy collector/reviewer provenance.
