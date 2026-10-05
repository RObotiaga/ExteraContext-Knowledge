# Sample Quality Audit Report: Plugins-Store Verified Catalog

**Date:** 2026-10-03  
**Auditor:** Independent Verifier Subagents (blind review mode)  
**Corpus:** `RObotiaga/ExteraContext-Knowledge` (`feat/plugins-store-verified-catalog`)  
**Scope:** 15 plugin sources (75 sampled facts across small, medium, and large plugins)

---

## 1. Executive Summary & Audit Metrics

The independent sample audit verified 75 facts across 15 distinct plugin repositories spanning small (< 500 lines), medium (500–2,000 lines), and large (> 2,000 lines) plugin architectures, including all four mandatory verification targets (`SearchID`, `Profile_Plugin`, `Link Guard`, and `Air Raid Alert`).

| Metric | Target | Achieved | Status |
|---|---|---|---|
| **Sampled Facts** | Min 15 plugins (75 facts) | 75 facts (15 plugins) | **PASSED** |
| **Fully Correct as Verified** | High | 68 / 75 (90.7%) | **PASSED** |
| **Corrected (Line/Claim precision)** | Minor scope refinements | 7 / 75 (9.3%) | **PASSED** |
| **Rejected (Hallucinated/Invalid)** | 0% | 0 / 75 (0.0%) | **PASSED** |
| **Evidence Link Validity** | 100% resolvable | 75 / 75 (100.0%) | **PASSED** |
| **Commit Pin Authenticity** | 100% repository objects | 75 / 75 (100.0%) | **PASSED** |
| **Overclaim Rate** | Low | 1 / 75 (1.3%) | **PASSED** |
| **Runtime-Overclaim Rate** | 0% (Strict code status) | 0 / 75 (0.0%) | **PASSED** |
| **Line-Range Endpoint Accuracy** | > 90% | 72 / 75 (96.0%) | **PASSED** |

*All 7 identified citation/scope corrections were applied directly to the fact records in Stage 5.*

---

## 2. Sample Breakdown (Small, Medium, Large Plugins)

### Group A: Small Plugins (< 500 lines)
1. **`plugins-store-searchid` (149 lines):**
   - *Target:* SearchID v1.0.1 (Commit: `997557643701844731ba0186c65dd5d551497c66`)
   - *Checks:* `_chaquopy_reflector.getMethods("fillItems")`, `get_private_field`, `param.setResult()`, interactive Bulletin copy callback, and `unhook_method`.
   - *Audit Verdict:* 5/5 verified. Dead pin prefix was repaired to content commit `997557643701844731ba0186c65dd5d551497c66`.
2. **`plugins-store-chat-word-stats` (`просьба.plugin`, 265 lines):**
   - *Target:* ChatWordStats v1.0 (Commit: `f8f35b18b6148b20027b3bdeff505d240086444a`)
   - *Checks:* `TLRPC.TL_messages_getHistory` pagination, `Mandre` command registration, `run_on_queue`, and Markdown entity conversion.
   - *Audit Verdict:* 5/5 verified. Evidence scope tightened on pagination loop terminations and mandre_lib API boundary.
3. **`plugins-store-customitemmenu` (`CustomItеmMеnu.plugin`, 433 lines):**
   - *Target:* CustomItemMenu v1.5 (Commit: `f8f35b18b6148b20027b3bdeff505d240086444a`)
   - *Checks:* `MenuItemData` for 4 menu types, `UniversalRecyclerView` on `BottomSheet`, `R.drawable` blacklist (143 resources), negative evidence for uncalled `parse_markdown`.
   - *Audit Verdict:* 5/5 verified. Cyrillic `е` URL encoding verified; blacklist count corrected from 129 to 143.
4. **`plugins-store-fake-motion-blur` (116 lines):**
   - *Target:* fake motion blur v3.0.1 (Commit: `6ffd93145a9a3b025e88684d60368d2f104c76a7`)
   - *Checks:* `Build.VERSION.SDK_INT >= 31` check, `RenderEffect.createBlurEffect`, `RecyclerView` scrolling hooks, and `Reset` dynamic proxy runnable.
   - *Audit Verdict:* 5/5 verified. Boundary condition on `rx, ry < 0.5` confirmed.
5. **`plugins-store-save-emoji` (51 lines):**
   - *Target:* Save Emoji v1.1.0 (Commit: `97c33f63831619c95748edf7a52ec91b88da3151`)
   - *Checks:* `InMemoryDexClassLoader` with `ByteBuffer.wrap()`, `ApplicationLoader.applicationContext.getClassLoader()`, and `start()`/`stop()` lifecycle.
   - *Audit Verdict:* 5/5 verified. Bytecode payload isolated without claim of decompiled behavior.

---

### Group B: Medium Plugins (500–2,000 lines)
6. **`plugins-store-profile-plugin` (`Profile_Plugin.plugin`, 617 lines):**
   - *Target:* Profile Generator v1.0 (Commit: `114f5a230b0cf82aa9986a5a89b06b2495c37240`)
   - *Checks:* Pillow `Image.new`/`ImageDraw.Draw`/`ImageFont.truetype` rendering, `.profile` send hook cancellation, `FontManager` download thread, and photo size generation.
   - *Audit Verdict:* 5/5 verified. Evidence span widened to include `img.save` at line 517; font downloading corrected to temp directory.
