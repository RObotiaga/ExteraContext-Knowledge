---
type: source
source_id: plugins-store-media-files
platform: Android
review_status: accepted-with-gaps
review: ../reviews/plugins-store-media-files.md
date: 2026-10-01
---

# Kangel-Plugins/Plugins-Store — Партиция медиа, звука и файлов (31 плагин)

Источник: репозиторий [Kangel-Plugins/Plugins-Store](https://github.com/Kangel-Plugins/Plugins-Store), ветка `main`, коммит `00de67026419f9dbe3a2787bb1236e8aaead8f76`. Данная партиция охватывает 31 плагин каталога Plugins-Store, реализующих механизмы работы с медиафайлами, аудиопотоками, видеосообщениями (кружочками), воспроизведением и записью звука, WebRTC VoIP-вызовами, файловым кэшем `FileLoader`, загрузчиком `FileLoadOperation` и компонентами интерфейса отображения медиа (`AudioPlayerAlert`, `PhotoViewer`, `ChatMessageCell`).

## Роль и границы источника

Партиция представляет собой крупнейший срез практической реализации медиа-механизмов в плагинах для Android-клиентов Telegram (ExteraGram, AyuGram). Плагины извлекают и модифицируют закрытые внутренние API клиента и системные службы Android:
- Модификация и перехват низкоуровневых медиа-пайплайнов (`android.media.MediaRecorder`, `android.media.MediaFormat`, `android.media.CamcorderProfile`, `android.media.AudioManager`, `android.media.AudioTrack`).
- Перехват и прямое инжектирование PCM-байтов в поток записи голосовых сообщений (`MediaController.writeFrame`) и в нативный WebRTC движок звонков (`WebRtcAudioRecord.nativeDataIsRecorded`).
- Полный цикл разрешения путей к файлам сообщений через `FileLoader` (`getPathToMessage`, `getPathToAttach`, `getDocumentFilePath`, `getDocumentExtension`).
- Предотвращение сброса фоновых загрузок при уходе из чата (`FileLoader.changePriority`, `FileLoadOperation.cancel`).
- Каскадное извлечение и декодирование обложек треков из `doc.thumbs` (`TL_photoStrippedSize`, `TL_photoCachedSize`), локального кэша и тегов ID3/Vorbis.
- Программная генерация нативных голосовых сообщений `TLRPC.TL_document` с 5-битной вейвформой (0..31) без задействования микрофона.
- Анализ заголовков и бинарных MP4-боксов `ftyp` для детекции клиентской платформы отправителя кружочков.

Границы доказательств: весь материал получен методом статического анализа исходного кода (`code`), запуск на реальных устройствах в рамках текущего этапа не проводился, поэтому статус верификации зафиксирован как `accepted-with-gaps`.

## Покрытие

| Файл плагина | Размер (байт) / Строк | Что извлечено | Границы и зависимости |
|---|---|---|---|
| `Fork_Round_Videos_Configurator.plugin` | 14 942 / 416 | Хуки `MediaFormat.setInteger/setFloat`, `MediaRecorder`, `CamcorderProfile`, `Camera$Parameters`, suppression оверлея `InstantCameraVideoEncoderOverlayHelper` | Зависит от Camera2 / MediaCodec в клиенте |
| `Round_Videos_Fork.plugin` | 8 017 / 180 | Перехват `AudioManager.requestAudioFocus` (фоновая музыка), выбор кодека H.264/HEVC, аудиоканалов и источника микрофона | Не тестировались аппаратные энкодеры всех SoC |
| `round_client_detector.plugin` | 29 192 / 705 | Детекция платформы по имени файла и бинарным боксам `ftyp` (CoreMedia, Stagefright, FFmpeg), бейдж в `ChatMessageCell` | Эвристический анализ первых 4096 байт файла |
| `save_voice_msg.plugin` | 4 197 / 80 | Контекстное меню `isVoice()`, разрешение пути через `FileLoader.getPathToAttach`, экспорт `.ogg` в `Downloads` | Требует права записи в ExternalStorage |
| `slashvoice.plugin` | 24 744 / 602 | Синхронизация Business Quick Replies (`TL_messages_getQuickReplies`), сериализация `TLRPC.Document` через `SerializedData` в Base64, отправка ГС | Требует аккаунт с Telegram Business для `.qsync` |
| `voice_soundpad.plugin` | 93 514 / 2 417 | Микширование звука в `MediaController.writeFrame`, хуки VoIP `WebRtcAudioRecord`, генерация вейвформы, `AudioTrack` | Глубокий рефлексивный доступ к нативным буферам |
| `voice_changer.plugin` | 4 595 / 123 | Питч-шифтинг через подмену семплирования в `MediaController.startRecord(String, int)` (16000/8000 Гц) | Работает за счет фиксированного воспроизведения 48 кГц |
| `second_voice.plugin` | 19 349 / 555 | Расширенный таймер в `ChatMessageCell.updatePlayingMessageProgress()` и `setMessageObject()`, замер ширины текста | Связан с версткой конкретной версии `ChatMessageCell` |
| `voice_timing.plugin` | 17 413 / 456 | Вставка тайминга цитаты через `MediaController.getPlayingMessageObject()`, хуки `ChatActivityEnterView` | Зависит от структуры полей `ChatActivityEnterView` |
| `voice_transcription.plugin` | 2 471 / 62 | Оборачивание расшифровки ГС в сворачиваемую цитату `TL_messageEntityBlockquote(collapsed=True)` | Хукает `MessageObject.getVoiceTranscription()` |
| `audio_quality_chip.plugin` | 10 718 / 293 | Бейдж формата/битрейта в `AudioPlayerAlert`, чтение `MediaMetadataRetriever.METADATA_KEY_BITRATE`, формула VBR | Зависит от разметки `AudioPlayerAlert` |
| `femboyaudioscope.plugin` | 28 188 / 779 | Трёхуровневое разрешение путей к файлам, извлечение аудиотегов через `MediaMetadataRetriever` и `mutagen` | Требует установленную библиотеку `mutagen` |
| `audio_router.plugin` | 18 768 / 449 | Маршрутизация звука, сканирование `am.getDevices(3)`, переключение `setMode(3)`, выборочный mute аудиопотоков | Системный API `android.media.AudioManager` |
| `audio_size_timer.plugin` | 23 418 / 554 | Инъекция размера трека в `ChatMessageCell`, `SharedAudioCell`, `AudioPlayerCell` через `StaticLayout` | Изменяет приватные поля отображения разметки |
| `auto_video_max_quality.plugin` | 8 455 / 258 | Автоматический выбор максимального разрешения видео в `PhotoViewer.updateQualityItems()`, фиксация качества | Зависит от интерфейса `VideoPlayer` |
| `gifs_unlocker.plugin` | 27 510 / 713 | Разблокировка вкладки GIF `EmojiPagesAdapter.canScrollToTab(1)`, отправка как MP4 видео без звука | Обход серверных запретов через локальную конвертацию |
| `gradient_mini_player.plugin` | 34 892 / 1 004 | Каскадное извлечение обложек (`thumbs`, `FileLoader`, `getAudioInfo`), генерация градиентного фона | Активная анимация в интерфейсе |
| `mediaglow.plugin` | 42 358 / 1 112 | Эмбиент-подсветка краев видео/фото в `PhotoViewer`, нативное размытие через `Utilities.stackBlurBitmap` | Хукает отрисовку `Canvas` |
| `shareui_dkta.plugin` | 1 246 / 34 | Предотвращение остановки загрузок: блокировка `FileLoader.changePriority(PRIORITY_LOW)` и `cancel()` | Блокирует стандартную оптимизацию трафика |
| `avatar_cleanup.plugin` | 34 981 / 908 | Пакетное удаление аватарок `TL_photos_deletePhotos`, предпросмотр через `BackupImageView` и `ImageLocation` | Использует прямое взаимодействие с MTProto |
| `imitator.plugin` | 70 758 / 1 660 | Имитация статусов записи аудио/видео (`TL_messages_setTyping` с `TL_sendMessageRecord*Action`) | Требует периодической отправки запросов |
| `metadata.plugin` | 26 268 / 533 | Извлечение EXIF-данных фотографий (`ExifInterface`) и медиа-атрибутов документов | Чтение метаданных с диска |
| `real_metadata.plugin` | 28 491 / 844 | Исчерпывающий поиск локальных файлов в `FileLoader`, вызов `MediaExtractor` и `ExifInterface` | Полная разборка структур вложений |
| `cactusLibMini.plugin` | 6 345 / 146 | Экспорт и отправка файлов плагинов через `client_utils.send_document`, `getExternalCacheDir` | Вспомогательная утилита передачи файлов |
| `plugin_update_checker.plugin` | 54 904 / 1 393 | Асинхронное скачивание файлов каналов через `FileLoader.loadFile(PRIORITY_HIGH)`, чтение метаданных | Фоновый опрос завершения загрузки |
| `sql_viewer.plugin` | 16 002 / 523 | Разрешение файлов `.db` из ответов на сообщения через `MessageObject.getDocument` | Чтение локальных баз SQLite |
| `Python Interpreter - 0.1.3.plugin` | 37 504 / 828 | Извлечение имени документа через `FileLoader.getDocumentFileName`, путь к аттачу | Интерактивная среда исполнения |
| `gift_stats.plugin` | 91 863 / 2 250 | Извлечение растровых изображений `ImageReceiver.getBitmap()`, отключение привязки к View | Отрисовка статистики подарков |
| `explore_search.plugin` | 276 690 / 6 867 | Поиск и выбор размеров фото через `FileLoader.getClosestPhotoSizeWithSize` | Комплексный плагин поиска |
| `hook_inspector.plugin` | 165 205 / 3 668 | Диагностический инспектор хуков `ChatMessageCell` и `MediaController` | Справочный реестр точек перехвата |
| `VoiceRelay.plugin` | 15 925 / 440 | Проксирование WebRTC голосовых звонков через UDP релей, перехват `Instance` и `NativeInstance` | Требует внешний релей-сервер |

---

## Технические факты

### 1. Видеосообщения (кружочки): кодеки, битрейты, FPS и фоновая музыка

- **Перехват параметров кодировщика через MediaFormat:** В плагине `Fork_Round_Videos_Configurator.plugin` ([строки 112–149](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Fork_Round_Videos_Configurator.plugin#L112-L149)) перехватываются методы `android.media.MediaFormat.setInteger` и `setFloat`. Видео-битрейт отделяется от аудио-битрейта по пороговому значению: если текущий битрейт `>= 200 000` bps, аргумент заменяется на выбранный битрейт видео (`bitrate_video * 1000`, диапазон 600..3000 кбит/с). Если `0 < cur < 200 000` bps, устанавливается битрейт звука (`bitrate_audio * 1000`, диапазон 64..512 кбит/с). Частота кадров перехватывается по ключу `"frame-rate"` (30, 40, 60 FPS), а разрешение — по ключам `"width"` и `"height"` в диапазоне 64..1024 px.
- **Прямое конфигурирование MediaRecorder и CamcorderProfile:** В `Fork_Round_Videos_Configurator.plugin` ([строки 151–190](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Fork_Round_Videos_Configurator.plugin#L151-L190)) перехватываются вызовы `MediaRecorder`: `setVideoEncodingBitRate`, `setVideoSize(res, res)`, `setVideoFrameRate(fps)`, `setAudioEncodingBitRate` и `setAudioSamplingRate(48000)`. Также перехватывается фабрика `CamcorderProfile.get()`, где полям возвращаемого профиля принудительно назначаются переопределенные значения FPS, видео/аудио битрейтов и размеров кадра.
- **Подавление оверлея InstantCameraView:** При смене разрешения и FPS стандартный оверлей кодировщика может накладывать искажённые кадры. Для предотвращения этого плагин хукает класс `org.telegram.ui.Components.InstantCameraVideoEncoderOverlayHelper` ([строки 288–293](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Fork_Round_Videos_Configurator.plugin#L288-L293)), вызывая `param.setResult(None)` на методах `bind` и `render`.
- **Запись кружков с фоновой музыкой (AudioFocus suppression):** В `Round_Videos_Fork.plugin` ([строки 97–100, 171–178](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Round_Videos_Fork.plugin#L97-L100)) метод `android.media.AudioManager.requestAudioFocus(...)` перехватывается хуком `replace_hooked_method`, возвращающим `AUDIOFOCUS_REQUEST_GRANTED` (`1`). Это предотвращает отправку паузы сторонним музыкальным плеерам при запуске видеозаписи.
- **Выбор видеокодека и источника аудио:** `Round_Videos_Fork.plugin` ([строки 78–93](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/Round_Videos_Fork.plugin#L78-L93)) позволяет переключать видеокодек в `MediaRecorder.setVideoEncoder`: значение `2` соответствует `VideoEncoder.H264`, а значение `5` — `VideoEncoder.HEVC` (H.265). В `MediaRecorder.setAudioSource` поддерживаются режимы `1` (`AudioSource.MIC`), `6` (`VOICE_RECOGNITION`) и `9` (`UNPROCESSED` для чистого звука без шумоподавления Android).

### 2. Детекция платформы клиента по метаданным и MP4-контейнеру

В плагине `round_client_detector.plugin` ([строки 91–165](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/round_client_detector.plugin#L91-L165)) реализована система идентификации операционной системы отправителя видеосообщения:
1. **Эвристика по имени файла в атрибутах:**
   - `"video.mp4"` — отправлено с iOS (iPhone/iPad).
   - Шаблон `"round_YYYY-MM-DD_HH-MM-SS.mp4"` или префикс `"round"`/подстрока `"desktop"` — Telegram Desktop.
   - Имя файла отсутствует (`None` или пусто) — стандартный клиент Android.
2. **Анализ первых 4096 байт бинарного потока MP4:**
   - Проверяется маркер контейнера: смещение `[4:8] == b"ftyp"`.
   - Наличие меток `b"Core Media"`, `b"Apple"`, `b"com.apple"` или брендов `qt  `, `CAEP` идентифицирует энкодер Apple QuickTime (iOS).
   - Подстроки `b"libstagefright"`, `b"c2.android"`, `b"OMX.google"` или `b"Android"` подтверждают системный энкодер Android MediaCodec / Stagefright.
   - Подстроки `b"Lavf"` или `b"Lavc"` указывают на сборку библиотеки FFmpeg, характерную для Telegram Desktop.

### 3. Голосовые сообщения: перехват PCM, аудиоэффекты и создание Waveform

- **Прямой перехват микрофонного потока в реальном времени:** В `voice_soundpad.plugin` ([строки 666–726, 790–799](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L666-L726)) обнаружен перехват метода `org.telegram.messenger.MediaController.writeFrame(ByteBuffer byteBuffer, int length)`. Плагин извлекает массив байтов из переданного `java.nio.ByteBuffer`, применяет программное микширование PCM-сэмплов и записывает модифицированный звук обратно в буфер перед передачей на кодирование в Opus.
- **Жизненный цикл аудиозаписи:** Метод `MediaController.startRecord(String path, int sampleRate)` инициализирует захват с частотой дискретизации (обычно 48000 Гц). Остановка отслеживается через `MediaController.stopRecord()`, `MediaController.stopRecording(int, boolean, int, boolean, long)` и `MediaController.cleanRecording(boolean)` ([строки 804–849](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L804-L849)).
- **Питч-шифтинг без внешних DSP (Voice Changer):** В `voice_changer.plugin` ([строки 64–70, 113–122](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_changer.plugin#L64-L70)) реализован прием изменения тональности голоса: при перехвате `MediaController.startRecord` параметр `sampleRate` подменяется на заниженный (например, 16000 Гц для «мужского» баса или 8000 Гц). Так как плеер Telegram декодирует и воспроизводит файл с жестко заданной частотой 48000 Гц, занижение частоты записи приводит к пропорциональному снижению тональности и замедлению звука.
- **Алгоритм генерации вейвформы голосового сообщения:** В `voice_soundpad.plugin` ([строки 2041–2065](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L2041-L2065)) реализована калькуляция формы волны для Telegram: массив 16-битных PCM сэмплов делится на 50 блоков, в каждом находится максимальный пик, который масштабируется в 5-битное целое число формулой `val = min(31, int(peak / 1057))`. Результирующий `bytearray` из 50 байт упаковывается в `TLRPC.TL_bytes` и передается в `TLRPC.TL_documentAttributeAudio.waveform`.
- **Программная сборка голосового сообщения:** В `voice_soundpad.plugin` ([строки 2000–2035](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L2000-L2035)) продемонстрировано создание нативного голосового сообщения: формируется `TLRPC.TL_document`, устанавливается `mime_type = "audio/ogg"`, добавляется `TL_documentAttributeAudio(voice=True, duration=..., waveform=...)`, имя файла `TL_documentAttributeFilename` и отправляется через `send_message({"peer": peer_id, "document": document, "path": path})`.

### 4. Инъекция звука в WebRTC VoIP-звонки

В `voice_soundpad.plugin` ([строки 876–923, 976–980, 1070–1088](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L876-L923)) реализован перехват низкоуровневых WebRTC классов:
- `org.webrtc.voiceengine.WebRtcAudioRecord.nativeDataIsRecorded(int length, long nativeAudioRecord)`
- `org.webrtc.audio.WebRtcAudioRecord.nativeDataIsRecorded(int length, long nativeAudioRecord)`
- `org.webrtc.audio.JavaAudioDeviceModule$WebRtcAudioRecord.nativeDataIsRecorded(int length, long nativeAudioRecord)`

Через рефлексию извлекается приватное поле `byteBuffer`. Если активен встроенный плеер саундпада, байты микрофона считываются, микшируются с воспроизводимым сэмплом и перезаписываются в `byteBuffer` непосредственно перед тем, как нативный C++ движок WebRTC передаст пакет в RTP-поток.

Отслеживание состояния звонков выполняется на `org.telegram.messenger.voip.VoIPService.dispatchStateChanged(int state)` ([строки 947–974](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/voice_soundpad.plugin#L947-L974)):
- `STATE_ESTABLISHED` (константа 3) — соединение установлено, активация оверлея и микшера.
- `STATE_ENDED` (11), `STATE_FAILED` (4), `STATE_BUSY` (17), `STATE_HANGING_UP` (10) — сброс буферов и остановка воспроизведения.

### 5. Сериализация TL-документов и интеграция с Telegram Business

- **Сериализация TLRPC.Document в Base64:** В `slashvoice.plugin` ([строки 75–102](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/slashvoice.plugin#L75-L102)) представлен способ сохранения TL-объектов медиа в настройках плагина без потери атрибутов. Объект сериализуется через системный поток: `data = SerializedData(doc.getObjectSize())`, затем `doc.serializeToStream(data)` и `base64.b64encode(data.toByteArray())`. Десериализация выполняется через `TLRPC.Document.TLdeserialize(data, data.readInt32(False), False)`.
- **Загрузка быстрых ответов Business:** `slashvoice.plugin` ([строки 263–337](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/slashvoice.plugin#L263-L337)) запрашивает быстрые ответы аккаунта через `TLRPC.TL_messages_getQuickReplies()`, перебирает `response.messages`, извлекает медиавложения типа `TLRPC.TL_messageMediaDocument` и индексирует их по шорткатам (`quick_reply_shortcut_id`).

### 6. Управление загрузками и файловым кэшем FileLoader

- **Предотвращение сброса фоновой загрузки файлов:** Плагин `shareui_dkta.plugin` ([строки 14–34](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/shareui_dkta.plugin#L14-L34)) блокирует логику клиента, снижающую приоритет или отменяющую скачивание файлов при выходе из чата:
  - Хук `org.telegram.messenger.FileLoader.changePriority(int priority, ...)`: при попытке выставить `PRIORITY_LOW` (0) вызывается `param.setResult(None)`, сохраняя высокий приоритет операции.
  - Хук `org.telegram.messenger.FileLoadOperation.cancel(...)`: если флаг `loadingCancelled` родительского объекта не установлен пользователем, вызов подавляется (`param.setResult(None)`).
- **Трёхуровневое разрешение путей к файлам на диске:** В `femboyaudioscope.plugin` ([строки 605–636](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/femboyaudioscope.plugin#L605-L636)) и `real_metadata.plugin` ([строки 343–373](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/real_metadata.plugin#L343-L373)) зафиксирован универсальный паттерн поиска пути к скачанному медиа:
  1. `message.messageOwner.attachPath` (локальный путь исходящего файла перед отправкой).
  2. `FileLoader.getInstance(account).getPathToMessage(message.messageOwner, [use_q])`.
  3. `FileLoader.getInstance(account).getPathToAttach(message.getDocument(), [force_cache], [use_q])`.
  4. Метод сообщения `message.getDocumentFilePath()`.
- **Асинхронная загрузка файлов плагинов и миниатюр:** В `plugin_update_checker.plugin` ([строки 779–807](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/plugin_update_checker.plugin#L779-L807)) вызов `FileLoader.getInstance(account).loadFile(doc, entry["message"], FileLoader.PRIORITY_HIGH, 0)` инициирует немедленное скачивание документа с высоким приоритетом.

### 7. Аудиоплеер (AudioPlayerAlert) и каскадное извлечение обложек

- **Извлечение формата и битрейта:** В `audio_quality_chip.plugin` ([строки 171–218](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/audio_quality_chip.plugin#L171-L218)) формат трека извлекается через `FileLoader.getDocumentExtension(document)`. Для полностью скачанных файлов битрейт считывается через `MediaMetadataRetriever.extractMetadata(METADATA_KEY_BITRATE)`. Если файл ещё не скачан, применяется расчетная формула среднего битрейта для VBR:
  `bitrate_kbps = int((document.size * 8 / message.getDuration() + 500) // 1000)`
- **Каскадный алгоритм поиска обложки трека:** В `gradient_mini_player.plugin` ([строки 848–925](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/gradient_mini_player.plugin#L848-L925)) извлечение обложки для мини-плеера выполняется по приоритетной цепочке:
  1. Перебор `doc.thumbs`: игнорируются `Empty`, проверяются `Stripped` (`ImageLoader.getStrippedPhotoBitmap`) и `Cached` (`BitmapFactory.decodeByteArray`).
  2. Обычные миниатюры сортируются по близости к размеру 160 px: `cands.sort(key=lambda s: abs(max(int(s.w), int(s.h)) - 160))`. Проверяется локальный кэш `FileLoader.getInstance(account).getPathToAttach(s, True)`. Если файла нет, отправляется запрос `FileLoader.getInstance(account).loadFile(ImageLocation.getForDocument(size, doc), mo, None, 1, 1)`.
  3. Если в документе миниатюр нет, вызывается fallback на встроенную обложку метаданных трека: `MediaController.getInstance().getAudioInfo().getCover()`.
- **Даунсемплинг битмапов и извлечение палитры:** `gradient_mini_player.plugin` ([строки 930–950](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/gradient_mini_player.plugin#L930-L950)) декодирует файлы с `BitmapFactory.Options.inSampleSize = max(1, side // 96)`, масштабирует в `32x32` и извлекает пиксели в `jarray(jint)(1024)` для быстрого вычисления цветовой палитры.

### 8. Просмотрщик медиа (PhotoViewer): качество видео и нативное размытие

- **Принудительное максимальное качество видео:** В `auto_video_max_quality.plugin` ([строки 50–141, 220–238](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/auto_video_max_quality.plugin#L50-L141)) хукается `PhotoViewer.updateQualityItems()`. Из объекта `videoPlayer` опрашиваются доступные варианты качества через `video_player.getQuality(i)`, находится поток с максимальным количеством пикселей (`q.width * q.height` или `q.p()`), применяется `video_player.setSelectedQuality(target_index)` и фиксируется вызовом `VideoPlayer.saveQuality(quality_obj, message_object)`.
- **Нативное аппаратное размытие битмапов:** В `mediaglow.plugin` ([строки 275–285](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/mediaglow.plugin#L275-L285)) для создания фонового свечения вокруг видео и фото в полноэкранном режиме используется нативная функция клиента `org.telegram.messenger.Utilities.stackBlurBitmap(Bitmap bitmap, int radius)`. Это эффективнее рендеринга через RenderScript/Vulkan и не требует сторонних C++ библиотек.

### 9. Разблокировка и отправка GIF как зацикленного видео

В плагине `gifs_unlocker.plugin` ([строки 50–110, 542–599](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/gifs_unlocker.plugin#L50-L110)) решена проблема отправки GIF в чатах с запретом стикеров/GIF:
1. Метод `EmojiView$EmojiPagesAdapter.canScrollToTab(int position)` перехватывается: для вкладки GIF (позиция 1) возвращается `True`, если в чате разрешены видеосообщения (`ChatObject.canSendVideo(chat)`).
2. При отправке через `SendMessagesHelper.sendMessage` документ GIF перехватывается. При наличии в кэше ранее загруженного видео-эквивалента (`cache hit`), `params.document` подменяется на серверный `TL_document` видеозаписи (`isVideo=True`, `isGif=False`, `isAnimated=False`), что обеспечивает моментальную отправку по MTProto. При `cache miss` файл скачивается и отправляется через `client_utils.send_video(peer, path)`.

### 10. Аппаратная маршрутизация аудио через AudioManager

В `audio_router.plugin` ([строки 34–100](https://github.com/Kangel-Plugins/Plugins-Store/blob/main/Plugins/audio_router.plugin#L34-L100)) через `ApplicationLoader.applicationContext.getSystemService(Context.AUDIO_SERVICE)` реализован доступ к системным устройствам ввода-вывода звука:
- Вызов `am.getDevices(3)` (`GET_DEVICES_ALL`) сканирует устройства ввода (`isSource()`) и вывода (`isSink()`).
- Разрешенные типы входов: проводная гарнитура (3), Bluetooth SCO (7), встроенный микрофон (15), USB гарнитура (22).
- Разрешенные типы выходов: слуховой динамик (1), встроенный громкоговоритель (2), проводные наушники (4), Bluetooth A2DP (8), Bluetooth LE (26).
- Управление приоритетом звукового тракта: `am.setMode(3)` (`MODE_IN_COMMUNICATION`) для звонков и видеосообщений, либо `am.setMode(0)` (`MODE_NORMAL`).
- Выборочное глушение аудиопотоков: вызов `am.setStreamMute(stream_id, True)` для `STREAM_VOICE_CALL` (0), `STREAM_RING` (2), `STREAM_MUSIC` (3), `STREAM_NOTIFICATION` (5).

---

## Вызовы и наблюдаемые контракты

| Класс / Объект | Сигнатура вызова | Назначение и контекст | Доказательство в коде |
|---|---|---|---|
| `MediaFormat` | `setInteger(String name, int value)` | Переопределение битрейта, разрешения и FPS видеосообщений при записи | `Fork_Round_Videos_Configurator.plugin:112-139` |
| `MediaFormat` | `setFloat(String name, float value)` | Переопределение дробной частоты кадров видеозаписи | `Fork_Round_Videos_Configurator.plugin:140-149` |
| `MediaRecorder` | `setVideoEncodingBitRate(int bitRate)` | Установка кастомного битрейта видеопотока кружочка | `Fork_Round_Videos_Configurator.plugin:158-159` |
| `MediaRecorder` | `setVideoSize(int width, int height)` | Установка разрешения видеосообщения (128x128 .. 640x640) | `Fork_Round_Videos_Configurator.plugin:160-163` |
| `MediaRecorder` | `setVideoFrameRate(int rate)` | Установка FPS видеосообщения (30, 40, 60 кадров/сек) | `Fork_Round_Videos_Configurator.plugin:164-165` |
| `MediaRecorder` | `setAudioSamplingRate(int rate)` | Фиксация частоты дискретизации звука (48 000 Гц) | `Fork_Round_Videos_Configurator.plugin:168-169` |
| `MediaRecorder` | `setVideoEncoder(int encoder)` | Выбор кодека видеозаписи (2 = H.264, 5 = HEVC) | `Round_Videos_Fork.plugin:78-81` |
| `MediaRecorder` | `setAudioChannels(int numChannels)` | Выбор режима каналов аудио (1 = моно, 2 = стерео) | `Round_Videos_Fork.plugin:82-85` |
| `MediaRecorder` | `setAudioSource(int audioSource)` | Выбор источника звука (1 = MIC, 6 = REC, 9 = UNPROCESSED) | `Round_Videos_Fork.plugin:86-90` |
| `AudioManager` | `requestAudioFocus(listener, stream, hint)` | Подавление запроса аудиофокуса для сохранения фоновой музыки | `Round_Videos_Fork.plugin:97-100,176-178` |
| `MediaController` | `writeFrame(ByteBuffer buf, int len)` | Прямой перехват и микширование PCM-аудиопотока микрофона | `voice_soundpad.plugin:666-726,790-795` |
| `MediaController` | `startRecord(String path, int sampleRate)` | Старт аудиозаписи; точка изменения частоты (Voice Changer) | `voice_soundpad.plugin:804-817`; `voice_changer.plugin:64-70` |
| `MediaController` | `stopRecord()` / `cleanRecording(boolean)` | Завершение и очистка состояния аудиозаписи | `voice_soundpad.plugin:818-849` |
| `WebRtcAudioRecord` | `nativeDataIsRecorded(int len, long ptr)` | Перехват и подмешивание аудио в реальном времени при VoIP звонках | `voice_soundpad.plugin:876-923,1072-1088` |
| `VoIPService` | `dispatchStateChanged(int state)` | Мониторинг фаз соединения голосового вызова WebRTC | `voice_soundpad.plugin:947-974,1054-1066` |
| `FileLoader` | `getPathToAttach(Document doc)` | Получение локального файла вложения из дискового кэша | `save_voice_msg.plugin:49-56`; `femboyaudioscope.plugin:626-631` |
| `FileLoader` | `getPathToMessage(Message msg)` | Разрешение пути к медиа по владельцу сообщения | `audio_quality_chip.plugin:196-198`; `femboyaudioscope.plugin:614-620` |
| `FileLoader` | `loadFile(ImageLocation, Object, ...)` | Запуск принудительного скачивания миниатюры или документа | `gradient_mini_player.plugin:925`; `plugin_update_checker.plugin:801` |
| `FileLoader` | `changePriority(int priority, ...)` | Подавление перевода загрузок в фоновый низкий приоритет | `shareui_dkta.plugin:22-25,33` |
| `FileLoadOperation` | `cancel()` | Блокировка отмены активных загрузок при закрытии диалога | `shareui_dkta.plugin:26-31,34` |
| `FileLoader` | `getDocumentExtension(Document doc)` | Определение расширения файла медиа по документу Telegram | `audio_quality_chip.plugin:174` |
| `MediaMetadataRetriever` | `extractMetadata(int keyCode)` | Считывание битрейта (20), частоты (28), длительности (9), MIME (12) | `femboyaudioscope.plugin:643-655`; `audio_quality_chip.plugin:220-234` |
| `AudioTrack` | `write(byte[] audioData, int offset, int size)` | Прямой вывод PCM-сэмплов на системный динамик устройства | `voice_soundpad.plugin:543-610` |
| `ChatMessageCell` | `updatePlayingMessageProgress()` | Хук обновления отображения прогресса воспроизведения звука | `second_voice.plugin:508`; `audio_size_timer.plugin:79-84` |
| `VideoPlayer` | `saveQuality(Quality q, MessageObject mo)` | Фиксация выбранного пользователем качества видеопотока | `auto_video_max_quality.plugin:110-113` |
| `PhotoViewer` | `updateQualityItems()` | Хук точки переключения доступных разрешений потокового видео | `auto_video_max_quality.plugin:224-238` |
| `Utilities` | `stackBlurBitmap(Bitmap bmp, int radius)` | Нативное C-размытие битмапа по алгоритму StackBlur | `mediaglow.plugin:275-285` |
| `EmojiPagesAdapter` | `canScrollToTab(int position)` | Разблокировка вкладки GIF (позиция 1) в запрещенных чатах | `gifs_unlocker.plugin:50-73` |
| `SerializedData` | `serializeToStream(SerializedData data)` | Двоичная упаковка структуры TLRPC.Document в массив байт | `slashvoice.plugin:75-86` |
| `TL_messages_setTyping` | `send_request(req, callback)` | Имитация статусов записи кружка, голосового, заливки файла | `imitator.plugin:443-448,579-605` |

---

## Практические приёмы и рецепты

### Рецепт 1: Разрешение полного пути к медиафайлу сообщения
Для гарантированного нахождения пути к аудио/видеофайлу на устройстве без падений используйте трёхуровневую цепочку:
```python
def resolve_media_path(message_object):
    owner = getattr(message_object, "messageOwner", None)
    if owner and getattr(owner, "attachPath", None):
        if os.path.isfile(str(owner.attachPath)):
            return str(owner.attachPath)
    account = getattr(message_object, "currentAccount", 0)
    fl = FileLoader.getInstance(int(account))
    if owner:
        f = fl.getPathToMessage(owner)
        if f and f.exists() and f.length() > 0:
            return f.getAbsolutePath()
    doc = message_object.getDocument()
    if doc:
        f = fl.getPathToAttach(doc, True)
        if f and f.exists() and f.length() > 0:
            return f.getAbsolutePath()
    return None
```

### Рецепт 2: Запись видеосообщений под фоновую музыку
Чтобы воспроизведение музыки на телефоне не прерывалось при зажатии кнопки записи кружочка:
```python
class AudioFocusHook:
    def replace_hooked_method(self, param):
        return jint(1) # AUDIOFOCUS_REQUEST_GRANTED

def install_music_hook(plugin):
    am_cls = find_class("android.media.AudioManager")
    m = am_cls.getDeclaredMethod("requestAudioFocus", [
        find_class("android.media.AudioManager$OnAudioFocusChangeListener"),
        jint.TYPE, jint.TYPE
    ])
    plugin.hook_method(m, AudioFocusHook())
```

### Рецепт 3: Инъекция PCM-звука в микрофонный поток голосового сообщения
Для подмешивания фонового звука в запись голосового сообщения перехватывайте `MediaController.writeFrame`:
```python
class WriteFrameHook(MethodHook):
    def before_hooked_method(self, param):
        byte_buffer = param.args[0]
        length = param.args[1]
        orig_pos = byte_buffer.position()
        orig_lim = byte_buffer.limit()
        
        byte_buffer.position(0)
        byte_buffer.limit(length)
        raw = bytearray(length)
        byte_buffer.get(raw, 0, length)
        
        mixed = my_audio_engine.mix(bytes(raw))
        if mixed != bytes(raw):
            byte_buffer.position(0)
            byte_buffer.put(mixed, 0, len(mixed))
            
        byte_buffer.limit(orig_lim)
        byte_buffer.position(orig_pos)
```

### Рецепт 4: Программная генерация голосового сообщения с вейвформой
Отправка заранее подготовленного OGG Opus файла как полноценного голосового сообщения:
```python
def send_custom_voice(peer_id, ogg_path, duration_sec, pcm_samples):
    doc = TLRPC.TL_document()
    doc.id = 0
    doc.access_hash = 0
    doc.date = int(time.time())
    doc.mime_type = "audio/ogg"
    doc.size = os.path.getsize(ogg_path)
    
    audio_attr = TLRPC.TL_documentAttributeAudio()
    audio_attr.voice = True
    audio_attr.duration = int(duration_sec)
    
    # Генерация 50 баров вейвформы
    num_bars = 50
    chunk = max(1, len(pcm_samples) // num_bars)
    waveform = bytearray(num_bars)
    for i in range(num_bars):
        peak = max(abs(s) for s in pcm_samples[i*chunk:(i+1)*chunk])
        waveform[i] = min(31, int(peak / 1057))
        
    tl_bytes = TLRPC.TL_bytes()
    tl_bytes.bytes = waveform
    audio_attr.waveform = tl_bytes
    doc.attributes.add(audio_attr)
    
    send_message({"peer": peer_id, "document": doc, "path": ogg_path})
```

### Рецепт 5: Вычисление битрейта VBR-аудио до завершения загрузки
Для треков с переменным битрейтом или форматов без прямого чтения заголовка используйте формулу усредненного битрейта:
```python
def estimate_bitrate_kbps(document, duration_seconds):
    if not document or duration_seconds <= 0:
        return None
    size_bytes = int(getattr(document, "size", 0))
    if size_bytes <= 0:
        return None
    # Округление: (bytes * 8 / seconds + 500) // 1000
    return int((size_bytes * 8 / duration_seconds + 500) // 1000)
```

### Рецепт 6: Непрерывное скачивание файлов в фоне
Блокировка сброса скорости и отмены загрузки при навигации пользователя по клиенту:
```python
def prevent_download_interruption(plugin):
    fl_cls = find_class("org.telegram.messenger.FileLoader")
    flo_cls = find_class("org.telegram.messenger.FileLoadOperation")
    
    # 0 = FileLoader.PRIORITY_LOW
    plugin.hook_all_methods(fl_cls, "changePriority", 
        before=lambda p: p.setResult(None) if p.args[0] == 0 else None)
        
    plugin.hook_all_methods(flo_cls, "cancel", 
        before=lambda p: p.setResult(None) if not getattr(p.thisObject.parentObject, "loadingCancelled", False) else None)
```

### Рецепт 7: Быстрое размытие битмапа нативным C-методом Telegram
Создание эмбиент-подсветки без внешних библиотек:
```python
from org.telegram.messenger import Utilities
from android.graphics import Bitmap

def blur_media_frame(src_bitmap, radius=30):
    # Уменьшаем для ускорения обработки и снижения нагрузки на память
    small = Bitmap.createScaledBitmap(src_bitmap, 240, 240, True)
    Utilities.stackBlurBitmap(small, max(1, min(radius, 60)))
    return small
```

### Рецепт 8: Сериализация и восстановление медиа-вложений TLRPC.Document
Сохранение документов в строковый JSON/настройки плагина:
```python
import base64
from org.telegram.tgnet import SerializedData, TLRPC

def serialize_doc(doc):
    size = doc.getObjectSize()
    data = SerializedData(size)
    doc.serializeToStream(data)
    raw = data.toByteArray()
    data.cleanup()
    return base64.b64encode(bytes(raw)).decode("ascii")

def deserialize_doc(b64_str):
    raw = base64.b64decode(b64_str)
    data = SerializedData(bytes(raw))
    constructor = data.readInt32(False)
    doc = TLRPC.Document.TLdeserialize(data, constructor, False)
    data.cleanup()
    return doc
```

---

## Ограничения и противоречия

1. **Зависимость от внутренней архитектуры Telegram/ExteraGram:** Имена полей и приватных методов (`durationLayout`, `descriptionLayout`, `timeWidthAudio` в `ChatMessageCell`, `playerLayout` в `AudioPlayerAlert`) подвержены обфускации и изменению между релизами. Вызовы `getDeclaredField` требуют обработки `NoSuchFieldError` и fallback-стратегий.
2. **Ограничения файлового кэша при потоковом воспроизведении:** При потоковом прослушивании аудиозаписи файл на диске растет по мере буферизации. Чтение метаданных через `MediaMetadataRetriever` во время воспроизведения может возвращать неполные данные или вызывать сбой, если размер файла меньше `document.size`.
3. **Питч-шифтинг через занижение sampleRate:** Прием с подменой частоты дискретизации в `MediaController.startRecord` эффективен только при условии, что декодер на стороне получателя воспроизводит голосовые сообщения на фиксированных 48000 Гц. Сторонние клиенты с гибким выбором частоты могут воспроизводить такой звук на исходной скорости без эффекта понижения тона.
4. **Аппаратные ограничения энкодеров Camera2:** Установка произвольных значений разрешения и FPS в `MediaRecorder` и `MediaFormat` ограничивается возможностями конкретного чипсета и камеры. Некоторые SoC не поддерживают видеозапись 60 FPS в нестандартных квадратных разрешениях (например, 512x512) и выбрасывают `MediaCodec.CodecException`.
5. **Потокобезопасность WebRTC аудио-буферов:** Модификация байтов в `WebRtcAudioRecord.nativeDataIsRecorded` выполняется в реальном времени на высокоприоритетном системном аудиопотоке. Любая задержка обработки (I/O, сборка мусора, блокировки) приводит к пропускам кадров (buffer underrun) и треску в разговоре.
