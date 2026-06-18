---
argos_import: project_file
source_path: tmp/kolibrios/programs/fs/unzip60/zipgrep.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\fs\unzip60\zipgrep.txt
source_ext: .txt
source_sha256: d49b7c86df25b01ed125c57a1663f71638268d9e9c87d4e487b8a3e0e3db2548
text_sha256: 8583592b89c3736ee2bcfe270199c5ec4e8dc48f14f22e0f35aa2f75647b31e4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# zipgrep.txt

- Source: `tmp/kolibrios/programs/fs/unzip60/zipgrep.txt`
- Extract: `text`
- SHA256: `d49b7c86df25b01ed125c57a1663f71638268d9e9c87d4e487b8a3e0e3db2548`

## Content

ZIPGREP(1L)                                                        ZIPGREP(1L)

NAME
       zipgrep - search files in a ZIP archive for lines matching a pattern

SYNOPSIS
       zipgrep     [egrep_options]     pattern     file[.zip]    [file(s) ...]
       [-x xfile(s) ...]

DESCRIPTION
       zipgrep will search files within a ZIP archive for lines  matching  the
       given  string  or  pattern.   zipgrep  is  a  shell script and requires
       egrep(1) and unzip(1L) to function.  Its output is identical to that of
       egrep(1).

ARGUMENTS
       pattern
              The  pattern  to  be  located  within a ZIP archive.  Any
              string or regular expression accepted by egrep(1) may  be
              used.   file[.zip]  Path  of  the ZIP archive.  (Wildcard
              expressions for the ZIP archive name are not  supported.)
              If  the literal filename is not found, the suffix .zip is
              appended.  Note that self-extracting ZIP files  are  sup-
              ported,  as  with any other ZIP archive; just specify the
              .exe suffix (if any) explicitly.

       [file(s)]
              An optional list of archive members to be processed, sep-
              arated  by spaces.  If no member files are specified, all
              members of the ZIP archive are searched.  Regular expres-
              sions (wildcards) may be used to match multiple members:

              *      matches a sequence of 0 or more characters

              ?      matches exactly 1 character

              [...]  matches  any  single  character  found  inside the
                     brackets; ranges  are  specified  by  a  beginning
                     character,  a hyphen, and an ending character.  If
                     an exclamation point or a caret (`!' or `^')  fol-
                     lows  the  left bracket, then the range of charac-
                     ters within the brackets is complemented (that is,
                     anything except the characters inside the brackets
                     is considered a match).

              (Be sure to quote any character that might  otherwise  be
              interpreted or modified by the operating system.)

       [-x xfile(s)]
              An  optional  list of archive members to be excluded from
              processing.  Since wildcard  characters  match  directory
              separators  (`/'), this option may be used to exclude any
              files that are in subdirectories.  For example, ``zipgrep
              grumpy  foo  *.[ch]  -x */*'' would search for the string
              ``grumpy'' in all C source files in the main directory of
              the  ``foo''  archive,  but  none  in any subdirectories.
              Without the -x option, all C source files in all directo-
              ries within the zipfile would be searched.

OPTIONS
       All  options  prior  to  the  ZIP archive filename are passed to
       egrep(1).

SEE ALSO
       egrep(1), unzip(1L),  zip(1L),  funzip(1L),  zipcloak(1L),  zip-
       info(1L), zipnote(1L), zipsplit(1L)

URL
       The   Info-ZIP   home  page  is  currently  at  http://www.info-
       zip.org/pub/infozip/ or ftp://ftp.info-zip.org/pub/infozip/ .

AUTHORS
       zipgrep was written by Jean-loup Gailly.

Info-ZIP                         20 April 2009                     ZIPGREP(1L)

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
