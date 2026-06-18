---
argos_import: project_file
source_path: .pio/libdeps/esp32dev/ArduinoJson/src/CMakeLists.txt
source_abs: F:\debug\argoss\.pio\libdeps\esp32dev\ArduinoJson\src\CMakeLists.txt
source_ext: .txt
source_sha256: 3978c6ece5b6575dc8fa005a3b7ec020079b5cfd56c4ba0e6f96dcea44f35d01
text_sha256: 3978c6ece5b6575dc8fa005a3b7ec020079b5cfd56c4ba0e6f96dcea44f35d01
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# CMakeLists.txt

- Source: `.pio/libdeps/esp32dev/ArduinoJson/src/CMakeLists.txt`
- Extract: `text`
- SHA256: `3978c6ece5b6575dc8fa005a3b7ec020079b5cfd56c4ba0e6f96dcea44f35d01`

## Content

# ArduinoJson - https://arduinojson.org
# Copyright © 2014-2026, Benoit BLANCHON
# MIT License

# I have no idea what this is about, I simply followed the instructions from:
# https://dominikberner.ch/cmake-interface-lib/

add_library(ArduinoJson INTERFACE)

include(GNUInstallDirs)

# Adding the install interface generator expression makes sure that the include
# files are installed to the proper location (provided by GNUInstallDirs)
target_include_directories(ArduinoJson
	INTERFACE
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_compile_definitions(ArduinoJson
	INTERFACE
		ARDUINOJSON_DEBUG=$<CONFIG:Debug>
)

# locations are provided by GNUInstallDirs
install(
	TARGETS
		ArduinoJson
	EXPORT
		ArduinoJson_Targets
	ARCHIVE DESTINATION
		${CMAKE_INSTALL_LIBDIR}
	LIBRARY DESTINATION
		${CMAKE_INSTALL_LIBDIR}
	RUNTIME DESTINATION
		${CMAKE_INSTALL_BINDIR}
)

include(CMakePackageConfigHelpers)

if(${CMAKE_VERSION} VERSION_GREATER "3.14.0")
	set(ARCH_INDEPENDENT "ARCH_INDEPENDENT")
endif()

write_basic_package_version_file(
		"${PROJECT_BINARY_DIR}/ArduinoJsonConfigVersion.cmake"
	VERSION
		${PROJECT_VERSION}
	COMPATIBILITY
		SameMajorVersion
	${ARCH_INDEPENDENT}
)

configure_package_config_file(
		"${PROJECT_SOURCE_DIR}/extras/ArduinoJsonConfig.cmake.in"
		"${PROJECT_BINARY_DIR}/ArduinoJsonConfig.cmake"
	INSTALL_DESTINATION
		${CMAKE_INSTALL_DATAROOTDIR}/ArduinoJson/cmake
)

install(
	EXPORT
		ArduinoJson_Targets
	FILE
		ArduinoJsonTargets.cmake
	DESTINATION
		${CMAKE_INSTALL_DATAROOTDIR}/ArduinoJson/cmake
)

install(
	FILES
		"${PROJECT_BINARY_DIR}/ArduinoJsonConfig.cmake"
		"${PROJECT_BINARY_DIR}/ArduinoJsonConfigVersion.cmake"
	DESTINATION
		"${CMAKE_INSTALL_DATAROOTDIR}/ArduinoJson/cmake"
)

install(
	FILES
		ArduinoJson.h
		ArduinoJson.hpp
	DESTINATION
		include
)

install(
	DIRECTORY
		"${CMAKE_CURRENT_SOURCE_DIR}/ArduinoJson"
	DESTINATION
		include
)

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
