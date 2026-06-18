---
argos_import: project_file
source_path: claude-code-templates/docs/guides/claude-jobs.md
source_abs: F:\debug\argoss\claude-code-templates\docs\guides\claude-jobs.md
source_ext: .md
source_sha256: b26088e25eb6aac96cf57c6b1d4d73d3281f51e1a8d8a3bb9a6a8ec3618f6fb3
text_sha256: ae73462533cfa985d335c7d0b4a5d530a030565274f2fcba6f506df58e130730
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# claude-jobs.md

- Source: `claude-code-templates/docs/guides/claude-jobs.md`
- Extract: `text`
- SHA256: `b26088e25eb6aac96cf57c6b1d4d73d3281f51e1a8d8a3bb9a6a8ec3618f6fb3`

## Content

# Claude Jobs Scraper

Script para encontrar trabajos relacionados con Claude Code y Anthropic Claude utilizando múltiples fuentes y APIs profesionales.

## 🎯 Características

- **APIs Profesionales**: RapidAPI Jobs, Google Jobs (SerpAPI)
- **Scraping Tradicional**: GitHub, YCombinator, WeWorkRemotely (fallback)
- **Filtrado Estricto**: Solo trabajos que mencionen "Claude" explícitamente
- **Datos Estructurados**: JSON compatible con la web existente
- **Rate Limiting**: Manejo responsable de APIs

## 📋 Requisitos

### Opción 1: APIs Profesionales (Recomendado)

1. **RapidAPI Jobs API** - Acceso a 200M+ trabajos de LinkedIn, Indeed, Glassdoor
   - Regístrate en: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jobs-search-realtime-data-api/
   - Plan gratuito: 100 requests/mes
   - Plan pagado: Desde $10/mes

2. **SerpAPI (Google Jobs)** - Búsqueda semántica avanzada
   - Regístrate en: https://serpapi.com/
   - Plan gratuito: 100 búsquedas/mes
   - Plan pagado: Desde $50/mes

### Opción 2: Solo Scraping Gratuito

- No requiere APIs pagadas
- Resultados limitados debido a restricciones de sitios web

## ⚙️ Configuración

1. **Copia el archivo de configuración**:
   ```bash
   cp .env.example .env
   ```

2. **Agrega tus API keys en `.env`**:
   ```bash
   # Para mejores resultados
   RAPIDAPI_KEY=tu_clave_rapidapi
   SERPAPI_KEY=tu_clave_serpapi
   
   # Opcional
   GITHUB_TOKEN=tu_token_github
   ```

3. **Instala dependencias**:
   ```bash
   pip install requests python-dotenv
   ```

## 🚀 Uso

```bash
python generate_claude_jobs.py
```

### Flujo de Funcionamiento:

1. **APIs Profesionales** (si están configuradas)
   - RapidAPI: Busca en LinkedIn, Indeed, Glassdoor, etc.
   - Google Jobs: Búsqueda semántica avanzada
   
2. **Scraping Tradicional** (fallback si no hay APIs)
   - GitHub Issues/Discussions
   - YCombinator Who's Hiring
   - WeWorkRemotely RSS

3. **Generación del JSON**:
   - Archivo: `docs/claude-jobs.json`
   - Estructura compatible con la web existente

## 📊 Datos Generados

Cada trabajo incluye:

```json
{
  "company": "Anthropic",
  "company_icon": "https://anthropic.com/favicon.ico",
  "location": "Remote",
  "description": "Senior AI Developer to enhance Claude Code capabilities...",
  "job_link": "https://anthropic.com/careers/claude-developer",
  "source": "RapidAPI Jobs",
  "date_posted": "2025-09-10T10:00:00Z",
  "salary": 150000
}
```

## 🔧 Filtros Aplicados

El script usa filtrado **ultra-estricto**:

- **Debe mencionar "Claude"** explícitamente
- Términos específicos: `claude code`, `anthropic claude`, `claude ai`, etc.
- Validación de contexto laboral: `hiring`, `position`, `engineer`, etc.

## 📈 Resultados Esperados

Dado que Claude Code es muy nuevo (2025), los resultados serán limitados pero precisos:

- **Con APIs**: 5-20 trabajos relevantes potenciales
- **Solo Scraping**: 0-5 trabajos (debido a restricciones)
- **Calidad**: 100% relevantes (menciones específicas de Claude)

## 🔄 Automatización

Para ejecutar periódicamente:

```bash
# Cron job diario a las 9 AM
0 9 * * * cd /path/to/project && python generate_claude_jobs.py

# GitHub Actions (recomendado)
# Ver ejemplo en .github/workflows/
```

## ⚠️ Limitaciones

1. **Claude Code es nuevo**: Pocas ofertas laborales específicas aún
2. **APIs pagadas**: Mejores resultados requieren suscripciones
3. **Rate limits**: Respetar límites de APIs para evitar bloqueos
4. **Falsos positivos**: Filtrado estricto puede omitir trabajos relevantes

## 🆘 Troubleshooting

### Sin resultados:
- ✅ Verifica API keys en `.env`
- ✅ Revisa límites de rate en las APIs
- ✅ Claude Code es muy específico - resultados limitados son normales

### Errores de API:
- ✅ Verifica saldo en RapidAPI/SerpAPI
- ✅ Revisa formato de API keys
- ✅ Usa VPN si hay restricciones geográficas

## 🔮 Futuro

A medida que Claude Code se popularice (2025-2026):
- Más trabajos específicos aparecerán
- Términos de búsqueda se pueden expandir
- APIs especializadas en AI jobs pueden surgir

---

**Resultado**: JSON estructurado en `docs/claude-jobs.json` listo para consumo por la web.

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
