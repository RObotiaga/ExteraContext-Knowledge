# Independent review: exteraStuff/gradle-plugin

- **Scope:** `exteraStuff/gradle-plugin`, commit `290bb3bc34e8cc8e8126a880a464a77bfa572d80`; reviewed source page `../sources/gradle-plugin.md` and fact ledger `work/gradle-plugin-facts.json`.
- **Verdict:** `accepted-with-gaps`.
- **Coverage:** independently inspected the complete captured README, build/settings/toolchain metadata, full tree and all 16 captured Kotlin implementation files (22 files total in `raw/gradle-plugin/files`). The radar context and source record were checked for the intended scope. The implementation review covered plugin application/AGP gating, DSL extensions, variant task registration and outputs, Shadow inputs and relocation, Telegram JAR filtering and ASM `InnerClasses` reconstruction, R8/D8 classpaths and worker isolation, service scopes and nested-JAR packing, manifest metadata, dependency validation, signing/TSA handling, build-cache annotations, publication clues, and absent tests/workflows/consumer fixtures.
- **Evidence boundary:** all conclusions about implementation are source inspection at the pinned commit, not a Gradle build or runtime test. No downloaded code was executed. The README's Gradle/AGP compatibility and cache/configuration-cache support remain documentation claims.

## Findings and corrections

1. The source page's README cache summary missed a code/documentation conflict. README classifies `buildDex*` as up-to-date-only, while `BuildDexTask` is annotated `@CacheableTask`. I amended the page to keep the README statement attributed to docs and record the implementation annotation separately. No consumer build was run, so actual build-cache behavior remains unverified. The corresponding additional ledger fact is `gradle-plugin-039`.
2. Ledger fact `gradle-plugin-036` incorrectly said README reports version `0.1.2`; that value and plugin id come from `build.gradle.kts`. I corrected the claim to identify the actual source.
3. Reviewed facts `gradle-plugin-001` through `gradle-plugin-038` against their cited snapshot paths and the corresponding source sections. Their DSL signatures, task gates, artifact/manifest behavior, relocation and R8/D8 claims, signing defaults, and no-permission/no-reload boundaries are consistent with the inspected code, subject to the caveats above.

## Coverage, duplicates, and remaining gaps

The 39 ledger entries are unique within this source by claim. Some intentionally neighboring claims describe separate contracts: default directories versus archive names; packaging versus signing task gates; dependency metadata versus provided/required service packaging. I found no exact duplicate that should be merged. Cross-source canonical topic consolidation belongs to the later synthesis pass and was not changed here.

The page correctly avoids attributing permissions DSL, `publishPlugin`, DevServer payloads, reload/watch behavior, or client-side manifest validation to this Gradle plugin. `tree.json` contains no test source, CI workflow, or sample consumer project. Therefore plugin application, DSL compilation, task execution, cache behavior, output validity, consumer compatibility, signature verification, and client loading remain untested. These are explicit gaps, not claims of failure.

**Accepted with gaps:** the page and ledger cover the captured implementation and documentation scope; the remaining limits are integration/runtime verification and the noted README/cache discrepancy.