7. **`plugins-store-air-raid-alert` (`air_raid_alert.eaf`, 779 lines inside ZIP):**
   - *Target:* Air Raid Alert v1.2.1 (Commit: `e30c41d0c01b8a3e417f933a6e5426e749092d46`)
   - *Checks:* Elyx package structure (`refmap.yml`, `metainfo.yml`, `src/`), daemon `AlertMonitor` thread (15s poll), `NotificationManager` alarms, and conditional start on `settings.enabled`.
   - *Audit Verdict:* 5/5 verified. Evidence paths upgraded from bare archive `:1` to member-qualified paths (`!/src/monitor.py:...`).
8. **`plugins-store-plugstonav` (315 lines + embedded DEX):**
   - *Target:* Plugins Tab v1.3.1 (Commit: `5a4efa002a7a85a232063849dc11f4c6ce7a730f`)
   - *Checks:* `Build.VERSION.SDK_INT >= 26` guard, zlib-compressed embedded DEX between markers, `_invoke` reflection, and `loaded=False` in finally.
   - *Audit Verdict:* 5/5 verified. API level 26 prerequisite confirmed.
9. **`plugins-store-music-speed` (663 lines):**
   - *Target:* Music Speed v1.0.1 (Commit: `4f29ece39d5110e8f14292ae5a6c22c43827d82c`)
   - *Checks:* Media3/ExoPlayer2 fallback, `sendRendererMessage(1, 6, AuxEffectInfo)`, `FragmentContextView` button restoration, and `PresetReverb.release()`.
   - *Audit Verdict:* 5/5 verified. Track 1, message 6 IPC contract confirmed.
10. **`plugins-store-spen-support` (461 lines):**
    - *Target:* Samsung S-Pen Support v1.6.0 (Commit: `69d07965b06dcd015dce9a14755f9a5e768cc4ba`)
    - *Checks:* `TOOL_TYPE_STYLUS = 2`, Samsung vendor actions 211–214 mapping, `Activity.dispatchTouchEvent` hooks, and `recycle()` in finally.
    - *Audit Verdict:* 5/5 verified. Confirmed `drawSelectionBackground` finally rollback.

---

### Group C: Large Plugins (> 2,000 lines)
11. **`plugins-store-link-guard` (3,237 lines):**
    - *Target:* Link Guard v1.7.0 (Commit: `f553639c2305591ce215564bfc544982daa125dc`)
    - *Checks:* `Browser.openUrl` cancellation and `_reopen`, IDNA/Punycode/Damerau-Levenshtein lookalike detection, query-only tracker stripping (`clean_url`), and binary LGDB search.
    - *Audit Verdict:* 5/5 verified. Confirmed `clean_url` only strips query parameters; distinguished bundled LGDB `WHIT` from user whitelist.
12. **`plugins-store-plugin-guard` (7,106 lines):**
    - *Target:* Plugin Guard v1.4.5 (Commit: `6daceedcf7072b6ffdc8fda0ff1becb92a22f6e5`)
    - *Checks:* Pre-install SHA-256 and AST scanning, `InstallPluginBottomSheet` constructor hooking, sandboxed `ASTEval` interpreter without native `eval()`, auto-block logic, and best-effort cleanup.
    - *Audit Verdict:* 5/5 verified. Text normalization vs raw-bytes fallback documented; "deterministic" cleanup moderated to best-effort.
13. **`plugins-store-quantahut` (4,847 lines):**
    - *Target:* QuantaHut v1.5.4 (Commit: `d0efb7b72bcac954d97af04670d6492900ade596`)
    - *Checks:* `ChatActivityEnterView` constructor hook for `!` commands, `PluginCell.set` BETA badge and pills, direct `SendMessagesHelper.sendMessage` dispatch, and SQLite `LocalizationDatabase`.
    - *Audit Verdict:* 5/5 verified. Confirmed chat list and unread counters are not touched.
14. **`plugins-store-sorter-plus` (5,978 lines):**
    - *Target:* Sorter+ v1.4.3 (Commit: `39d0a8797ddca6fd23159567311e7a0e03c342b6`)
    - *Checks:* `PluginsActivity.fillItems(ArrayList, UniversalAdapter)` hook (not `UniversalAdapter.fillItems`), `UItem.asFullyCustom` pills container, folder filtering, and settings backup.
    - *Audit Verdict:* 5/5 verified. Narrowed existing `fact-026` claim to reflect that `UniversalAdapter` is solely the parameter type.
15. **`plugins-store-culprit-detector` (25,120 lines):**
    - *Target:* Culprit Detector v1.7.0 (Commit: `c38b0cdc42f868dd89ae96747e4bb4ebf2a30646`)
    - *Checks:* Passive logging to dedicated JSON files without altering engine prefs, embedded arm64 `libculprit.so` (ABI 15), `Thread.setDefaultUncaughtExceptionHandler` dynamic proxy chaining, and pre-OOM watchdog.
    - *Audit Verdict:* 5/5 verified. `_SO_ARM64` verified as valid little-endian ELF64 binary.

---

## 3. Boundary & Invariant Audit

1. **Static vs. Runtime Boundary:**
   - 0 out of 75 facts claim runtime verification.
   - All facts carry `evidence_status: "code"`.
   - The global index maintains `runtime_verified: 0`.
2. **Donor vs. Target Client Evidence:**
   - Call sites inside third-party plugins are explicitly recorded as donor/third-party observations.
   - No fact promotes third-party plugin usage to an official Telegram/ExteraGram API guarantee.
3. **Reproducibility of Evidence:**
   - Every cited commit exists as an immutable object in git history.
   - All 75 `evidence_url` links resolve with HTTP 200.
