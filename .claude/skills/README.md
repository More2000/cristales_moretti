# Skills

Seis skills para Claude Code, equivalentes en espíritu a las que ofrece v0
(`vercel-react-best-practices`, `web-design-guidelines`, `vercel-composition-patterns`,
`next-best-practices`, `vercel-react-view-transitions`) más una skill de criterio estético.

**No son las skills de Vercel.** Esas son de v0 y no están publicadas en el catálogo de
Claude — no hay forma de importarlas. Estas están escritas de cero sobre las mismas prácticas.

| Skill | Para qué |
|---|---|
| `taste` | Criterio estético: cómo hacer que algo se vea bien y no a plantilla. Tiene modo construcción y modo crítica. |
| `web-design-guidelines` | Lo verificable: semántica, WCAG AA, responsive, estados, Core Web Vitals. |
| `react-best-practices` | Estado, cuándo sobra un `useEffect`, keys, memoización con React Compiler, Actions, Suspense. |
| `composition-patterns` | APIs de componentes: `children` sobre configuración, componentes compuestos, inversión de control, borde server/client. |
| `next-best-practices` | App Router: servidor por defecto, cascadas de datos, caché y revalidación, Server Actions seguras, metadata. |
| `react-view-transitions` | View Transitions API: `view-transition-name`, `flushSync` en React, transiciones entre documentos, accesibilidad. |

`taste` y `web-design-guidelines` se complementan y no se pisan: la primera es el juicio
(¿se ve bien?), la segunda es la correctitud (¿pasa el test?).

## Alcance

Como están en `.claude/skills/` de este repo, Claude Code las carga **solo en este proyecto**.

Para tenerlas en todos tus proyectos, copialas a tu carpeta de usuario:

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/*/ ~/.claude/skills/
```

Verificá que quedaron con `/skills` dentro de Claude Code.

Para compartirlas con un equipo conviene un repo de skills aparte conectado como marketplace,
en vez de copiarlas a mano en cada máquina.

## Cómo se disparan

Claude decide invocarlas leyendo el campo `description` del frontmatter. Están redactadas
para activarse solas en el contexto adecuado (`taste` en cualquier UI visible,
`next-best-practices` en cualquier proyecto Next), pero también se pueden llamar por nombre:
"usá la skill de taste para revisar esta pantalla".

Si alguna se dispara de más o de menos, lo que se ajusta es la `description`, no el cuerpo.
