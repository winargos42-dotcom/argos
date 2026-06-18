---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/multithreading.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\ffmpeg\ffmpeg-2.8\doc\multithreading.txt
source_ext: .txt
source_sha256: 8cddf7d90d93af0218fffaf428263f6f5d3ac4d981916d34e4777be1f34744eb
text_sha256: ade31886a9e64ac3b5d377819240b2aa56fd32c7b331064707d06ea729d1c093
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:29
---

# multithreading.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/multithreading.txt`
- Extract: `text`
- SHA256: `8cddf7d90d93af0218fffaf428263f6f5d3ac4d981916d34e4777be1f34744eb`

## Content

FFmpeg multithreading methods
==============================================

FFmpeg provides two methods for multithreading codecs.

Slice threading decodes multiple parts of a frame at the same time, using
AVCodecContext execute() and execute2().

Frame threading decodes multiple frames at the same time.
It accepts N future frames and delays decoded pictures by N-1 frames.
The later frames are decoded in separate threads while the user is
displaying the current one.

Restrictions on clients
==============================================

Slice threading -
* The client's draw_horiz_band() must be thread-safe according to the comment
  in avcodec.h.

Frame threading -
* Restrictions with slice threading also apply.
* For best performance, the client should set thread_safe_callbacks if it
  provides a thread-safe get_buffer() callback.
* There is one frame of delay added for every thread beyond the first one.
  Clients must be able to handle this; the pkt_dts and pkt_pts fields in
  AVFrame will work as usual.

Restrictions on codec implementations
==============================================

Slice threading -
 None except that there must be something worth executing in parallel.

Frame threading -
* Codecs can only accept entire pictures per packet.
* Codecs similar to ffv1, whose streams don't reset across frames,
  will not work because their bitstreams cannot be decoded in parallel.

* The contents of buffers must not be read before ff_thread_await_progress()
  has been called on them. reget_buffer() and buffer age optimizations no longer work.
* The contents of buffers must not be written to after ff_thread_report_progress()
  has been called on them. This includes draw_edges().

Porting codecs to frame threading
==============================================

Find all context variables that are needed by the next frame. Move all
code changing them, as well as code calling get_buffer(), up to before
the decode process starts. Call ff_thread_finish_setup() afterwards. If
some code can't be moved, have update_thread_context() run it in the next
thread.

If the codec allocates writable tables in its init(), add an init_thread_copy()
which re-allocates them for other threads.

Add AV_CODEC_CAP_FRAME_THREADS to the codec capabilities. There will be very little
speed gain at this point but it should work.

If there are inter-frame dependencies, so the codec calls
ff_thread_report/await_progress(), set AVCodecInternal.allocate_progress. The
frames must then be freed with ff_thread_release_buffer().
Otherwise leave it at zero and decode directly into the user-supplied frames.

Call ff_thread_report_progress() after some part of the current picture has decoded.
A good place to put this is where draw_horiz_band() is called - add this if it isn't
called anywhere, as it's useful too and the implementation is trivial when you're
doing this. Note that draw_edges() needs to be called before reporting progress.

Before accessing a reference frame or its MVs, call ff_thread_await_progress().

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
