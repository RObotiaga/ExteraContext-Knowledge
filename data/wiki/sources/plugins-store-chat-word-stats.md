---
type: source
source_id: plugins-store-chat-word-stats
title: "Source: Chat Word Stats plugin"
source_type: plugin
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: f8f35b18b6148b20027b3bdeff505d240086444a
path: "Plugins/просьба.plugin"
artifact_sha256: 339c4b0f072967a3bd35e34f6f085403a2bdd4c1dcad4e6bf35f59919f6947ed
plugin_id: "chat_word_stats"
plugin_version: "1.0"
author: null
min_version: "11.9.0"
app_version: null
sdk_version: null
platform: Android
evidence_status: code
review_status: accepted
collector_model: "deepseek-v4.1-flash-expires-on-0910"
reviewer_model: "deepseek-v4.1-flash-expires-on-0910"
review_mode: independent-source-reread-nonblind
review: ../reviews/plugins-store-chat-word-stats.md
date: "2026-10-03"
---

# Source: Chat Word Stats plugin

- Repository: `Kangel-Plugins/Plugins-Store`
- File: `Plugins/просьба.plugin`
- Plugin id: `chat_word_stats` (declared in source, line 34)
- Name / version: `ChatWordStats` / `1.0` (lines 35–36; same version under the `chat_word_stats` key in `store.json`)
- Pinned commit: `f8f35b18b6148b20027b3bdeff505d240086444a` (`Add plugins 11.12.25`, 2025-12-10)
- Pinned URL: https://github.com/Kangel-Plugins/Plugins-Store/blob/f8f35b18b6148b20027b3bdeff505d240086444a/Plugins/%D0%BF%D1%80%D0%BE%D1%81%D1%8C%D0%B1%D0%B0.plugin
- File length: 265 lines. SHA256 `339c4b0f072967a3bd35e34f6f085403a2bdd4c1dcad4e6bf35f59919f6947ed`, which equals `store.json.hash` for `chat_word_stats`.
- Blob identity: `git rev-parse f8f35b18b6148b20027b3bdeff505d240086444a:Plugins/просьба.plugin` == `git hash-object Plugins/просьба.plugin` == `8437043fa31704ba892239ac3031da4552ef197d`.
- External check on 2026-10-05: the raw file at the pinned commit returned HTTP 200 and matches the local blob.

## Relevant source spans

1. Batch history collection, `req.limit = 500`, `offset_id` pagination, word regex and `Counter`: lines 145, 151–158, 160–170, 177–186, 188–198 (setting read for the minimum word length: 140, default at 100).
2. mandre_lib integration (`Mandre.use_persistent_storage`, `Mandre.register_command("chatstat", ...)`) and the send-message hook registration/handler: lines 73–75, 81–86.
3. `.chatstat` handler: `client_utils.run_on_queue` background dispatch plus `run_on_ui_thread` + `BulletinHelper` messages: lines 113–134, with error toasts at 174, 217, 265.
4. Report formatting and sending: Markdown text (242–248), `parse_markdown` (251), `entity.to_tlrpc_object()` (253), `send_message` (255–260).
5. Negative evidence — `on_plugin_unload` contains only a log line, and no deregistration of the `chatstat` command or of the send-message hook exists anywhere in the file: lines 78–79 (the never-removed registrations are at 73–75).

The claims below are source-code observations only for this pinned revision. `check_compatibility` returns `unknown` for `Mandre.register_command`, `BasePlugin.add_on_send_message_hook` and `TLRPC.TL_messages_getHistory` on exteraGram 11.9.0 / Android, so no runtime or version-compatibility guarantee is implied.
