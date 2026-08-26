---
name: ai-seo
description: AEO — optimización para que un buscador con IA (ChatGPT, Perplexity, Copilot, Gemini, Claude) encuentre y cite el sitio, no solo Google clásico. Cubre acceso de los crawlers de IA en robots.txt, llms.txt, contenido en formato pregunta-respuesta directa, y por qué los datos estructurados pesan el doble acá. Usá esta skill junto con `seo-audit` siempre que construyas o revises un sitio pensado para ser encontrado, o cuando pidan "que aparezca en ChatGPT", "posicionar con IA", "AEO" o "answer engine optimization". El SEO clásico ya no alcanza solo: cada vez más gente pregunta en lugar de buscar.
---

# AEO — optimización para buscadores con IA

Google devuelve una lista de links para que el usuario elija y lea. ChatGPT,
Perplexity, Copilot y las Overviews de Google **leen el contenido por vos y
entregan una respuesta ya armada**, citando (a veces) de dónde la sacaron.
Eso cambia qué hay que optimizar:

- No compite por posición 1 a 10 — compite por **ser la fuente que el modelo
  eligió citar** entre todo lo que rastreó para esa pregunta.
- El contenido se evalúa por **qué tan fácil es extraer una respuesta limpia**
  de él, no por cuántas palabras clave repite.
- Un motor de IA no lee la página como la ve un humano con ojos y scroll: la lee
  como texto plano, en el orden del HTML. Si la respuesta está enterrada dentro
  de un párrafo de marketing, es más difícil de citar que si está en una oración
  directa.

Nada de esto reemplaza `seo-audit` — lo complementa. Un sitio con SEO técnico roto
(sin sitemap, con `noindex` por error, JS-only) tampoco lo va a rastrear bien un
crawler de IA: la mayoría no ejecuta JavaScript de forma confiable, así que el
contenido tiene que estar en el HTML crudo, no armado por un framework en el
navegador.

---

## Paso 1: dejar entrar a los crawlers de IA

Este es el paso que más se salta, y sin él nada de lo demás importa: si el
`robots.txt` bloquea a estos user-agents (a veces por una plantilla vieja, a
veces por un `Disallow: /` genérico que alguien copió sin pensar), el sitio es
invisible para esos motores sin importar qué tan bueno sea el contenido.

```
# Además del User-agent: * general, dejar explícito el acceso
# de los crawlers que alimentan las respuestas de IA:

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: CCbot
Allow: /
```

Notas:
- `Google-Extended` es distinto de `Googlebot`: controla específicamente si Google
  puede usar el contenido para Gemini y AI Overviews. Bloquearlo no saca al sitio
  de la búsqueda normal, pero sí de las respuestas generadas.
- `CCbot` (Common Crawl) no es un motor de respuestas en sí, pero varios modelos
  se entrenan con ese dataset — es la forma más indirecta y de más largo plazo de
  aparecer.
- Esta lista cambia: los nombres de user-agent de estas empresas se agregan y a
  veces se renombran. Si al auditar un sitio parece desactualizada, buscar la
  lista vigente antes de copiarla a ciegas.

## Paso 2: `llms.txt`

Es una convención nueva (2024 en adelante, todavía no la respetan todos los
motores) para darle a un LLM un resumen del sitio en texto plano y estructurado,
sin tener que rastrear e interpretar el HTML completo. Cuesta casi nada agregarlo
y no tiene downside — en el peor caso, el motor que lo lea lo ignora.

Va en la raíz del sitio (`/llms.txt`), en Markdown simple:

```markdown
# Nombre del Negocio

> Una línea que resuma qué es y para quién, sin adjetivos de marketing.

Datos concretos: rubro, ubicación, años en el mercado, qué lo distingue.

## Servicios
- Servicio uno: qué es, en una oración
- Servicio dos: qué es, en una oración

## Contacto
- Dirección: ...
- Teléfono: ...
- Sitio: https://dominio.com/
```

