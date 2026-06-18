# AI Code Generator Skill

Навык для генерации Python кода через AI (Gemini/Ollama) по описанию задачи на естественном языке.

## Возможности

- **Генерация кода**: Создание Python кода по описанию задачи
- **Валидация**: Проверка синтаксиса сгенерированного кода
- **Безопасность**: Обнаружение и предупреждение о потенциально опасных операциях
- **Исправление ошибок**: Автоматическая попытка исправления синтаксических ошибок
- **Форматирование**: Чистый, хорошо документированный код с комментариями на русском

## Триггерные фразы

Навык активируется при обнаружении следующих фраз в сообщении:

- `сгенерируй код`
- `напиши код` 
- `генерация кода`
- `ai код`
- `code generation`
- `generate code`
- `write code`
- `создай скрипт`
- `напиши скрипт`
- `скрипт python`

## Использование

### Через Telegram бот ARGOS

```
Пользователь: сгенерируй код для парсинга веб-страницы

ARGOS: ✅ **Код сгенерирован успешно!**

**Задача:** сгенерируй код для парсинга веб-страницы

```python
import requests
from bs4 import BeautifulSoup

def parse_webpage(url: str) -> dict:
    """
    Парсит веб-страницу и извлекает заголовок и все ссылки.
    
    Args:
        url: URL веб-страницы для парсинга
        
    Returns:
        Словарь с заголовком и списком ссылок
    """
    try:
        # Отправляем GET-запрос
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Извлекаем заголовок страницы
        title = soup.title.string if soup.title else "Без заголовка"
        
        # Извлекаем все ссылки
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.text.strip(),
                'url': link['href']
            })
        
        return {
            'title': title,
            'links': links
        }
        
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return {}

# Пример использования
if __name__ == "__main__":
    result = parse_webpage("https://example.com")
    print(f"Заголовок: {result.get('title')}")
    print(f"Найдено ссылок: {len(result.get('links', []))}")
```

*Проверка: Код валиден*
```

### Программное использование

```python
from src.skills.ai_code_generator.skill import AICodeGenerator

# Инициализация
generator = AICodeGenerator(core=argos_core)

# Генерация кода
result = generator.generate_code(
    description="напиши функцию для шифрования строки",
    language="python"
)

if result["success"]:
    print(f"Сгенерированный код:\\n{result['code']}")
else:
    print(f"Ошибка: {result.get('error')}")
```

## Архитектура

### Основные компоненты

1. **Класс `AICodeGenerator`**:
   - `generate_code()`: Основной метод генерации кода
   - `handle()`: Обработчик сообщений для интеграции с ARGOS
   - `_ask_ai()`: Запрос к AI моделям (Gemini → Ollama fallback)
   - `_extract_code()`: Извлечение чистого кода из ответа AI
   - `_validate_python_code()`: Проверка синтаксиса Python
   - `_add_safety_checks()`: Добавление проверок безопасности

2. **Модульные функции**:
   - `handle()`: Точка входа для skill_loader
   - `setup()`: Настройка навыка с ядром ARGOS

### Безопасность

Навык включает несколько уровней безопасности:

1. **Валидация синтаксиса**: Проверка через `ast.parse()`
2. **Обнаружение опасных операций**: Поиск `eval`, `exec`, `__import__`, `os.system`, etc.
3. **Предупреждения**: Добавление комментариев-предупреждений при обнаружении рисков
4. **Изоляция**: Генерация кода выполняется без его автоматического исполнения

## Интеграция с Evolution Engine

Навык может быть использован Evolution Engine для самоулучшения ARGOS:

```python
from evolution_engine import EvolutionEngine

# Создание навыка через эволюцию
engine = EvolutionEngine(core=argos_core)
result = engine.evolve(target="улучшение генерации кода")
```

## Тестирование

```bash
# Запуск тестов
python -m unittest tests.test_ai_code_generator -v

# Покрытие тестами
# Все основные функции покрыты unit-тестами
```

## Зависимости

- `ast`: Для проверки синтаксиса Python
- `re`: Для работы с регулярными выражениями
- `json`: Для обработки структур данных
- `argos_core`: Для доступа к AI моделям (Gemini/Ollama)

## Ограничения

1. **Требуется ядро ARGOS**: Для доступа к AI моделям
2. **Только Python**: В текущей версии поддерживается только генерация Python кода
3. **Без исполнения**: Сгенерированный код не выполняется автоматически
4. **Качество AI**: Зависит от используемой AI модели (Gemini/Ollama)

## Планы развития

1. **Поддержка других языков**: JavaScript, Go, Rust
2. **Контекстная генерация**: Учет существующего кода в проекте
3. **Интерактивный режим**: Уточняющие вопросы для улучшения результата
4. **Интеграция с IDE**: Плагины для VS Code, PyCharm
5. **База знаний**: Сохранение и повторное использование успешных шаблонов