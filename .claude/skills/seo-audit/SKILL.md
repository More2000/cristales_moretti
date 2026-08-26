---
name: seo-audit
description: Checklist de SEO técnico y on-page verificable — títulos, meta description, encabezados, canonical, sitemap.xml, robots.txt, datos estructurados, Open Graph, imágenes, enlaces internos. Usá esta skill siempre que construyas o revises una página pensada para buscadores (una landing, un sitio de negocio, un blog), o cuando pidan "mejorar el SEO", "que aparezca en Google", "posicionar" o "auditar el sitio". Es la mitad clásica del par SEO/AEO: acá se optimiza para el buscador de toda la vida (Google, Bing); para que te encuentren los buscadores con IA (ChatGPT, Perplexity, Copilot) usá `ai-seo` además de esta.
---

# Auditoría de SEO

Todo lo de acá es verificable: se puede mirar el HTML y decir "pasa" o "no pasa".
Si además necesitás performance y accesibilidad, esas viven en `web-design-guidelines`
— esta skill no las repite, se enfoca en lo específico de motores de búsqueda.

Trabajá de arriba hacia abajo: **metadata de la página → estructura del contenido →
descubribilidad (sitemap/robots) → datos estructurados → detalles**.

---

## Metadata de la página

- **`<title>`**: único por página, 50–60 caracteres, con la palabra clave principal
  y la ubicación/marca si aplica. `"Vidrios y DVH a medida en Villa María | Cristales
  Monetti"` funciona; `"Inicio"` o `"Cristales Monetti"` a secas no.
- **`meta description`**: 120–155 caracteres, con una razón concreta para hacer clic
  (no es una etiqueta de ranking, pero define el CTR desde el resultado). Escribila
  como una frase real, no una lista de keywords separadas por comas.
- **`canonical`**: siempre presente, siempre absoluto (`https://dominio.com/`, no
  relativo), y apunta a la URL que realmente querés que se indexe. Sin esto, una
  página accesible por `/`, `/index.html` y con o sin `www` puede contar como
  contenido duplicado.
- **`meta robots`**: `index, follow` en lo que querés indexado. Si hay páginas de
  prueba, checkout, admin, etc., van `noindex` — no dependas de robots.txt para eso
  (robots.txt evita el rastreo, no la indexación: una URL bloqueada por robots.txt
  igual puede aparecer indexada sin descripción si alguien la enlaza).

## Open Graph y Twitter Card

Esto no afecta el ranking, pero es lo primero que ve un humano cuando comparten el
link — y un share con preview rota mata más clics que un mal título.

- `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width/height`,
  `og:type`, `og:locale`, `og:site_name`.
- La imagen: **1200×630**, con el nombre y la propuesta legibles incluso en miniatura
  chica (probala achicada al tamaño de un thumbnail de WhatsApp antes de darla por
  buena).
- `twitter:card=summary_large_image` + título/descripción/imagen propios (pueden
  repetir los de Open Graph, no hace falta reescribirlos).
- Verificá con el debugger real de la plataforma antes de confiar en que "debería
  funcionar" — Facebook/LinkedIn cachean agresivo y a veces hay que forzar el
  re-scrape.

## Estructura del contenido

- **Un solo `<h1>`** por página, que describe de qué se trata (no el nombre de la
  empresa a secas).
- Jerarquía sin saltos: h1 → h2 → h3, nunca h2 → h4. Los buscadores arman un índice
  de la página a partir de esto tanto como los lectores de pantalla.
- Encabezados descriptivos y específicos del contenido real, no genéricos
  ("Sección 1", "Nuestros servicios" repetido igual en diez sitios distintos).
- El texto visible dice lo mismo que la metadata promete. Un `<title>` sobre
  "reparación de vidrios 24hs" en una página que no menciona ese servicio en el
  cuerpo es la clase de discordancia que un buscador penaliza.
- **Contenido real, no relleno.** Una página de 80 palabras genéricas compite peor
  que una de 300 palabras específicas del negocio, con datos concretos (ubicación,
  qué se hace, para quién).

## Descubribilidad: sitemap.xml y robots.txt

- **`sitemap.xml` tiene que existir de verdad.** Un `robots.txt` que referencia un
  sitemap que da 404 es peor que no mencionarlo — es una señal de sitio descuidado.
  Para un sitio de una sola página, el sitemap es una sola entrada; igual se hace.
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
      <loc>https://dominio.com/</loc>
      <lastmod>2026-08-26</lastmod>
      <changefreq>monthly</changefreq>
    </url>
  </urlset>
  ```
- **`robots.txt`** en la raíz, con `Sitemap:` apuntando a la URL absoluta y real del
  sitemap. No bloquees `/css/`, `/js/` ni ningún recurso que el navegador necesite
  para renderizar la página — Google renderiza antes de indexar, y un sitio que
  parece roto en el render cuenta en contra.
- Verificá que no haya un `noindex` global heredado de un entorno de staging que
  se olvidó de sacar (pasa más de lo que parece).

## Datos estructurados (schema.org)

- Elegí el tipo más específico que aplique, no el genérico: para un negocio físico
  con local, `LocalBusiness` o una subclase más precisa (`HomeAndConstructionBusiness`,
  `Restaurant`, `Dentist`, etc.) antes que `Organization` a secas.
- Campos mínimos para `LocalBusiness`: `name`, `address` (con `PostalAddress`
  completo), `telephone`, `url`. Si hay redes, `sameAs` con los links reales.
- Si hay preguntas frecuentes reales (no inventadas para llenar espacio),
  `FAQPage` con `mainEntity` → `Question`/`Answer`. Doble beneficio: puede generar
  rich results en Google y es el mismo formato que más ayuda en AEO (ver `ai-seo`).
- **Validalo de verdad**, no asumas que el JSON es correcto porque parsea. Un campo
  mal tipado (`"telephone": 1234}` en vez de string) invalida el bloque entero
  silenciosamente. Antes de dar por terminada la auditoría, corré el sitio por el
  Rich Results Test de Google o el validador de schema.org.
- No inventes datos para completar campos (rating, reviews, precios) — schema con
  datos falsos es exactamente el tipo de cosa que genera una acción manual de
  Google contra el sitio.

## Imágenes y enlaces

- `alt` descriptivo en toda imagen con contenido informativo; `alt=""` en las
  puramente decorativas. Nunca `alt="imagen"` o el nombre del archivo.
- Nombre de archivo descriptivo antes de subir (`vidrio-templado-mampara.jpg`, no
  `IMG_4821.jpg`) — pesa poco en el ranking pero es gratis y a veces suma en
  búsqueda de imágenes.
- Enlaces internos con texto de anclaje descriptivo ("ver los planes", no "click
  acá"). Ayuda tanto a SEO como a accesibilidad — es la misma regla en las dos
  skills, no es casualidad.
- Un solo dominio canónico: si el sitio responde en `http://`, `https://`, con y
  sin `www`, todas las variantes tienen que redirigir (301) a una sola versión.

## Antes de dar la auditoría por cerrada

- [ ] `<title>` y `meta description` únicos, con longitud correcta
- [ ] `canonical` absoluto y correcto
- [ ] Open Graph completo, imagen verificada a tamaño miniatura
- [ ] Un solo `<h1>`, jerarquía sin saltos
- [ ] `sitemap.xml` existe y carga (no 404)
- [ ] `robots.txt` no bloquea recursos necesarios para renderizar
- [ ] Datos estructurados presentes, tipados bien, y validados con una herramienta real
- [ ] Todas las imágenes con `alt` apropiado
- [ ] Un solo dominio canónico, sin variantes sueltas sin redirigir
