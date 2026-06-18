---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/midamp/trunk/midamp.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\midamp\trunk\midamp.txt
source_ext: .txt
source_sha256: 6ea8e33715ee399ddede415b7a0e623affb2cec821d4eb12481f4e0ab582f908
text_sha256: e21d3b57181e8972fb1352601340f0fc7f8ec8881b81654273b3e6e615546a79
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# midamp.txt

- Source: `tmp/kolibrios/programs/media/midamp/trunk/midamp.txt`
- Extract: `text`
- SHA256: `6ea8e33715ee399ddede415b7a0e623affb2cec821d4eb12481f4e0ab582f908`

## Content

MIDAMP for Menuet v1.0       July 29, 2005
 Written in pure assembler by Ivushkin Andrey aka Willow

Monophonic MIDI player

Vivat assembler et MENUETOS!
MenuetOS still has a poor sound capabilities. Drivers are written for a few
soundcard models. Till recently I considered MEOS to be as voiceless as an
oyster. But then an alternative appeared; dear VaStaNi wrote kernel support of 
PC speaker. Old good times of Pascal and MS-DOS came to me again. About 5 years
ago I wrote a Pascal application that parsed and played a note string in QBasic
syntax.

Now MeOS gets the simplest, speaker-driven sound scheme in Mario79's distro,
but the first melody in Menuet I heard was from the my program MIDAMP in
December, 2004. On technical reasons its release takes place only now.

