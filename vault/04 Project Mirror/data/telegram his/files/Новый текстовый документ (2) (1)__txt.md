---
argos_import: project_file
source_path: data/telegram his/files/Новый текстовый документ (2) (1).txt
source_abs: F:\debug\argoss\data\telegram his\files\Новый текстовый документ (2) (1).txt
source_ext: .txt
source_sha256: 5274652686031929423486c7f24b01ee468681d7d610ef0e848d927d713d323c
text_sha256: 6246e32502c04611162fe521d64e947b91818352c392b4e6ca4e344fc72b66cc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 13:16:46
---

# Новый текстовый документ (2) (1).txt

- Source: `data/telegram his/files/Новый текстовый документ (2) (1).txt`
- Extract: `text`
- SHA256: `5274652686031929423486c7f24b01ee468681d7d610ef0e848d927d713d323c`

## Content

return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


                # в”Ђв”Ђ РЈРїСЂР°РІР»РµРЅРёРµ РјС‹С€СЊСЋ Рё РєР»Р°РІРёР°С‚СѓСЂРѕР№ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РјС‹С€СЊ", "mouse", "РєСѓСЂСЃРѕСЂ"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            parts = text.strip().split()
            if len(parts) < 2:
                return ctrl.status()
            cmd = parts[1].lower()
            nums = []
            for p in parts[2:]:
                try: nums.append(int(p))
                except: pass
            if cmd in ("move", "РїРµСЂРµРјРµСЃС‚РёС‚СЊ", "РїРµСЂРµРјРµСЃС‚Рё"):
                return ctrl.move(nums[0], nums[1]) if len(nums) >= 2 else "вќ“ РјС‹С€СЊ move X Y"
            elif cmd in ("click", "РєР»РёРє", "РєР»РёРєРЅРё"):
                return ctrl.click(nums[0] if len(nums) > 0 else None,
                                   nums[1] if len(nums) > 1 else None)
            elif cmd in ("rclick", "РїСЂР°РІС‹Р№"):
                return ctrl.right_click(nums[0] if nums else None,
                                         nums[1] if len(nums)>1 else None)
            elif cmd in ("dclick", "РґРІРѕР№РЅРѕР№"):
                return ctrl.double_click(nums[0] if nums else None,
                                          nums[1] if len(nums)>1 else None)
            elif cmd in ("scroll", "РїСЂРѕРєСЂСѓС‚РєР°"):
                return ctrl.scroll(nums[0] if nums else 3)
            elif cmd in ("drag", "РїРµСЂРµС‚Р°С‰Рё"):
                return ctrl.drag(*nums[:4]) if len(nums) >= 4 else "вќ“ РјС‹С€СЊ drag X1 Y1 X2 Y2"
            elif cmd in ("РїРѕР·РёС†РёСЏ", "position", "pos"):
                return ctrl.position()
            return ctrl.status()

        if any(k in t for k in ["РєР»Р°РІРёС€Р°", "РЅР°Р¶РјРё", "hotkey", "keyboard"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            key = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.press(key) if key else "вќ“ РєР»Р°РІРёС€Р° ENTER / РєР»Р°РІРёС€Р° ctrl+c"

        if t.startswith("РїРµС‡Р°С‚Р°Р№ ") or t.startswith("РЅР°РїРµС‡Р°С‚Р°Р№ "):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            txt = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.type_text(txt) if txt else "вќ“ РїРµС‡Р°С‚Р°Р№ РўР•РљРЎРў"

        if t.startswith("Р±СѓС„РµСЂ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                txt = text.split(None, 1)[1].strip()
                return ctrl.write_clipboard(txt)

        if t.startswith("РјР°РєСЂРѕСЃ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                name = text.split(None, 1)[1].strip()
                return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


                # в”Ђв”Ђ РЈРїСЂР°РІР»РµРЅРёРµ РјС‹С€СЊСЋ Рё РєР»Р°РІРёР°С‚СѓСЂРѕР№ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РјС‹С€СЊ", "mouse", "РєСѓСЂСЃРѕСЂ"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            parts = text.strip().split()
            if len(parts) < 2:
                return ctrl.status()
            cmd = parts[1].lower()
            nums = []
            for p in parts[2:]:
                try: nums.append(int(p))
                except: pass
            if cmd in ("move", "РїРµСЂРµРјРµСЃС‚РёС‚СЊ", "РїРµСЂРµРјРµСЃС‚Рё"):
                return ctrl.move(nums[0], nums[1]) if len(nums) >= 2 else "вќ“ РјС‹С€СЊ move X Y"
            elif cmd in ("click", "РєР»РёРє", "РєР»РёРєРЅРё"):
                return ctrl.click(nums[0] if len(nums) > 0 else None,
                                   nums[1] if len(nums) > 1 else None)
            elif cmd in ("rclick", "РїСЂР°РІС‹Р№"):
                return ctrl.right_click(nums[0] if nums else None,
                                         nums[1] if len(nums)>1 else None)
            elif cmd in ("dclick", "РґРІРѕР№РЅРѕР№"):
                return ctrl.double_click(nums[0] if nums else None,
                                          nums[1] if len(nums)>1 else None)
            elif cmd in ("scroll", "РїСЂРѕРєСЂСѓС‚РєР°"):
                return ctrl.scroll(nums[0] if nums else 3)
            elif cmd in ("drag", "РїРµСЂРµС‚Р°С‰Рё"):
                return ctrl.drag(*nums[:4]) if len(nums) >= 4 else "вќ“ РјС‹С€СЊ drag X1 Y1 X2 Y2"
            elif cmd in ("РїРѕР·РёС†РёСЏ", "position", "pos"):
                return ctrl.position()
            return ctrl.status()

        if any(k in t for k in ["РєР»Р°РІРёС€Р°", "РЅР°Р¶РјРё", "hotkey", "keyboard"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            key = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.press(key) if key else "вќ“ РєР»Р°РІРёС€Р° ENTER / РєР»Р°РІРёС€Р° ctrl+c"

        if t.startswith("РїРµС‡Р°С‚Р°Р№ ") or t.startswith("РЅР°РїРµС‡Р°С‚Р°Р№ "):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            txt = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.type_text(txt) if txt else "вќ“ РїРµС‡Р°С‚Р°Р№ РўР•РљРЎРў"

        if t.startswith("Р±СѓС„РµСЂ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                txt = text.split(None, 1)[1].strip()
                return ctrl.write_clipboard(txt)

        if t.startswith("РјР°РєСЂРѕСЃ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                name = text.split(None, 1)[1].strip()
                return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


                # в”Ђв”Ђ РЈРїСЂР°РІР»РµРЅРёРµ РјС‹С€СЊСЋ Рё РєР»Р°РІРёР°С‚СѓСЂРѕР№ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РјС‹С€СЊ", "mouse", "РєСѓСЂСЃРѕСЂ"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            parts = text.strip().split()
            if len(parts) < 2:
                return ctrl.status()
            cmd = parts[1].lower()
            nums = []
            for p in parts[2:]:
                try: nums.append(int(p))
                except: pass
            if cmd in ("move", "РїРµСЂРµРјРµСЃС‚РёС‚СЊ", "РїРµСЂРµРјРµСЃС‚Рё"):
                return ctrl.move(nums[0], nums[1]) if len(nums) >= 2 else "вќ“ РјС‹С€СЊ move X Y"
            elif cmd in ("click", "РєР»РёРє", "РєР»РёРєРЅРё"):
                return ctrl.click(nums[0] if len(nums) > 0 else None,
                                   nums[1] if len(nums) > 1 else None)
            elif cmd in ("rclick", "РїСЂР°РІС‹Р№"):
                return ctrl.right_click(nums[0] if nums else None,
                                         nums[1] if len(nums)>1 else None)
            elif cmd in ("dclick", "РґРІРѕР№РЅРѕР№"):
                return ctrl.double_click(nums[0] if nums else None,
                                          nums[1] if len(nums)>1 else None)
            elif cmd in ("scroll", "РїСЂРѕРєСЂСѓС‚РєР°"):
                return ctrl.scroll(nums[0] if nums else 3)
            elif cmd in ("drag", "РїРµСЂРµС‚Р°С‰Рё"):
                return ctrl.drag(*nums[:4]) if len(nums) >= 4 else "вќ“ РјС‹С€СЊ drag X1 Y1 X2 Y2"
            elif cmd in ("РїРѕР·РёС†РёСЏ", "position", "pos"):
                return ctrl.position()
            return ctrl.status()

        if any(k in t for k in ["РєР»Р°РІРёС€Р°", "РЅР°Р¶РјРё", "hotkey", "keyboard"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            key = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.press(key) if key else "вќ“ РєР»Р°РІРёС€Р° ENTER / РєР»Р°РІРёС€Р° ctrl+c"

        if t.startswith("РїРµС‡Р°С‚Р°Р№ ") or t.startswith("РЅР°РїРµС‡Р°С‚Р°Р№ "):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            txt = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.type_text(txt) if txt else "вќ“ РїРµС‡Р°С‚Р°Р№ РўР•РљРЎРў"

        if t.startswith("Р±СѓС„РµСЂ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                txt = text.split(None, 1)[1].strip()
                return ctrl.write_clipboard(txt)

        if t.startswith("РјР°РєСЂРѕСЃ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                name = text.split(None, 1)[1].strip()
                return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


                # в”Ђв”Ђ РЈРїСЂР°РІР»РµРЅРёРµ РјС‹С€СЊСЋ Рё РєР»Р°РІРёР°С‚СѓСЂРѕР№ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РјС‹С€СЊ", "mouse", "РєСѓСЂСЃРѕСЂ"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            parts = text.strip().split()
            if len(parts) < 2:
                return ctrl.status()
            cmd = parts[1].lower()
            nums = []
            for p in parts[2:]:
                try: nums.append(int(p))
                except: pass
            if cmd in ("move", "РїРµСЂРµРјРµСЃС‚РёС‚СЊ", "РїРµСЂРµРјРµСЃС‚Рё"):
                return ctrl.move(nums[0], nums[1]) if len(nums) >= 2 else "вќ“ РјС‹С€СЊ move X Y"
            elif cmd in ("click", "РєР»РёРє", "РєР»РёРєРЅРё"):
                return ctrl.click(nums[0] if len(nums) > 0 else None,
                                   nums[1] if len(nums) > 1 else None)
            elif cmd in ("rclick", "РїСЂР°РІС‹Р№"):
                return ctrl.right_click(nums[0] if nums else None,
                                         nums[1] if len(nums)>1 else None)
            elif cmd in ("dclick", "РґРІРѕР№РЅРѕР№"):
                return ctrl.double_click(nums[0] if nums else None,
                                          nums[1] if len(nums)>1 else None)
            elif cmd in ("scroll", "РїСЂРѕРєСЂСѓС‚РєР°"):
                return ctrl.scroll(nums[0] if nums else 3)
            elif cmd in ("drag", "РїРµСЂРµС‚Р°С‰Рё"):
                return ctrl.drag(*nums[:4]) if len(nums) >= 4 else "вќ“ РјС‹С€СЊ drag X1 Y1 X2 Y2"
            elif cmd in ("РїРѕР·РёС†РёСЏ", "position", "pos"):
                return ctrl.position()
            return ctrl.status()

        if any(k in t for k in ["РєР»Р°РІРёС€Р°", "РЅР°Р¶РјРё", "hotkey", "keyboard"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            key = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.press(key) if key else "вќ“ РєР»Р°РІРёС€Р° ENTER / РєР»Р°РІРёС€Р° ctrl+c"

        if t.startswith("РїРµС‡Р°С‚Р°Р№ ") or t.startswith("РЅР°РїРµС‡Р°С‚Р°Р№ "):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            txt = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.type_text(txt) if txt else "вќ“ РїРµС‡Р°С‚Р°Р№ РўР•РљРЎРў"

        if t.startswith("Р±СѓС„РµСЂ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                txt = text.split(None, 1)[1].strip()
                return ctrl.write_clipboard(txt)

        if t.startswith("РјР°РєСЂРѕСЃ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                name = text.split(None, 1)[1].strip()
                return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


                # в”Ђв”Ђ РЈРїСЂР°РІР»РµРЅРёРµ РјС‹С€СЊСЋ Рё РєР»Р°РІРёР°С‚СѓСЂРѕР№ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РјС‹С€СЊ", "mouse", "РєСѓСЂСЃРѕСЂ"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            parts = text.strip().split()
            if len(parts) < 2:
                return ctrl.status()
            cmd = parts[1].lower()
            nums = []
            for p in parts[2:]:
                try: nums.append(int(p))
                except: pass
            if cmd in ("move", "РїРµСЂРµРјРµСЃС‚РёС‚СЊ", "РїРµСЂРµРјРµСЃС‚Рё"):
                return ctrl.move(nums[0], nums[1]) if len(nums) >= 2 else "вќ“ РјС‹С€СЊ move X Y"
            elif cmd in ("click", "РєР»РёРє", "РєР»РёРєРЅРё"):
                return ctrl.click(nums[0] if len(nums) > 0 else None,
                                   nums[1] if len(nums) > 1 else None)
            elif cmd in ("rclick", "РїСЂР°РІС‹Р№"):
                return ctrl.right_click(nums[0] if nums else None,
                                         nums[1] if len(nums)>1 else None)
            elif cmd in ("dclick", "РґРІРѕР№РЅРѕР№"):
                return ctrl.double_click(nums[0] if nums else None,
                                          nums[1] if len(nums)>1 else None)
            elif cmd in ("scroll", "РїСЂРѕРєСЂСѓС‚РєР°"):
                return ctrl.scroll(nums[0] if nums else 3)
            elif cmd in ("drag", "РїРµСЂРµС‚Р°С‰Рё"):
                return ctrl.drag(*nums[:4]) if len(nums) >= 4 else "вќ“ РјС‹С€СЊ drag X1 Y1 X2 Y2"
            elif cmd in ("РїРѕР·РёС†РёСЏ", "position", "pos"):
                return ctrl.position()
            return ctrl.status()

        if any(k in t for k in ["РєР»Р°РІРёС€Р°", "РЅР°Р¶РјРё", "hotkey", "keyboard"]):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            key = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.press(key) if key else "вќ“ РєР»Р°РІРёС€Р° ENTER / РєР»Р°РІРёС€Р° ctrl+c"

        if t.startswith("РїРµС‡Р°С‚Р°Р№ ") or t.startswith("РЅР°РїРµС‡Р°С‚Р°Р№ "):
            ctrl = getattr(self, "input_ctrl", None)
            if not ctrl:
                return "вќЊ input_control РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"
            txt = text.split(None, 1)[1].strip() if len(text.split()) > 1 else ""
            return ctrl.type_text(txt) if txt else "вќ“ РїРµС‡Р°С‚Р°Р№ РўР•РљРЎРў"

        if t.startswith("Р±СѓС„РµСЂ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                txt = text.split(None, 1)[1].strip()
                return ctrl.write_clipboard(txt)

        if t.startswith("РјР°РєСЂРѕСЃ "):
            ctrl = getattr(self, "input_ctrl", None)
            if ctrl:
                name = text.split(None, 1)[1].strip()
                return ctrl.run_macro(name)

        if t in ("СЃРєСЂРёРЅС€РѕС‚", "screenshot"):
            ctrl = getattr(self, "input_ctrl", None)
            return ctrl.screenshot() if ctrl else "вќЊ input_control РЅРµРґРѕСЃС‚СѓРїРµРЅ"


        if any(k in t for k in ["РєРѕРЅСЃРѕР»СЊ", "С‚РµСЂРјРёРЅР°Р»"]):
            if not self.context.allow_root:
                return "в›” РљРѕРјР°РЅРґС‹ С‚РµСЂРјРёРЅР°Р»Р° РѕРіСЂР°РЅРёС‡РµРЅС‹ С‚РµРєСѓС‰РёРј РєРІР°РЅС‚РѕРІС‹Рј РїСЂРѕС„РёР»РµРј (Р±РµР· root-РґРѕРїСѓСЃРєР°)."
            cmd = text.split("РєРѕРЅСЃРѕР»СЊ",1)[-1].strip() if "РєРѕРЅСЃРѕР»СЊ" in t else text.split("С‚РµСЂРјРёРЅР°Р»",1)[-1].strip()
            if self.constitution_hooks:
                guard = self.constitution_hooks.guard_shell(cmd)
                if not guard.ok:
                    return f"в›” {guard.message}"
            return admin.run_cmd(cmd, user="argos")

        # в”Ђв”Ђ Vision в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if self.vision:
            if any(k in t for k in ["РїРѕСЃРјРѕС‚СЂРё РЅР° СЌРєСЂР°РЅ", "С‡С‚Рѕ РЅР° СЌРєСЂР°РЅРµ", "СЃРєСЂРёРЅС€РѕС‚"]):
                question = text.replace("Р°СЂРіРѕСЃ","").replace("РїРѕСЃРјРѕС‚СЂРё РЅР° СЌРєСЂР°РЅ","").replace("С‡С‚Рѕ РЅР° СЌРєСЂР°РЅРµ","").replace("СЃРєСЂРёРЅС€РѕС‚","").strip()
                return self.vision.look_at_screen(question or "Р§С‚Рѕ РїСЂРѕРёСЃС…РѕРґРёС‚ РЅР° СЌРєСЂР°РЅРµ?")
            if any(k in t for k in ["РїРѕСЃРјРѕС‚СЂРё РІ РєР°РјРµСЂСѓ", "С‡С‚Рѕ РІРёРґРёС‚ РєР°РјРµСЂР°", "РІРєР»СЋС‡Рё РєР°РјРµСЂСѓ"]):
                question = text.replace("Р°СЂРіРѕСЃ","").replace("РїРѕСЃРјРѕС‚СЂРё РІ РєР°РјРµСЂСѓ","").replace("С‡С‚Рѕ РІРёРґРёС‚ РєР°РјРµСЂР°","").strip()
                return self.vision.look_through_camera(question or "Р§С‚Рѕ С‚С‹ РІРёРґРёС€СЊ?")
            if "РїСЂРѕР°РЅР°Р»РёР·РёСЂСѓР№ РёР·РѕР±СЂР°Р¶РµРЅРёРµ" in t or "Р°РЅР°Р»РёР· С„РѕС‚Рѕ" in t:
                path = text.split()[-1]
                return self.vision.analyze_file(path)

        # в”Ђв”Ђ РђРіРµРЅС‚ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if "РѕС‚С‡С‘С‚ Р°РіРµРЅС‚Р°" in t or "РїРѕСЃР»РµРґРЅРёР№ РїР»Р°РЅ" in t:
            return self.agent.last_report()
        if "РѕСЃС‚Р°РЅРѕРІРё Р°РіРµРЅС‚Р°" in t:
            self._agent_enabled = False
            return self.agent.stop() if self.agent else "РђРіРµРЅС‚ РѕСЃС‚Р°РЅРѕРІР»РµРЅ"

        # в”Ђв”Ђ РљРѕРЅС‚РµРєСЃС‚ РґРёР°Р»РѕРіР° в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["СЃР±СЂРѕСЃ РєРѕРЅС‚РµРєСЃС‚Р°", "Р·Р°Р±СѓРґСЊ СЂР°Р·РіРѕРІРѕСЂ", "РЅРѕРІС‹Р№ РґРёР°Р»РѕРі"]):
            return self.context.clear()
        if "РєРѕРЅС‚РµРєСЃС‚ РґРёР°Р»РѕРіР°" in t:
            return self.context.summary()

        # в”Ђв”Ђ Р РµРїР»РёРєР°С†РёСЏ + IoT в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in [
            "СЃРѕР·РґР°Р№ РѕР±СЂР°Р·", "СЃРѕР·РґР°Р№ os РѕР±СЂР°Р·", "РєР»РѕРЅРёСЂСѓР№ СЃРµР±СЏ",
            "РѕР±СЂР°Р· argos", "argos os РѕР±СЂР°Р·", "argos os РєР»РѕРЅ",
            "СЃРѕР·РґР°Р№ РєР»РѕРЅ os", "СЃРѕР·РґР°Р№ РєР»РѕРЅ СЃРµР±СЏ",
        ]):
            return self.replicator.create_os_image()

        # в”Ђв”Ђ РђРґР°РїС‚РёРІРЅС‹Р№ СЃР±РѕСЂС‰РёРє РїРѕРґ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in [
            "СЃРѕР·РґР°Р№ РѕР±СЂР°Р· РґР»СЏ СѓСЃС‚СЂРѕР№СЃС‚РІР°", "СЃРѕР·РґР°Р№ РѕР±СЂР°Р· РїРѕРґ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ",
            "Р°РґР°РїС‚РёРІРЅС‹Р№ РѕР±СЂР°Р·", "РѕР±СЂР°Р· РїРѕРґ СЌС‚Рѕ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ",
            "СЃРѕР±РµСЂРё РѕР±СЂР°Р· РґР»СЏ СЌС‚РѕРіРѕ СѓСЃС‚СЂРѕР№СЃС‚РІР°",
        ]):
            try:
                from src.device_scanner import AdaptiveImageBuilder
                return AdaptiveImageBuilder().build_for_this_device()
            except Exception as e:
                return f"вќЊ AdaptiveImageBuilder: {e}"

        if any(k in t for k in [
            "СЃРєР°РЅ СѓСЃС‚СЂРѕР№СЃС‚РІР°", "СЃРєР°РЅРёСЂРѕРІР°С‚СЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ",
            "РїСЂРѕС„РёР»СЊ СѓСЃС‚СЂРѕР№СЃС‚РІР°", "device scan", "device profile",
            "РїСЂРѕРІРµСЂСЊ Р¶РµР»РµР·Рѕ", "РєР°РєРѕРµ Р¶РµР»РµР·Рѕ", "Р¶РµР»РµР·Рѕ РёРЅС„Рѕ",
            "Р¶РµР»РµР·Рѕ РёРЅС„РѕСЂРјР°С†РёСЏ", "Р°РїРїР°СЂР°С‚РЅРѕРµ РѕР±РµСЃРїРµС‡РµРЅРёРµ",
            "С…Р°СЂР°РєС‚РµСЂРёСЃС‚РёРєРё СѓСЃС‚СЂРѕР№СЃС‚РІР°", "РёРЅС„Рѕ РѕР± СѓСЃС‚СЂРѕР№СЃС‚РІРµ",
            "РґРёР°РіРЅРѕСЃС‚РёРєР° Р¶РµР»РµР·Р°", "С…Р°СЂРґРІРµСЂ", "Р¶РµР»РµР·Рѕ СЃС‚Р°С‚СѓСЃ",
        ]):
            try:
                from src.device_scanner import DeviceScanner
                return DeviceScanner().report()
            except Exception as e:
                return f"вќЊ DeviceScanner: {e}"

        # в”Ђв”Ђ KolibriOS / РјСѓР»СЊС‚РёРїР»Р°С‚С„РѕСЂРјРµРЅРЅС‹Р№ РѕР±СЂР°Р· в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in [
            "РѕР±СЂР°Р· kolibri", "РѕР±СЂР°Р· РєРѕР»РёР±СЂРё РѕСЃ", "kolibrios РѕР±СЂР°Р·",
            "argos on kolibrios", "argos kolibri os", "СЃРѕР·РґР°Р№ РѕР±СЂР°Р· kolibri",
        ]):
            try:
                from src.kolibri_os_builder import build_kolibri_image
                return build_kolibri_image()
            except Exception as e:
                return f"вќЊ KolibriOS РѕР±СЂР°Р·: {e}"

        if any(k in t for k in [
            "РјСѓР»СЊС‚РёРїР»Р°С‚С„РѕСЂРјРµРЅРЅС‹Р№ РѕР±СЂР°Р·", "РѕР±СЂР°Р· РґР»СЏ РІСЃРµС… РїР»Р°С‚С„РѕСЂРј",
            "СЃРѕР·РґР°Р№ РѕР±СЂР°Р· РґР»СЏ РІСЃРµС…", "multiplatform image",
            "argos РґР»СЏ РІСЃРµС… РїР»Р°С‚С„РѕСЂРј", "СЃРѕР±РµСЂРё РІСЃРµ РѕР±СЂР°Р·С‹",
        ]):
            try:
                from src.kolibri_os_builder import build_multiplatform
                return build_multiplatform()
            except Exception as e:
                return f"вќЊ Multi-platform РѕР±СЂР°Р·: {e}"

        if any(k in t for k in [
            "kolibrios СЃС‚Р°С‚СѓСЃ", "СЃС‚Р°С‚СѓСЃ kolibri os", "СЃС‚Р°С‚СѓСЃ РѕР±СЂР°Р·РѕРІ",
            "РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё РѕР±СЂР°Р·РѕРІ", "СѓСЃС‚Р°РЅРѕРІС‰РёРє РѕР±СЂР°Р·РѕРІ СЃС‚Р°С‚СѓСЃ",
        ]):
            try:
                from src.kolibri_os_builder import kolibri_status
                return kolibri_status()
            except Exception as e:
                return f"вќЊ KolibriOS СЃС‚Р°С‚СѓСЃ: {e}"

        if "СЃРѕР·РґР°Р№ РѕР±СЂР°Р· РґР»СЏ" in t:
            try:
                target = t.replace("СЃРѕР·РґР°Р№ РѕР±СЂР°Р· РґР»СЏ", "").strip().split()[0]
                # РџР»Р°С‚С„РѕСЂРјС‹ РјСѓР»СЊС‚РёСѓСЃС‚Р°РЅРѕРІС‰РёРєР°
                _mp_targets = {"pc", "android", "mac", "РјР°Рє", "Р°РЅРґСЂРѕРёРґ",
                               "kolibri", "macos", "apk", "termux"}
                if any(k in target.lower() for k in _mp_targets):
                    from src.kolibri_os_builder import MultiPlatformInstaller
                    return MultiPlatformInstaller().build_for(target)
                from src.device_scanner import AdaptiveImageBuilder
                return AdaptiveImageBuilder().build_for_target(target)
            except Exception as e:
                return f"вќЊ {e}"

        if any(k in t for k in ["СЃРѕР·РґР°Р№ РєРѕРїРёСЋ", "СЂРµРїР»РёРєР°С†РёСЏ"]):
            if getattr(self, "awa", None) and getattr(self.awa, "lazarus", None):
                self.awa.lazarus.spread_to_nodes()
            return self.replicator.create_replica()
        if "СЃРєР°РЅРёСЂСѓР№ РїРѕСЂС‚С‹" in t:
            try:
                _fl = flasher
                if _fl is None:
                    from src.factory.flasher import AirFlasher
                    _fl = AirFlasher()
                return f"РџРѕСЂС‚С‹: {_fl.scan_ports()}"
            except Exception as e:
                return f"вќЊ scan_ports: {e}"
        if any(k in t for k in [
            "argos os РґР»СЏ android",
            "Р°СЂРіРѕСЃ РѕСЃ РґР»СЏ android",
            "argos os android",
            "Р°СЂРіРѕСЃ РѕСЃ android",
            "argos os РґР»СЏ С‚РµР»РµС„РѕРЅР°",
            "argos os РґР»СЏ РїР»Р°РЅС€РµС‚Р°",
            "argos os РґР»СЏ tv",
        ]):
            if hasattr(flasher, "android_argos_os_plan"):
                profile = "phone"
                if "РїР»Р°РЅС€РµС‚" in t or "tablet" in t:
                    profile = "tablet"
                elif "tv" in t or "С‚РµР»РµРІРёР·" in t:
                    profile = "tv"
                return flasher.android_argos_os_plan(profile=profile, preserve_features=True)
            return "вќЊ РњРѕРґСѓР»СЊ android_argos_os_plan РЅРµРґРѕСЃС‚СѓРїРµРЅ РІ С‚РµРєСѓС‰РµРј flasher."
        if any(k in t for k in [
            "РјРѕРґРёС„РёРєР°С†РёРё РїСЂРѕС€РёРІРѕРє РЅРѕСЃРёРјС‹С… СѓСЃС‚СЂРѕР№СЃС‚РІ Р°СЂРіРѕСЃ РѕСЃ",
            "РјРѕРґРёС„РёРєР°С†РёРё РїСЂРѕС€РёРІРѕРє РЅРѕСЃРёРјС‹С… СѓСЃС‚СЂРѕР№СЃС‚РІ argos os",
            "РјРѕРґРёС„РёРєР°С†РёСЏ РїСЂРѕС€РёРІРєРё РЅРѕСЃРёРјРѕРіРѕ",
            "РјРѕРґРёС„РёС†РёСЂСѓР№ РїСЂРѕС€РёРІРєСѓ РЅРѕСЃРёРјРѕРіРѕ",
        ]):
            if hasattr(flasher, "wearable_firmware_mod"):
                port_match = re.search(r"(/dev/\S+|\bCOM\d+\b)", text, flags=re.IGNORECASE)
                port = port_match.group(1) if port_match else ""
                include_4pda = "4pda" in t
                device = re.sub(
                    r"(?i)(РјРѕРґРёС„РёРєР°С†РёРё РїСЂРѕС€РёРІРѕРє РЅРѕСЃРёРјС‹С… СѓСЃС‚СЂРѕР№СЃС‚РІ Р°СЂРіРѕСЃ РѕСЃ|"
                    r"РјРѕРґРёС„РёРєР°С†РёРё РїСЂРѕС€РёРІРѕРє РЅРѕСЃРёРјС‹С… СѓСЃС‚СЂРѕР№СЃС‚РІ argos os|"
                    r"РјРѕРґРёС„РёРєР°С†РёСЏ РїСЂРѕС€РёРІРєРё РЅРѕСЃРёРјРѕРіРѕ|РјРѕРґРёС„РёС†РёСЂСѓР№ РїСЂРѕС€РёРІРєСѓ РЅРѕСЃРёРјРѕРіРѕ)",
                    "",
                    text,
                )
                device = re.sub(r"(?i)\b4pda\b", "", device)
                if port:
                    device = device.replace(port, "")
                device = " ".join(device.split()) or "argos os wearable"
                return flasher.wearable_firmware_mod(
                    device=device,
                    port=port,
                    avatar="sigtrip",
                    include_4pda=include_4pda,
                )
            return "вќЊ РњРѕРґСѓР»СЊ wearable_firmware_mod РЅРµРґРѕСЃС‚СѓРїРµРЅ РІ С‚РµРєСѓС‰РµРј flasher."
        if any(k in t for k in ["РЅР°Р№РґРё usb С‡РёРїС‹", "usb С‡РёРїС‹", "СЃРјР°СЂС‚ РїСЂРѕС€РёРІРєР° usb", "smart flasher usb"]):
            if hasattr(flasher, "detect_usb_chips_report"):
                return flasher.detect_usb_chips_report()
            return "вќЊ Smart Flasher РЅРµРґРѕСЃС‚СѓРїРµРЅ РІ С‚РµРєСѓС‰РµРј flasher-РјРѕРґСѓР»Рµ."
        if any(k in t for k in ["СѓРјРЅР°СЏ РїСЂРѕС€РёРІРєР°", "smart flash", "СЃРјР°СЂС‚ РїСЂРѕС€РёРІРєР°"]):
            if hasattr(flasher, "smart_flash"):
                parts = text.split()
                port = None
                for p in parts:
                    if p.startswith("/dev/") or p.upper().startswith("COM"):
                        port = p
                        break
                return flasher.smart_flash(port=port)

        # в”Ђв”Ђ ST-Link v2 / RP2350 / MicroPython в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["st-link", "stlink", "st link", "СЃС‚-Р»РёРЅРє"]):
            try:
                _fl = flasher
                if _fl is None:
                    from src.factory.flasher import AirFlasher
                    _fl = AirFlasher()
                if hasattr(_fl, "stlink_info"):
                    return _fl.stlink_info()
            except Exception as e:
                return f"вќЊ ST-Link: {e}"

        if any(k in t for k in ["РїСЂРѕС€РµР№ rp2350", "РїСЂРѕС€РёС‚СЊ rp2350", "РѕР±РЅРѕРІРё rp2350",
                                 "РїСЂРѕС€РµР№ rp2040", "РїСЂРѕС€РёС‚СЊ rp2040",
                                 "РїСЂРѕС€РµР№ pico",   "РїСЂРѕС€РёС‚СЊ pico",
                                 "РїСЂРѕС€РµР№ РіРµРµРє",   "РїСЂРѕС€РёС‚СЊ РіРµРµРє",
                                 "flash rp2350",  "flash rp2040", "flash pico",
                                 "rp2350 РїСЂРѕС€РёРІРєР°", "rp2040 РїСЂРѕС€РёРІРєР°"]):
            try:
                _fl = flasher
                if _fl is None:
                    from src.factory.flasher import AirFlasher
                    _fl = AirFlasher()
                import re as _re_fw
                fw_match = _re_fw.search(r'[\w/\\:.\-]+\.(uf2|py|bin)', text, _re_fw.IGNORECASE)
                fw_path = fw_match.group(0) if fw_match else "assets/firmware/argos_rp2350_geek.py"
                port_m = _re_fw.search(r'(/dev/tty\S+|COM\d+)', text, _re_fw.IGNORECASE)
                port_s = port_m.group(1) if port_m else ""
                chip = "rp2350" if "rp2350" in t else "rp2040"
                return _fl.flash_chip(port_s, chip, fw_path)
            except Exception as e:
                return f"вќЊ RP2350 flash: {e}"

        if any(k in t for k in ["РїРѕРґРєР»СЋС‡Рё rp2350", "РїРѕРґРєР»СЋС‡Рё rp2040", "РїРѕРґРєР»СЋС‡Рё pico", "РїРѕРґРєР»СЋС‡Рё РіРµРµРє"]):
            try:
                from src.skills.esp32_usb_bridge import handle as _esp_handle
                import re as _re_rp
                _pm = _re_rp.search(r'(/dev/tty\S+|COM\d+|ttyUSB\d+|ttyACM\d+)', text, _re_rp.IGNORECASE)
                _conn_text = text
                if _pm:
                    _conn_text = f"РїРѕРґРєР»СЋС‡Рё esp {_pm.group(1)}"
                else:
                    _conn_text = "РїРѕРґРєР»СЋС‡Рё esp"
                result = _esp_handle(_conn_text, core=self)
                return result if result else "вќЊ RP2350 USB РјРѕСЃС‚ РЅРµ РѕС‚РІРµС‚РёР»"
            except Exception as e:
                return f"вќЊ RP2350 РїРѕРґРєР»СЋС‡РµРЅРёРµ: {e}"

        if any(k in t for k in ["rp2350 СЃС‚Р°С‚СѓСЃ", "waveshare rp2350", "РіРµРµРє СЃС‚Р°С‚СѓСЃ", "rp2350 РіРµРµРє"]):
            return (
                "рџџў Waveshare RP2350-GEEK\n"
                "  Р”РёСЃРїР»РµР№: ST7789 1.14\" 135Г—240\n"
                "  РџСЂРѕС‚РѕРєРѕР»: USB CDC 115200 baud (JSON)\n"
                "  РџСЂРѕС€РёРІРєР°: assets/firmware/argos_rp2350_geek.py\n"
                "  РЈСЃС‚Р°РЅРѕРІРєР°: СЃРєРѕРїРёСЂСѓР№ РєР°Рє main.py С‡РµСЂРµР· Thonny РёР»Рё mpremote\n"
                "  РљРѕРјР°РЅРґС‹: РїСЂРѕС€РµР№ rp2350 | РїРѕРґРєР»СЋС‡Рё rp2350 | stlink СЃС‚Р°С‚СѓСЃ"
            )

        # в”Ђв”Ђ STM32H503 / PB_MCU01_H503A в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РїСЂРѕС€РµР№ stm32h503", "РїСЂРѕС€РёС‚СЊ stm32h503", "РѕР±РЅРѕРІРё stm32",
                                 "РїСЂРѕС€РµР№ h503",      "РїСЂРѕС€РёС‚СЊ h503",
                                 "РїСЂРѕС€РµР№ pb mcu",    "РїСЂРѕС€РёС‚СЊ pb mcu",
                                 "flash stm32h503",  "flash h503",
                                 "h503 РїСЂРѕС€РёРІРєР°",    "pb_mcu01 РїСЂРѕС€РёРІРєР°", "stm32h503 РїСЂРѕС€РёРІРєР°"]):
            try:
                _fl = flasher
                if _fl is None:
                    from src.factory.flasher import AirFlasher
                    _fl = AirFlasher()
                import re as _re_fw
                fw_match = _re_fw.search(r'[\w/\\:.\-]+\.(bin|hex|c)', text, _re_fw.IGNORECASE)
                fw_path  = fw_match.group(0) if fw_match else \
                           "assets/firmware/argos_pb_mcu01_h503a.c"
                port_m   = _re_fw.search(r'(/dev/tty\S+|COM\d+|\(dfu\))', text, _re_fw.IGNORECASE)
                port_s   = port_m.group(1) if port_m else ""
                return _fl.flash_chip(port_s, "stm32h503", fw_path)
            except Exception as e:
                return f"вќЊ STM32H503 flash: {e}"

        if any(k in t for k in ["stm32h503 СЃС‚Р°С‚СѓСЃ", "pb_mcu01 СЃС‚Р°С‚СѓСЃ", "pb mcu01 СЃС‚Р°С‚СѓСЃ",
                                 "h503a СЃС‚Р°С‚СѓСЃ", "stm32h503"]):
            try:
                _fl = flasher
                if _fl is None:
                    from src.factory.flasher import AirFlasher
                    _fl = AirFlasher()
                if hasattr(_fl, "stm32h503_info"):
                    return _fl.stm32h503_info()
            except Exception as e:
                return f"вќЊ STM32H503 info: {e}"
            return (
                "рџ”· PB_MCU01_H503A вЂ” STM32H503CBT6\n"
                "  ARM Cortex-M33 @ 250 MHz | 128KB Flash | 32KB RAM\n"
                "  РџСЂРѕС‚РѕРєРѕР»: USB CDC (VID:0483 PID:5740) 115200 baud JSON\n"
                "  РџСЂРѕС€РёРІРєР°: assets/firmware/argos_pb_mcu01_h503a.c\n"
                "  РЎР±РѕСЂРєР°: STM32CubeIDE в†’ .bin в†’ РїСЂРѕС€РµР№ stm32h503\n"
                "  РљРѕРјР°РЅРґС‹: РїСЂРѕС€РµР№ stm32h503 | РїРѕРґРєР»СЋС‡Рё stm32 | stlink СЃС‚Р°С‚СѓСЃ"
            )

        if any(k in t for k in ["РїРѕРґРєР»СЋС‡Рё stm32", "stm32 РјРѕСЃС‚", "stm32 СЃС‚Р°СЂС‚", "h503 РјРѕСЃС‚"]):
            if self.esp32_bridge:
                # РџСЂРёРЅСѓРґРёС‚РµР»СЊРЅРѕ РІС‹Р±РёСЂР°РµРј STM32 С‚РёРї
                self.esp32_bridge._device_type = "stm32h503"
                return self.esp32_bridge.start()
            return "вќЊ USB РјРѕСЃС‚ РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"

        # в”Ђв”Ђ OTG (USB Host) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["otg СЃС‚Р°С‚СѓСЃ", "otg status", "РѕС‚Рі СЃС‚Р°С‚СѓСЃ"]):
            return self.otg.status() if self.otg else "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["otg СЃРєР°РЅ", "otg scan", "otg СѓСЃС‚СЂРѕР№СЃС‚РІР°", "РѕС‚Рі СЃРєР°РЅ"]):
            return self.otg.scan_report() if self.otg else "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["otg РїРѕРґРєР»СЋС‡Рё", "otg connect", "РѕС‚Рі РїРѕРґРєР»СЋС‡Рё"]):
            if self.otg:
                parts = text.split()
                idx = next((i for i, p in enumerate(parts)
                            if p.lower() in ("РїРѕРґРєР»СЋС‡Рё", "connect", "РїРѕРґРєР»СЋС‡Рё")), -1)
                device_id = parts[idx + 1] if idx >= 0 and idx + 1 < len(parts) else ""
                baud = 115200
                for p in parts:
                    if p.isdigit() and int(p) in (9600, 19200, 38400, 57600, 115200, 230400, 460800):
                        baud = int(p)
                return self.otg.connect_serial(device_id, baud) if device_id else "вќЊ OTG: СѓРєР°Р¶Рё ID РёР»Рё РїРѕСЂС‚ СѓСЃС‚СЂРѕР№СЃС‚РІР°."
            return "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["otg РѕС‚РїСЂР°РІСЊ", "otg send", "РѕС‚Рі РѕС‚РїСЂР°РІСЊ"]):
            if self.otg:
                parts = text.split(maxsplit=3)
                if len(parts) >= 3:
                    device_id = parts[2]
                    data = parts[3] if len(parts) > 3 else ""
                    return self.otg.send_data(device_id, data)
            return "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["otg РѕС‚РєР»СЋС‡Рё", "otg disconnect", "РѕС‚Рі РѕС‚РєР»СЋС‡Рё"]):
            if self.otg:
                parts = text.split()
                device_id = parts[-1] if len(parts) > 1 else ""
                return self.otg.disconnect(device_id) if device_id else "вќЊ OTG: СѓРєР°Р¶Рё ID СѓСЃС‚СЂРѕР№СЃС‚РІР°."
            return "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["otg РјРѕРЅРёС‚РѕСЂРёРЅРі", "otg monitor", "РѕС‚Рі РјРѕРЅРёС‚РѕСЂРёРЅРі"]):
            return self.otg.start_monitor() if self.otg else "вќЊ OTG Manager РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["rs ttl", "uart ttl", "ttl uart", "rs-ttl", "uart-ttl", "ttl-uart"]):
            return self._rs_ttl_help()
        if any(k in t for k in [
            "РїСЂРѕРІРµСЂСЊ РґСЂР°Р№РІРµСЂС‹", "РґСЂР°Р№РІРµСЂС‹ android", "РґСЂР°Р№РІРµСЂС‹ gui",
            "РЅРёР·РєРѕСѓСЂРѕРІРЅРµРІС‹Рµ РґСЂР°Р№РІРµСЂС‹", "driver check",
        ]):
            return self._low_level_drivers_report()

        # в”Ђв”Ђ Р“РћРЎРў РљСЂРёРїС‚РѕРіСЂР°С„РёСЏ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РіРѕСЃС‚ СЃС‚Р°С‚СѓСЃ", "gost СЃС‚Р°С‚СѓСЃ", "РіРѕСЃС‚ РёРЅС„Рѕ"]):
            try:
                from src.security.gost_cipher import gost_status
                return gost_status()
            except Exception as e:
                return f"вќЊ Р“РћРЎРў: {e}"
        if any(k in t for k in ["РіРѕСЃС‚ С…РµС€", "gost hash", "СЃС‚СЂРёР±РѕРі"]):
            payload = text.split(maxsplit=2)[-1] if len(text.split()) > 2 else ""
            if not payload:
                return "вќЊ Р“РћРЎРў С…РµС€: СѓРєР°Р¶Рё С‚РµРєСЃС‚. РџСЂРёРјРµСЂ: РіРѕСЃС‚ С…РµС€ РїСЂРёРІРµС‚"
            try:
                from src.security.gost_cipher import gost_hash
                h = gost_hash(payload, bits=256).hex()
                return f"рџ”ђ РЎС‚СЂРёР±РѕРі-256:\n   {payload!r}\n   в†’ {h}"
            except Exception as e:
                return f"вќЊ Р“РћРЎРў С…РµС€: {e}"
        if any(k in t for k in ["РіРѕСЃС‚ p2p СЃС‚Р°С‚СѓСЃ", "gost p2p"]):
            try:
                from src.connectivity.gost_p2p import get_gost_p2p
                return get_gost_p2p().status()
            except Exception as e:
                return f"вќЊ Р“РћРЎРў P2P: {e}"

        # в”Ђв”Ђ Grist P2P РҐСЂР°РЅРёР»РёС‰Рµ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["grist СЃС‚Р°С‚СѓСЃ", "РіСЂРёСЃС‚ СЃС‚Р°С‚СѓСЃ", "grist status"]):
            return self.grist.status() if self.grist else "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist С‚Р°Р±Р»РёС†С‹", "grist tables"]):
            return self.grist.list_tables() if self.grist else "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist СЃРїРёСЃРѕРє", "grist list", "grist РєР»СЋС‡Рё"]):
            return self.grist.list_keys() if self.grist else "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist РЅРѕРґС‹", "grist nodes", "grist p2p"]):
            return self.grist.get_nodes() if self.grist else "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist СЃРёРЅРє", "grist sync", "grist СЃРёРЅС…СЂРѕРЅРёР·Р°С†РёСЏ"]):
            if self.grist:
                return self.grist.sync_node()
            return "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist СЃРѕС…СЂР°РЅРё", "grist save", "grist Р·Р°РїРёС€Рё"]):
            if self.grist:
                # Р¤РѕСЂРјР°С‚: "grist СЃРѕС…СЂР°РЅРё <РєР»СЋС‡> <Р·РЅР°С‡РµРЅРёРµ>"
                # parts[0]=grist, parts[1]=СЃРѕС…СЂР°РЅРё, parts[2]=РєР»СЋС‡, parts[3]=Р·РЅР°С‡РµРЅРёРµ
                parts = text.split(maxsplit=3)
                key   = parts[2] if len(parts) > 2 else ""
                val   = parts[3] if len(parts) > 3 else ""
                if not key:
                    return "вќЊ Grist СЃРѕС…СЂР°РЅРё: СѓРєР°Р¶Рё РєР»СЋС‡ Рё Р·РЅР°С‡РµРЅРёРµ.\n   РџСЂРёРјРµСЂ: grist СЃРѕС…СЂР°РЅРё РјРѕСЏ_РїРµСЂРµРјРµРЅРЅР°СЏ Р·РЅР°С‡РµРЅРёРµ"
                return self.grist.save(key, val)
            return "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."
        if any(k in t for k in ["grist РїРѕР»СѓС‡Рё", "grist get", "grist С‡РёС‚Р°Р№"]):
            if self.grist:
                # Р¤РѕСЂРјР°С‚: "grist РїРѕР»СѓС‡Рё <РєР»СЋС‡>"
                # parts[0]=grist, parts[1]=РїРѕР»СѓС‡Рё, parts[2]=РєР»СЋС‡
                parts = text.split(maxsplit=2)
                key   = parts[2] if len(parts) > 2 else ""
                if not key:
                    return "вќЊ Grist РїРѕР»СѓС‡Рё: СѓРєР°Р¶Рё РєР»СЋС‡. РџСЂРёРјРµСЂ: grist РїРѕР»СѓС‡Рё РјРѕСЏ_РїРµСЂРµРјРµРЅРЅР°СЏ"
                return self.grist.get(key)
            return "вќЊ Grist РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ."

        # в”Ђв”Ђ Р“РѕР»РѕСЃ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in [
            "РїСЂРѕРІРµСЂСЊ СЂР°Р±РѕС‚Сѓ РіРѕР»РѕСЃРѕРІС‹С… СЃР»СѓР¶Р±",
            "РїСЂРѕРІРµСЂСЊ РіРѕР»РѕСЃРѕРІС‹Рµ СЃР»СѓР¶Р±С‹",
            "СЃС‚Р°С‚СѓСЃ РіРѕР»РѕСЃРѕРІС‹С… СЃР»СѓР¶Р±",
            "РіРѕР»РѕСЃРѕРІС‹С… СЃР»СѓР¶Р± РІРІРѕРґР° Рё РІС‹РІРѕРґР°",
            "РіРѕР»РѕСЃРѕРІС‹С… СЃР»СѓР¶Р± РІРѕРґР° Рё РІС‹РІРѕРґР°",
            "voice services check",
        ]):
            return self.voice_services_report()
        if any(k in t for k in ["РіРѕР»РѕСЃ РІРєР»", "РІРєР»СЋС‡Рё РіРѕР»РѕСЃ"]):
            self.voice_on = True; return "рџ”Љ Р“РѕР»РѕСЃРѕРІРѕР№ РјРѕРґСѓР»СЊ Р°РєС‚РёРІРёСЂРѕРІР°РЅ."
        if any(k in t for k in ["РіРѕР»РѕСЃ РІС‹РєР»", "РІС‹РєР»СЋС‡Рё РіРѕР»РѕСЃ"]):
            self.voice_on = False; return "рџ”‡ Р“РѕР»РѕСЃРѕРІРѕР№ РјРѕРґСѓР»СЊ РѕС‚РєР»СЋС‡С‘РЅ."
        if any(k in t for k in ["СЂРµР¶РёРј РёРё Р°РІС‚Рѕ", "РјРѕРґРµР»СЊ Р°РІС‚Рѕ", "ai mode auto"]):
            return self.set_ai_mode("auto")
        if any(k in t for k in ["СЂРµР¶РёРј РёРё gemini", "РјРѕРґРµР»СЊ gemini", "ai mode gemini"]):
            return self.set_ai_mode("gemini")
        if any(k in t for k in [
            "СЂРµР¶РёРј РёРё gigachat", "РјРѕРґРµР»СЊ gigachat", "ai mode gigachat", "СЂРµР¶РёРј РёРё РіРёРіР°С‡Р°С‚",
            "РіРёРіР°С‡Р°С‚", "gigachat",
        ]):
            return self.set_ai_mode("gigachat")
        if any(k in t for k in ["СЂРµР¶РёРј РёРё yandexgpt", "РјРѕРґРµР»СЊ yandexgpt", "ai mode yandexgpt", "СЂРµР¶РёРј РёРё СЏРЅРґРµРєСЃ"]):
            return self.set_ai_mode("yandexgpt")
        if any(k in t for k in ["СЂРµР¶РёРј РёРё kimi", "РјРѕРґРµР»СЊ kimi", "ai mode kimi", "СЂРµР¶РёРј РёРё РєРёРјРё", "РјРѕРґРµР»СЊ РєРёРјРё"]):
            return self.set_ai_mode("kimi")
        if any(k in t for k in ["СЂРµР¶РёРј РёРё kimi СЃ РёРЅСЃС‚СЂСѓРјРµРЅС‚Р°РјРё", "kimi tools", "kimi СЃ РЅР°РІС‹РєР°РјРё"]):
            self._kimi_tools_enabled = True
            return self.set_ai_mode("kimi") + " (СЃ РёРЅСЃС‚СЂСѓРјРµРЅС‚Р°РјРё вњ…)"
        if any(k in t for k in ["РІС‹РєР»СЋС‡Рё РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹ kimi", "kimi Р±РµР· РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ"]):
            self._kimi_tools_enabled = False
            return "рџ”§ РРЅСЃС‚СЂСѓРјРµРЅС‚С‹ Kimi РѕС‚РєР»СЋС‡РµРЅС‹"
        if any(k in t for k in ["СЂРµР¶РёРј РёРё ollama", "РјРѕРґРµР»СЊ ollama", "ai mode ollama"]):
            return self.set_ai_mode("ollama")
        if any(k in t for k in ["С‚РµРєСѓС‰РёР№ СЂРµР¶РёРј РёРё", "РєР°РєР°СЏ РјРѕРґРµР»СЊ", "ai mode"]):
            return f"рџ¤– РўРµРєСѓС‰РёР№ СЂРµР¶РёРј РР: {self.ai_mode_label()}"
        if any(k in t for k in ["РІРєР»СЋС‡Рё wake word", "wake word РІРєР»"]):
            return self.start_wake_word(admin, flasher)

        # в”Ђв”Ђ РќР°РІС‹РєРё в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        # в”Ђв”Ђ Р”РёР°РіРЅРѕСЃС‚РёРєР° РЅР°РІС‹РєРѕРІ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РґРёР°РіРЅРѕСЃС‚РёРєР° РЅР°РІС‹РєРѕРІ", "РїСЂРѕРІРµСЂСЊ РЅР°РІС‹РєРё", "РЅР°РІС‹РєРё СЃС‚Р°С‚СѓСЃ"]):
            return self._skills_diagnostic()

        # в”Ђв”Ђ Р”РёРЅР°РјРёС‡РµСЃРєРёР№ Р·Р°РїСѓСЃРє РЅР°РІС‹РєР° в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if t.startswith("Р·Р°РїСѓСЃС‚Рё РЅР°РІС‹Рє ") or t.startswith("skill run "):
            skill_name = text.replace("Р·Р°РїСѓСЃС‚Рё РЅР°РІС‹Рє", "").replace("skill run", "").strip()
            if not skill_name:
                return "Р¤РѕСЂРјР°С‚: Р·Р°РїСѓСЃС‚Рё РЅР°РІС‹Рє [РёРјСЏ]"
            # РС‰РµРј РЅР°РІС‹Рє
            from pathlib import Path as _P
            import os as _dos
            for base in ["src/skills", "skills"]:
                for candidate in [
                    _P(_dos.path.join(base, skill_name, "__init__.py")),
                    _P(_dos.path.join(base, skill_name + ".py")),
                ]:
                    if candidate.exists():
                        try:
                            import importlib.util as _ilu
                            _spec = _ilu.spec_from_file_location(f"dyn_{skill_name}", str(candidate))
                            _mod  = _ilu.module_from_spec(_spec)
                            _spec.loader.exec_module(_mod)
                            # РС‰РµРј С‚РѕС‡РєСѓ РІС…РѕРґР°
                            for entry in ["handle", "execute", "run", "main"]:
                                fn = getattr(_mod, entry, None)
                                if callable(fn):
                                    result = fn(text) if entry == "handle" else fn()
                                    return f"вњ… РќР°РІС‹Рє {skill_name} Р·Р°РїСѓС‰РµРЅ:\n{result}"
                            # РС‰РµРј РєР»Р°СЃСЃ СЃ РјРµС‚РѕРґРѕРј run/execute/report
                            for k in dir(_mod):
                                if k[0].isupper():
                                    cls = getattr(_mod, k)
                                    for m in ["run", "execute", "report", "scan"]:
                                        if hasattr(cls, m):
                                            return f"вњ… {k}.{m}():\n{getattr(cls(), m)()}"
                            return f"вњ… РќР°РІС‹Рє {skill_name} Р·Р°РіСЂСѓР¶РµРЅ (РЅРµС‚ handle/execute)"
                        except Exception as e:
                            return f"вќЊ РќР°РІС‹Рє {skill_name}: {e}"
            return f"вќЊ РќР°РІС‹Рє '{skill_name}' РЅРµ РЅР°Р№РґРµРЅ РІ src/skills/"

        # в”Ђв”Ђ Watson / IBM WatsonX в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["watson СЃС‚Р°С‚СѓСЃ", "watsonx СЃС‚Р°С‚СѓСЃ", "watson status",
                                  "СЂРµР¶РёРј РёРё watsonx", "watsonx"]):
            w = getattr(self, "watson", None)
            if w is None:
                try:
                    from src.quantum.watson_bridge import WatsonXBridge
                    self.watson = w = WatsonXBridge()
                except Exception as e:
                    return f"вќЊ Watson: {e}"
            return w.status()

        # в”Ђв”Ђ IBM Quantum в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["ibm quantum", "ibm РєРІР°РЅС‚РѕРІС‹Р№", "РєРІР°РЅС‚РѕРІС‹Р№ РјРѕСЃС‚",
                                  "quantum bridge", "ibm quantum СЃС‚Р°С‚СѓСЃ"]):
            q = getattr(self, "ibm_quantum", None)
            if q is None:
                try:
                    from src.quantum.ibm_bridge import IBMQuantumBridge
                    self.ibm_quantum = q = IBMQuantumBridge()
                except Exception as e:
                    return f"вќЊ IBM Quantum: {e}"
            return q.status()

        if any(k in t for k in ["bell circuit", "quantum bell", "РєРІР°РЅС‚РѕРІС‹Р№ bell"]):
            q = getattr(self, "ibm_quantum", None)
            if q:
                return q.run_bell_circuit()
            return "вќЊ IBM Quantum РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"

        # в”Ђв”Ђ Slack в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["slack СЃС‚Р°С‚СѓСЃ", "slack status", "СЃР»Р°Рє СЃС‚Р°С‚СѓСЃ"]):
            s = getattr(self, "slack", None)
            if s is None:
                try:
                    from src.connectivity.slack_bridge import SlackBridge
                    self.slack = s = SlackBridge()
                except Exception as e:
                    return f"вќЊ Slack: {e}"
            configured = bool(s.bot_token)
            return (
                f"рџ’¬ Slack Bridge\n"
                f"  РЎС‚Р°С‚СѓСЃ: {'вњ… С‚РѕРєРµРЅ Р·Р°РґР°РЅ' if configured else 'вќЊ SLACK_BOT_TOKEN РЅРµ Р·Р°РґР°РЅ'}\n"
                f"  Socket Mode: {'вњ…' if s.socket_mode_ready() else 'вќЊ SLACK_APP_TOKEN РЅРµ Р·Р°РґР°РЅ'}\n"
                f"  РљР°РЅР°Р»: {s.default_channel or 'вЂ” Р·Р°РґР°Р№ SLACK_DEFAULT_CHANNEL'}"
            )

        if t.startswith("slack РѕС‚РїСЂР°РІСЊ ") or t.startswith("РѕС‚РїСЂР°РІСЊ РІ slack "):
            msg = re.sub(r"^(slack РѕС‚РїСЂР°РІСЊ|РѕС‚РїСЂР°РІСЊ РІ slack)\s*", "", text, flags=re.IGNORECASE).strip()
            s = getattr(self, "slack", None)
            if s and s.bot_token:
                result = s.send_message(msg)
                return "вњ… РћС‚РїСЂР°РІР»РµРЅРѕ РІ Slack" if result.get("ok") else f"вќЊ Slack: {result.get('error')}"
            return "вќЊ Slack РЅРµ РЅР°СЃС‚СЂРѕРµРЅ. Р—Р°РґР°Р№ SLACK_BOT_TOKEN РІ .env"

        # в”Ђв”Ђ SerpSearch / РІРµР±-РїРѕРёСЃРє в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РїРѕРёС‰Рё", "РЅР°Р№РґРё РІ РёРЅС‚РµСЂРЅРµС‚Рµ", "serp", "web search",
                                  "РіСѓРіР» РїРѕРёСЃРє", "РїРѕРёСЃРє РІ СЃРµС‚Рё"]):
            query = re.sub(
                r"^(РїРѕРёС‰Рё|РЅР°Р№РґРё РІ РёРЅС‚РµСЂРЅРµС‚Рµ|serp|web search|РіСѓРіР» РїРѕРёСЃРє|РїРѕРёСЃРє РІ СЃРµС‚Рё)\s*",
                "", text, flags=re.IGNORECASE
            ).strip()
            if not query:
                s = getattr(self, "serp_search", None)
                if s:
                    return s.status()
                return "Р¤РѕСЂРјР°С‚: РїРѕРёС‰Рё [Р·Р°РїСЂРѕСЃ]"
            try:
                if not getattr(self, "serp_search", None):
                    from src.skills.serp_search import SerpSearch
                    self.serp_search = SerpSearch()
                return self.serp_search.quick_search(query)
            except Exception as e:
                return f"вќЊ SerpSearch: {e}"

        # в”Ђв”Ђ Shodan в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["shodan РїРѕРёСЃРє", "shodan СЃРєР°РЅ", "shodan СЃС‚Р°С‚СѓСЃ"]):
            query = re.sub(r"^(shodan РїРѕРёСЃРє|shodan СЃРєР°РЅ|shodan СЃС‚Р°С‚СѓСЃ)\s*", "", text,
                           flags=re.IGNORECASE).strip()
            try:
                from src.skills.shodan_scanner import ShodanScanner
                sc = ShodanScanner()
                if "СЃС‚Р°С‚СѓСЃ" in t:
                    return (f"рџ”Ћ Shodan\n  API РєР»СЋС‡: {'вњ… Р·Р°РґР°РЅ' if sc.is_configured() else 'вќЊ SHODAN_API_KEY РЅРµ Р·Р°РґР°РЅ'}")
                if query and sc.is_configured():
                    res = sc.search(query, page=1)
                    total = res.get("total", 0)
                    matches = res.get("matches", [])[:3]
                    lines = [f"рџ”Ћ Shodan: '{query}' в†’ {total} СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ"]
                    for m in matches:
                        lines.append(f"  вЂў {m.get('ip_str','')} [{m.get('port','')}] {m.get('org','')} вЂ” {m.get('os','')}")
                    return "\n".join(lines)
                return "вќЊ SHODAN_API_KEY РЅРµ Р·Р°РґР°РЅ РІ .env"
            except Exception as e:
                return f"вќЊ Shodan: {e}"

        # в”Ђв”Ђ HuggingFace в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["huggingface СЃС‚Р°С‚СѓСЃ", "hf СЃС‚Р°С‚СѓСЃ", "huggingface status"]):
            try:
                from src.skills.huggingface_ai import HuggingFaceAI
                hf = HuggingFaceAI()
                return hf.run()
            except Exception as e:
                return f"вќЊ HuggingFace: {e}"

        # в”Ђв”Ђ Windows Bridge СЃС‚Р°С‚СѓСЃ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["win bridge", "win_bridge", "Р±СЂРёРґР¶ СЃС‚Р°С‚СѓСЃ",
                                  "usb СѓСЃС‚СЂРѕР№СЃС‚РІР°", "com РїРѕСЂС‚С‹", "windows СѓСЃС‚СЂРѕР№СЃС‚РІР°"]):
            try:
                from src.connectivity.windows_devices import format_report
                return format_report()
            except ImportError:
                pass
            try:
                from src.connectivity.system_health import _powershell
                out = _powershell(
                    "Get-WmiObject Win32_PnPEntity | "
                    "Where-Object{$_.Name -match 'COM|USB Serial|Arduino|ESP|CH340'} | "
                    "Select-Object Name | Format-Table -HideTableHeaders"
                )
                if out:
                    return f"рџ”Њ Windows СѓСЃС‚СЂРѕР№СЃС‚РІР°:\n{out[:1000]}"
            except Exception as e:
                return f"вќЊ Windows СѓСЃС‚СЂРѕР№СЃС‚РІР°: {e}"
            return "рџ”Њ РљРѕРјР°РЅРґР°: Р·Р°РїСѓСЃС‚Рё win_bridge_host.py РґР»СЏ СЂР°СЃС€РёСЂРµРЅРЅРѕРіРѕ РґРѕСЃС‚СѓРїР°"

        # в”Ђв”Ђ SKILL DISPATCHER (РЅРµС‡С‘С‚РєРѕРµ СЃРѕРїРѕСЃС‚Р°РІР»РµРЅРёРµ С‡РµСЂРµР· _SKILL_MAP) в”Ђв”Ђ
        _SKILL_MAP = {
            "РєСЂРёРїС‚Рѕ":          ("crypto_monitor", "CryptoSentinel",  "report"),
            "Р±РёС‚РєРѕРёРЅ":         ("crypto_monitor", "CryptoSentinel",  "report"),
            "bitcoin":         ("crypto_monitor", "CryptoSentinel",  "report"),
            "btc":             ("crypto_monitor", "CryptoSentinel",  "report"),
            "ethereum":        ("crypto_monitor", "CryptoSentinel",  "report"),
            "РґР°Р№РґР¶РµСЃС‚":        ("content_gen",    "ContentGen",      "generate_digest"),
            "РїРѕРіРѕРґР°":          ("weather",         None,              None),
            "weather":         ("weather",         None,              None),
            "СЃРєР°РЅРµСЂ":          ("net_scanner",    "NetGhost",        "scan"),
            "СЃРєР°РЅ СЃРµС‚Рё":       ("net_scanner",    "NetGhost",        "scan"),
            "РїСЂРѕРІРµСЂСЊ Р¶РµР»РµР·Рѕ":  ("hardware_intel",  None,              None),
            "hardware":        ("hardware_intel",  None,              None),
            "shodan":          ("shodan_scanner",  None,              None),
            "huggingface":     ("huggingface_ai",  None,              None),
            "СЃРµС‚РµРІРѕР№ РїСЂРёР·СЂР°Рє": ("network_shadow",  None,              None),
            # в”Ђв”Ђ РќРѕРІС‹Рµ СЃРєРёР»С‹ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            "СЃРёСЃС‚РµРјРЅС‹Р№ РјРѕРЅРёС‚РѕСЂ": ("system_monitor", "SystemMonitor",  "report"),
            "РјРѕРЅРёС‚РѕСЂРёРЅРі СЃРёСЃС‚РµРјС‹": ("system_monitor","SystemMonitor",  "report"),
            "cpu ram":           ("system_monitor", "SystemMonitor",  "report"),
            "СЂРµСЃСѓСЂСЃС‹":           ("system_monitor", "SystemMonitor",  "report"),
            "Р±СЌРєР°Рї":             ("auto_backup",    "AutoBackup",     "execute"),
            "СЂРµР·РµСЂРІРЅР°СЏ РєРѕРїРёСЏ":   ("auto_backup",    "AutoBackup",     "execute"),
            "СЃРїРёСЃРѕРє Р±СЌРєР°РїРѕРІ":    ("auto_backup",    "AutoBackup",     "report"),
            "watchdog":          ("iot_watchdog",   "IoTWatchdog",    "report"),
            "СЃС‚РѕСЂРѕР¶РµРІРѕР№":        ("iot_watchdog",   "IoTWatchdog",    "report"),
            "РЅР°РїРёС€Рё РєРѕРґ":        ("ai_coder",       "AICoder",        None),
            "СЃРѕР·РґР°Р№ СЃРєРёР»":       ("ai_coder",       "AICoder",        None),
            "РѕР±СЉСЏСЃРЅРё РєРѕРґ":       ("ai_coder",       "AICoder",        None),
            "РёСЃРїСЂР°РІСЊ РєРѕРґ":       ("ai_coder",       "AICoder",        None),
            "СЂРµС„Р°РєС‚РѕСЂРёРЅРі":       ("ai_coder",       "AICoder",        None),
        }
        for _kw, (_sn, _sc, _sm) in _SKILL_MAP.items():
            if _kw in t:
                _skill_result = self._run_skill(_sn, _sc, _sm, text)
                if _skill_result is not None:
                    return _skill_result
                break

        # в”Ђв”Ђ AI Coder: РєРѕРјР°РЅРґС‹ СЃ С‚РµРєСЃС‚РѕРј в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РЅР°РїРёС€Рё РєРѕРґ", "СЃРѕР·РґР°Р№ СЃРєРёР»", "РѕР±СЉСЏСЃРЅРё РєРѕРґ",
                                  "РёСЃРїСЂР°РІСЊ РєРѕРґ", "СЂРµС„Р°РєС‚РѕСЂРёРЅРі", "РЅР°РїРёС€Рё С‚РµСЃС‚С‹",
                                  "write code", "gen tests"]):
            try:
                from src.skills.ai_coder import AICoder
                coder = AICoder(core=self)
                result = coder.handle_command(text)
                if result:
                    return result
            except Exception as e:
                return f"вќЊ AICoder: {e}"

        # в”Ђв”Ђ ARC-AGI-3: СЃРѕСЂРµРІРЅРѕРІР°РЅРёРµ РїРѕ РёСЃРєСѓСЃСЃС‚РІРµРЅРЅРѕРјСѓ РёРЅС‚РµР»Р»РµРєС‚Сѓ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["arc СЃС‚Р°С‚СѓСЃ", "arc СЃСЂРµРґС‹", "arc СЂРµС€Р°Р№", "arc СЃС‚РѕРї",
                                  "arc С€Р°Рі", "arc-agi", "arcagi", "arc3 СЃС‚Р°С‚СѓСЃ",
                                  "arc3 СЃС‚РѕРї"]) or re.match(r'^arc\s+\w', t):
            try:
                from src.skills.arc_agi3_skill import handle as _arc_handle
                _arc_result = _arc_handle(text, core=self)
                if _arc_result is not None:
                    return _arc_result
            except Exception as e:
                return f"вќЊ ARC-AGI-3: {e}"

        # в”Ђв”Ђ TG Code Injector: Р·Р°РїСѓСЃРє в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["Р·Р°РїСѓСЃС‚Рё РёРЅР¶РµРєС‚РѕСЂ", "tg injector", "code injector",
                                  "РёРЅР¶РµРєС‚РѕСЂ РєРѕРґР°", "СЃС‚Р°СЂС‚ РёРЅР¶РµРєС‚РѕСЂ"]):
            try:
                from src.skills.tg_code_injector import TGCodeInjector
                if not hasattr(self, "_tg_injector") or not self._tg_injector:
                    self._tg_injector = TGCodeInjector(core=self)
                return self._tg_injector.start_polling()
            except Exception as e:
                return f"вќЊ TGCodeInjector: {e}"

        # в”Ђв”Ђ Watchdog: РґРѕР±Р°РІРёС‚СЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if "РґРѕР±Р°РІСЊ РІ watchdog" in t or "watchdog РґРѕР±Р°РІСЊ" in t:
            try:
                from src.skills.iot_watchdog import IoTWatchdog
                if not hasattr(self, "_watchdog"):
                    self._watchdog = IoTWatchdog(core=self)
                parts = re.sub(r"(РґРѕР±Р°РІСЊ РІ watchdog|watchdog РґРѕР±Р°РІСЊ)\s*", "", t).split()
                if len(parts) >= 3:
                    dev_id, dtype, target = parts[0], parts[1], parts[2]
                    name = " ".join(parts[3:]) if len(parts) > 3 else dev_id
                    return self._watchdog.add_device(dev_id, dtype, target, name)
                return "Р¤РѕСЂРјР°С‚: РґРѕР±Р°РІСЊ РІ watchdog [id] [ping|tcp|serial|http] [С†РµР»СЊ] [РёРјСЏ?]"
            except Exception as e:
                return f"вќЊ Watchdog: {e}"

        # в”Ђв”Ђ System Monitor: РїРѕСЂРѕРі в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if "РїРѕСЂРѕРі РјРѕРЅРёС‚РѕСЂР°" in t or "sysmon РїРѕСЂРѕРі" in t:
            try:
                from src.skills.system_monitor import SystemMonitor
                sm = SystemMonitor(core=self)
                # РїРѕСЂРѕРі РјРѕРЅРёС‚РѕСЂР° cpu_pct 90
                m = re.search(r"(cpu_pct|ram_pct|disk_pct|temp_cpu)\s+([\d.]+)", t)
                if m:
                    return sm.set_threshold(m.group(1), float(m.group(2)))
                return f"Р¤РѕСЂРјР°С‚: РїРѕСЂРѕРі РјРѕРЅРёС‚РѕСЂР° [cpu_pct|ram_pct|disk_pct|temp_cpu] [Р·РЅР°С‡РµРЅРёРµ]"
            except Exception as e:
                return f"вќЊ SysMonitor: {e}"

        if getattr(self, "skill_loader", None) and any(k in t for k in ["РЅР°РІС‹РєРё v2", "skills v2", "skillloader"]):
            return self.skill_loader.list_skills()
        if getattr(self, "skill_loader", None) and any(
            k in t for k in ["skills check all", "РїСЂРѕРІРµСЂСЊ РІСЃРµ РЅР°РІС‹РєРё", "РїСЂРѕРІРµСЂРєР° РІСЃРµС… РЅР°РІС‹РєРѕРІ", "РґРёР°РіРЅРѕСЃС‚РёРєР° РІСЃРµС… РЅР°РІС‹РєРѕРІ"]
        ):
            return self.skill_loader.smoke_check_all(core=self)
        if getattr(self, "skill_loader", None) and t.startswith("Р·Р°РіСЂСѓР·Рё РЅР°РІС‹Рє "):
            name = text.split("Р·Р°РіСЂСѓР·Рё РЅР°РІС‹Рє ", 1)[-1].strip()
            return self.skill_loader.load(name, core=self)
        if getattr(self, "skill_loader", None) and t.startswith("РІС‹РіСЂСѓР·Рё РЅР°РІС‹Рє "):
            name = text.split("РІС‹РіСЂСѓР·Рё РЅР°РІС‹Рє ", 1)[-1].strip()
            return self.skill_loader.unload(name)
        if getattr(self, "skill_loader", None) and t.startswith("РїРµСЂРµР·Р°РіСЂСѓР·Рё РЅР°РІС‹Рє "):
            name = text.split("РїРµСЂРµР·Р°РіСЂСѓР·Рё РЅР°РІС‹Рє ", 1)[-1].strip()
            return self.skill_loader.reload(name, core=self)

        if "РґР°Р№РґР¶РµСЃС‚" in t:
            ContentGen = self._import_skill("content_gen", "ContentGen")
            if ContentGen is None:
                return "вќЊ РќР°РІС‹Рє content_gen РЅРµ РЅР°Р№РґРµРЅ РІ src/skills/content_gen/"
            try:
                return ContentGen().generate_digest()
            except Exception as e:
                return f"вќЊ Р”Р°Р№РґР¶РµСЃС‚: {e}"
        if "РѕРїСѓР±Р»РёРєСѓР№" in t:
            from src.skills.content_gen import ContentGen
            return ContentGen().publish()
        # в”Ђв”Ђ РџР РЇРњРћР™ Р—РђРџРЈРЎРљ РќРђР’Р«РљРћР’ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        # РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ Р·Р°РїСѓСЃРє Р»СЋР±РѕРіРѕ РЅР°РІС‹РєР° Р±РµР· Р·РЅР°РЅРёСЏ РёРјС‘РЅ РєР»Р°СЃСЃРѕРІ
        _SKILL_MAP = {
            # С‚СЂРёРіРіРµСЂ -> (РјРѕРґСѓР»СЊ, РјРµС‚РѕРґ)
            "РєСЂРёРїС‚Рѕ":           ("crypto_monitor", "report"),
            "Р±РёС‚РєРѕРёРЅ":          ("crypto_monitor", "report"),
            "bitcoin":          ("crypto_monitor", "report"),
            "ethereum":         ("crypto_monitor", "report"),
            "РґР°Р№РґР¶РµСЃС‚":         ("content_gen",    "generate_digest"),
            "РѕРїСѓР±Р»РёРєСѓР№":        ("content_gen",    "publish"),
            "СЃРєР°РЅРёСЂСѓР№ СЃРµС‚СЊ":    ("net_scanner",    "scan"),
            "СЃРµС‚РµРІРѕР№ РїСЂРёР·СЂР°Рє":  ("net_scanner",    "scan"),
            "РїСЂРѕРІРµСЂСЊ Р¶РµР»РµР·Рѕ":   ("hardware_intel", "execute"),
            "Р¶РµР»РµР·Рѕ РёРЅС„Рѕ":      ("hardware_intel", "execute"),
            "shodan":           ("shodan_scanner", "scan"),
            "СЃРєР°РЅРёСЂСѓР№ shodan":  ("shodan_scanner", "scan"),
            "hf РјРѕРґРµР»СЊ":        ("huggingface_ai", "run"),
            "huggingface":      ("huggingface_ai", "run"),
            "РѕР±РЅРѕРІРё С‚Р°СЃРјРѕС‚Р°":   ("tasmota_updater","run"),
            # в”Ђв”Ђ РќРѕРІС‹Рµ РЅР°РІС‹РєРё (2026) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            "pip СѓСЃС‚Р°РЅРѕРІРё":     ("pip_manager",    "run"),
            "pip СѓРґР°Р»Рё":        ("pip_manager",    "run"),
            "pip РѕР±РЅРѕРІРё":       ("pip_manager",    "run"),
            "pip СЃРїРёСЃРѕРє":       ("pip_manager",    "run"),
            "pip РїРѕРёСЃРє":        ("pip_manager",    "run"),
            "pip РёРЅС„Рѕ":         ("pip_manager",    "run"),
            "pip РїСЂРѕРІРµСЂСЊ":      ("pip_manager",    "run"),
            "pypi РїРѕРёСЃРє":       ("pip_manager",    "run"),
            "РѕС‚РїСЂР°РІСЊ РїРёСЃСЊРјРѕ":   ("smtp_mailer",    "run"),
            "smtp СЃС‚Р°С‚СѓСЃ":      ("smtp_mailer",    "run"),
            "smtp С‚РµСЃС‚":        ("smtp_mailer",    "run"),
            "email РѕС‚РїСЂР°РІСЊ":    ("smtp_mailer",    "run"),
            "ton Р±Р°Р»Р°РЅСЃ":       ("ton_blockchain", "run"),
            "ton С‚СЂР°РЅР·Р°РєС†РёРё":   ("ton_blockchain", "run"),
            "ton СЃС‚Р°С‚СѓСЃ":       ("ton_blockchain", "run"),
            "ton С†РµРЅР°":         ("ton_blockchain", "run"),
            "ton Р°РґСЂРµСЃ":        ("ton_blockchain", "run"),
            "toncoin":          ("ton_blockchain", "run"),
            "Р·Р°С€РёС„СЂСѓР№":         ("crypto_utils",   "run"),
            "СЂР°СЃС€РёС„СЂСѓР№":        ("crypto_utils",   "run"),
            "РіРµРЅРµСЂРёСЂСѓР№ РєР»СЋС‡":   ("crypto_utils",   "run"),
            "РіРµРЅРµСЂРёСЂСѓР№ РїР°СЂРѕР»СЊ": ("crypto_utils",   "run"),
            "base64 РєРѕРґРёСЂСѓР№":   ("crypto_utils",   "run"),
            "base64 СЂР°СЃРєРѕРґРёСЂСѓР№":("crypto_utils",   "run"),
            "ga4 РѕС‚С‡С‘С‚":        ("ga4_analytics",  "run"),
            "ga4 СЃРµСЃСЃРёРё":       ("ga4_analytics",  "run"),
            "ga4 РїРѕР»СЊР·РѕРІР°С‚РµР»Рё": ("ga4_analytics",  "run"),
            "ga4 СЃС‚СЂР°РЅРёС†С‹":     ("ga4_analytics",  "run"),
            "ga4 СЃС‚Р°С‚СѓСЃ":       ("ga4_analytics",  "run"),
            "google analytics": ("ga4_analytics",  "run"),
            "ebay РїРѕРёСЃРє":       ("ebay_parser",    "run"),
            "ebay С†РµРЅР°":        ("ebay_parser",    "run"),
            "ebay СЃС‚Р°С‚СѓСЃ":      ("ebay_parser",    "run"),
            "fastapi СЃС‚Р°СЂС‚":    ("fastapi_skill",  "run"),
            "fastapi СЃС‚РѕРї":     ("fastapi_skill",  "run"),
            "fastapi СЃС‚Р°С‚СѓСЃ":   ("fastapi_skill",  "run"),
            "fastapi РјР°СЂС€СЂСѓС‚С‹": ("fastapi_skill",  "run"),
            "api СЃРµСЂРІРµСЂ":       ("fastapi_skill",  "run"),
            "Р·Р°РїСѓСЃС‚Рё api":      ("fastapi_skill",  "run"),
        }
        for _trigger, (_mod_name, _method) in _SKILL_MAP.items():
            if _trigger in t:
                _cls = self._import_skill(_mod_name)
                if _cls is None:
                    return f"вќЊ РќР°РІС‹Рє {_mod_name} РЅРµ РЅР°Р№РґРµРЅ РІ src/skills/{_mod_name}/"
                try:
                    _inst = _cls(core=self) if _cls.__init__.__code__.co_varnames.__contains__("core") else _cls()
                except Exception:
                    try:
                        _inst = _cls()
                    except Exception as _ie:
                        return f"вќЊ {_mod_name} init: {_ie}"
                try:
                    # РЎРЅР°С‡Р°Р»Р° РїСЂРѕР±СѓРµРј handle_command(text) вЂ” РґР»СЏ СЃРєРёР»РѕРІ СЃ РїР°СЂСЃРёРЅРіРѕРј РєРѕРјР°РЅРґС‹
                    if hasattr(_inst, "handle_command"):
                        _hc_result = _inst.handle_command(text)
                        if _hc_result is not None:
                            return _hc_result
                    # Р—Р°С‚РµРј РІС‹Р·С‹РІР°РµРј РјРµС‚РѕРґ РёР· РєР°СЂС‚С‹
                    if hasattr(_inst, _method):
                        return getattr(_inst, _method)()
                    return f"вќЊ РќР°РІС‹Рє {_mod_name}: РјРµС‚РѕРґ {_method} РЅРµ РЅР°Р№РґРµРЅ"
                except Exception as _se:
                    return f"вќЊ {_mod_name}: {_se}"

        # СЃРїРёСЃРѕРє РЅР°РІС‹РєРѕРІ вЂ” РѕР±СЂР°Р±Р°С‚С‹РІР°РµС‚СЃСЏ РІ INTERCEPT Р±Р»РѕРєРµ
        if any(k in t for k in ["РЅР°РїРёС€Рё РЅР°РІС‹Рє", "СЃРѕР·РґР°Р№ РЅР°РІС‹Рє"]):
            from src.skills.evolution import ArgosEvolution
            desc = text.replace("РЅР°РїРёС€Рё РЅР°РІС‹Рє","").replace("СЃРѕР·РґР°Р№ РЅР°РІС‹Рє","").strip()
            return ArgosEvolution(ai_core=self).generate_skill(desc)

        # в”Ђв”Ђ РџР°РјСЏС‚СЊ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if self.memory:
            if any(t.startswith(p) for p in ("Р·Р°РїРѕРјРЅРё ", "Р·Р°РїРёС€Рё С„Р°РєС‚ ", "remember ")):
                q = text
                for pref in ("Р·Р°РїРѕРјРЅРё", "Р·Р°РїРёС€Рё С„Р°РєС‚", "remember", "Р°СЂРіРѕСЃ"):
                    q = q.replace(pref, "")
                return self.memory.parse_and_remember(q.strip())
            if any(t.startswith(p) for p in ("СѓРґР°Р»Рё С„Р°РєС‚", "delete С„Р°РєС‚", "delete fact", "remove fact")):
                q = text
                for pref in ("СѓРґР°Р»Рё С„Р°РєС‚", "delete С„Р°РєС‚", "delete fact", "remove fact", ":", "Р°СЂРіРѕСЃ"):
                    q = q.replace(pref, "")
                q = q.strip()
                return self.memory.forget(q) if q else "Р¤РѕСЂРјР°С‚: СѓРґР°Р»Рё С„Р°РєС‚ [С‚РµРєСЃС‚ С„Р°РєС‚Р°]"
            if any(k in t for k in ["С‡С‚Рѕ С‚С‹ Р·РЅР°РµС€СЊ", "РјРѕСЏ РїР°РјСЏС‚СЊ", "РїРѕРєР°Р¶Рё РїР°РјСЏС‚СЊ"]):
                return self.memory.format_memory()
            if any(k in t for k in ["РїРѕРёСЃРє РїРѕ РїР°РјСЏС‚Рё", "РЅР°Р№РґРё РІ РїР°РјСЏС‚Рё", "rag РїР°РјСЏС‚СЊ"]):
                q = text
                for pref in ["РїРѕРёСЃРє РїРѕ РїР°РјСЏС‚Рё", "РЅР°Р№РґРё РІ РїР°РјСЏС‚Рё", "rag РїР°РјСЏС‚СЊ", "Р°СЂРіРѕСЃ"]:
                    q = q.replace(pref, "")
                q = q.strip()
                if not q:
                    return "Р¤РѕСЂРјР°С‚: РЅР°Р№РґРё РІ РїР°РјСЏС‚Рё [Р·Р°РїСЂРѕСЃ]"
                rag = self.memory.get_rag_context(q, top_k=5)
                return rag or "РќРёС‡РµРіРѕ СЂРµР»РµРІР°РЅС‚РЅРѕРіРѕ РІ РІРµРєС‚РѕСЂРЅРѕР№ РїР°РјСЏС‚Рё РЅРµ РЅР°Р№РґРµРЅРѕ."
            if any(k in t for k in ["РіСЂР°С„ Р·РЅР°РЅРёР№", "СЃРІСЏР·Рё РїР°РјСЏС‚Рё", "РјРѕРё СЃРІСЏР·Рё"]):
                return self.memory.graph_report()
            if any(t.startswith(p) for p in ("Р·Р°Р±СѓРґСЊ ", "forget ")) and "СЂР°Р·РіРѕРІРѕСЂ" not in t:
                q = text
                for pref in ("Р·Р°Р±СѓРґСЊ", "forget", "Р°СЂРіРѕСЃ"):
                    q = q.replace(pref, "")
                return self.memory.forget(q.strip())
            if any(k in t for k in ["Р·Р°РїРёС€Рё Р·Р°РјРµС‚РєСѓ", "РЅРѕРІР°СЏ Р·Р°РјРµС‚РєР°"]):
                parts = text.replace("Р·Р°РїРёС€Рё Р·Р°РјРµС‚РєСѓ","").replace("РЅРѕРІР°СЏ Р·Р°РјРµС‚РєР°","").strip().split(":",1)
                return self.memory.add_note(parts[0].strip(), parts[1].strip() if len(parts)>1 else parts[0])
            if any(k in t for k in ["РјРѕРё Р·Р°РјРµС‚РєРё", "СЃРїРёСЃРѕРє Р·Р°РјРµС‚РѕРє"]):
                return self.memory.get_notes()
            if "РїСЂРѕС‡РёС‚Р°Р№ Р·Р°РјРµС‚РєСѓ" in t:
                try: return self.memory.read_note(int(text.split()[-1]))
                except: return "РЈРєР°Р¶Рё РЅРѕРјРµСЂ: РїСЂРѕС‡РёС‚Р°Р№ Р·Р°РјРµС‚РєСѓ 1"
            if "СѓРґР°Р»Рё Р·Р°РјРµС‚РєСѓ" in t:
                try: return self.memory.delete_note(int(text.split()[-1]))
                except: return "РЈРєР°Р¶Рё РЅРѕРјРµСЂ: СѓРґР°Р»Рё Р·Р°РјРµС‚РєСѓ 1"

        # в”Ђв”Ђ РџР»Р°РЅРёСЂРѕРІС‰РёРє в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if self.scheduler:
            if any(k in t for k in ["СЂР°СЃРїРёСЃР°РЅРёРµ", "СЃРїРёСЃРѕРє Р·Р°РґР°С‡"]):
                return self.scheduler.list_tasks()
            starts_sched = any(t.strip().startswith(p) for p in ("РєР°Р¶РґС‹Р№ ", "РєР°Р¶РґС‹Рµ ", "РєР°Р¶РґСѓСЋ ", "РЅР°РїРѕРјРЅРё ", "РµР¶РµРґРЅРµРІРЅРѕ", "РІ "))
            has_delay = bool(_re_sched.search(r"^\s*С‡РµСЂРµР·\s+\d+", t))
            if starts_sched or has_delay:
                return self.scheduler.parse_and_add(text)
            if "СѓРґР°Р»Рё Р·Р°РґР°С‡Сѓ" in t or "delete Р·Р°РґР°" in t:
                m = _re_sched.search(r"(?:СѓРґР°Р»Рё\s+Р·Р°РґР°С‡[Р°СѓРё]?|delete\s+Р·Р°РґР°С‡[Р°СѓРё]?|delete\s+task)\s*#?\s*(\d+)", t)
                if not m:
                    m = _re_sched.search(r"#\s*(\d+)", t)
                if m:
                    return self.scheduler.remove(int(m.group(1)))
                return "РЈРєР°Р¶Рё РЅРѕРјРµСЂ: СѓРґР°Р»Рё Р·Р°РґР°С‡Сѓ 1"

        # в”Ђв”Ђ РђР»РµСЂС‚С‹ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if self.alerts:
            if any(k in t for k in ["СЃС‚Р°С‚СѓСЃ Р°Р»РµСЂС‚РѕРІ", "Р°Р»РµСЂС‚С‹"]):
                return self.alerts.status()
            if "СѓСЃС‚Р°РЅРѕРІРё РїРѕСЂРѕРі" in t:
                try:
                    parts = text.split()
                    return self.alerts.set_threshold(parts[-2], float(parts[-1].replace("%","")))
                except: return "Р¤РѕСЂРјР°С‚: СѓСЃС‚Р°РЅРѕРІРё РїРѕСЂРѕРі cpu 85"

        # в”Ђв”Ђ Р’РµР±-РїР°РЅРµР»СЊ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if (
            t.strip() in {"РІРµР±-РїР°РЅРµР»СЊ", "РІРµР± РїР°РЅРµР»СЊ", "dashboard", "РѕС‚РєСЂРѕР№ РїР°РЅРµР»СЊ"}
            or t.startswith("РІРµР±-РїР°РЅРµР»СЊ ")
            or t.startswith("РІРµР± РїР°РЅРµР»СЊ ")
            or t.startswith("dashboard ")
            or t.startswith("РѕС‚РєСЂРѕР№ РїР°РЅРµР»СЊ")
        ):
            return self.start_dashboard(admin, flasher)

        # в”Ђв”Ђ Р“РµРѕР»РѕРєР°С†РёСЏ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РіРµРѕР»РѕРєР°С†РёСЏ", "РјРѕР№ ip", "РіРґРµ СЏ", "РјРѕР№ Р°РґСЂРµСЃ"]):
            from src.connectivity.spatial import SpatialAwareness
            return SpatialAwareness(db=self.db).get_full_report()

        # в”Ђв”Ђ Р—Р°РіСЂСѓР·С‡РёРє в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["Р·Р°РіСЂСѓР·С‡РёРє", "boot info"]):
            from src.security.bootloader_manager import BootloaderManager
            if not self._boot: self._boot = BootloaderManager()
            return self._boot.full_report()
        if "ARGOS-BOOT-CONFIRM" in t.upper():
            from src.security.bootloader_manager import BootloaderManager
            if not self._boot: self._boot = BootloaderManager()
            return self._boot.confirm("ARGOS-BOOT-CONFIRM")
        if any(k in t for k in ["СѓСЃС‚Р°РЅРѕРІРё persistence", "РїРµСЂСЃРёСЃС‚РµРЅСЃ"]):
            from src.security.bootloader_manager import BootloaderManager
            if not self._boot: self._boot = BootloaderManager()
            return self._boot.install_persistence()
        if "РѕР±РЅРѕРІРё grub" in t:
            from src.security.bootloader_manager import BootloaderManager
            if not self._boot: self._boot = BootloaderManager()
            return self._boot.linux_update_grub()

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # РџР›РђРўР¤РћР РњР•РќРќРћР• РђР”РњРРќРРЎРўР РР РћР’РђРќРР• (Linux / Windows / Android)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.platform_admin:
            _platform_keywords = [
                # РЎС‚Р°С‚СѓСЃ
                "РїР»Р°С‚С„РѕСЂРјР° СЃС‚Р°С‚СѓСЃ", "platform status", "os СЃС‚Р°С‚СѓСЃ",
                # Linux
                "apt СѓСЃС‚Р°РЅРѕРІРё", "apt СѓРґР°Р»Рё", "apt РѕР±РЅРѕРІРёС‚СЊ", "apt РїРѕРёСЃРє", "apt СЃРїРёСЃРѕРє",
                "apt РѕР±РЅРѕРІР»РµРЅРёРµ", "linux СѓСЃС‚Р°РЅРѕРІРё РїР°РєРµС‚", "linux СѓРґР°Р»Рё РїР°РєРµС‚",
                "linux РѕР±РЅРѕРІРёС‚СЊ РїР°РєРµС‚С‹", "linux РїРѕРёСЃРє РїР°РєРµС‚Р°", "СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РїР°РєРµС‚С‹ linux",
                "snap СѓСЃС‚Р°РЅРѕРІРё", "snap СЃРїРёСЃРѕРє", "snap list",
                "СЃРµСЂРІРёСЃ Р·Р°РїСѓСЃС‚Рё", "СЃРµСЂРІРёСЃ СЃС‚РѕРї", "СЃРµСЂРІРёСЃ РѕСЃС‚Р°РЅРѕРІРё",
                "СЃРµСЂРІРёСЃ РїРµСЂРµР·Р°РїСѓСЃРє", "СЃРµСЂРІРёСЃ СЃС‚Р°С‚СѓСЃ", "СЃРµСЂРІРёСЃ РІРєР»СЋС‡Рё", "СЃРµСЂРІРёСЃ РѕС‚РєР»СЋС‡Рё",
                "СЃРїРёСЃРѕРє СЃРµСЂРІРёСЃРѕРІ", "РІСЃРµ СЃРµСЂРІРёСЃС‹", "СЃРµСЂРІРёСЃС‹ linux",
                "systemctl start", "systemctl stop", "systemctl restart",
                "systemctl status", "systemctl enable", "systemctl disable",
                "Р»РѕРіРё СЃРёСЃС‚РµРјС‹", "logРё ", "journalctl",
                "РґРёСЃРє linux", "РґРёСЃРє РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ",
                "СЂР°Р·РјРµСЂ РїР°РїРєРё", "df",
                "РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ linux", "whoami linux", "linux РєС‚Рѕ СЏ",
                "СЃРїРёСЃРѕРє РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№ linux", "РїРѕР»СЊР·РѕРІР°С‚РµР»Рё linux",
                "РґРѕР±Р°РІСЊ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ", "СѓРґР°Р»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ",
                "СЃРµС‚СЊ linux", "ip Р°РґСЂРµСЃР°", "СЃРµС‚РµРІС‹Рµ РёРЅС‚РµСЂС„РµР№СЃС‹",
                "РѕС‚РєСЂС‹С‚С‹Рµ РїРѕСЂС‚С‹", "РїРѕСЂС‚С‹ linux", "ss linux", "netstat linux",
                "С„Р°РµСЂРІРѕР» linux", "ufw СЃС‚Р°С‚СѓСЃ", "firewall linux",
                "СЃРёСЃС‚РµРјР° linux", "linux РёРЅС„Рѕ", "linux РёРЅС„РѕСЂРјР°С†РёСЏ",
                "РїСЂРѕС†РµСЃСЃРѕСЂ linux", "cpu linux", "lscpu",
                "РїСЂРѕС†РµСЃСЃС‹ linux", "top linux", "ps linux",
                # Windows
                "winget СѓСЃС‚Р°РЅРѕРІРё", "winget СѓРґР°Р»Рё", "winget РѕР±РЅРѕРІРёС‚СЊ", "winget РїРѕРёСЃРє",
                "winget СЃРїРёСЃРѕРє", "winget upgrade", "windows СѓСЃС‚Р°РЅРѕРІРё", "windows СѓРґР°Р»Рё",
                "windows РѕР±РЅРѕРІРёС‚СЊ РїР°РєРµС‚С‹", "СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Рµ РїР°РєРµС‚С‹ windows",
                "windows СЃРµСЂРІРёСЃ Р·Р°РїСѓСЃС‚Рё", "windows СЃРµСЂРІРёСЃ СЃС‚РѕРї",
                "windows СЃРµСЂРІРёСЃ СЃС‚Р°С‚СѓСЃ", "windows СЃРµСЂРІРёСЃС‹",
                "sc start", "sc stop", "sc query",
                "СЃРїРёСЃРѕРє СЃРµСЂРІРёСЃРѕРІ windows",
                "СЂРµРµСЃС‚СЂ Р·Р°РїСЂРѕСЃ",
                "Р·Р°РґР°С‡Рё windows", "РїСЂРѕС†РµСЃСЃС‹ windows", "tasklist",
                "СѓР±РµР№ Р·Р°РґР°С‡Сѓ", "taskkill",
                "СЃРµС‚СЊ windows", "ipconfig", "windows СЃРµС‚СЊ",
                "С„Р°РµСЂРІРѕР» windows", "windows firewall",
                "РѕР±РЅРѕРІР»РµРЅРёСЏ windows", "windows update", "windows РѕР±РЅРѕРІР»РµРЅРёСЏ",
                "РѕС€РёР±РєРё windows", "event log windows", "windows Р»РѕРіРё",
                "РґРёСЃРє windows", "windows РґРёСЃРє",
                "СЃРёСЃС‚РµРјР° windows", "windows РёРЅС„Рѕ", "systeminfo",
                "defender СЃС‚Р°С‚СѓСЃ", "windows defender",
                "defender СЃРєР°РЅРёСЂРѕРІР°С‚СЊ", "defender scan",
                "РїРѕР»СЊР·РѕРІР°С‚РµР»Рё windows", "windows РїРѕР»СЊР·РѕРІР°С‚РµР»Рё",
                "windows РєС‚Рѕ СЏ", "whoami windows",
                # Android
                "adb СѓСЃС‚СЂРѕР№СЃС‚РІР°", "adb devices",
                "adb РїРѕРґРєР»СЋС‡Рё", "adb РѕС‚РєР»СЋС‡Рё",
                "android РїСЂРёР»РѕР¶РµРЅРёСЏ", "pm list packages", "СЃРїРёСЃРѕРє РїСЂРёР»РѕР¶РµРЅРёР№ android",
                "android СЃРёСЃС‚РµРјРЅС‹Рµ РїСЂРёР»РѕР¶РµРЅРёСЏ",
                "android СѓСЃС‚Р°РЅРѕРІРё", "pm install",
                "android СѓРґР°Р»Рё", "pm uninstall",
                "android Р·Р°РїСѓСЃС‚Рё", "android РѕСЃС‚Р°РЅРѕРІРё", "android РѕС‡РёСЃС‚Рё",
                "pkg СѓСЃС‚Р°РЅРѕРІРё", "pkg СѓРґР°Р»Рё", "pkg РѕР±РЅРѕРІРёС‚СЊ", "pkg РїРѕРёСЃРє", "pkg СЃРїРёСЃРѕРє",
                "termux СѓСЃС‚Р°РЅРѕРІРё", "termux СѓРґР°Р»Рё", "termux РѕР±РЅРѕРІРёС‚СЊ",
                "termux РїРѕРёСЃРє", "termux РїР°РєРµС‚С‹", "termux list",
                "android Р±Р°С‚Р°СЂРµСЏ", "battery status", "Р±Р°С‚Р°СЂРµСЏ",
                "android С…СЂР°РЅРёР»РёС‰Рµ", "android РґРёСЃРє", "android storage",
                "android РёРЅС„Рѕ", "android РёРЅС„РѕСЂРјР°С†РёСЏ", "android sys",
                "android wifi", "android СЃРµС‚СЊ", "wifi android",
                "android РїСЂРѕС†РµСЃСЃС‹", "android top",
                "android РЅР°СЃС‚СЂРѕР№РєРё",
                "android СЃРєСЂРёРЅС€РѕС‚", "adb screenshot",
                "adb logcat", "adb push", "adb pull",
                "android РїРµСЂРµР·Р°РіСЂСѓР·РєР°", "adb reboot",
                "android recovery", "android fastboot",
            ]
            if any(k in t for k in _platform_keywords):
                return self.platform_admin.handle_command(t)

        # в”Ђв”Ђ РђРІС‚РѕР·Р°РїСѓСЃРє в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if "СѓСЃС‚Р°РЅРѕРІРё Р°РІС‚РѕР·Р°РїСѓСЃРє" in t:
            from src.security.autostart import ArgosAutostart
            return ArgosAutostart().install()
        if "СЃС‚Р°С‚СѓСЃ Р°РІС‚РѕР·Р°РїСѓСЃРєР°" in t:
            from src.security.autostart import ArgosAutostart
            return ArgosAutostart().status()
        if "СѓРґР°Р»Рё Р°РІС‚РѕР·Р°РїСѓСЃРє" in t:
            from src.security.autostart import ArgosAutostart
            return ArgosAutostart().uninstall()

        # в”Ђв”Ђ P2P в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["СЃС‚Р°С‚СѓСЃ СЃРµС‚Рё", "p2p СЃС‚Р°С‚СѓСЃ", "СЃРµС‚СЊ РЅРѕРґ"]):
            return self.p2p.network_status() if self.p2p else "P2P РЅРµ Р·Р°РїСѓС‰РµРЅ. РљРѕРјР°РЅРґР°: Р·Р°РїСѓСЃС‚Рё p2p"
        if any(k in t for k in ["РїСЂРѕС‚РѕРєРѕР» p2p", "p2p РїСЂРѕС‚РѕРєРѕР»", "libp2p", "zkp"]):
            return p2p_protocol_roadmap()
        if "Р·Р°РїСѓСЃС‚Рё p2p" in t:
            return self.start_p2p()
        if "СЃРёРЅС…СЂРѕРЅРёР·РёСЂСѓР№ РЅР°РІС‹РєРё" in t:
            return self.p2p.sync_skills_from_network() if self.p2p else "P2P РЅРµ Р·Р°РїСѓС‰РµРЅ."
        if "РїРѕРґРєР»СЋС‡РёСЃСЊ Рє " in t:
            ip = text.split("РїРѕРґРєР»СЋС‡РёСЃСЊ Рє ")[-1].strip().split()[0]
            return self.p2p.connect_to(ip) if self.p2p else "P2P РЅРµ Р·Р°РїСѓС‰РµРЅ."
        if any(k in t for k in ["СЂР°СЃРїСЂРµРґРµР»Рё Р·Р°РґР°С‡Сѓ", "РѕР±С‰Р°СЏ РјРѕС‰РЅРѕСЃС‚СЊ"]):
            if self.p2p:
                q = text.replace("СЂР°СЃРїСЂРµРґРµР»Рё Р·Р°РґР°С‡Сѓ","").replace("РѕР±С‰Р°СЏ РјРѕС‰РЅРѕСЃС‚СЊ","").strip()
                route_type = "heavy" if any(k in q.lower() for k in ["vision", "РєР°РјРµСЂ", "РєРѕРјРїРёР»СЏ", "compile", "РїСЂРѕС€РёРІ"]) else None
                return self.p2p.route_query(q or "РЎС‚Р°С‚СѓСЃ СЃРµС‚Рё РђСЂРіРѕСЃР°.", task_type=route_type)
            return "P2P РЅРµ Р·Р°РїСѓС‰РµРЅ."

        # в”Ђв”Ђ DAG в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if getattr(self, "dag_manager", None) and any(k in t for k in ["СЃРїРёСЃРѕРє dag", "dag СЃРїРёСЃРѕРє", "РґРѕСЃС‚СѓРїРЅС‹Рµ dag"]):
            return self.dag_manager.list_dags()
        if getattr(self, "dag_manager", None) and ("Р·Р°РїСѓСЃС‚Рё_dag" in t or "Р·Р°РїСѓСЃС‚Рё dag" in t):
            name = text.replace("Р·Р°РїСѓСЃС‚Рё_dag", "").replace("Р·Р°РїСѓСЃС‚Рё dag", "").strip()
            name = name.replace(".json", "")
            name = name.split("/")[-1]
            if not name:
                return "Р¤РѕСЂРјР°С‚: Р·Р°РїСѓСЃС‚Рё_dag РёРјСЏ_РіСЂР°С„Р°"
            return self.dag_manager.run(name)
        if getattr(self, "dag_manager", None) and ("СЃРѕР·РґР°Р№_dag" in t or "СЃРѕР·РґР°Р№ dag" in t):
            desc = text.replace("СЃРѕР·РґР°Р№_dag", "").replace("СЃРѕР·РґР°Р№ dag", "").strip()
            if not desc:
                return "Р¤РѕСЂРјР°С‚: СЃРѕР·РґР°Р№_dag РѕРїРёСЃР°РЅРёРµ С€Р°РіРѕРІ"
            return self.dag_manager.create_from_text(desc)
        if getattr(self, "dag_manager", None) and any(k in t for k in ["СЃРёРЅС…СЂРѕРЅРёР·РёСЂСѓР№ dag", "dag sync"]):
            return self.dag_manager.sync_to_p2p()

        # в”Ђв”Ђ GitHub Marketplace в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if getattr(self, "marketplace", None) and "СѓСЃС‚Р°РЅРѕРІРё РЅР°РІС‹Рє РёР· github" in t:
            spec = text.split("СѓСЃС‚Р°РЅРѕРІРё РЅР°РІС‹Рє РёР· github", 1)[-1].strip().split()
            if len(spec) < 2:
                return "Р¤РѕСЂРјР°С‚: СѓСЃС‚Р°РЅРѕРІРё РЅР°РІС‹Рє РёР· github USER/REPO SKILL"
            return self.marketplace.install(repo=spec[0], skill_name=spec[1])
        if getattr(self, "marketplace", None) and "РѕР±РЅРѕРІРё РёР· github" in t:
            spec = text.split("РѕР±РЅРѕРІРё РёР· github", 1)[-1].strip().split()
            if len(spec) < 2:
                return "Р¤РѕСЂРјР°С‚: РѕР±РЅРѕРІРё РёР· github USER/REPO SKILL"
            return self.marketplace.update(repo=spec[0], skill_name=spec[1])
        if getattr(self, "marketplace", None) and "РѕС†РµРЅРё РЅР°РІС‹Рє" in t:
            spec = text.split("РѕС†РµРЅРё РЅР°РІС‹Рє", 1)[-1].strip().split()
            if len(spec) < 2:
                return "Р¤РѕСЂРјР°С‚: РѕС†РµРЅРё РЅР°РІС‹Рє SKILL [1-5]"
            return self.marketplace.rate(spec[0], spec[1])
        if getattr(self, "marketplace", None) and any(k in t for k in ["СЂРµР№С‚РёРЅРі РЅР°РІС‹РєРѕРІ", "РѕС†РµРЅРєРё РЅР°РІС‹РєРѕРІ"]):
            return self.marketplace.ratings_report()

        # в”Ђв”Ђ РСЃС‚РѕСЂРёСЏ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РёСЃС‚РѕСЂРёСЏ", "РїСЂРµРґС‹РґСѓС‰РёРµ СЂР°Р·РіРѕРІРѕСЂС‹"]):
            return self.db.format_history(10) if self.db else "Р‘Р” РЅРµ РїРѕРґРєР»СЋС‡РµРЅР°."

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # РЈРњРќР«Р• РЎРРЎРўР•РњР« (РґРѕРј, С‚РµРїР»РёС†Р°, РіР°СЂР°Р¶, РїРѕРіСЂРµР±, РёРЅРєСѓР±Р°С‚РѕСЂ, Р°РєРІР°СЂРёСѓРј, С‚РµСЂСЂР°СЂРёСѓРј)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.smart_sys:
            if any(k in t for k in ["СЃРѕР·РґР°Р№ СѓРјРЅСѓСЋ СЃРёСЃС‚РµРјСѓ", "РґРѕР±Р°РІСЊ СѓРјРЅСѓСЋ СЃРёСЃС‚РµРјСѓ", "РјР°СЃС‚РµСЂ СѓРјРЅРѕР№ СЃРёСЃС‚РµРјС‹"]):
                return self._start_smart_create_wizard()
            if any(k in t for k in ["СѓРјРЅС‹Рµ СЃРёСЃС‚РµРјС‹", "СЃС‚Р°С‚СѓСЃ СЃРёСЃС‚РµРј", "РјРѕРё СЃРёСЃС‚РµРјС‹", "СѓРјРЅС‹Р№ РґРѕРј"]):
                return self.smart_sys.full_status()
            if any(k in t for k in ["С‚РёРїС‹ СЃРёСЃС‚РµРј", "РґРѕСЃС‚СѓРїРЅС‹Рµ СЃРёСЃС‚РµРјС‹"]):
                return self.smart_sys.available_types()
            if "РґРѕР±Р°РІСЊ СЃРёСЃС‚РµРјСѓ" in t or "СЃРѕР·РґР°Р№ СЃРёСЃС‚РµРјСѓ" in t:
                parts = text.replace("РґРѕР±Р°РІСЊ СЃРёСЃС‚РµРјСѓ","").replace("СЃРѕР·РґР°Р№ СЃРёСЃС‚РµРјСѓ","").strip().split()
                if not parts:
                    return self.smart_sys.available_types()
                sys_type = parts[0]
                sys_id   = parts[1] if len(parts) > 1 else None
                return self.smart_sys.add_system(sys_type, sys_id)
            if "РѕР±РЅРѕРІРё СЃРµРЅСЃРѕСЂ" in t or "СЃРµРЅСЃРѕСЂ" in t and "=" in t:
                # Р¤РѕСЂРјР°С‚: РѕР±РЅРѕРІРё СЃРµРЅСЃРѕСЂ [СЃРёСЃС‚РµРјР°] [СЃРµРЅСЃРѕСЂ] [Р·РЅР°С‡РµРЅРёРµ]
                parts = text.replace("РѕР±РЅРѕРІРё СЃРµРЅСЃРѕСЂ","").strip().split()
                if len(parts) >= 3:
                    return self.smart_sys.update(parts[0], parts[1], parts[2])
                return "Р¤РѕСЂРјР°С‚: РѕР±РЅРѕРІРё СЃРµРЅСЃРѕСЂ [id_СЃРёСЃС‚РµРјС‹] [СЃРµРЅСЃРѕСЂ] [Р·РЅР°С‡РµРЅРёРµ]"
            if any(k in t for k in ["РІРєР»СЋС‡Рё", "РІС‹РєР»СЋС‡Рё", "СѓСЃС‚Р°РЅРѕРІРё"]) and self.smart_sys.systems:
                # РІРєР»СЋС‡Рё РїРѕР»РёРІ greenhouse / РІС‹РєР»СЋС‡Рё РѕР±РѕРіСЂРµРІ home
                for action_w, state in [("РІРєР»СЋС‡Рё","on"),("РІС‹РєР»СЋС‡Рё","off"),("СѓСЃС‚Р°РЅРѕРІРё","set")]:
                    if action_w in t:
                        rest = text.split(action_w, 1)[-1].strip().split()
                        if len(rest) >= 2:
                            actuator = rest[0]
                            sys_id   = rest[1]
                            if sys_id in self.smart_sys.systems:
                                return self.smart_sys.command(sys_id, actuator, state)
                        break
            if "РґРѕР±Р°РІСЊ РїСЂР°РІРёР»Рѕ" in t:
                # РґРѕР±Р°РІСЊ РїСЂР°РІРёР»Рѕ [СЃРёСЃС‚РµРјР°] РµСЃР»Рё [СѓСЃР»РѕРІРёРµ] С‚Рѕ [РґРµР№СЃС‚РІРёРµ]
                rest = text.split("РґРѕР±Р°РІСЊ РїСЂР°РІРёР»Рѕ", 1)[-1].strip()
                parts = rest.split(maxsplit=1)
                if len(parts) >= 2 and parts[0] in self.smart_sys.systems:
                    rule_text = parts[1]
                    if "РµСЃР»Рё" in rule_text and "С‚Рѕ" in rule_text:
                        cond = rule_text.split("РµСЃР»Рё")[1].split("С‚Рѕ")[0].strip()
                        act  = rule_text.split("С‚Рѕ")[1].strip()
                        return self.smart_sys.systems[parts[0\]\].add_rule(cond, act)
                return "Р¤РѕСЂРјР°С‚: РґРѕР±Р°РІСЊ РїСЂР°РІРёР»Рѕ [СЃРёСЃС‚РµРјР°] РµСЃР»Рё [СѓСЃР»РѕРІРёРµ] С‚Рѕ [РґРµР№СЃС‚РІРёРµ]"

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # IoT РњРћРЎРў (СѓСЃС‚СЂРѕР№СЃС‚РІР°, РїСЂРѕС‚РѕРєРѕР»С‹)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.iot_bridge:
            if any(k in t for k in ["iot СЃС‚Р°С‚СѓСЃ", "iot СѓСЃС‚СЂРѕР№СЃС‚РІР°", "СѓСЃС‚СЂРѕР№СЃС‚РІР° iot"]):
                return self.iot_bridge.status()
            if any(k in t for k in ["iot РїСЂРѕС‚РѕРєРѕР»С‹", "РїСЂРѕС‚РѕРєРѕР»С‹ iot", "РїСЂРѕРј РїСЂРѕС‚РѕРєРѕР»С‹", "РєР°РєРёРµ РїСЂРѕС‚РѕРєРѕР»С‹"]):
                return self._iot_protocols_help()
            if "Р·Р°СЂРµРіРёСЃС‚СЂРёСЂСѓР№ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ" in t or "РґРѕР±Р°РІСЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ" in t:
                # РґРѕР±Р°РІСЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [id] [С‚РёРї] [РїСЂРѕС‚РѕРєРѕР»] [Р°РґСЂРµСЃ] [РёРјСЏ]
                parts = text.split("СѓСЃС‚СЂРѕР№СЃС‚РІРѕ", 1)[-1].strip().split()
                if len(parts) >= 3:
                    dev_id, dtype, proto = parts[0], parts[1], parts[2]
                    addr = parts[3] if len(parts) > 3 else ""
                    name = parts[4] if len(parts) > 4 else dev_id
                    return self.iot_bridge.register_device(dev_id, dtype, proto, addr, name)
                return "Р¤РѕСЂРјР°С‚: РґРѕР±Р°РІСЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [id] [С‚РёРї] [РїСЂРѕС‚РѕРєРѕР»] [Р°РґСЂРµСЃ] [РёРјСЏ]"
            if "СЃС‚Р°С‚СѓСЃ СѓСЃС‚СЂРѕР№СЃС‚РІР°" in t or "РјРѕРЅРёС‚РѕСЂРёРЅРі СѓСЃС‚СЂРѕР№СЃС‚РІР°" in t:
                parts = text.split("СѓСЃС‚СЂРѕР№СЃС‚РІР°" if "СѓСЃС‚СЂРѕР№СЃС‚РІР°" in t else "СѓСЃС‚СЂРѕР№СЃС‚РІРѕ")[-1].strip().split()
                if parts:
                    return self.iot_bridge.device_status(parts[0])
                return "Р¤РѕСЂРјР°С‚: СЃС‚Р°С‚СѓСЃ СѓСЃС‚СЂРѕР№СЃС‚РІР° [id]"
            if "РїРѕРґРєР»СЋС‡Рё zigbee" in t:
                parts = text.split("РїРѕРґРєР»СЋС‡Рё zigbee")[-1].strip().split()
                host = parts[0] if parts else "localhost"
                port = int(parts[1]) if len(parts) > 1 else 1883
                return self.iot_bridge.connect_zigbee(host, port)
            if "РїРѕРґРєР»СЋС‡Рё lora" in t:
                parts = text.split("РїРѕРґРєР»СЋС‡Рё lora")[-1].strip().split()
                port = parts[0] if parts else "/dev/ttyUSB0"
                baud = int(parts[1]) if len(parts) > 1 else 9600
                return self.iot_bridge.connect_lora(port, baud)
            if "Р·Р°РїСѓСЃС‚Рё mesh" in t or "mesh СЃС‚Р°СЂС‚" in t:
                return self.iot_bridge.start_mesh()
            if "РїРѕРґРєР»СЋС‡Рё mqtt" in t:
                parts = text.split("РїРѕРґРєР»СЋС‡Рё mqtt")[-1].strip().split()
                host = parts[0] if parts else "localhost"
                port = int(parts[1]) if len(parts) > 1 else 1883
                return self.iot_bridge.connect_mqtt(host, port)
            if any(k in t for k in ["РєРѕРјР°РЅРґР° СѓСЃС‚СЂРѕР№СЃС‚РІСѓ", "РѕС‚РїСЂР°РІСЊ РєРѕРјР°РЅРґСѓ"]):
                parts = text.split("СѓСЃС‚СЂРѕР№СЃС‚РІСѓ" if "СѓСЃС‚СЂРѕР№СЃС‚РІСѓ" in t else "РєРѕРјР°РЅРґСѓ")[-1].strip().split()
                if len(parts) >= 2:
                    return self.iot_bridge.send_command(parts[0], parts[1],
                                                       parts[2] if len(parts) > 2 else None)
                return "Р¤РѕСЂРјР°С‚: РєРѕРјР°РЅРґР° СѓСЃС‚СЂРѕР№СЃС‚РІСѓ [id] [РєРѕРјР°РЅРґР°] [Р·РЅР°С‡РµРЅРёРµ]"

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # ARGOS IoT HUB (РїРѕР»РЅС‹Р№ СЂРѕСѓС‚РµСЂ РїСЂРѕС‚РѕРєРѕР»РѕРІ)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.iot_hub:
            _IOT_HUB_KEYS = (
                "iot С…Р°Р±", "iot hub", "С…Р°Р± СЃС‚Р°С‚СѓСЃ",
                "Р·Р°РїСѓСЃС‚Рё iot", "iot Р·Р°РїСѓСЃРє", "СЃС‚Р°СЂС‚ iot",
                "iot С‚РµР»РµРјРµС‚СЂРёСЏ", "С‚РµР»РµРјРµС‚СЂРёСЏ iot",
                "СѓРјРЅС‹Рµ СѓСЃС‚СЂРѕР№СЃС‚РІР°", "СѓРјРЅС‹Р№ РґРѕРј СЃС‚Р°С‚СѓСЃ",
            )
            if any(k in t for k in _IOT_HUB_KEYS):
                if any(k in t for k in ("Р·Р°РїСѓСЃС‚Рё iot", "iot Р·Р°РїСѓСЃРє", "СЃС‚Р°СЂС‚ iot")):
                    return self.iot_hub.start_all()
                if any(k in t for k in ("iot С‚РµР»РµРјРµС‚СЂРёСЏ", "С‚РµР»РµРјРµС‚СЂРёСЏ iot")):
                    tele = self.iot_hub.collect_telemetry()
                    if not tele:
                        return "рџ“Љ IoT С‚РµР»РµРјРµС‚СЂРёСЏ: РґР°РЅРЅС‹С… РЅРµС‚ (РЅРµС‚ Р°РєС‚РёРІРЅС‹С… РґР°С‚С‡РёРєРѕРІ)"
                    return "рџ“Љ IoT С‚РµР»РµРјРµС‚СЂРёСЏ:\n" + "\n".join(f"  {k}: {v}" for k, v in tele.items())
                # РРЅР°С‡Рµ вЂ” РѕР±С‰РёР№ СЃС‚Р°С‚СѓСЃ С…Р°Р±Р°
                return self.iot_hub.status()
            # Р”РµР»РµРіРёСЂСѓРµРј РѕСЃС‚Р°С‚РѕРє handle_command С…Р°Р±Р°
            try:
                _hub_result = self.iot_hub.handle_command(t)
                if _hub_result is not None:
                    return _hub_result
            except Exception as _hub_e:
                log.debug("iot_hub.handle_command: %s", _hub_e)

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # РџР РћРњР«РЁР›Р•РќРќР«Р• РџР РћРўРћРљРћР›Р« (KNX, LonWorks, M-Bus, OPC-UA)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.industrial:
            if any(k in t for k in [
                "industrial СЃС‚Р°С‚СѓСЃ", "РїСЂРѕРјС‹С€Р»РµРЅРЅС‹Рµ РїСЂРѕС‚РѕРєРѕР»С‹",
                "industrial discovery", "industrial РїРѕРёСЃРє",
                "industrial СѓСЃС‚СЂРѕР№СЃС‚РІР°",
                "knx РїРѕРґРєР»СЋС‡Рё", "opcua РїРѕРґРєР»СЋС‡Рё",
                "mbus serial", "mbus tcp",
                "opcua browse", "opcua С‡РёС‚Р°Р№", "opcua РїРёС€Рё",
                "knx С‡РёС‚Р°Р№", "knx РїРёС€Рё",
                "lonworks С‡РёС‚Р°Р№", "lonworks РїРёС€Рё",
            ]):
                return self.industrial.handle_command(t)

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # MESH-РЎР•РўР¬ (Zigbee, LoRa, WiFi Mesh)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.mesh_net:
            if any(k in t for k in ["СЃС‚Р°С‚СѓСЃ mesh", "mesh СЃС‚Р°С‚СѓСЃ", "mesh СЃРµС‚СЊ", "mesh-СЃРµС‚СЊ"]):
                return self.mesh_net.status_report()
            if "Р·Р°РїСѓСЃС‚Рё zigbee" in t:
                parts = text.split("Р·Р°РїСѓСЃС‚Рё zigbee")[-1].strip().split()
                port = parts[0] if parts else "/dev/ttyUSB0"
                baud = int(parts[1]) if len(parts) > 1 else 115200
                return self.mesh_net.start_zigbee(port, baud)
            if "Р·Р°РїСѓСЃС‚Рё lora" in t:
                parts = text.split("Р·Р°РїСѓСЃС‚Рё lora")[-1].strip().split()
                port = parts[0] if parts else "/dev/ttyUSB1"
                baud = int(parts[1]) if len(parts) > 1 else 9600
                return self.mesh_net.start_lora(port, baud)
            if "Р·Р°РїСѓСЃС‚Рё wifi mesh" in t:
                ssid = text.split("Р·Р°РїСѓСЃС‚Рё wifi mesh")[-1].strip() or "ArgosNet"
                return self.mesh_net.start_wifi_mesh(ssid)
            if "РґРѕР±Р°РІСЊ mesh СѓСЃС‚СЂРѕР№СЃС‚РІРѕ" in t:
                parts = text.split("mesh СѓСЃС‚СЂРѕР№СЃС‚РІРѕ")[-1].strip().split()
                if len(parts) >= 3:
                    return self.mesh_net.add_device(parts[0], parts[1], parts[2],
                                                    parts[3] if len(parts) > 3 else "",
                                                    parts[4] if len(parts) > 4 else "")
                return "Р¤РѕСЂРјР°С‚: РґРѕР±Р°РІСЊ mesh СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [id] [РїСЂРѕС‚РѕРєРѕР»] [Р°РґСЂРµСЃ] [РёРјСЏ] [РєРѕРјРЅР°С‚Р°]"
            if "mesh broadcast" in t or "mesh СЂР°СЃСЃС‹Р»РєР°" in t:
                parts = text.split("broadcast" if "broadcast" in t else "СЂР°СЃСЃС‹Р»РєР°")[-1].strip().split(maxsplit=1)
                if len(parts) >= 2:
                    return self.mesh_net.broadcast(parts[0], parts[1])
                return "Р¤РѕСЂРјР°С‚: mesh broadcast [РїСЂРѕС‚РѕРєРѕР»] [РєРѕРјР°РЅРґР°]"
            if "РїСЂРѕС€РµР№ gateway" in t:
                parts = text.split("gateway")[-1].strip().split()
                if len(parts) >= 1:
                    port = parts[0]
                    fw   = parts[1] if len(parts) > 1 else "zigbee_gateway"
                    return self.mesh_net.flash_gateway(port, fw)
                return "Р¤РѕСЂРјР°С‚: РїСЂРѕС€РµР№ gateway [РїРѕСЂС‚] [РїСЂРѕС€РёРІРєР°]"

        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        # IoT РЁР›Р®Р—Р« (СЃРѕР·РґР°РЅРёРµ, РєРѕРЅС„РёРі, РїСЂРѕС€РёРІРєР°)
        # в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
        if self.gateway_mgr:
            if any(k in t for k in ["СЃРїРёСЃРѕРє С€Р»СЋР·РѕРІ", "С€Р»СЋР·С‹", "gateways"]):
                return self.gateway_mgr.list_gateways()
            if any(k in t for k in ["С€Р°Р±Р»РѕРЅС‹ С€Р»СЋР·РѕРІ", "С‚РёРїС‹ С€Р»СЋР·РѕРІ"]):
                return self.gateway_mgr.list_templates()
            if any(k in t for k in ["РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»", "РІС‹СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»", "РЅР°СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»"]):
                tail = text
                for marker in ("РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»", "РІС‹СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»", "РЅР°СѓС‡Рё РїСЂРѕС‚РѕРєРѕР»"):
                    if marker in t:
                        tail = text.split(marker, 1)[-1].strip()
                        break
                parts = tail.split()
                if len(parts) >= 2:
                    template = parts[0]
                    protocol = parts[1]
                    firmware = parts[2] if len(parts) > 2 else ""
                    description = " ".join(parts[3:]) if len(parts) > 3 else f"РђРІС‚РѕС€Р°Р±Р»РѕРЅ РґР»СЏ {protocol}"
                    return self.gateway_mgr.register_template(
                        name=template,
                        description=description,
                        protocol=protocol,
                        firmware=firmware,
                    )
                return ("Р¤РѕСЂРјР°С‚: РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР» [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [РїСЂРѕС€РёРІРєР°?] [РѕРїРёСЃР°РЅРёРµ?]\n"
                        "РџСЂРёРјРµСЂ: РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР» bt_gateway bluetooth custom_bridge BLE С€Р»СЋР·")
            if any(k in t for k in ["РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ", "РІС‹СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ", "РёР·СѓС‡Рё СѓСЃС‚СЂРѕС†", "РІС‹СѓС‡Рё СѓСЃС‚СЂРѕС†"]):
                tail = text
                for marker in ("РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ", "РІС‹СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ", "РёР·СѓС‡Рё СѓСЃС‚СЂРѕС†", "РІС‹СѓС‡Рё СѓСЃС‚СЂРѕС†"):
                    if marker in t:
                        tail = text.split(marker, 1)[-1].strip()
                        break
                parts = tail.split()
                if len(parts) >= 2:
                    template = parts[0]
                    protocol = parts[1]
                    hardware = " ".join(parts[2:]) if len(parts) > 2 else "Generic gateway"
                    return self.gateway_mgr.register_template(
                        name=template,
                        description=f"РЁР°Р±Р»РѕРЅ СѓСЃС‚СЂРѕР№СЃС‚РІР°: {hardware}",
                        protocol=protocol,
                        hardware=hardware,
                    )
                return ("Р¤РѕСЂРјР°С‚: РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [hardware?]\n"
                        "РџСЂРёРјРµСЂ: РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ rtu_bridge modbus USB-RS485 Р°РґР°РїС‚РµСЂ")
            if "СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ" in t or "СЃРѕР±РµСЂРё РїСЂРѕС€РёРІРєСѓ" in t:
                # "СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ СЃ РЅСѓР»СЏ [СѓСЃС‚СЂРѕР№СЃС‚РІРѕ]" вЂ” СѓРјРЅС‹Р№ РїРѕРёСЃРє РѕРЅР»Р°Р№РЅ
                if "СЃ РЅСѓР»СЏ" in t or "from scratch" in t or "РѕРЅР»Р°Р№РЅ" in t:
                    device_query = re.sub(
                        r"(СЃРѕР·РґР°Р№|СЃРѕР±РµСЂРё)\s+РїСЂРѕС€РёРІРєСѓ\s+(СЃ\s+РЅСѓР»СЏ|from\s+scratch|РѕРЅР»Р°Р№РЅ)\s*",
                        "", t, flags=re.IGNORECASE
                    ).strip() or text
                    try:
                        from src.smart_firmware_researcher import SmartFirmwareResearcher
                        r = SmartFirmwareResearcher()
                        result = r.research_and_build(device_query)
                        return result["message"]
                    except Exception as e:
                        return f"вќЊ SmartFirmware: {e}"

                # СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ [id] [С€Р°Р±Р»РѕРЅ] [РїРѕСЂС‚?]
                tail = text.split("РїСЂРѕС€РёРІРєСѓ", 1)[-1].strip().split()
                if len(tail) >= 2:
                    gw_id = tail[0]
                    template = tail[1]
                    port = tail[2] if len(tail) > 2 else None
                    return self.gateway_mgr.prepare_firmware(gw_id, template, port)
                # РћРґРёРЅ Р°СЂРіСѓРјРµРЅС‚ вЂ” СѓРјРЅС‹Р№ РїРѕРёСЃРє РїРѕ РёРјРµРЅРё СѓСЃС‚СЂРѕР№СЃС‚РІР°
                if len(tail) == 1:
                    try:
                        from src.smart_firmware_researcher import SmartFirmwareResearcher
                        r = SmartFirmwareResearcher()
                        result = r.research_and_build(tail[0])
                        return result["message"]
                    except Exception as e:
                        pass
                return f"Р¤РѕСЂРјР°С‚: СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ [id] [С€Р°Р±Р»РѕРЅ] [РїРѕСЂС‚]\n{self.gateway_mgr.list_templates()}"
            if "СЃРѕР·РґР°Р№ С€Р»СЋР·" in t or "СЃРѕР·РґР°Р№ gateway" in t:
                parts = text.split("С€Р»СЋР·" if "С€Р»СЋР·" in t else "gateway")[-1].strip().split()
                if len(parts) >= 2:
                    return self.gateway_mgr.create_gateway(parts[0], parts[1])
                return f"Р¤РѕСЂРјР°С‚: СЃРѕР·РґР°Р№ С€Р»СЋР· [id] [С€Р°Р±Р»РѕРЅ]\n{self.gateway_mgr.list_templates()}"
            if "РїСЂРѕС€РµР№ С€Р»СЋР·" in t or "flash gateway" in t:
                parts = text.split("С€Р»СЋР·" if "С€Р»СЋР·" in t else "gateway")[-1].strip().split()
                if parts:
                    port = parts[1] if len(parts) > 1 else None
                    return self.gateway_mgr.flash_gateway(parts[0], port)
                return "Р¤РѕСЂРјР°С‚: РїСЂРѕС€РµР№ С€Р»СЋР· [id] [РїРѕСЂС‚]"
            if any(k in t for k in ["Р·РґРѕСЂРѕРІСЊРµ С€Р»СЋР·РѕРІ", "health С€Р»СЋР·РѕРІ", "РїСЂРѕРІРµСЂСЊ С€Р»СЋР·С‹"]):
                parts = text.split()
                gw_id = parts[-1] if len(parts) >= 3 and parts[-1] not in {"С€Р»СЋР·РѕРІ", "С€Р»СЋР·С‹"} else None
                return self.gateway_mgr.health_check(gw_id)
            if "РѕС‚РєР°С‚ РїСЂРѕС€РёРІРєРё" in t:
                parts = text.split("РѕС‚РєР°С‚ РїСЂРѕС€РёРІРєРё", 1)[-1].strip().split()
                if not parts:
                    return "Р¤РѕСЂРјР°С‚: РѕС‚РєР°С‚ РїСЂРѕС€РёРІРєРё [id] [С€Р°РіРѕРІ?]"
                steps = 1
                if len(parts) > 1:
                    try:
                        steps = max(1, int(parts[1]))
                    except Exception:
                        steps = 1
                return self.gateway_mgr.rollback_firmware(parts[0], steps)
            if "РєРѕРЅС„РёРі С€Р»СЋР·Р°" in t:
                gw_id = text.split("РєРѕРЅС„РёРі С€Р»СЋР·Р°")[-1].strip().split()[0] if text.split("РєРѕРЅС„РёРі С€Р»СЋР·Р°")[-1].strip() else ""
                if gw_id:
                    return self.gateway_mgr.get_config(gw_id)
                return "Р¤РѕСЂРјР°С‚: РєРѕРЅС„РёРі С€Р»СЋР·Р° [id]"

        # в”Ђв”Ђ РљРІР°РЅС‚РѕРІС‹Р№ РѕСЂР°РєСѓР» в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РѕСЂР°РєСѓР» СЃС‚Р°С‚СѓСЃ", "oracle status", "quantum oracle"]):
            try:
                from src.quantum.oracle import QuantumOracle
                return QuantumOracle().status()
            except Exception as e:
                return f"QuantumOracle: {e}"
        if any(k in t for k in ["РѕСЂР°РєСѓР» СЃРµРјСЏ", "oracle seed", "quantum seed"]):
            try:
                from src.quantum.oracle import QuantumOracle
                seed = QuantumOracle().generate_seed(256)
                return f"рџ”® РљРІР°РЅС‚РѕРІРѕРµ СЃРµРјСЏ ({len(seed)*8} Р±РёС‚): {seed.hex()[:32]}вЂ¦"
            except Exception as e:
                return f"QuantumOracle СЃРµРјСЏ: {e}"
        if any(k in t for k in ["РѕСЂР°РєСѓР» СЂРµР¶РёРј", "oracle mode", "СЂРµР¶РёРј oracle", "РѕСЂР°РєСѓР» СЃРѕСЃС‚РѕСЏРЅРёРµ"]):
            try:
                from src.quantum.logic import QuantumEngine, STATES
                q = QuantumEngine()
                return f"рџ”® Oracle СЂРµР¶РёРј | РЎРѕСЃС‚РѕСЏРЅРёРµ: {q.state} вЂ” {STATES.get(q.state, '')}"
            except Exception as e:
                return f"Oracle СЂРµР¶РёРј: {e}"

        # в”Ђв”Ђ ESP32-2432S024 USB РјРѕСЃС‚ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["РїРѕРґРєР»СЋС‡Рё esp", "Р·Р°РїСѓСЃС‚Рё РјРѕСЃС‚", "esp32 РјРѕСЃС‚",
                                  "esp32 СЃС‚Р°СЂС‚", "esp bridge", "РѕС‚РєР»СЋС‡Рё esp",
                                  "СЃС‚РѕРї РјРѕСЃС‚", "СЃС‚Р°С‚СѓСЃ esp", "esp32 СЃС‚Р°С‚СѓСЃ",
                                  "РјРѕСЃС‚ СЃС‚Р°С‚СѓСЃ", "РїРѕСЂС‚С‹ usb", "com РїРѕСЂС‚С‹",
                                  "esp РІРµР±", "esp web", "РѕС‚РєСЂРѕР№ esp",
                                  "РїСЂРѕС€РёС‚СЊ esp", "РїСЂРѕС€РµР№ esp",
                                  "РѕР±РЅРѕРІРё esp", "РѕР±РЅРѕРІРё esp32",
                                  "flash esp", "flash esp32",
                                  "ota esp", "СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ esp", "РїСЂРѕС€РёРІРєР° esp32"]):
            try:
                from src.skills.esp32_usb_bridge import handle as _esp_handle
                result = _esp_handle(text, core=self)
                if result is not None:
                    return result
            except Exception as e:
                return f"вќЊ ESP32 РјРѕСЃС‚: {e}"

        # в”Ђв”Ђ USB С‚РѕС‡РєР° РґРѕСЃС‚СѓРїР° + РІРµР±-РјРѕСЂРґР° в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["Р·Р°РїСѓСЃС‚Рё С‚РѕС‡РєСѓ РґРѕСЃС‚СѓРїР°", "usb ap ", "С‚РѕС‡РєР° РґРѕСЃС‚СѓРїР°",
                                  "usb РіР°РґР¶РµС‚", "usb gadget", "РІРµР± РјРѕСЂРґР°", "РІРµР±-РјРѕСЂРґР°",
                                  "webui", "web ui", "СЃС‚РѕРї С‚РѕС‡РєРё РґРѕСЃС‚СѓРїР°", "ap СЃС‚Р°С‚СѓСЃ",
                                  "Р·Р°РїСѓСЃС‚Рё РІРµР±", "web interface", "РёРЅС‚РµСЂС„РµР№СЃ argos",
                                  "С‚РѕС‡РєР° РґРѕСЃС‚СѓРїР° СЃС‚Р°С‚СѓСЃ", "СЃС‚Р°С‚СѓСЃ С‚РѕС‡РєРё РґРѕСЃС‚СѓРїР°",
                                  "wifi ap", "wifi С‚РѕС‡РєР°"]):
            try:
                from src.skills.usb_access_point import handle as _usb_handle
                result = _usb_handle(text, core=self)
                if result is not None:
                    return result
            except Exception as e:
                return f"вќЊ USB AP: {e}"

        # в”Ђв”Ђ РљРѕР»РёР±СЂРё в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in ["Р·Р°РїСѓСЃС‚Рё РєРѕР»РёР±СЂРё", "СЃС‚Р°СЂС‚ РєРѕР»РёР±СЂРё", "colibri start",
                                  "РєРѕР»РёР±СЂРё Р·Р°РїСѓСЃРє", "РІРєР»СЋС‡Рё РєРѕР»РёР±СЂРё"]):
            try:
                from src.connectivity.colibri_daemon import start as _col_start
                if not hasattr(self, "_colibri_daemon") or not self._colibri_daemon:
                    from src.connectivity.colibri_daemon import ColibriDaemon
                    self._colibri_daemon = ColibriDaemon()
                result = self._colibri_daemon.start()
                return result
            except Exception as e:
                return f"вќЊ РљРѕР»РёР±СЂРё Р·Р°РїСѓСЃРє: {e}"

        if any(k in t for k in ["РѕСЃС‚Р°РЅРѕРІРё РєРѕР»РёР±СЂРё", "СЃС‚РѕРї РєРѕР»РёР±СЂРё", "colibri stop",
                                  "РІС‹РєР»СЋС‡Рё РєРѕР»РёР±СЂРё"]):
            try:
                if hasattr(self, "_colibri_daemon") and self._colibri_daemon:
                    return self._colibri_daemon.stop()
                return "рџђ¦ РљРѕР»РёР±СЂРё РЅРµ Р·Р°РїСѓС‰РµРЅ"
            except Exception as e:
                return f"вќЊ РљРѕР»РёР±СЂРё СЃС‚РѕРї: {e}"

        if any(k in t for k in ["РєРѕР»РёР±СЂРё СЃС‚Р°С‚СѓСЃ", "СЃС‚Р°С‚СѓСЃ РєРѕР»РёР±СЂРё", "colibri status",
                                  "colibri СЃС‚Р°С‚СѓСЃ", "РєРѕР»РёР±СЂРё"]):
            try:
                if hasattr(self, "_colibri_daemon") and self._colibri_daemon:
                    return self._colibri_daemon.status_str()
                from src.connectivity.colibri_daemon import ColibriDaemon
                return "рџђ¦ РљРѕР»РёР±СЂРё: РјРѕРґСѓР»СЊ РґРѕСЃС‚СѓРїРµРЅ. Р”Р»СЏ Р·Р°РїСѓСЃРєР°: 'Р·Р°РїСѓСЃС‚Рё РєРѕР»РёР±СЂРё'."
            except ImportError:
                return "вќЊ РљРѕР»РёР±СЂРё: РјРѕРґСѓР»СЊ РЅРµ РЅР°Р№РґРµРЅ"
            except Exception as e:
                return f"рџђ¦ РљРѕР»РёР±СЂРё: {e}"

        # в”Ђв”Ђ Р¤СѓРЅРєС†РёРё РђСЂРіРѕСЃРљРѕСЂРµ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if any(k in t for k in [
            "С„СѓРЅРєС†РёРё Р°СЂРіРѕСЃРєРѕСЂРµ", "Р°СЂРіРѕСЃРєРѕСЂРµ С„СѓРЅРєС†РёРё", "С„СѓРЅРєС†РёРё СЏРґСЂР°",
            "РїСЂРѕРІРµСЂСЊ Р°СЂРіРѕСЃРєРѕСЂРµ", "Р°СЂРіРѕСЃРєРѕСЂРµ РїСЂРѕРІРµСЂСЊ", "РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё Р°СЂРіРѕСЃРєРѕСЂРµ",
            "Р°СЂРіРѕСЃРєРѕСЂРµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё", "С‡С‚Рѕ СѓРјРµРµС‚ Р°СЂРіРѕСЃРєРѕСЂРµ", "argoscore С„СѓРЅРєС†РёРё",
            "argoscore РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё", "СЃРїРёСЃРѕРє С„СѓРЅРєС†РёР№ Р°СЂРіРѕСЃР°", "С„СѓРЅРєС†РёРё argos",
            "С„СѓРЅРєС†РёРё Р°СЂРіРѕСЃР°", "СЃРїРёСЃРѕРє С„СѓРЅРєС†РёР№",
        ]):
            return self._argoscore_functions()

        # в”Ђв”Ђ РџРѕРјРѕС‰СЊ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        if t.strip() in ("РїРѕРјРѕС‰СЊ", "РєРѕРјР°РЅРґС‹", "С‡С‚Рѕ СѓРјРµРµС€СЊ", "help", "?"):
            return self._help()

        return None

    def _operator_incident(self, admin) -> str:
        lines = ["рџљЁ РћРџР•Р РђРўРћР : РРќР¦РР”Р•РќРў"]
        lines.append(admin.get_stats())
        if self.alerts:
            lines.append(self.alerts.status())
        if self.gateway_mgr:
            lines.append(self.gateway_mgr.health_check())
        lines.append("Р РµРєРѕРјРµРЅРґР°С†РёСЏ: Р·Р°РїСѓСЃС‚Рё 'РѕРїРµСЂР°С‚РѕСЂ РґРёР°РіРЅРѕСЃС‚РёРєР°' РґР»СЏ РґРµС‚Р°Р»СЊРЅРѕРіРѕ Р°РЅР°Р»РёР·Р°.")
        return "\n\n".join(lines)

    def _operator_diagnostics(self, admin) -> str:
        lines = ["рџ©є РћРџР•Р РђРўРћР : Р”РРђР“РќРћРЎРўРРљРђ"]
        lines.append(admin.get_stats())
        lines.append(self.sensors.get_full_report())
        if self.iot_bridge:
            lines.append(self.iot_bridge.status())
        if self.industrial:
            lines.append(self.industrial.status())
        if self.platform_admin:
            lines.append(self.platform_admin.status())
        if self.mesh_net:
            lines.append(self.mesh_net.status_report())
        if self.gateway_mgr:
            lines.append(self.gateway_mgr.health_check())
        return "\n\n".join(lines)

    def _operator_recovery(self) -> str:
        lines = ["рџ› пёЏ РћРџР•Р РђРўРћР : Р’РћРЎРЎРўРђРќРћР’Р›Р•РќРР•"]
        if self.gateway_mgr:
            lines.append(self.gateway_mgr.health_check())
        lines.append("Р§РµРє-Р»РёСЃС‚:\n  1) РџСЂРѕРІРµСЂРёС‚СЊ РїРѕСЂС‚С‹/СЃРµС‚СЊ\n  2) РџРµСЂРµРїРѕРґРіРѕС‚РѕРІРёС‚СЊ РїСЂРѕС€РёРІРєСѓ\n  3) Р’С‹РїРѕР»РЅРёС‚СЊ РѕС‚РєР°С‚ РїСЂРѕС€РёРІРєРё РїСЂРё РґРµРіСЂР°РґР°С†РёРё")
        return "\n\n".join(lines)

    def _ai_modes_diagnostic(self) -> str:
        import platform, sys, threading

        # в”Ђв”Ђ РР в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        ai_mode = self.ai_mode_label() if hasattr(self, "ai_mode_label") else str(getattr(self, "ai_mode", "unknown"))
        try:
            from src.skills.evolution import ArgosEvolution
            evo_ready = "вњ…"
        except Exception:
            evo_ready = "вљ пёЏ РЅРµ СѓСЃС‚Р°РЅРѕРІР»РµРЅ"
        learning  = self.own_model.status() if getattr(self, "own_model", None) else "вљ пёЏ РЅРµРґРѕСЃС‚СѓРїРµРЅ"
        cognition = "вњ…" if getattr(self, "memory", None) else "вќЊ"
        curiosity = self.curiosity.status() if getattr(self, "curiosity", None) else "вљ пёЏ"
        dialog_ctx = "вњ…" if getattr(self, "context", None) else "вќЊ"

        # в”Ђв”Ђ Р–Р•Р›Р•Р—Рћ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        is_win    = platform.system() == "Windows"
        is_android = getattr(self, "_android", False) or "ANDROID_ROOT" in __import__("os").environ
        cpu_count = __import__("psutil").cpu_count(logical=True) if True else 0
        py_threads = threading.active_count()
        try:
            import psutil as _ps
            bat = _ps.sensors_battery()
            power_str = f"рџ”‹ {bat.percent:.0f}%" if bat else "вњ… СЃС‚Р°С†РёРѕРЅР°СЂРЅС‹Р№"
        except Exception:
            power_str = "вњ… СЃС‚Р°С†РёРѕРЅР°СЂРЅС‹Р№"

        # в”Ђв”Ђ GPU Windows в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        gpu_info = "вљ пёЏ РЅРµ РѕР±РЅР°СЂСѓР¶РµРЅ"
        if is_win:
            # РњРµС‚РѕРґ 1: nvidia-smi
            try:
                import subprocess as _sp
                r = _sp.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total",
                              "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=4)
                if r.returncode == 0 and r.stdout.strip():
                    parts = r.stdout.strip().split(",")
                    name = parts[0].strip()
                    util = parts[1].strip() if len(parts) > 1 else "?"
                    vram_used = parts[2].strip() if len(parts) > 2 else "?"
                    vram_total = parts[3].strip() if len(parts) > 3 else "?"
                    gpu_info = f"вњ… {name} | {util}% | VRAM {vram_used}/{vram_total} РњР‘"
            except Exception:
                pass
            # РњРµС‚РѕРґ 2: WMI/PowerShell
            if "вљ пёЏ" in gpu_info:
                try:
                    import subprocess as _sp
                    r = _sp.run(
                        ["powershell", "-NoProfile", "-Command",
                         "Get-WmiObject Win32_VideoController | "
                         "Select-Object -First 1 Name,AdapterRAM | "
                         "Format-Table -HideTableHeaders"],
                        capture_output=True, text=True, timeout=5, encoding="cp866"
                    )
                    if r.returncode == 0 and r.stdout.strip():
                        line = " ".join(r.stdout.strip().split())
                        gpu_info = f"вњ… {line[:60]}" if line else "вљ пёЏ WMI РЅРµС‚ РґР°РЅРЅС‹С…"
                except Exception:
                    pass
        else:
            # Linux/Mac: psutil + /sys
            from src.connectivity.system_health import get_gpu
            gpus = get_gpu()
            if gpus:
                g = gpus[0]
                if "util" in g:
                    gpu_info = f"вњ… {g.get('name','?')[:30]} | {g['util']}% | {g.get('vram_used_mb',0)}/{g.get('vram_total_mb',0)} РњР‘"
                else:
                    gpu_info = f"вњ… {g.get('vendor','')} {g.get('name','?')[:30]}"

        # в”Ђв”Ђ Р‘РР‘Р›РРћРўР•РљР (С‡РµСЃС‚РЅР°СЏ РїСЂРѕРІРµСЂРєР°) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        def _chk(mod):
            try:
                import importlib.util
                return "вњ…" if importlib.util.find_spec(mod) is not None else "вќЊ"
            except Exception:
                return "вќЊ"

        jnius_ok    = _chk("jnius")   # С‚РѕР»СЊРєРѕ РЅР° СЂРµР°Р»СЊРЅРѕРј Android
        kivy_ok     = _chk("kivy")
        plyer_ok    = _chk("plyer")
        pyserial_ok = _chk("serial")
        ctk_ok      = _chk("customtkinter")

        # OTG СЃС‚Р°С‚СѓСЃ (С‡РµСЃС‚РЅС‹Р№)
        otg = getattr(self, "otg", None)
        if otg:
            otg_devices = getattr(otg, "_devices", []) or []
            otg_str = f"вњ… Р°РєС‚РёРІРµРЅ | СѓСЃС‚СЂРѕР№СЃС‚РІ: {len(otg_devices)}"
        else:
            otg_str = "вљ пёЏ РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅ"

        # в”Ђв”Ђ GRIST / P2P SYNC в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        _grist = getattr(self, "grist", None)
        grist_ok = "вњ…" if (_grist and getattr(_grist, "_configured", False)) else "вќЊ"

        # в”Ђв”Ђ РЎР‘РћР РљРђ РћРўР’Р•РўРђ в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
        lines = [
            "рџ§Є Р”РРђР“РќРћРЎРўРРљРђ РЎРРЎРўР•РњР« Р РР\n",
            "рџ“Ў РРЎРљРЈРЎРЎРўР’Р•РќРќР«Р™ РРќРўР•Р›Р›Р•РљРў:",
            f"  вЂў Р РµР¶РёРј РР: {ai_mode}",
            f"  вЂў РњРѕРґРµР»СЊ Ollama: {__import__('os').getenv('OLLAMA_MODEL','poilopr57/Argoss')}",
            f"  вЂў Р­РІРѕР»СЋС†РёСЏ РЅР°РІС‹РєРѕРІ: {evo_ready}",
            f"  вЂў РћР±СѓС‡РµРЅРёРµ РјРѕРґРµР»Рё: {learning}",
            f"  вЂў РЎРёРЅС…СЂРѕРЅРёР·Р°С†РёСЏ Р·РЅР°РЅРёР№ (Р“РћРЎРў P2P Grist): {grist_ok}",
            f"  вЂў РџРѕР·РЅР°РЅРёРµ (РїР°РјСЏС‚СЊ): {cognition}",
            f"  вЂў Р›СЋР±РѕРїС‹С‚СЃС‚РІРѕ: {curiosity}",
            f"  вЂў Р”РёР°Р»РѕРіРѕРІС‹Р№ РєРѕРЅС‚РµРєСЃС‚: {dialog_ctx}",
            "",
            "рџ–Ґ РђРџРџРђР РђРўРЈР Рђ:",
            f"  вЂў РџР»Р°С‚С„РѕСЂРјР°:    {platform.system()} {platform.release()} {platform.machine()}",
            f"  вЂў Р РµР¶РёРј:        {'Android' if is_android else 'Desktop/Server'}",
            f"  вЂў CPU РїРѕС‚РѕРєРё:   {cpu_count} Р»РѕРіРёС‡РµСЃРєРёС… | Python РїРѕС‚РѕРєРѕРІ: {py_threads}",
            f"  вЂў РџРёС‚Р°РЅРёРµ:      {power_str}",
            f"  вЂў GPU:          {gpu_info}",
            "",
            "рџ“¦ Р‘РР‘Р›РРћРўР•РљР:",
            f"  вЂў customtkinter (GUI Desktop):   {ctk_ok}",
            f"  вЂў pyserial (USB Serial/COM):     {pyserial_ok}",
            f"  вЂў kivy (Android UI):             {kivy_ok}",
            f"  вЂў plyer (Android sensors):       {plyer_ok}",
            f"  вЂў jnius (Android USB API):       {jnius_ok}" +
                (" в†ђ С‚РѕР»СЊРєРѕ РЅР° СЂРµР°Р»СЊРЅРѕРј Android" if jnius_ok == "вќЊ" else ""),
            "",
            "рџ”Њ OTG / USB HOST:",
            f"  вЂў РЎС‚Р°С‚СѓСЃ:       {otg_str}",
            f"  вЂў pyserial:     {pyserial_ok} (PC COM-РїРѕСЂС‚С‹)",
            f"  вЂў jnius:        {jnius_ok} (С‚СЂРµР±СѓРµС‚ Android)",
        ]
        return "\n".join(lines)

    def _help(self) -> str:
        return """рџ‘ЃпёЏ РђР Р“РћРЎ UNIVERSAL OS вЂ” РљРћРњРђРќР”Р«:

рџ“Љ РњРћРќРРўРћР РРќР“
  СЃС‚Р°С‚СѓСЃ СЃРёСЃС‚РµРјС‹ В· С‡РµРє-Р°Рї В· СЃРїРёСЃРѕРє РїСЂРѕС†РµСЃСЃРѕРІ
  Р°Р»РµСЂС‚С‹ В· СѓСЃС‚Р°РЅРѕРІРё РїРѕСЂРѕРі [РјРµС‚СЂРёРєР°] [%] В· РіРµРѕР»РѕРєР°С†РёСЏ

рџ“Ѓ Р¤РђР™Р›Р«
  С„Р°Р№Р»С‹ [РїСѓС‚СЊ] В· РїСЂРѕС‡РёС‚Р°Р№ С„Р°Р№Р» [РїСѓС‚СЊ]
  СЃРѕР·РґР°Р№ С„Р°Р№Р» [РёРјСЏ] [С‚РµРєСЃС‚] В· СѓРґР°Р»Рё С„Р°Р№Р» [РїСѓС‚СЊ]

вљ™пёЏ РЎРРЎРўР•РњРђ
  РєРѕРЅСЃРѕР»СЊ [РєРѕРјР°РЅРґР°] В· СѓР±РµР№ РїСЂРѕС†РµСЃСЃ [РёРјСЏ]
  СЂРµРїР»РёРєР°С†РёСЏ В· Р·Р°РіСЂСѓР·С‡РёРє В· РѕР±РЅРѕРІРё grub
  СѓСЃС‚Р°РЅРѕРІРё Р°РІС‚РѕР·Р°РїСѓСЃРє В· РІРµР±-РїР°РЅРµР»СЊ
    РіРѕРјРµРѕСЃС‚Р°Р· СЃС‚Р°С‚СѓСЃ В· РіРѕРјРµРѕСЃС‚Р°Р· РІРєР»/РІС‹РєР»
    Р»СЋР±РѕРїС‹С‚СЃС‚РІРѕ СЃС‚Р°С‚СѓСЃ В· Р»СЋР±РѕРїС‹С‚СЃС‚РІРѕ РІРєР»/РІС‹РєР» В· Р»СЋР±РѕРїС‹С‚СЃС‚РІРѕ СЃРµР№С‡Р°СЃ
        git СЃС‚Р°С‚СѓСЃ В· git РєРѕРјРјРёС‚ [msg] В· git РїСѓС€ В· git Р°РІС‚РѕРєРѕРјРјРёС‚ Рё РїСѓС€ [msg]

рџ‘ЃпёЏ VISION (РЅСѓР¶РµРЅ Gemini API)
  РїРѕСЃРјРѕС‚СЂРё РЅР° СЌРєСЂР°РЅ В· С‡С‚Рѕ РЅР° СЌРєСЂР°РЅРµ
  РїРѕСЃРјРѕС‚СЂРё РІ РєР°РјРµСЂСѓ В· Р°РЅР°Р»РёР· С„РѕС‚Рѕ [РїСѓС‚СЊ]

рџ¤– РђР“Р•РќРў (С†РµРїРѕС‡РєРё Р·Р°РґР°С‡)
  СЃС‚Р°С‚СѓСЃ в†’ Р·Р°С‚РµРј РєСЂРёРїС‚Рѕ в†’ РїРѕС‚РѕРј РґР°Р№РґР¶РµСЃС‚
  РѕС‚С‡С‘С‚ Р°РіРµРЅС‚Р° В· РѕСЃС‚Р°РЅРѕРІРё Р°РіРµРЅС‚Р°

рџ§  РџРђРњРЇРўР¬
  Р·Р°РїРѕРјРЅРё [РєР»СЋС‡]: [Р·РЅР°С‡РµРЅРёРµ] В· С‡С‚Рѕ С‚С‹ Р·РЅР°РµС€СЊ
    РЅР°Р№РґРё РІ РїР°РјСЏС‚Рё [Р·Р°РїСЂРѕСЃ] В· РїРѕРёСЃРє РїРѕ РїР°РјСЏС‚Рё [Р·Р°РїСЂРѕСЃ]
    РіСЂР°С„ Р·РЅР°РЅРёР№ В· СЃРІСЏР·Рё РїР°РјСЏС‚Рё
  Р·Р°РїРёС€Рё Р·Р°РјРµС‚РєСѓ [РЅР°Р·РІР°РЅРёРµ]: [С‚РµРєСЃС‚]
  РјРѕРё Р·Р°РјРµС‚РєРё В· РїСЂРѕС‡РёС‚Р°Р№ Р·Р°РјРµС‚РєСѓ [в„–]

вЏ° Р РђРЎРџРРЎРђРќРР•
  РєР°Р¶РґС‹Рµ 2 С‡Р°СЃР° [Р·Р°РґР°С‡Р°] В· РІ 09:00 [Р·Р°РґР°С‡Р°]
  С‡РµСЂРµР· 30 РјРёРЅ [Р·Р°РґР°С‡Р°] В· СЂР°СЃРїРёСЃР°РЅРёРµ

рџЊђ P2P РЎР•РўР¬
  СЃС‚Р°С‚СѓСЃ СЃРµС‚Рё В· СЃРёРЅС…СЂРѕРЅРёР·РёСЂСѓР№ РЅР°РІС‹РєРё
  РїРѕРґРєР»СЋС‡РёСЃСЊ Рє [IP] В· СЂР°СЃРїСЂРµРґРµР»Рё Р·Р°РґР°С‡Сѓ [РІРѕРїСЂРѕСЃ]
    p2p РїСЂРѕС‚РѕРєРѕР» В· libp2p В· zkp

рџ§  TOOL CALLING
    СЃС…РµРјС‹ РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ В· json СЃС…РµРјС‹ РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ

пїЅ РЈРњРќР«Р• РЎРРЎРўР•РњР«
  СѓРјРЅС‹Рµ СЃРёСЃС‚РµРјС‹ В· С‚РёРїС‹ СЃРёСЃС‚РµРј
  РґРѕР±Р°РІСЊ СЃРёСЃС‚РµРјСѓ [С‚РёРї] [id]
  РѕР±РЅРѕРІРё СЃРµРЅСЃРѕСЂ [СЃРёСЃС‚РµРјР°] [СЃРµРЅСЃРѕСЂ] [Р·РЅР°С‡РµРЅРёРµ]
  РІРєР»СЋС‡Рё/РІС‹РєР»СЋС‡Рё [Р°РєС‚СѓР°С‚РѕСЂ] [СЃРёСЃС‚РµРјР°]
  РґРѕР±Р°РІСЊ РїСЂР°РІРёР»Рѕ [СЃРёСЃС‚РµРјР°] РµСЃР»Рё [СѓСЃР»РѕРІРёРµ] С‚Рѕ [РґРµР№СЃС‚РІРёРµ]
  РўРёРїС‹: home, greenhouse, garage, cellar, incubator, aquarium, terrarium

рџ“Ў IoT / MESH-РЎР•РўР¬
  iot СЃС‚Р°С‚СѓСЃ В· РґРѕР±Р°РІСЊ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [id] [С‚РёРї] [РїСЂРѕС‚РѕРєРѕР»]
    СЃС‚Р°С‚СѓСЃ СѓСЃС‚СЂРѕР№СЃС‚РІР° [id] В· iot РїСЂРѕС‚РѕРєРѕР»С‹
  РїРѕРґРєР»СЋС‡Рё zigbee/lora/mqtt В· Р·Р°РїСѓСЃС‚Рё mesh
  СЃС‚Р°С‚СѓСЃ mesh В· Р·Р°РїСѓСЃС‚Рё zigbee/lora [РїРѕСЂС‚]
  Р·Р°РїСѓСЃС‚Рё wifi mesh [SSID]
  РґРѕР±Р°РІСЊ mesh СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [id] [РїСЂРѕС‚РѕРєРѕР»] [Р°РґСЂРµСЃ]
  mesh broadcast [РїСЂРѕС‚РѕРєРѕР»] [РєРѕРјР°РЅРґР°]
    РЅР°Р№РґРё usb С‡РёРїС‹ В· СѓРјРЅР°СЏ РїСЂРѕС€РёРІРєР° [РїРѕСЂС‚]
    РџСЂРѕС‚РѕРєРѕР»С‹: BACnet, Modbus RTU/ASCII/TCP, KNX, LonWorks, M-Bus, OPC UA, MQTT
    РЎРµС‚Рё: Zigbee mesh, LoRa (SX1276), WiFi mesh

рџ”Њ OTG (USB HOST)
  opi СЃС‚Р°С‚СѓСЃ                           вЂ” Orange Pi One РјРѕСЃС‚
  opi РїРёРЅС‹                             вЂ” РєР°СЂС‚Р° РїРёРЅРѕРІ OPi One
  opi gpio [РїРёРЅ] [0/1]                 вЂ” СѓРїСЂР°РІР»РµРЅРёРµ GPIO
  opi i2c СЃРєР°РЅРёСЂРѕРІР°С‚СЊ                  вЂ” РїРѕРёСЃРє I2C СѓСЃС‚СЂРѕР№СЃС‚РІ
  opi 1wire                            вЂ” С‚РµРјРїРµСЂР°С‚СѓСЂР° DS18B20
  opi modbus [СЋРЅРёС‚] [СЂРµРі] [РєРѕР»-РІРѕ]     вЂ” Modbus RTU С‡С‚РµРЅРёРµ
  opi uart [РґР°РЅРЅС‹Рµ]                    вЂ” UART РѕС‚РїСЂР°РІРєР°
  opi rs485 [hex]                      вЂ” RS-485 СЃС‹СЂС‹Рµ Р±Р°Р№С‚С‹
  opi РґР°С‚С‡РёРєРё                          вЂ” РІСЃРµ РґР°С‚С‡РёРєРё СЃСЂР°Р·Сѓ

otg СЃС‚Р°С‚СѓСЃ                           вЂ” СЃРѕСЃС‚РѕСЏРЅРёРµ OTG-РјРµРЅРµРґР¶РµСЂР°
  otg СЃРєР°РЅ                             вЂ” СЃРїРёСЃРѕРє USB-СѓСЃС‚СЂРѕР№СЃС‚РІ С‡РµСЂРµР· OTG
  otg РїРѕРґРєР»СЋС‡Рё [id/РїРѕСЂС‚] [baudrate]    вЂ” РїРѕРґРєР»СЋС‡РёС‚СЊСЃСЏ Рє USB-Serial
  otg РѕС‚РїСЂР°РІСЊ [id] [РґР°РЅРЅС‹Рµ]            вЂ” РѕС‚РїСЂР°РІРёС‚СЊ РґР°РЅРЅС‹Рµ РІ СѓСЃС‚СЂРѕР№СЃС‚РІРѕ
  otg РѕС‚РєР»СЋС‡Рё [id]                     вЂ” Р·Р°РєСЂС‹С‚СЊ OTG-СЃРѕРµРґРёРЅРµРЅРёРµ
  otg РјРѕРЅРёС‚РѕСЂРёРЅРі                       вЂ” Р°РІС‚Рѕ-РјРѕРЅРёС‚РѕСЂРёРЅРі РїРѕРґРєР»СЋС‡РµРЅРёР№
  rs ttl / uart ttl                    вЂ” СЃРїСЂР°РІРєР° РїРѕ UART TTL Рё РєРѕРЅРІРµСЂС‚РµСЂР°Рј
  РїСЂРѕРІРµСЂСЊ РґСЂР°Р№РІРµСЂС‹ android gui         вЂ” РЅРёР·РєРѕСѓСЂРѕРІРЅРµРІС‹Рµ РґСЂР°Р№РІРµСЂС‹ Android/GUI

рџ”ђ Р“РћРЎРў РљР РРџРўРћР“Р РђР¤РРЇ (Р“РћРЎРў Р  34.12-2015 + Р  34.11-2012)
  РіРѕСЃС‚ СЃС‚Р°С‚СѓСЃ                          вЂ” СЃРѕСЃС‚РѕСЏРЅРёРµ Р“РћРЎРў-РјРѕРґСѓР»СЏ (РљСѓР·РЅРµС‡РёРє/РњР°РіРјР°/РЎС‚СЂРёР±РѕРі)
  РіРѕСЃС‚ С…РµС€ [С‚РµРєСЃС‚]                     вЂ” С…РµС€ РЎС‚СЂРёР±РѕРі-256 (Р“РћРЎРў Р  34.11-2012)
  РіРѕСЃС‚ p2p СЃС‚Р°С‚СѓСЃ                      вЂ” Р“РћРЎРў-Р·Р°С‰РёС‚Р° P2P (HMAC-РЎС‚СЂРёР±РѕРі + CTR-РљСѓР·РЅРµС‡РёРє)

рџ—„ GRIST P2P РҐР РђРќРР›РР©Р•
  grist СЃС‚Р°С‚СѓСЃ                         вЂ” СЃРѕСЃС‚РѕСЏРЅРёРµ РїРѕРґРєР»СЋС‡РµРЅРёСЏ Рє Grist
  grist С‚Р°Р±Р»РёС†С‹                        вЂ” СЃРїРёСЃРѕРє С‚Р°Р±Р»РёС† РґРѕРєСѓРјРµРЅС‚Р°
  grist СЃРѕС…СЂР°РЅРё [РєР»СЋС‡] [Р·РЅР°С‡РµРЅРёРµ]      вЂ” СЃРѕС…СЂР°РЅРёС‚СЊ Р·Р°РїРёСЃСЊ (Р“РћРЎРў-С€РёС„СЂРѕРІР°РЅРёРµ)
  grist РїРѕР»СѓС‡Рё [РєР»СЋС‡]                  вЂ” РїРѕР»СѓС‡РёС‚СЊ Р·Р°РїРёСЃСЊ
  grist СЃРїРёСЃРѕРє                         вЂ” РІСЃРµ Р·Р°РїРёСЃРё РЅРѕРґС‹
  grist РЅРѕРґС‹                           вЂ” СЂРµРµСЃС‚СЂ P2P-РЅРѕРґ РІ Grist
  grist СЃРёРЅРє                           вЂ” Р·Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°С‚СЊ РЅРѕРґСѓ РІ Grist

рџ”§ IoT РЁР›Р®Р—Р«
  СЃРїРёСЃРѕРє С€Р»СЋР·РѕРІ В· С€Р°Р±Р»РѕРЅС‹ С€Р»СЋР·РѕРІ
  СЃРѕР·РґР°Р№ С€Р»СЋР· [id] [С€Р°Р±Р»РѕРЅ]
    СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ [id] [С€Р°Р±Р»РѕРЅ] [РїРѕСЂС‚]
    РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР» [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [РїСЂРѕС€РёРІРєР°] [РѕРїРёСЃР°РЅРёРµ]
    РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [hardware]
  РїСЂРѕС€РµР№ С€Р»СЋР· [id] [РїРѕСЂС‚] В· РїСЂРѕС€РµР№ gateway [РїРѕСЂС‚] [РїСЂРѕС€РёРІРєР°]
  РєРѕРЅС„РёРі С€Р»СЋР·Р° [id]
    MCU: STM32H503, ESP8266, RP2040

рџЏ  HOME ASSISTANT
    ha СЃС‚Р°С‚СѓСЃ В· ha СЃРѕСЃС‚РѕСЏРЅРёСЏ
    ha СЃРµСЂРІРёСЃ [domain] [service] [key=value]
    ha mqtt [topic] [key=value]

рџ§© РњРћР”РЈР›Р
    СЃРїРёСЃРѕРє РјРѕРґСѓР»РµР№

рџђ¦ РљРћР›РР‘Р Р (P2P mesh-Р°РіРµРЅС‚)
  РєРѕР»РёР±СЂРё СЃС‚Р°С‚СѓСЃ В· Р·Р°РїСѓСЃС‚Рё РєРѕР»РёР±СЂРё

рџ”® РљР’РђРќРўРћР’Р«Р™ РћР РђРљРЈР›
  РѕСЂР°РєСѓР» СЃС‚Р°С‚СѓСЃ В· РѕСЂР°РєСѓР» СЃРµРјСЏ В· РѕСЂР°РєСѓР» СЂРµР¶РёРј

рџЋ¤ Р“РћР›РћРЎ
  СЃС‚Р°С‚СѓСЃ РїСЂРѕРІР°Р№РґРµСЂРѕРІ В· ai РїСЂРѕРІР°Р№РґРµСЂС‹ В· РґРѕСЃС‚СѓРїРЅС‹Рµ РјРѕРґРµР»Рё

рџ¤– РЎРћР‘РЎРўР’Р•РќРќРђРЇ РњРћР”Р•Р›Р¬
  РјРѕРґРµР»СЊ СЃС‚Р°С‚СѓСЃ В· РјРѕРґРµР»СЊ РѕР±СѓС‡РёС‚СЊ В· РјРѕРґРµР»СЊ СЃРѕС…СЂР°РЅРёС‚СЊ
  РјРѕРґРµР»СЊ РёСЃС‚РѕСЂРёСЏ В· РјРѕРґРµР»СЊ РІРµСЂСЃРёСЏ В· РјРѕРґРµР»СЊ РєРІР°РЅС‚РѕРІС‹Р№ СЃС‚Р°С‚СѓСЃ
  РјРѕРґРµР»СЊ СЃРїСЂРѕСЃРёС‚СЊ [РІРѕРїСЂРѕСЃ]
  argoss СЃС‚Р°С‚СѓСЃ вЂ” СЃС‚Р°С‚СѓСЃ РјРѕРґРµР»Рё

рџ§  NeuralSwarm (GPU СЂРѕСѓС‚РµСЂ RX 580/RX 560)
  neuralswarm СЃС‚Р°С‚СѓСЃ В· gpu СЂРѕСѓС‚РµСЂ

рџЋ¤ Р“РћР›РћРЎ
  РіРѕР»РѕСЃ РІРєР»/РІС‹РєР» В· РІРєР»СЋС‡Рё wake word

рџ’¬ Р”РРђР›РћР“
  РєРѕРЅС‚РµРєСЃС‚ РґРёР°Р»РѕРіР° В· СЃР±СЂРѕСЃ РєРѕРЅС‚РµРєСЃС‚Р°
  РёСЃС‚РѕСЂРёСЏ В· РїРѕРјРѕС‰СЊ"""

    def _argoscore_functions(self) -> str:
        """Р’РѕР·РІСЂР°С‰Р°РµС‚ СЃС‚СЂСѓРєС‚СѓСЂРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚С‡С‘С‚ Рѕ С„СѓРЅРєС†РёСЏС… Рё РїРѕРґСЃРёСЃС‚РµРјР°С… ArgosCore."""
        lines = [f"рџ§  ArgosCore v{self.VERSION} вЂ” Р¤РЈРќРљР¦РР Р РџРћР”РЎРРЎРўР•РњР«:\n"]

        # РџРѕРґСЃРёСЃС‚РµРјС‹ Рё РёС… СЃС‚Р°С‚СѓСЃ
        subsystems = [
            ("рџ§® РљРІР°РЅС‚РѕРІС‹Р№ РјРѕРґСѓР»СЊ (quantum)",    self.quantum),
            ("рџ§  РџР°РјСЏС‚СЊ (memory)",               self.memory),
            ("рџЋЇ РђРіРµРЅС‚ (agent)",                 self.agent),
            ("рџ“Ў РЎРµРЅСЃРѕСЂС‹ (sensors)",             self.sensors),
            ("рџ“љ РќР°РІС‹РєРё (skill_loader)",         self.skill_loader),
            ("рџ”® Р›СЋР±РѕРїС‹С‚СЃС‚РІРѕ (curiosity)",       self.curiosity),
            ("вќ¤пёЏ Р“РѕРјРµРѕСЃС‚Р°Р· (homeostasis)",      self.homeostasis),
            ("рџ“† РџР»Р°РЅРёСЂРѕРІС‰РёРє (scheduler)",       self.scheduler),
            ("рџ”” РђР»РµСЂС‚С‹ (alerts)",               self.alerts),
            ("рџ‘Ѓ Р—СЂРµРЅРёРµ (vision)",               self.vision),
            ("рџЊђ P2P СЃРµС‚СЊ",                      self.p2p),
            ("рџ¤– IoT-РјРѕСЃС‚ (iot_bridge)",         self.iot_bridge),
            ("рџЏ­ РџСЂРѕРјС‹С€Р»РµРЅРЅС‹Рµ РїСЂРѕС‚РѕРєРѕР»С‹",        self.industrial),
            ("рџ–Ґ РџР»Р°С‚С„РѕСЂРјРµРЅРЅС‹Р№ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂ",   self.platform_admin),
            ("рџЏ  РЈРјРЅС‹Рµ СЃРёСЃС‚РµРјС‹ (smart_sys)",     self.smart_sys),
            ("рџЏЎ Home Assistant (ha)",            self.ha),
            ("рџ”— Git РѕРїРµСЂР°С†РёРё (git_ops)",        self.git_ops),
            ("рџ“¦ РњРѕРґСѓР»Рё (module_loader)",        self.module_loader),
            ("рџ—„ Grist P2P С…СЂР°РЅРёР»РёС‰Рµ",           self.grist),
            ("вЃпёЏ РћР±Р»Р°С‡РЅРѕРµ С…СЂР°РЅРёР»РёС‰Рµ",           self.cloud_object_storage),
            ("рџ”Њ OTG (USB HOST)",                self.otg),
            ("рџџ  Orange Pi One Bridge (opi)",    getattr(self, "opi", None)),
            ("рџ§Є РЎРѕР±СЃС‚РІРµРЅРЅР°СЏ РјРѕРґРµР»СЊ (own_model)", getattr(self, "own_model", None)),
        ]

        lines.append("рџ“¦ РџРћР”РЎРРЎРўР•РњР«:")
        for name, obj in subsystems:
            status = "вњ… Р°РєС‚РёРІРЅР°" if obj is not None else "вљ пёЏ РЅРµ Р·Р°РіСЂСѓР¶РµРЅР°"
            lines.append(f"  {name}: {status}")

        # РџСѓР±Р»РёС‡РЅС‹Рµ РјРµС‚РѕРґС‹ API
        lines.append("\nрџ”§ РџРЈР‘Р›РР§РќР«Р• РњР•РўРћР”Р«:")
        public_api = [
            ("process(user_text)",              "Р“Р»Р°РІРЅР°СЏ С‚РѕС‡РєР° РІС…РѕРґР°: РѕР±СЂР°Р±РѕС‚РєР° РєРѕРјР°РЅРґС‹/Р·Р°РїСЂРѕСЃР°"),
            ("execute_intent(text, admin)",     "РњР°СЂС€СЂСѓС‚РёР·Р°С†РёСЏ РЅР°РјРµСЂРµРЅРёСЏ Рє РЅСѓР¶РЅРѕРјСѓ РѕР±СЂР°Р±РѕС‚С‡РёРєСѓ"),
            ("say(text)",                       "TTS: РѕР·РІСѓС‡РёС‚СЊ С‚РµРєСЃС‚"),
            ("listen()",                        "STT: РїСЂРѕСЃР»СѓС€Р°С‚СЊ СЂРµС‡СЊ СЃ РјРёРєСЂРѕС„РѕРЅР°"),
            ("transcribe_audio_path(path)",     "STT: С‚СЂР°РЅСЃРєСЂРёР±РёСЂРѕРІР°С‚СЊ Р°СѓРґРёРѕС„Р°Р№Р»"),
            ("set_ai_mode(mode)",               "РџРµСЂРµРєР»СЋС‡РёС‚СЊ AI-РїСЂРѕРІР°Р№РґРµСЂР° (auto/gemini/ollama/вЂ¦)"),
            ("ai_mode_label()",                 "РџРѕР»СѓС‡РёС‚СЊ С‚РµРєСѓС‰РёР№ AI-СЂРµР¶РёРј"),
            ("voice_services_report()",         "РћС‚С‡С‘С‚ Рѕ РіРѕР»РѕСЃРѕРІС‹С… СЃР»СѓР¶Р±Р°С…"),
            ("start_p2p()",                     "Р—Р°РїСѓСЃС‚РёС‚СЊ P2P-СЃРµС‚СЊ"),
            ("start_dashboard(admin, flasher)", "Р—Р°РїСѓСЃС‚РёС‚СЊ РІРµР±-РїР°РЅРµР»СЊ"),
            ("start_wake_word(admin, flasher)", "Р—Р°РїСѓСЃС‚РёС‚СЊ wake-word СЃР»СѓС€Р°С‚РµР»СЊ"),
            ("load_skill(name)",                "Р—Р°РіСЂСѓР·РёС‚СЊ РЅР°РІС‹Рє РїРѕ РёРјРµРЅРё"),
        ]
        for method, desc in public_api:
            lines.append(f"  вЂў {method} вЂ” {desc}")

        # AI-СЂРµР¶РёРј
        try:
            ai_lbl = self.ai_mode_label()
        except Exception:
            ai_lbl = str(getattr(self, "ai_mode", "unknown"))
        lines.append(f"\nрџ¤– РўР•РљРЈР©РР™ AI-Р Р•Р–РРњ: {ai_lbl}")
        lines.append(f"рџ“Њ Р’РµСЂСЃРёСЏ СЏРґСЂР°: {self.VERSION}")
        lines.append("\nв„№пёЏ Р”Р»СЏ РїРѕР»РЅРѕРіРѕ СЃРїРёСЃРєР° РєРѕРјР°РЅРґ РІРІРµРґРё: РїРѕРјРѕС‰СЊ")

        return "\n".join(lines)

    def _iot_protocols_help(self) -> str:
        return """рџЏ­ РџРћР”Р”Р•Р Р–РР’РђР•РњР«Р• IoT/РџР РћРњ РџР РћРўРћРљРћР›Р«:

    вЂў BACnet (Building Automation and Control Networks)
    вЂў Modbus RTU / ASCII / TCP
    вЂў KNX
    вЂў LonWorks (Local Operating Network)
    вЂў M-Bus (Meter-Bus)
    вЂў OPC UA (Open Platform Communications Unified Architecture)
    вЂў MQTT
    вЂў RS TTL / UART TTL (TX, RX, GND; 3.3V/5V Р»РѕРіРёРєР°)

рџ“Ў Mesh Рё СЂР°РґРёРѕ:
    вЂў Zigbee mesh
    вЂў LoRa mesh (РІРєР»СЋС‡Р°СЏ SX1276)
    вЂў WiFi mesh / gateway bridge

рџ”§ РџСЂРѕС€РёРІРєР° СѓСЃС‚СЂРѕР№СЃС‚РІ:
    вЂў STM32H503, ESP8266, RP2040
    вЂў РљРѕРјР°РЅРґС‹: СЃРѕР·РґР°Р№ РїСЂРѕС€РёРІРєСѓ [id] [С€Р°Р±Р»РѕРЅ] [РїРѕСЂС‚]
                РёР·СѓС‡Рё РїСЂРѕС‚РѕРєРѕР» [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [РїСЂРѕС€РёРІРєР°] [РѕРїРёСЃР°РЅРёРµ]
                РёР·СѓС‡Рё СѓСЃС‚СЂРѕР№СЃС‚РІРѕ [С€Р°Р±Р»РѕРЅ] [РїСЂРѕС‚РѕРєРѕР»] [hardware]

рџ”Њ UART TTL / RS TTL:
    вЂў Р›РёРЅРёРё: TX, RX, GND
    вЂў РЈСЂРѕРІРЅРё: 0/3.3V РёР»Рё 0/5V (Р±РµР·РѕРїР°СЃРЅРѕ С‚РѕР»СЊРєРѕ РІ РїСЂРµРґРµР»Р°С… TTL)
    вЂў TTL в†” RS-232: MAX232
    вЂў TTL в†” RS-485: MAX485
    вЂў TTL в†” USB: FT232RL / CH340"""

    def _rs_ttl_help(self) -> str:
        return """рџ”Њ RS TTL / UART TTL вЂ” СЃРїСЂР°РІРєР°:

  вЂў РўРёРї СЃРІСЏР·Рё: РїРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅР°СЏ Р°СЃРёРЅС…СЂРѕРЅРЅР°СЏ (UART), Р±РµР· РѕР±С‰РµРіРѕ С‚Р°РєС‚РѕРІРѕРіРѕ СЃРёРіРЅР°Р»Р°
  вЂў Р›РёРЅРёРё: TX, RX, GND
  вЂў Р›РѕРіРёС‡РµСЃРєРёРµ СѓСЂРѕРІРЅРё:
      - HIGH: РѕР±С‹С‡РЅРѕ 3.3V РёР»Рё 5V
      - LOW: РѕРєРѕР»Рѕ 0V
  вЂў Р”РёСЃС‚Р°РЅС†РёСЏ: РѕР±С‹С‡РЅРѕ РґРѕ РЅРµСЃРєРѕР»СЊРєРёС… РјРµС‚СЂРѕРІ (РЅРёР·РєР°СЏ РїРѕРјРµС…РѕСѓСЃС‚РѕР№С‡РёРІРѕСЃС‚СЊ)

вљ пёЏ РќРµР»СЊР·СЏ РїРѕРґРєР»СЋС‡Р°С‚СЊ TTL РЅР°РїСЂСЏРјСѓСЋ Рє RS-232/RS-485:
  вЂў TTL в†” RS-232: РёСЃРїРѕР»СЊР·СѓР№С‚Рµ MAX232
  вЂў TTL в†” RS-485: РёСЃРїРѕР»СЊР·СѓР№С‚Рµ MAX485
  вЂў TTL в†” USB: РёСЃРїРѕР»СЊР·СѓР№С‚Рµ FT232RL / CH340

Р”Р»СЏ СЂР°Р±РѕС‚С‹ РІ С‚РµСЂРјРёРЅР°Р»Рµ:
  вЂў otg СЃРєР°РЅ
  вЂў otg РїРѕРґРєР»СЋС‡Рё [id/РїРѕСЂС‚] [baudrate]
  вЂў otg РѕС‚РїСЂР°РІСЊ [id] [РґР°РЅРЅС‹Рµ]
  вЂў otg РѕС‚РєР»СЋС‡Рё [id]"""

    def _low_level_drivers_report(self) -> str:
        def _module_ok(name: str) -> bool:
            try:
                import importlib.util
                return importlib.util.find_spec(name) is not None
            except Exception:
                return False

        def _threading_line() -> str:
            cores = os.cpu_count() or 1
            active_threads = threading.active_count()
            return f"  РњРЅРѕРіРѕРїРѕС‚РѕС‡РЅРѕСЃС‚СЊ CPU: {cores} Р»РѕРіРёС‡. РїРѕС‚РѕРєРѕРІ | Р°РєС‚РёРІРЅС‹С… РїРѕС‚РѕРєРѕРІ Python: {active_threads}"

        def _power_line() -> str:
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery is None:
                    return "  РџРёС‚Р°РЅРёРµ/РјРѕС‰РЅРѕСЃС‚СЊ: вњ… СЃРµС‚СЊ/СЃС‚Р°С†РёРѕРЅР°СЂРЅС‹Р№ СЂРµР¶РёРј (battery sensor РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚)"
                src = "рџ”Њ СЃРµС‚СЊ" if battery.power_plugged else "рџ”‹ Р±Р°С‚Р°СЂРµСЏ"
                return f"  РџРёС‚Р°РЅРёРµ/РјРѕС‰РЅРѕСЃС‚СЊ: {src}, Р·Р°СЂСЏРґ {battery.percent:.0f}%"
            except Exception:
                return "  РџРёС‚Р°РЅРёРµ/РјРѕС‰РЅРѕСЃС‚СЊ: вљ пёЏ РЅРµРґРѕСЃС‚СѓРїРЅРѕ (РЅРµС‚ psutil sensors)"

        def _video_line() -> str:
            try:
                import glob
                import shutil
                import subprocess

                trusted_dirs = ("/usr/bin", "/usr/local/bin", "/bin", "/sbin")
                def _trusted_binary(path: str | None) -> str | None:
                    if not path:
                        return None
                    real = os.path.realpath(path)
                    if not isinstance(real, str):
                        return None
                    for directory in trusted_dirs:
                        try:
                            if os.path.commonpath([real, directory]) == directory:
                                return real
                        except Exception:
                            continue
                    return None

                def _sanitize_gpu_name(text: str, max_length: int = 120) -> str:
                    safe = "".join(ch for ch in text if ch.isprintable() and ch != "\x7f")
                    return safe[:max_length]

                details = []
                if glob.glob("/dev/dri/renderD*"):
                    details.append("DRM render nodes")
                nvidia_smi = _trusted_binary(shutil.which("nvidia-smi"))
                if nvidia_smi:
                    result = subprocess.run(
                        [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
                        capture_output=True,
                        text=True,
                        timeout=2,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        raw_gpu_name = result.stdout.strip().splitlines()[0]
                        gpu_name = _sanitize_gpu_name(raw_gpu_name)
                        details.append(f"NVIDIA: {gpu_name}")
                vcgencmd = _trusted_binary(shutil.which("vcgencmd"))
                if vcgencmd:
                    result = subprocess.run(
                        [vcgencmd, "get_mem", "gpu"],
                        capture_output=True,
                        text=True,
                        timeout=2,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        details.append(f"VideoCore: {result.stdout.strip()}")
                if details:
                    return f"  Р’РёРґРµРѕСЏРґСЂР°/GPU: вњ… {'; '.join(details)}"
                return "  Р’РёРґРµРѕСЏРґСЂР°/GPU: вљ пёЏ РЅРµ РѕР±РЅР°СЂСѓР¶РµРЅС‹/РґСЂР°Р№РІРµСЂС‹ РЅРµ Р°РєС‚РёРІРЅС‹"
            except Exception:
                return "  Р’РёРґРµРѕСЏРґСЂР°/GPU: вљ пёЏ РїСЂРѕРІРµСЂРєР° РЅРµРґРѕСЃС‚СѓРїРЅР°"

        is_android = os.path.exists("/system/build.prop")
        lines = [
            "рџ§Є РќРР—РљРћРЈР РћР’РќР•Р’Р«Р• Р”Р РђР™Р’Р•Р Р« (Android / GUI):",
            f"  Р РµР¶РёРј Android: {'вњ…' if is_android else 'вќЊ (desktop/linux)'}",
            _threading_line(),
            _power_line(),
            _video_line(),
            "",
            "  Р”СЂР°Р№РІРµСЂС‹ Рё Р±РёР±Р»РёРѕС‚РµРєРё С„СѓРЅРєС†РёР№:",
            f"  Android USB API (jnius): {'вњ…' if _module_ok('jnius') else 'вќЊ'}",
            f"  Android UI (kivy): {'вњ…' if _module_ok('kivy') else 'вќЊ'}",
            f"  Android sensors/services (plyer): {'вњ…' if _module_ok('plyer') else 'вќЊ'}",
            f"  USB-Serial (pyserial): {'вњ…' if _module_ok('serial') else 'вќЊ'}",
            f"  GUI Desktop (customtkinter): {'вњ…' if _module_ok('customtkinter') else 'вќЊ'}",
        ]
        if self.otg:
            lines.append("")
            lines.append(self.otg.status())
        return "\n".join(lines)

    def _start_smart_create_wizard(self) -> str:
        if not self.smart_sys:
            return "вќЊ РЈРјРЅС‹Рµ СЃРёСЃС‚РµРјС‹ РЅРµ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°РЅС‹."

        self._smart_create_wizard = {
            "step": "type",
            "type": None,
            "id": None,
            "purpose": "",
            "functions": [],
        }
        types = ", ".join(self.smart_profiles.keys()) if self.smart_profiles else "home, greenhouse, garage, cellar, incubator, aquarium, terrarium"
        return (
            "рџ§­ РњР°СЃС‚РµСЂ СЃРѕР·РґР°РЅРёСЏ СѓРјРЅРѕР№ СЃРёСЃС‚РµРјС‹.\n"
            "РЁР°Рі 1/4: РІС‹Р±РµСЂРё С‚РёРї СЃРёСЃС‚РµРјС‹:\n"
            f"{types}\n"
            "РџСЂРёРјРµСЂ: greenhouse\n"
            "(РґР»СЏ РѕС‚РјРµРЅС‹: 'РѕС‚РјРµРЅР°')"
        )

    def _continue_smart_create_wizard(self, text: str) -> str:
        wiz = self._smart_create_wizard
        if not wiz:
            return None

        value = text.strip()
        step = wiz.get("step")

        if step == "type":
            sys_type = value.split()[0].lower()
            if sys_type not in self.smart_profiles:
                types = ", ".join(self.smart_profiles.keys())
                return f"вќЊ РќРµРёР·РІРµСЃС‚РЅС‹Р№ С‚РёРї. Р”РѕСЃС‚СѓРїРЅС‹Рµ: {types}\nР’РІРµРґРё С‚РёРї РµС‰С‘ СЂР°Р·."
            wiz["type"] = sys_type
            wiz["step"] = "id"
            profile = self.smart_profiles.get(sys_type, {})
            return (
                f"вњ… РўРёРї: {profile.get('icon','вљ™пёЏ')} {profile.get('name', sys_type)}\n"
                "РЁР°Рі 2/4: Р·Р°РґР°Р№ ID СЃРёСЃС‚РµРјС‹ (Р»Р°С‚РёРЅРёС†Р°/С†РёС„СЂС‹), РЅР°РїСЂРёРјРµСЂ: my_greenhouse\n"
                "РР»Рё РЅР°РїРёС€Рё 'Р°РІС‚Рѕ' РґР»СЏ ID РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ."
            )

        if step == "id":
            if value.lower() in ("Р°РІС‚Рѕ", "auto", "default"):
                wiz["id"] = wiz["type"]
            else:
                wiz["id"] = value.split()[0]
            wiz["step"] = "purpose"
            return (
                f"вњ… ID: {wiz['id']}\n"
                "РЁР°Рі 3/4: С‡С‚Рѕ СЃРёСЃС‚РµРјР° РґРѕР»Р¶РЅР° РґРµР»Р°С‚СЊ?\n"
                "РџСЂРёРјРµСЂ: РїРѕРґРґРµСЂР¶РёРІР°С‚СЊ РєР»РёРјР°С‚ Рё Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ, СѓРїСЂР°РІР»СЏС‚СЊ РїРѕР»РёРІРѕРј Рё РІРµРЅС‚РёР»СЏС†РёРµР№."
            )

        if step == "purpose":
            wiz["purpose"] = value
            wiz["step"] = "functions"
            profile = self.smart_profiles.get(wiz["type"], {})
            actuators = ", ".join(profile.get("actuators", []))
            return (
                f"вњ… РќР°Р·РЅР°С‡РµРЅРёРµ: {wiz['purpose']}\n"
                "РЁР°Рі 4/4: РєР°РєРёРµ С„СѓРЅРєС†РёРё РІРєР»СЋС‡РёС‚СЊ СЃСЂР°Р·Сѓ?\n"
                f"Р”РѕСЃС‚СѓРїРЅС‹Рµ С„СѓРЅРєС†РёРё: {actuators}\n"
                "Р’РІРµРґРё С‡РµСЂРµР· Р·Р°РїСЏС‚СѓСЋ (РїСЂРёРјРµСЂ: irrigation, ventilation)\n"
                "РёР»Рё РЅР°РїРёС€Рё 'Р°РІС‚Рѕ' РґР»СЏ СЃС‚Р°РЅРґР°СЂС‚РЅРѕРіРѕ РїСЂРѕС„РёР»СЏ."
            )

        if step == "functions":
            profile = self.smart_profiles.get(wiz["type"], {})
            actuators = profile.get("actuators", [])
            if value.lower() not in ("Р°РІС‚Рѕ", "auto", "default"):
                selected = [x.strip() for x in value.split(",") if x.strip()]
                valid = [x for x in selected if x in actuators]
                wiz["functions"] = valid
            else:
                wiz["functions"] = []

            create_msg = self.smart_sys.add_system(wiz["type"], wiz["id"])
            if create_msg.startswith("вќЊ"):
                self._smart_create_wizard = None
                return create_msg

            if wiz["functions"]:
                for function_name in wiz["functions"]:
                    self.smart_sys.command(wiz["id"], function_name, "on")

            summary = (
                f"рџ§ѕ РЎРѕР·РґР°РЅРѕ: {wiz['type']} [{wiz['id']}]\n"
                f"рџЋЇ РќР°Р·РЅР°С‡РµРЅРёРµ: {wiz['purpose']}\n"
                f"рџ§© Р¤СѓРЅРєС†РёРё: {', '.join(wiz['functions']) if wiz['functions'] else 'РЅРµС‚'}\n"
                f"вњ… SmartSystem-Р°РіРµРЅС‚ Р°РєС‚РёРІРёСЂРѕРІР°РЅ."
            )
            self._smart_create_wizard = None
            return summary
from __future__ import annotations

import os
import threading
import time
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


class ArgosMCPServer:
    """РњРёРЅРёРјР°Р»СЊРЅС‹Р№ HTTP MCP endpoint РґР»СЏ Р»РѕРєР°Р»СЊРЅРѕР№ РёРЅС‚РµРіСЂР°С†РёРё."""

    def __init__(self, core=None, admin=None):
        self.core = core
        self.admin = admin
        self.started_at = time.time()
        self.app = self._create_app()

    def _providers(self) -> str:
        try:
            from src.ai_providers import providers_status

            return providers_status()
        except Exception as exc:
            return f"providers error: {exc}"

    def _skills(self) -> str:
        if self.core and getattr(self.core, "skill_loader", None):
            try:
                return self.core.skill_loader.list_skills()
            except Exception as exc:
                return f"skills error: {exc}"
        return "skill_loader not initialized"

    def _limits(self) -> str:
        try:
            from src.connectivity.telegram_bot import ArgosTelegram

            bot = ArgosTelegram(self.core, self.admin, None)
            return bot._build_limits_report()
        except Exception as exc:
            return f"limits error: {exc}"

    def _status(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "ok": True,
            "uptime_seconds": int(time.time() - self.started_at),
            "ai_mode": self.core.ai_mode_label() if self.core and hasattr(self.core, "ai_mode_label") else "unknown",
        }
        try:
            import psutil

            out["cpu_pct"] = psutil.cpu_percent(interval=0.1)
            out["ram_pct"] = psutil.virtual_memory().percent
        except Exception:
            pass
        return out

    def _image_generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        steps: int = 20,
        width: int = 1024,
        height: int = 1024,
        model_name: str | None = None,
    ) -> str:
        from src.tools.image_generator import ArgosImageGenerator

        gen = ArgosImageGenerator(model_name=model_name)
        return gen.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            steps=steps,
            width=width,
            height=height,
        )

    def _run_command(self, text: str) -> str:
        if not text.strip():
            return "empty command"
        if self.core and hasattr(self.core, "process_logic_async"):
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                try:
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(
                        self.core.process_logic_async(text, self.admin, None)
                    )
                finally:
                    loop.close()
                    asyncio.set_event_loop(None)
                if isinstance(result, dict):
                    return str(result.get("answer", result))
                return str(result)
            except Exception as exc:
                return f"command error: {exc}"
        return "core not initialized"

    def _create_app(self) -> FastAPI:
        app = FastAPI(title="Argos MCP", version="1.0")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")
        def health():
            return self._status()

        @app.get("/mcp")
        def mcp_ping():
            return {
                "name": "argos",
                "ok": True,
                "transport": "http",
                "hint": "POST JSON-RPC to /mcp",
            }

        @app.post("/mcp")
        async def mcp_rpc(request: Request):
            payload = await request.json()
            if not isinstance(payload, dict):
                raise HTTPException(status_code=400, detail="JSON object expected")

            method = payload.get("method", "")
            req_id = payload.get("id")          # None РґР»СЏ notifications
            is_notification = req_id is None    # MCP notifications РЅРµ РёРјРµСЋС‚ id

            def _ok(result: Any):
                return {"jsonrpc": "2.0", "id": req_id, "result": result}

            def _err(code: int, message: str):
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

            # в”Ђв”Ђ Notifications (РЅРµС‚ id) в†’ РїСѓСЃС‚РѕР№ РѕС‚РІРµС‚ 200 в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            if is_notification:
                # notifications/initialized, notifications/cancelled, etc.
                return {}

            # в”Ђв”Ђ ping в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            if method == "ping":
                return _ok({})

            # в”Ђв”Ђ initialize в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            if method == "initialize":
                return _ok(
                    {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "argos", "version": "2.1.3"},
                        "capabilities": {
                            "tools": {"listChanged": False},
                        },
                        "instructions": (
                            "ARGOS Universal OS вЂ” AI-СЌРєРѕСЃРёСЃС‚РµРјР°. "
                            "РСЃРїРѕР»СЊР·СѓР№ РёРЅСЃС‚СЂСѓРјРµРЅС‚ 'command' РґР»СЏ РІС‹РїРѕР»РЅРµРЅРёСЏ Р»СЋР±С‹С… РєРѕРјР°РЅРґ ARGOS. "
                            "РРЅСЃС‚СЂСѓРјРµРЅС‚С‹: providers, skills, limits, status, command, image_generate."
                        ),
                    }
                )

            # в”Ђв”Ђ tools/list в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            if method == "tools/list":
                tools = [
                    {
                        "name": "providers",
                        "description": "РџРѕРєР°Р·С‹РІР°РµС‚ СЃС‚Р°С‚СѓСЃ РІСЃРµС… AI-РїСЂРѕРІР°Р№РґРµСЂРѕРІ ARGOS (Gemini, GigaChat, Grok, OpenAI, Groq, DeepSeek, Kimi, Ollama Рё РґСЂ.) СЃ Р»РёРјРёС‚Р°РјРё Рё РєРІРѕС‚Р°РјРё.",
                        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                    },
                    {
                        "name": "skills",
                        "description": "РЎРїРёСЃРѕРє Р·Р°РіСЂСѓР¶РµРЅРЅС‹С… СЃРєРёР»РѕРІ (РЅР°РІС‹РєРѕРІ) ARGOS вЂ” РІРЅРµС€РЅРёРµ РёРЅС‚РµРіСЂР°С†РёРё Рё РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹.",
                        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                    },
                    {
                        "name": "limits",
                        "description": "РћС‚С‡С‘С‚ Рѕ С‚РµРєСѓС‰РёС… Р»РёРјРёС‚Р°С… Рё РєРІРѕС‚Р°С… РїСЂРѕРІР°Р№РґРµСЂРѕРІ.",
                        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                    },
                    {
                        "name": "status",
                        "description": "РўРµРєСѓС‰РёР№ СЃС‚Р°С‚СѓСЃ ARGOS: uptime, CPU, RAM, СЂРµР¶РёРј РР.",
                        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                    },
                    {
                        "name": "image_generate",
                        "description": "Generate image from prompt and return absolute file path.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"},
                                "negative_prompt": {"type": "string"},
                                "steps": {"type": "integer", "minimum": 1, "maximum": 80},
                                "width": {"type": "integer", "minimum": 256, "maximum": 1536},
                                "height": {"type": "integer", "minimum": 256, "maximum": 1536},
                                "model_name": {"type": "string"},
                            },
                            "required": ["prompt"],
                            "additionalProperties": False,
                        },
                    },
                    {
                        "name": "command",
                        "description": (
                            "Р’С‹РїРѕР»РЅРёС‚СЊ РєРѕРјР°РЅРґСѓ С‡РµСЂРµР· СЏРґСЂРѕ ARGOS. "
                            "РџСЂРёРјРµСЂС‹: 'СЃС‚Р°С‚СѓСЃ', 'hf status', 'РїСЂРѕРІР°Р№РґРµСЂС‹', 'РїР°РјСЏС‚СЊ', 'РјС‹СЃР»Рё', 'СЌРІРѕР»СЋС†РёСЏ', 'СЂРµР¶РёРј РёРё grok'. "
                            "РџРѕРґРґРµСЂР¶РёРІР°СЋС‚СЃСЏ РІСЃРµ РєРѕРјР°РЅРґС‹ ARGOS."
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "РљРѕРјР°РЅРґР° РґР»СЏ ARGOS РЅР° СЂСѓСЃСЃРєРѕРј РёР»Рё Р°РЅРіР»РёР№СЃРєРѕРј СЏР·С‹РєРµ",
                                }
                            },
                            "required": ["text"],
                            "additionalProperties": False,
                        },
                    },
                ]
                return _ok({"tools": tools})

            # в”Ђв”Ђ tools/call в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
            if method == "tools/call":
                params = payload.get("params") or {}
                name = params.get("name")
                args = params.get("arguments") or {}
                try:
                    if name == "providers":
                        text = self._providers()
                    elif name == "skills":
                        text = self._skills()
                    elif name == "limits":
                        text = self._limits()
                    elif name == "status":
                        text = str(self._status())
                    elif name == "image_generate":
                        text = self._image_generate(
                            prompt=str(args.get("prompt", "")),
                            negative_prompt=str(args.get("negative_prompt", "")),
                            steps=int(args.get("steps", 20) or 20),
                            width=int(args.get("width", 1024) or 1024),
                            height=int(args.get("height", 1024) or 1024),
                            model_name=(str(args.get("model_name")) if args.get("model_name") else None),
                        )
                    elif name == "command":
                        text = self._run_command(str(args.get("text", "")))
                    else:
                        return _err(-32601, f"Unknown tool: {name}")
                except Exception as exc:
                    text = f"tool error: {exc}"
                return _ok({"content": [{"type": "text", "text": text}]})

            return _err(-32601, f"Method not found: {method}")

        return app


