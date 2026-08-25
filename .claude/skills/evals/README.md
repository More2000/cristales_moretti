# Evals de las skills

Una eval por skill, corridas el 2026-08-25 con `claude-opus-5`: para cada caso se
ejecutó un agente **con** la skill y otro **sin** ella, con el mismo prompt.

- `evals.json` — los 6 prompts y sus assertions
- `check.py` — verificador programático (contraste real vía Chromium, análisis de
  código con los comentarios removidos)
- `benchmark.json` / `benchmark.md` — resultados y observaciones

## Resultado

| | Con skill | Sin skill |
|---|---|---|
| Assertions aprobadas | 100% (33/33) | 97% (32/33) |
| Tiempo por tarea | 135,9s | 83,6s |
| Tokens por tarea | 46.370 | 38.986 |

**El delta es casi nulo y hay que leerlo con cuidado**: 32 de 33 assertions pasan en
las dos configuraciones, así que no discriminan. Opus sin las skills ya deriva estado
sin `useEffect`, refactoriza a componentes compuestos y usa `flushSync` con feature
detection por su cuenta.

La única diferencia real apareció en la eval de Next.js: **sin la skill, la Server Action
dejó la autorización como comentario** (`// TODO: verificar acá que la sesión...`) mientras
implementaba el resto. El modelo base enunció el principio y no lo ejecutó.

## Limitaciones

- **Una sola corrida por eval y configuración.** Los ± del resumen son la dispersión
  entre evals distintas, no la varianza de repetir la misma. No hay datos de flakiness.
- **`taste` no se puede medir así.** Sus assertions ("sin emojis", "dos pesos
  tipográficos") son proxies groseros; si el hero se ve bien se juzga mirándolo.
- **Los baselines corrieron en este repo**, donde las skills tienen alcance de proyecto.
  Se les indicó explícitamente no invocar ninguna skill, pero no hay garantía dura de
  aislamiento.
- **No se probó el disparo automático.** Estas evals miden la calidad del contenido con
  la skill ya cargada, no si Claude decide invocarla sola. Eso se mide aparte,
  optimizando el campo `description`.

## Para volver a correrlas

Los prompts están en `evals.json`. El procedimiento (lanzar agentes con y sin skill,
calificar, agregar el benchmark, generar el visor) está en la skill `skill-creator`.
