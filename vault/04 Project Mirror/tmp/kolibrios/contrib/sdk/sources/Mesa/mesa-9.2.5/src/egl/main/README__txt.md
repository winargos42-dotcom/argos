---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/egl/main/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\egl\main\README.txt
source_ext: .txt
source_sha256: 2fec206890ca07cee1114c76893550667de8f150fa2e97377c8ca63b9046ed1e
text_sha256: 1b337acab99235fec8e4a98d991afb8f6d21a2e57e48fd38905cf2e6a0fca0b1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:35
---

# README.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/egl/main/README.txt`
- Extract: `text`
- SHA256: `2fec206890ca07cee1114c76893550667de8f150fa2e97377c8ca63b9046ed1e`

## Content

Notes about the EGL library:


The EGL code here basically consists of two things:

1. An EGL API dispatcher.  This directly routes all the eglFooBar() API
   calls into driver-specific functions.

2. Fallbacks for EGL API functions.  A driver _could_ implement all the
   EGL API calls from scratch.  But in many cases, the fallbacks provided
   in libEGL (such as eglChooseConfig()) will do the job.



Bootstrapping:

When the apps calls eglOpenDisplay() a device driver is selected and loaded
(look for dlsym() or LoadLibrary() in egldriver.c).

The driver's _eglMain() function is then called.  This driver function
allocates, initializes and returns a new _EGLDriver object (usually a
subclass of that type).

As part of initialization, the dispatch table in _EGLDriver->API must be
populated with all the EGL entrypoints.  Typically, _eglInitDriverFallbacks()
can be used to plug in default/fallback functions.  Some functions like
driver->API.Initialize and driver->API.Terminate _must_ be implemented
with driver-specific code (no default/fallback function is possible).


A bit later, the app will call eglInitialize().  This will get routed
to the driver->API.Initialize() function.  Any additional driver
initialization that wasn't done in _eglMain() should be done at this
point.  Typically, this will involve setting up visual configs, etc.



Special Functions:

Certain EGL functions _must_ be implemented by the driver.  This includes:

eglCreateContext
eglCreateWindowSurface
eglCreatePixmapSurface
eglCreatePBufferSurface
eglMakeCurrent
eglSwapBuffers

Most of the EGLConfig-related functions can be implemented with the
defaults/fallbacks.  Same thing for the eglGet/Query functions.




Teardown:

When eglTerminate() is called, the driver->API.Terminate() function is
called.  The driver should clean up after itself.  eglTerminate() will
then close/unload the driver (shared library).




Subclassing:

The internal libEGL data structures such as _EGLDisplay, _EGLContext,
_EGLSurface, etc should be considered base classes from which drivers
will derive subclasses.

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
