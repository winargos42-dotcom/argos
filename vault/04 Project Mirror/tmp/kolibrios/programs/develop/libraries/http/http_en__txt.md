---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/libraries/http/http_en.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\libraries\http\http_en.txt
source_ext: .txt
source_sha256: c98fe9e0d85b0a847dc66b655975fd45444033782c02eba9661c9b71b99dcee8
text_sha256: 77ca70ed3edd411f3aeec08afbd54ca7e41482895614a273a80540a2c9a28a9b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# http_en.txt

- Source: `tmp/kolibrios/programs/develop/libraries/http/http_en.txt`
- Extract: `text`
- SHA256: `c98fe9e0d85b0a847dc66b655975fd45444033782c02eba9661c9b71b99dcee8`

## Content

get(*url, identifier, flags, *add_header);
	*url = pointer to ASCIIZ URL
	identifier = identifier of previously opened connection (keep-alive), or 0 to open a new one.
	flags = bit flags (see end of this document).
	*add_header = pointer to ASCIIZ additional header parameters, or null for none.
			Every additional parameter must end with CR LF bytes, including the last line.
Initiates a HTTP connection, using 'GET' method.
 - returns 0 on error, identifier otherwise.

head(*url, identifier, flags, *add_header);
	*url = pointer to ASCIIZ URL
	identifier = identifier of previously opened connection (keep-alive), or 0 to open a new one.
	flags = bit flags (see end of this document).
	*add_header = pointer to ASCIIZ additional header parameters, or null for none.	
			Every additional parameter must end with CR LF bytes, including the last line.	
Initiate a HTTP connection, using 'HEAD' method.
 - returns 0 on error, identifier otherwise

post(*url, identifier, flags, *add_header, *content-type, content-length);
	*url = pointer to ASCIIZ URL
	identifier = identifier of previously opened connection (keep-alive), or 0 to open a new one.
	flags = bit flags (see end of this document).
	*add_header = pointer to ASCIIZ additional header parameters, or null for none.	
			Every additional parameter must end with CR LF bytes, including the last line.
	*content-type = pointer to ASCIIZ string containing content type.
	content-length = length of the content (in bytes).
Initiate a HTTP connection, using 'POST' method.
The content itself must be send to the socket (which you can find in the structure),
using system function 75, 6.
 - returns 0 on error, identifier otherwise

receive(identifier);
	identifier = identifier which one of the previous functions returned
This procedure will handle all incoming data for a connection and place it in the buffer.
As long as the procedure expects more data, -1 is returned and the procedure must be called again.
 - When transfer is done, the procedure will return 0. 
The receive procedure is non-blocking by default, but can be made to block by setting FLAG_BLOCK.

The HTTP header is placed together with some flags and other attributes in the http_msg structure.
This structure is defined in http.inc (and not copied here because it might still change.)
The identifier used by the functions is actually a pointer to this structure.
In the dword named .flags, the library will set various bit-flags indicating the status of the process.
(When a transfer is done, one should check these bit-flags to find out if the transfer was error-free.)
The HTTP header is placed at the end of this structure. The content is placed in another buffer.
The dword .status contains the status code received from the server (e.g. 200 for OK).
In header_length you'll find the length of the header as soon as it has been received.
In content_ptr you'll find a pointer to the actual content.
In content_length you'll find the length of the content. 
In content_received, you'll find the number of content bytes already received.

send(identifier, *dataptr, datalength);
	identifier = identifier which one of the previous functions returned
	*dataptr = pointer to the data you want to send
	datalength = length of the data to send (in bytes)
This procedure can be used to send data to the server (POST)
 - returns number of bytes sent, -1 on error
 
 
User flags:

For the flag codes themselves, see http.inc file.

 FLAG_KEEPALIVE will keep the connection open after first GET/POST/.. so you can send a second request on the same TCP session. 
In this case, the session must be closed manually when done by using the exported disconnect() function.

 FLAG_STREAM will force receive() to put the received content in a series of fixed size buffers, instead of everything in one big buffer.
This can be used for example to receive an internet radio stream, 
but also to download larger files for which it does not make sense to put them completely in RAM first.

 FLAG_REUSE_BUFFER is to be used in combination with FLAG_STREAM and will make receive() function re-use the same buffer.
This, for example, can be used when downloading a file straight to disk.

 FLAG_BLOCK will make receive() function blocking. This is only to be used when receiving one file from a thread that has no other work.
If however, you want to receive multiple files, or do other things in the program mainloop, you should call the receive function periodically. 
You may use system function 10 or 23 to wait for network event before calling one or more receive() functions.

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
