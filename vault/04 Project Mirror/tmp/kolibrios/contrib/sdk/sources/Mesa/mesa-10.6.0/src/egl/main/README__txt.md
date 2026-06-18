---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/egl/main/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\src\egl\main\README.txt
source_ext: .txt
source_sha256: 53915b64df2c3c240709933703c89f18da36a030749bf89f06e455734ea74c14
text_sha256: 761acf7414389179d6ee5f59a073010d7c4cac781ee2ecc42b070632331c5b69
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:32
---

# README.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/egl/main/README.txt`
- Extract: `text`
- SHA256: `53915b64df2c3c240709933703c89f18da36a030749bf89f06e455734ea74c14`

## Content

Notes about the EGL library:


The EGL code here basically consists of two things:

1. An EGL API dispatcher.  This directly routes all the eglFooBar() API
   calls into driver-specific functions.

2. Fallbacks for EGL API functions.  A driver _could_ implement all the
   EGL API calls from scratch.  But in many cases, the fallbacks provided
   in libEGL (such as eglChooseConfig()) will do the job.



Bootstrapping:

When the apps calls eglInitialize() a device driver is selected and loaded
(look for _eglAddDrivers() and _eglLoadModule() in egldriver.c).

The built-in driver's entry point function is then called.  This driver function
allocates, initializes and returns a new _EGLDriver object (usually a
subclass of that type).

As part of initialization, the dispatch table in _EGLDriver->API must be
populated with all the EGL entrypoints.  Typically, _eglInitDriverFallbacks()
can be used to plug in default/fallback functions.  Some functions like
driver->API.Initialize and driver->API.Terminate _must_ be implemented
with driver-specific code (no default/fallback function is possible).


Shortly after, the driver->API.Initialize() function is executed.  Any additional
driver initialization that wasn't done in the driver entry point should be
done at this point.  Typically, this will involve setting up visual configs, etc.



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
