---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/docs/specs/MESA_image_dma_buf_export.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\docs\specs\MESA_image_dma_buf_export.txt
source_ext: .txt
source_sha256: e0f4d135a1048c73cbbe7e77202db2178cd8d10b26fb710be07ca05a9c99fb12
text_sha256: 0b7aae07bae0efc8d0d0eaccc6a229d6f800c61d84e159ed8e29dc2dd57617ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:32
---

# MESA_image_dma_buf_export.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/docs/specs/MESA_image_dma_buf_export.txt`
- Extract: `text`
- SHA256: `e0f4d135a1048c73cbbe7e77202db2178cd8d10b26fb710be07ca05a9c99fb12`

## Content

Name

    MESA_image_dma_buf_export

Name Strings

    EGL_MESA_image_dma_buf_export

Contributors

    Dave Airlie

Contact

    Dave Airlie (airlied 'at' redhat 'dot' com)

Status

    Complete, shipping.

Version

    Version 3, May 5, 2015

Number

    EGL Extension #87

Dependencies

    Requires EGL 1.4 or later.  This extension is written against the
    wording of the EGL 1.4 specification.

    EGL_KHR_base_image is required.

    The EGL implementation must be running on a Linux kernel supporting the
    dma_buf buffer sharing mechanism.

Overview

    This extension provides entry points for integrating EGLImage with the
    dma-buf infrastructure.  The extension allows creating a Linux dma_buf
    file descriptor or multiple file descriptors, in the case of multi-plane
    YUV image, from an EGLImage.

    It is designed to provide the complementary functionality to
    EGL_EXT_image_dma_buf_import.

IP Status

    Open-source; freely implementable.

New Types

    This extension uses the 64-bit unsigned integer type EGLuint64KHR
    first introduced by the EGL_KHR_stream extension, but does not
    depend on that extension. The typedef may be reproduced separately
    for this extension, if not already present in eglext.h.

    typedef khronos_uint64_t EGLuint64KHR;

New Procedures and Functions

    EGLBoolean eglExportDMABUFImageQueryMESA(EGLDisplay dpy,
                                  EGLImageKHR image,
				  int *fourcc,
				  int *num_planes,
				  EGLuint64KHR *modifiers);

    EGLBoolean eglExportDMABUFImageMESA(EGLDisplay dpy,
                                        EGLImageKHR image,
                                        int *fds,
				        EGLint *strides,
					EGLint *offsets);

New Tokens

    None


Additions to the EGL 1.4 Specification:

    To mirror the import extension, this extension attempts to return
    enough information to enable an exported dma-buf to be imported
    via eglCreateImageKHR and EGL_LINUX_DMA_BUF_EXT token.

    Retrieving the information is a two step process, so two APIs
    are required.

    The first entrypoint
       EGLBoolean eglExportDMABUFImageQueryMESA(EGLDisplay dpy,
                                  EGLImageKHR image,
				  int *fourcc,
				  int *num_planes,
				  EGLuint64KHR *modifiers);

    is used to retrieve the pixel format of the buffer, as specified by
    drm_fourcc.h, the number of planes in the image and the Linux
    drm modifiers. <fourcc>, <num_planes> and <modifiers> may be NULL,
    in which case no value is retrieved.

    The second entrypoint retrieves the dma_buf file descriptors,
    strides and offsets for the image. The caller should pass
    arrays sized according to the num_planes values retrieved previously.
    Passing arrays of the wrong size will have undefined results.
    If the number of fds is less than the number of planes, then
    subsequent fd slots should contain -1.

        EGLBoolean eglExportDMABUFImageMESA(EGLDisplay dpy,
                                         EGLImageKHR image,
					 int *fds,
                                         EGLint *strides,
                                         EGLint *offsets);

    <fds>, <strides>, <offsets> can be NULL if the infomatation isn't
    required by the caller.

Issues

1. Should the API look more like an attribute getting API?

ANSWER: No, from a user interface pov, having to iterate across calling
the API up to 12 times using attribs seems like the wrong solution.

2. Should the API take a plane and just get the fd/stride/offset for that
   plane?

ANSWER: UNKNOWN,this might be just as valid an API.

3. Does ownership of the file descriptor remain with the app?

ANSWER: Yes, the app is responsible for closing any fds retrieved.

4. If number of planes and number of fds differ what should we do?

ANSWER: Return -1 for the secondary slots, as this avoids having
to dup the fd extra times to make the interface sane.

Revision History

    Version 3, May, 2015
        Just use the KHR 64-bit type.
    Version 2, March, 2015
        Add a query interface (Dave Airlie)
    Version 1, June 3, 2014
        Initial draft (Dave Airlie)

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
