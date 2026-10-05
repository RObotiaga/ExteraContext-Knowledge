---
source_id: plugins-store-similar-nft
repository: https://github.com/Kangel-Plugins/Plugins-Store
commit: d49a795beae95c1c8a149c4ee94589d892404e9c
path: Plugins/similar_nft.plugin
version: 1.5.0
plugin_id: similar_nft
author: Daxo-Developer && @Daxo_OS
min_app_version: 12.5.1
evidence_status: code
---

# Similar NFT plugin source

Pinned source snapshot for plugin `similar_nft`, version 1.5.0. The metadata above is the supplied target context; claims below are independently checked against the pinned plugin source.

## Verified implementation facts

- In `on_plugin_load`, the plugin attempts to resolve `show()` on `org.telegram.ui.ActionBar.BottomSheet`, `android.app.Dialog`, and the classes listed in `_SHEET_CLASSES` (which contains `org.telegram.ui.Stars.StarGiftSheet`), then hooks the discovered method with `_ShowHook`. [Source](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L69-L69) [Implementation](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L2807-L2827)
- Duplicate hook registration is prevented within that loop by computing `declaringClass.show` from the reflected method and skipping identifiers already present in the local `hooked_methods` set. [Implementation](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L2808-L2824)
- Only if the initial `show()` loop registered zero hooks (`n == 0`), the plugin tries `hook_all_methods(c, "show", ...)` on BottomSheet and Dialog, stopping after the first successful attempt. [Implementation](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L2828-L2839)
- `_sync_menu` creates a `MenuItemData` for `MESSAGE_CONTEXT_MENU`, calls `add_menu_item`, and when disabling a previously enabled item calls `remove_menu_item` using the remembered reference or `MENU_ID`. [Implementation](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L2979-L3009)
- `on_plugin_unload` first attempts to disable/synchronize the menu and then clears `_CACHE` and `self._captured`; these are inside exception-guarded cleanup blocks. [Implementation](https://github.com/Kangel-Plugins/Plugins-Store/blob/d49a795beae95c1c8a149c4ee94589d892404e9c/Plugins/similar_nft.plugin#L2851-L2860)

## Scope note

These are source-code observations for the pinned snapshot, not runtime verification that reflection or hooks succeed on any particular app build.

## Evidence path convention

`Plugins/similar_nft.plugin:<start>-<end>`

- Hook target list: `Plugins/similar_nft.plugin:69-69`, `2807-2827`
- Hook deduplication: `Plugins/similar_nft.plugin:2808-2824`
- Zero-hook fallback: `Plugins/similar_nft.plugin:2828-2839`
- Menu add/remove: `Plugins/similar_nft.plugin:2979-3009`
- Unload cleanup: `Plugins/similar_nft.plugin:2851-2860`

## Metadata

- Commit: `d49a795beae95c1c8a149c4ee94589d892404e9c`
- Version: `1.5.0`
- ID: `similar_nft`
- Author: `Daxo-Developer && @Daxo_OS`
- Minimum app version: `12.5.1`

Metadata assertions reproduce the task-provided context; implementation assertions are backed by the pinned code evidence above.