No es un reemplazo del contenido real de la página — es un atajo. Si el `llms.txt`
dice algo que la página no respalda, es peor que no tenerlo.

## Paso 3: escribir para que se pueda citar

Esto es lo que más impacto real tiene, y es puro contenido, no configuración.

- **La respuesta va primero, la explicación después.** Si alguien pregunta
  "¿qué es el DVH?", la primera oración tiene que responder eso — no arrancar con
  contexto de la empresa y llegar a la respuesta en el tercer párrafo. Un modelo
  extrayendo una respuesta corta agarra lo que está arriba y es autocontenido.
- **Formato pregunta → respuesta directa, literal.** Una sección de FAQ con
  preguntas reales (las que un cliente haría) y respuestas de 2-4 líneas es,
  estructuralmente, exactamente lo que un motor de respuestas busca — es casi
  una cita lista para usar. Es el mismo contenido que alimenta el `FAQPage` de
  `seo-audit`: server la misma fuente para las dos cosas.
- **Afirmaciones específicas y verificables, no vagas.** "Más de 70 años de
  trayectoria" es citable. "Amplia experiencia en el rubro" no lo es — no hay
  nada ahí que un modelo pueda repetir con confianza.
- **Un hecho por oración cuando son datos.** Mezclar tres datos en una oración
  larga con subordinadas hace más difícil que el modelo extraiga uno solo limpio.
- **Nada de la respuesta detrás de una interacción.** Contenido que solo aparece
  al hacer click, con scroll infinito, o cargado por JS después del render
  inicial, es contenido que la mayoría de estos crawlers no ve.

## Paso 4: los datos estructurados pesan más acá

En SEO clásico, el schema markup es un extra que puede generar un rich result.
En AEO, varios motores lo usan como **fuente primaria** porque es la forma más
barata de extraer hechos sin tener que interpretar prosa. Por eso, para AEO,
priorizar:

1. `LocalBusiness` (o la subclase más específica) completo: nombre, dirección,
   teléfono, horario si se sabe, `sameAs` con redes reales.
2. `FAQPage` con las preguntas que la gente realmente hace — literal, se puede
   copiar/pegar del contenido visible de la página, no hay que inventar nada
   nuevo.
3. Si aplica: `Product`/`Offer` con precio y disponibilidad, `Review`/
   `AggregateRating` (solo con reseñas reales, nunca inventadas — un motor que
   cruza esto contra Google Maps y lo encuentra falso es peor que no tenerlo).

## Paso 5: lo que esta skill no puede resolver sola

Igual que el SEO clásico no depende solo de la propia página (los backlinks
importan), el AEO tampoco es 100% controlable desde el sitio: estos motores
frecuentemente cruzan y prefieren fuentes de terceros — Google Business Profile,
directorios del rubro, reseñas, menciones en prensa local. Un sitio impecable en
todo lo de arriba compite mejor, pero la presencia fuera del sitio (perfil de
Google Business completo y con los mismos datos exactos que la página — incluida
la dirección, mismo formato) sigue siendo parte real de la estrategia, aunque
quede fuera del alcance de esta skill.

## Antes de dar por terminada la optimización

- [ ] `robots.txt` permite explícitamente a los crawlers de IA relevantes
- [ ] `llms.txt` existe y es honesto (no dice nada que la página no respalde)
- [ ] Las respuestas clave (qué es, qué servicios, dónde, cuánto cuesta si aplica)
      están en oraciones directas y autocontenidas, no enterradas en prosa
- [ ] Hay una sección de preguntas frecuentes reales, con `FAQPage` en schema
- [ ] Todo el contenido crítico está en el HTML crudo, no depende de JS para
      aparecer
- [ ] Los datos de contacto son idénticos, carácter por carácter, a los que
      figuran en Google Business Profile y cualquier otro perfil oficial
