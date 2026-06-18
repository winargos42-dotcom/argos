---
argos_import: project_file
source_path: .openclaw-workspace/ai_coder_output.txt
source_abs: F:\debug\argoss\.openclaw-workspace\ai_coder_output.txt
source_ext: .txt
source_sha256: 8a90cef203b179fdb758c4a7197846df79914bc61d5d8941e99e86c44e22a43e
text_sha256: b92cc0556a92bf506fa68f007abd95156de58439d94e818ce92cf1c4412d1ce2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# ai_coder_output.txt

- Source: `.openclaw-workspace/ai_coder_output.txt`
- Extract: `text`
- SHA256: `8a90cef203b179fdb758c4a7197846df79914bc61d5d8941e99e86c44e22a43e`

## Content

def factorial(n: int) -> int:
    """
    Вычисляет факториал числа n.
    
    Args:
        n: Целое неотрицательное число
        
    Returns:
        Факториал числа n
        
    Raises:
        ValueError: Если n < 0
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    if n == 0:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    return result

# Пример использования
if __name__ == "__main__":
    try:
        num = 5
        print(f"Факториал {num} = {factorial(num)}")
    except ValueError as e:
        print(f"Ошибка: {e}")

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Agents Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Agents Hub]]
