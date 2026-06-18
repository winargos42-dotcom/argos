---
argos_import: project_file
source_path: llama.cpp/examples/llama.swiftui/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\llama.swiftui\README.md
source_ext: .md
source_sha256: 6f9e86689c3d638654a48df76d1e9d985e0a4b4843f1ee17358f201e2e199b89
text_sha256: 8794bd3f3817103b8e69086eded7608491b6b6c62b917558d76c233816f1c5a0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/llama.swiftui/README.md`
- Extract: `text`
- SHA256: `6f9e86689c3d638654a48df76d1e9d985e0a4b4843f1ee17358f201e2e199b89`

## Content

# llama.cpp/examples/llama.swiftui

Local inference of llama.cpp on an iPhone. This is a sample app that can be used as a starting
point for more advanced projects.

For usage instructions and performance stats, check the following discussion: https://github.com/ggml-org/llama.cpp/discussions/4508


### Building
First llama.cpp need to be built and a XCFramework needs to be created. This can be done by running
the following script from the llama.cpp project root:
```console
$ ./build-xcframework.sh
```
Open `llama.swiftui.xcodeproj` project in Xcode and you should be able to build and run the app on
a simulator or a real device.

To use the framework with a different project, the XCFramework can be added to the project by
adding `build-apple/llama.xcframework` by dragging and dropping it into the project navigator, or
by manually selecting the framework in the "Frameworks, Libraries, and Embedded Content" section
of the project settings.

![image](https://github.com/ggml-org/llama.cpp/assets/1991296/2b40284f-8421-47a2-b634-74eece09a299)

Video demonstration:

https://github.com/bachittle/llama.cpp/assets/39804642/e290827a-4edb-4093-9642-2a5e399ec545

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