def start_mcp_api(core=None, admin=None, host: str = "127.0.0.1", port: int = 8000):
    server = ArgosMCPServer(core=core, admin=admin)
    config = uvicorn.Config(server.app, host=host, port=port, log_level="warning")
    uv_server = uvicorn.Server(config)
    thread = threading.Thread(target=uv_server.run, daemon=True, name="ArgosMCP")
    thread.start()
    return thread


app = ArgosMCPServer(core=None, admin=None).app


    Каталог: F:\debug\argoss\src


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10.04.2026     18:18                connectivity
d-----        09.04.2026     10:59                core
d-----        09.04.2026     10:59                economy
d-----        09.04.2026     10:59                factory
d-----        09.04.2026     10:59                interface
d-----        09.04.2026     10:59                knowledge
d-----        09.04.2026     10:59                mind
d-----        09.04.2026     10:59                modules
d-----        09.04.2026     10:59                nlp
d-----        10.04.2026      7:19                quantum
d-----        09.04.2026     10:59                security
d-----        10.04.2026      7:33                skills
d-----        09.04.2026     10:59                tools
d-----        09.04.2026     10:59                vision
d-----        10.04.2026     12:49                __pycache__
-a----        02.04.2026     10:05           1957 ACPBridge.py
-a----        02.04.2026     10:05           2003 acp_bridge.py
-a----        27.03.2026      5:17           6899 adaptive_drafter.py
-a----        28.03.2026      5:05          16517 admin.py
-a----        27.03.2026      5:17          11152 agent (1).py
-a----        01.04.2026     14:55          20515 agent.py
-a----        01.04.2026     14:54           2606 agent_guard.py
-a----        27.03.2026     20:58           6596 ai_failover.py
-a----        27.03.2026      2:04           6140 ai_failover.py.bak
-a----        10.04.2026     11:39          19515 ai_providers.py
-a----        10.04.2026     11:39          19782 ai_router.py
-a----        10.04.2026     11:40           7905 api_cost_optimizer.py
-a----        05.04.2026     20:44           6162 argoss_evolver.py
-a----        31.03.2026      9:31          14602 argos_claude_api.py
-a----        31.03.2026     11:44          14751 argos_client.py
-a----        01.04.2026     14:53           6781 argos_constitution.py
-a----        31.03.2026     10:02           7075 argos_desktop.py
-a----        27.03.2026     20:49          20822 argos_input_control_patch.py
-a----        25.03.2026      0:36          20768 argos_input_control_patch.py.bak
-a----        06.04.2026     13:09          27365 argos_integrator.py
-a----        10.04.2026      7:13           4542 argos_logger.py
-a----        01.04.2026     23:02          34592 argos_model.py
-a----        27.03.2026      5:17          29823 argos_os_builder.py
-a----        10.04.2026      6:54          20025 argos_patcher.py
-a----        27.03.2026      8:10          39325 argos_patcher.py.bak
-a----        10.04.2026      6:54           2899 argos_service.py
-a----        27.03.2026      5:17           2720 argos_service.py.bak
-a----        27.03.2026     20:35           3023 auto_patcher.py
-a----        27.03.2026      5:17           5050 awareness (1).py
-a----        25.03.2026      2:20           5071 awareness (1).py.bak
-a----        27.03.2026      5:17           3764 awareness.py
-a----        27.03.2026      5:17          17915 awa_core.py
-a----        27.03.2026      5:17           5539 bump_version.py
-a----        25.03.2026      2:20           5560 bump_version.py.bak
-a----        02.04.2026      1:45          10372 check_all_patches.py
-a----        25.03.2026      0:36          10233 check_all_patches.py.bak
-a----        31.03.2026      9:30          21844 claude_templates_integrator.py
-a----        27.03.2026      5:17           5519 cleanup_repo.py
-a----        27.03.2026      2:03           5517 cleanup_repo.py.bak
-a----        19.03.2026      0:25           3931 cleanup_root.py
-a----        27.03.2026      5:17          73062 consciousness.py
-a----        01.04.2026     14:54           9153 constitution_hooks.py
-a----        05.04.2026     22:16           2164 content_api.py
-a----        27.03.2026      5:17          13688 context_engine.py
-a----        06.04.2026     12:16          15049 context_manager.py
-a----        10.04.2026     11:46         406782 core.py
-a----        10.04.2026      6:54           4216 crypto_monitor.py
-a----        19.03.2026      0:24           4613 crypto_monitor.py.bak
-a----        27.03.2026      5:17          18370 curiosity.py
-a----        27.03.2026      5:17          13382 dag_agent.py
-a----        27.03.2026      5:17           4470 db_init.py
-a----        27.03.2026      5:17          37557 device_scanner.py
-a----        27.03.2026      5:17          12399 dreamer.py
-a----        27.03.2026      5:17           1004 empathy_engine.py
-a----        31.03.2026      8:44           8472 event_bus.py
-a----        10.04.2026      6:54            288 evolution.py
-a----        22.03.2026     21:03             48 evolution.py.bak
-a----        31.03.2026     12:27          30034 firmware_builder.py
-a----        27.03.2026      5:17          28430 full_audit.py
-a----        27.03.2026      5:17           6376 github_marketplace.py
-a----        27.03.2026      5:17           4087 git_ops.py
-a----        27.03.2026      5:17           4508 graceful_shutdown.py
-a----        27.03.2026      2:03           4507 graceful_shutdown.py.bak
-a----        31.03.2026      9:41           9842 gui_awareness_patch.py
-a----        27.03.2026      5:17           5804 hardware_guard.py
-a----        10.04.2026      6:55           8812 hardware_intel.py
-a----        19.03.2026      0:24           4357 hardware_intel.py.bak
-a----        27.03.2026      5:17           7147 health_monitor.py
-a----        25.03.2026      2:20           6968 health_monitor.py.bak
-a----        27.03.2026      5:17           4689 icon_generator.py
-a----        27.03.2026      5:17          39001 infrastructure.py
-a----        27.03.2026     20:54          11890 input_control.py
-a----        03.04.2026     21:44           2814 integration_orchestrator.py
-a----        10.04.2026     11:02          10029 jarvis_engine.py
-a----        31.03.2026     11:25          11822 kimi_api.py
-a----        28.03.2026      9:26          46556 kolibri_os_builder.py
-a----        27.03.2026      5:17           1507 launch_config.py
-a----        25.03.2026      2:20           1462 launch_config.py.bak
-a----        10.04.2026     12:13          55550 life_support.py
-a----        10.04.2026     12:05          66831 life_support_v2.py
-a----        02.04.2026      0:09          29492 main.cpp
-a----        02.04.2026      0:03          29421 main.ino.bak
-a----        27.03.2026      5:17          37430 master_prompts.py
-a----        07.04.2026     12:42          12123 mcp_api.py
-a----        10.04.2026     12:07          27658 memory.py
-a----        09.04.2026      6:51          11668 mempalace_bridge.py
-a----        27.03.2026      5:17          11403 multi_model.py
-a----        27.03.2026      5:17           9690 observability.py
-a----        27.03.2026      5:17          21890 ollama_autoselect.py
-a----        27.03.2026      5:17           9599 ollama_three.py
-a----        01.04.2026     18:00           9784 openai_responses_tools.py
-a----        28.03.2026      8:49           9374 opi_gpio_patch.py
-a----        27.03.2026      5:17          25427 orangepi_bridge.py
-a----        27.03.2026      5:17           7332 organize_files.py
-a----        25.03.2026      2:20           7084 organize_files.py.bak
-a----        27.03.2026      5:17           5227 pack_archive.py
-a----        25.03.2026      2:20           4939 pack_archive.py.bak
-a----        27.03.2026      5:17          11378 patch_fix_providers.py
-a----        27.03.2026      5:17           8821 patch_mind.py
-a----        27.03.2026      5:17          13150 patch_windows_devices (2).py
-a----        27.03.2026      5:17          13150 patch_windows_devices.py
-a----        31.03.2026     11:24           5839 pip_api.py
-a----        01.04.2026     15:47          15381 pip_manager_ext.py
-a----        10.04.2026     11:46          44136 platform_admin.py
-a----        27.03.2026      5:17          33180 pricing.py
-a----        27.03.2026      5:17           1000 psutil_android.py
-a----        27.03.2026      5:17           3932 pupi_ops.py
-a----        27.03.2026      5:17          14635 pypi_publisher.py
-a----        26.03.2026      0:37          11260 requirements.txt
-a----        01.04.2026     14:54           2452 rollback_manager.py
-a----        27.03.2026      5:17          12928 self_healing.py
-a----        27.03.2026      2:04          12553 self_healing.py.bak
-a----        27.03.2026      5:17          16772 self_model_v2.py
-a----        27.03.2026      5:17           8431 self_sustain.py
-a----        27.03.2026      5:17          38324 server_rental.py
-a----        09.04.2026     22:09          22869 skill_loader.py
-a----        03.04.2026     20:15          24888 skill_loader_patch.py
-a----        27.03.2026     21:40          31459 smart_firmware_researcher.py
-a----        27.03.2026      5:17          16120 smart_systems.py
-a----        27.03.2026      5:17           7426 startup_validator.py
-a----        27.03.2026      2:03           7428 startup_validator.py.bak
-a----        27.03.2026      5:17          21756 status_report.py
-a----        27.03.2026      5:17          13083 sub_agency.py
-a----        27.03.2026      5:17           7546 task_queue.py
-a----        09.04.2026      6:53          43871 telegram_bot.py
-a----        01.04.2026     14:54           2455 telegram_direct_commands.py
-a----        27.03.2026      5:17          73582 thought_book.py
-a----        10.04.2026      6:28          20253 tool_calling.py
-a----        27.03.2026      1:12          16569 tool_calling.py.bak
-a----        10.04.2026     11:40          12772 vision.py
-a----        27.03.2026     20:49            491 win_bridge.py
-a----        27.03.2026     20:33           2329 win_bridge.py.py
-a----        10.04.2026      1:17            151 __init__.py
-a----        31.03.2026      8:43           2710 __init__.py.bak

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
