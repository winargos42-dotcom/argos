---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/docs/source/pipeline.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\src\gallium\docs\source\pipeline.txt
source_ext: .txt
source_sha256: 648bb12ec15c2e19502f7a64c901e52829dfbc3cc606e16eb222bdd6ef216938
text_sha256: 63753fb9e902d1f018715af01ddda16058b5b7315c57ec3731bc0eee53f3f2ec
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:33
---

# pipeline.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/docs/source/pipeline.txt`
- Extract: `text`
- SHA256: `648bb12ec15c2e19502f7a64c901e52829dfbc3cc606e16eb222bdd6ef216938`

## Content

XXX this could be converted/formatted for Sphinx someday.
XXX do not use tabs in this file.



            position                     ]
            primary/secondary colors     ]
            generics (normals,           ]
               texcoords, fog)           ] User vertices / arrays
            point size                   ]
            edge flag                    ]
            primitive ID                 } System-generated values
            vertex ID                    }
              | | |
              V V V
      +-------------------+
      |  Vertex shader    |
      +-------------------+
              | | |
              V V V
            position
            clip distance
            generics
            front/back & primary/secondary colors
            point size
            edge flag
            primitive ID
              | | |
              V V V
      +------------------------+
      |     Geometry shader    |
      | (consume vertex ID)    |
      | (may change prim type) |
      +------------------------+
              | | |
              V V V
            [...]
            fb layer
              | | |
              V V V
      +--------------------------+
      |         Clipper          |
      | (consume clip distances) |
      +--------------------------+
              | | |
              V V V
      +-------------------+
      |  Polygon Culling  |
      +-------------------+
              | | |
              V V V
      +-----------------------+
      |    Choose front or    |
      |    back face color    |
      | (consume other color) |
      +-----------------------+
              | | |
              V V V
            [...]
            primary/secondary colors only
              | | |
              V V V
      +-------------------+
      |   Polygon Offset  |
      +-------------------+
              | | |
              V V V
      +----------------------+
      | Unfilled polygons    |
      | (consume edge flags) |
      | (change prim type)   |
      +----------------------+
              | | |
              V V V
            position
            generics
            primary/secondary colors
            point size
            primitive ID
            fb layer
              | | |
              V V V
  +---------------------------------+ 
  | Optional Draw module helpers    |
  | * Polygon Stipple               |
  | * Line Stipple                  |
  | * Line AA/smooth (as tris)      |
  | * Wide lines (as tris)          |
  | * Wide points/sprites (as tris) |
  | * Point AA/smooth (as tris)     |
  | (NOTE: these stages may emit    |
  |  new/extra generic attributes   |
  |  such as texcoords)             |
  +---------------------------------+
              | | |
              V V V
            position                     ]
            generics (+ new/extra ones)  ]
            primary/secondary colors     ] Software rast vertices
            point size                   ]
            primitive ID                 ]
            fb layer                     ]
              | | |
              V V V
      +---------------------+
      | Triangle/Line/Point |
      |    Rasterization    |
      +---------------------+
              | | |
              V V V
            generic attribs
            primary/secondary colors
            primitive ID
            fragment win coord pos   } System-generated values
            front/back face flag     }
              | | |
              V V V
      +-------------------+
      |  Fragment shader  |
      +-------------------+
              | | |
              V V V
            zero or more colors
            zero or one Z value


NOTE: The instance ID is not shown.  It can be imagined to be a global variable
accessible to all shader stages.

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
