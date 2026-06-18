---
argos_import: project_file
source_path: tmp/kolibrios/kernel/branches/kolibri_pe/drivers/sb16/README.TXT
source_abs: F:\debug\argoss\tmp\kolibrios\kernel\branches\kolibri_pe\drivers\sb16\README.TXT
source_ext: .txt
source_sha256: f1806020048f2dfc14da07dc6b947ffcdf11d85d5a1f33571613990135b209d5
text_sha256: 99611282c1d397bb451cc2158dc1e99a790e1a6f13cf4831bb6424ee26f44e62
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:41
---

# README.TXT

- Source: `tmp/kolibrios/kernel/branches/kolibri_pe/drivers/sb16/README.TXT`
- Extract: `text`
- SHA256: `f1806020048f2dfc14da07dc6b947ffcdf11d85d5a1f33571613990135b209d5`

## Content

Nable 21.05.2008.
This driver is my contribution (or donation) to KolibriOS. This is provided
AS IS in hope it'll be useful, but WITHOUT ANY WARRANTY! No responcibility
for any hardware damage or data loss. Use at your own risk!

;-------------------------------------------------------------------------------
;Changelog:
;-------------------------------------------------------------------------------
v0.2 - DEV_SET(GET)_MASTERVOL functions are unlocked and implemented.

v0.1 - first release.

;-------------------------------------------------------------------------------
;Tiny FAQ for sound driver by Nable for SB16 sound card.
;-------------------------------------------------------------------------------

;What is it?--------------------------------------------------------------------
  As you may know there is a sound subsystem ('INFINITY') in KolibriOS.
This subsystem includes mixer and separate interface for soundplayer
program and driver, so player application don't need to know what soundcard
is installed and how to cope with it, all work with card do the driver.
Before this time there were drivers only for AC97 integrated sound, but I
don't have such at home and if I would upgrade my computer with a newest
hardware, with 100% probability integrated sound will be HD Codec, nowadays
AC97 is not actual (2008 year is at calendar). But I'm not planning to upgrade
my computer so much now (and in next 5-6 years), writing the driver for my PCI
ESS Maestro1 card is difficult for me (may be some time later), so I decided
to write a driver for SB16. At first it is easy, there are many working
examples for DOS, there are heaps of good documentation and as an ISA device
SB16 can be programmed through I/O ports (about 5 ports are used), that is
more easy than PCI access. Now, enough lirics, lets go to physics :-)
  If you still don't understand what stuff is it, I'll tell this in brief:
with this driver you can play MP3 and WAV music (using AC97SND player) and
sounds (some games and DOSBOX can produce sound output through sound
subsystem) in KolibriOS.

;Yeah! I need sound in Kolibri and I have SB16 card. Whats then?----------------
  At first copy my SOUND.OBJ to /sys/drivers at your Kolibri system. Note,
that if you have AC97 card and it's driver started - then new driver won't
run until reboot. Then run BOARD and go to 'user' tab. Then try to run
AC97SND player. At BOARD you will see the following (if you had a proper
card):
|----------------------------|
|detecting hardware...	     | <- detector startup message
|DSP found at port 220h      | <- if you have a proper card, it'll be
|DSP version 4.13 - SB16     |	  autodetected. Numbers may be different.
|failed to attach IRQ5	     | <- don't mention. Old kernels reserve IRQ5
|owner's handler: 0x80D74284 |    see below how to fix it.
|----------------------------|
  At first, note that DSP version must be 4.xx or higher. Older cards are not
supported in this first release, maybe some time later. If nothing detected
but PNP/BIOS or some other OS detects your card - I'm sorry, it's perverted
PNP card like OPTi16, that is like HD Codec - until you init it through
PCI->ISA bridge (HD Codec of course through PCI->PCI bridge), map it, etc,
you can't use it in any way. I'd rather write a PCI device driver, than
for this extreme perversion. If your card detected and has a proper version
but you see 'failed to attach IRQ' - delete stroke 'mov [irq_owner+4*5],1' from the
file kernel.asm of your kernel source, save it, rebuild kernel, copy new
kernel to /sys/ (did you rename 'kernel' to 'kernel.mnt'? You should do it),
restart kernel (Ctrl+Alt+F12, Home). THE EASIER WAY IS TO USE A NEWER KERNEL,
since SVN802 it's fixed.
Now everything should be OK.

;It works for a part of the second and then stops, but system doesn't hang------
Go to 'config.inc' of my driver and change 'sb_irq_num' value from 5 to 7.
Then save, rebuild driver (compile 'sound.asm'), put 'sound' to /sys/drivers/
(you need to rename file 'sound' to 'sound.obj'), restart kernel and try again
to produce sound.

;-------------------------------------------------------------------------------
Ask your questions at KolibriOS forum: board.kolibrios.org
I'll try to answer you if possible.

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
