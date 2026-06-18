---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/gmod-addon-maker/references/common-error.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\gmod-addon-maker\references\common-error.md
source_ext: .md
source_sha256: 086364dd5f10f0744a596246fb8ad8693b6bf61e603af35c26d40055366f13d1
text_sha256: efd3f782528ec4dc735d89d778b051bf435fc6b4321671e507aead3f81d66faa
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# common-error.md

- Source: `claude-code-templates/cli-tool/components/skills/gmod-addon-maker/references/common-error.md`
- Extract: `text`
- SHA256: `086364dd5f10f0744a596246fb8ad8693b6bf61e603af35c26d40055366f13d1`

## Content

#  Common Errors 

##  Attempt to call global '?' a nil value 

**Description:** You tried to call a function that doesn't exist.

**Possible causes:** 
* Your function might be defined in another Lua state. (e.g Calling a function on the client that only exists on the * server.)
* You're using a metafunction on the wrong kind of object. (e.g. Calling :SteamID() on a Vector)
* The function you're calling has an error in it which means it is not defined.
* You've misspelled the name of the function.

**Ways to fix:**
* Make sure the function exists
* Make sure your function is defined in the correct realm
* Check your function calls for spelling errors


##  Attempt to perform arithmetic on global '?' (a nil value) 

**Description:** You tried to perform arithmetic (+, -, *, /) on a global variable that is not defined.

**Possible causes:** 
* You tried to use a local variable that was defined later in the code
* You've misspelled the name of the global variable

**Ways to fix:**
* Make sure you define local variables before calling them in the code
* Check for spelling errors


##  Attempt to perform arithmetic on '?' (a type value) 

**Description:** You tried to perform arithmetic (+, -, *, /) on a variable that cannot perform arithmetic. (e.g. 2 + "some string")


##  Attempt to index global 'varname' (a nil value) 

**Description:** You tried to index an undefined variable (e.g. `print( variable.index )` where `variable` is undefined)

**Possible causes:**
* The variable is defined in a different realm
* The variable is local and defined later in the code
* You've misspelled the name of the variable

**Ways to fix:**
* Make sure the variable is only accessed in the realm it was defined in
* If the variable is local, define it before accessing it


##  Malformed number near 'number' 

**Description:** There is a malformed number in the code (e.g. 1.2.3, 2f) 

**Possible causes:**
* An IP address was written as a number instead of a string
* Incorrect writing of multiplication of a number and a variable
* Trying to concatenate a number to a string without a space between the number and the operator.

**Ways to fix:**
* Store IP addresses as a string
* Multiply variables with numbers by using the ***** operator
* Put a space between the concat (**..**) operator and the number.


##  Unexpected symbol near 'symbol' 

**Description:** You typed a symbol in the code that Lua didn't know how to interpret.

**Possible causes:**
* Incorrect syntax (e.g. Forgot to write "then" after an if statement)
* Not closing brackets and parentheses at the correct locations

**Ways to fix:**
* Make sure there are no mistypes in the code
* Close brackets and parentheses correctly (See: Code Indentation)


##  'symbol1' expected near 'symbol2' 
**Description:** Lua expected symbol1 instead of symbol2.
When 'symbol2' is <eof>, Lua expected a symbol before the end of the file

**Possible causes:**
* Not closing all brackets, parentheses or functions before the end of the file
* Having too many `end` statements
* Wrong operator calling (e.g. "==" instead of "=")
* Missing comma after table item.

**Ways to fix:**
* Close brackets and parentheses correctly (See: Code Indentation)
* Use the correct operators
* Add a comma after a table item

## Couldn't include file 'file' - File not found (<nowhere>)
**Description:** The file system tried to include a file that either doesn't exist or was added while the server was live.
This error can also be a `AddCSLuaFile` error.

**Possible causes:**
* Attempting to include / AddCSLuaFile a file that doesn't exist or is empty
* Creating a file while the server is still live

**Ways to fix:**
* Add the non-existent file, make sure the file isn't empty
* Restart the server

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