So, MIDAMP is the simplest single-voiced MIDI player. It cannot do much though
it resembles the famous WinAmp. All it can do is to beep MIDI files.
There are no equalizer, balance and fader, and they won't appear. Moreover,
I may guarantee the correct sound only for files having a single track, one
instrument channel and within technological range of notes :-(

#########
System requirements:
1. Kernel having following function implemented:
       55/55 - PC speaker interface (critical!)
       67    - window shading;
       66/3  - for extended mouse selection in playlist.
2. SYSXTREE version not below 52 - opening files and directories (critical!)
3. RAM amount for application - about 150 Kbytes.       
#########

MIDAMP still uses a single playlist - /HD/1/PLAYLIST.TXT by default. Persons
interested can change the PLAYLIST_PATH constant value in MIDAMP.ASM. Playlist 
is a simple text file having filenames to be played in each line. It is NOT 
RECOMMENDED to edit the playlist by hand - bugs may appear while loading MIDAMP.

When started, MIDAMP creates a new thread whose job is actually playing. Early
versions had main thread that processed everything, therefore unpleasant sound
delays appeared when managing the playlist. Threads communicate intensively
through IPC, although I think it's an excess in such a case. But it works not
bad.

MIDAMP is able to shade to window header by pressing the proper button. I tried
to perform complete minimization through mcall 18,10 (new feature of Kolibri4),
but ran into the problem while restoring of window when PANEL button pressed.
That function possibly does not support windows type II ?

Hotkeys - almost like in WinAmp:

Del - delete the selected tracks;
z   - previous track;
x, Enter, double click - play selected file;
c, Space - pause;
v   - stop;
b   - next track;

Esc - close the program;
m   - sound on/off;
PgUp, PgDn - swap 2 tracks (not completed!);
BackSpace  - rewind track;
Home/End - increase/decrease melody notes offset and play track from beginning 
    (it is shown near 'tone>' text).
   
In the case of polyphonic MIDI, if an intelligent melody isn't heard, you may
try to choose another track 'trk' or instrument channel 'chnl', pressing '[' or
']' accordingly and then a number key from '0' to '9'. The file will be played
from the beginning. To reset track and channel to the default value, press '\' .

Explaining some interface buttons:
Shuffle toggles random playback on/off. Repeat - current track will loop again
and again. An icon in the top left corner outputs a brief info about the 
program to the Debug Board. Clicking the time toggles its view - from beginning
or from the end of file.

Mouse click on playlist when holding Shift or Ctrl button works like in WinAmp.

Remarks to bottom buttons:
'Add URL' not implemented, on clear reasons;
'Add Dir' - specify any file in the directory desired. *.MID and *.KAR files of 
     that directory will be added to the list;
'Misc' submenu is not implemented;
'New List' does nothing. MIDAMP still uses a fixed playlist.

One of the following flags may precede a filename in the commandline:

W - to load a file and wait (default);
P - to play a file;
H - to start shaded and close after playback.

To-Do list:

1.  Increase playlist size (40 items for now).
2.  Add dialog to select tracks of polyphonic melodies including analysis on 
    notes.
3.  Reading text in Karaoke files.
4.  Playlist select.
5.  Note editor, as in Ringtone Editor.
6.  Add comments to source.
7.  Correct bugs to be found.

Special thanks to:

   VaStaNi - there would be no need of MIDAMP w/o his code
   Standard MIDI Files 0.06        March 1, 1988
   MIDI 1.0 Specification
   General MIDI Level Spec
   MIDI SAMPLE DUMP STANDARD
   Standard MIDI File Format by Dustin Caldwell
   Files format of MIDI
   The USENET MIDI Primer by Bob McQueer
   Pavlushin Evgeny for his splendid SYSXTREE (DLGS.INC is the opendialog macro
       of ASCL library edited to meet MIDAMP specific needs)

Send the wishes and bug reports to wil_low@hotbox.ru or to the meos.sysbin.com
forum.

See you later!


****************************************
****************************************

MIDAMP  Menuet v1.0       29  2005 .
 ᠭ  ⮬ ᥬ 誨 ॥ (Willow)

䮭᪨ MIDI-

Vivat assembler et MENUETOS!
 㪮  MenuetOS 㣮   . ࠩ ᠭ  ࠭祭 㣠
㪮 .   ६ MeOS 뫠   ,  론.  ⮬
 ୠ⨢ - 㢠 VaStaNi ᠫ প PC ᯨ.  
ࠧ ᯮ   ६ ᪠  MS-DOS.  5  ᠫ
 ᪠ ணࠬ,  ᨫ,  ⮬ ந ப  
ᨭ⠪ QBasic.

 MeOS  ਡ⨢ Mario79 ⠥ ⥩ 㪮 奬  
ᯨ,     Menuet  蠫 -⠪  ᢮ ணࠬ -
MIDAMP   2004 .  孨᪨ 稭  ५ ந室 ⮫쪮 
ᥩ.

⠪, MIDAMP - ⥩訩  MIDI-ந뢠⥫.   ⥭  
,   宦  WinAmp. ,   㬥,   MIDI-䠩.
,   ॣ ஬    ।.  ⮣,
४⭮ 砭  ࠭஢   䠩  1 ४, 1 
㬥   । 孮᪮   :-(

#########
⥬ ॡ:
1.   ॠ樥 ᫥ ⥬ 㭪権:
       55/55 - 䥩 PC ᯨ (室!);
       67    - ᢮稢   ;
       66/3  -  ० 뤥 ४ .
2. SYSXTREE ᨨ   52 - ⨥ 䠩  ⠫ (室!)
3. ꥬ   ணࠬ -  150 .      
#########

  MIDAMP ᯮ ⢥  -  㬮砭
/HD/1/PLAYLIST.TXT. 騥   祭 ⠭ PLAYLIST_PATH  
䠩 MIDAMP.ASM.  -  ⥪⮢ 䠩,   ப ண
室  䠩  ந.    ࠢ  -
   ᫥饩 㧪  ਫ.

 ᪥ MIDAMP ᮧ  ⮪, 祩 ண  ᮡ⢥
窠.  ࠭     ⮪, ⮬  
প  砭  ६ ࠢ ⮬. ⮪ ⥭ᨢ 
 ᮡ १ IPC,   ᪫  ⮬,    砥 
⢮.  ࠡ⠥ .

MIDAMP 㬥 ᢮稢  ப  ⨥ ᮮ⢥饩 .
 ⠫ ᤥ  ᢮稢 १ mcall 18,10 (  Kolibri4),
 ⮫  ஡ ⠭  ⨥  PANEL. ,
㭪  ন  ⨯ II ?

稥  -    WinAmp:

Del - 㤠 뤥 ४;
z   - ।騩 ४;
x, Enter,  饫箪  䠩 - ந;
c, Space - 㧠;
v   - ⮯;
b   - ᫥騩 ४;

Esc -  ணࠬ;
m   - /몫 ;
PgUp, PgDn -  ⠬ 2 ᥤ ४ ( 祭!);
BackSpace - ६⪠ ४  砫;
Home/End - 㢥/㬥 ⮭쭮   ந   砫
    (⮡ࠦ 冷   'tone>').
    
 砥 䮭᪨ MIDI, ᫨ ᫥   砥, 
஡  㣮 ४ 'trk'   㬥 'chnl', 
ᮮ⢥⢥ '['  ']'  ⥬   ஬  0  9.  㤥
ந  ᠬ 砫.  ஦    祭  㬮砭 -
⨥ '\' .

祭   䥩:
Shuffle - 砩 冷 ந뢠 ४. Repeat  - ⥪騩 ४ 㤥
ந뢠 ᭮  ᭮. 箪   孥 㣫 뢮 
ଠ  ணࠬ   ⫠. 箪  ६ ⪥ 
ᯮᮡ  ⮡ࠦ -  砫    䠩.

箪      Shift  Ctrl ࠡ⠥ 筮 WinAmp.

砭 ⭮⥫쭮  :
'Add URL'  ॠ   稭;
'Add Dir' - 㪠  䠩   ⠫.  *.MID  *.KAR ⮣ 
     ⠫    ᯨ᮪;
'Misc'   ॠ;
'New List' 祣  .  ᯮ 䨪஢ .

  ப ।  䠩  ந    
䫠:

W -  㧨 䠩 ( 㬮砭);
P - ந 䠩;
H - ⮢ ᢥ  ,  ᫥ ந.

  㦭 ᤥ:

1.   ࠧ  (ᥩ 40 権).
2.    롮 ४ 䮭᪨      
     .
3.  ⥭ ⥪  ࠮-䠩.
4.  롮 .
5.   ।,   Ringtone Editor.
6.  ⪮஢  ( ᥣ, ).
7.  ࠢ , , ᮬ,  ;-)

ᮡ ୮:

   VaStaNi -    ᠭ MIDAMP    ᫠
   Standard MIDI Files 0.06        March 1, 1988
   MIDI 1.0 Specification
   General MIDI Level Spec
   MIDI SAMPLE DUMP STANDARD
   Standard MIDI File Format by Dustin Caldwell
   ଠ 䠩 MIDI
   The USENET MIDI Primer by Bob McQueer
   設   ॢ SYSXTREE (DLGS.INC - ࠡ⠭ 
      ⮬ ᯥ䨪 MIDAMP'a  opendialog ⥪ ASCL)

  ᮮ饭  訡 ࠢ  wil_low@hotbox.ru   
meos.sysbin.com.

  !

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
