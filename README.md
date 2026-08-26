# Landing — Cristales Monetti S.R.L.

Landing de una sola página para Cristales Monetti S.R.L. (Paso de los Libres 1921, Villa María,
Córdoba). HTML estático, sin build ni dependencias: se sube tal cual a cualquier hosting.

```
index.html                        página completa (CSS y JS embebidos)
assets/og-cristales-monetti.jpg   imagen para compartir (1200×630)
assets/favicon.svg                ícono
robots.txt
```

## Cómo verla

Abrir `index.html` en el navegador, o servirla con `npx http-server .`

## Pendientes antes de publicar

Están marcados en la página con el cartel **“Falta confirmar”** y con comentarios
`PLACEHOLDER` / `PENDIENTE` en el HTML. Ninguno se completó con datos inventados.

1. **WhatsApp Business** — falta el número. En la sección de contacto hay un botón ya
   escrito y comentado (`https://wa.me/549XXXXXXXXXX`) listo para reemplazar el cartel
   y pasar a ser el CTA principal. Mientras tanto el CTA es el teléfono fijo.
2. **Horario de atención** — falta definir días y horarios. Además, agregar
   `openingHoursSpecification` al JSON-LD (hay un comentario indicando dónde).
3. **Dominio** — hoy figura `https://cristalesmonetti.com.ar/` como placeholder en
   `canonical`, Open Graph, JSON-LD y `robots.txt`. Reemplazar por el dominio real
   (las URLs de Open Graph tienen que ser absolutas para que se vea la preview).
4. **Foto de la fachada** — el hero usa una composición de vidrios hecha con CSS.
   En `index.html` hay un comentario con el `<img>` y su `alt` ya redactados para
   reemplazarla por la foto real (`assets/fachada-cristales-monetti.jpg`).
5. **Coordenadas del local** — agregar `geo` (lat/long) al JSON-LD para el mapa.

## Datos usados (confirmados)

Paso de los Libres 1921, Villa María, Córdoba · (0353) 453-3054 · [@cristalesmonetti](https://www.instagram.com/cristalesmonetti/)
· Distribuidor oficial VASA · más de 70 años de trayectoria · venta mayorista y minorista.

No se incluyeron testimonios: todavía no hay ninguno recopilado, así que la prueba social
se apoya solo en señales verificables (trayectoria, VASA, local con link a Google Maps,
Instagram).

## Decisiones técnicas

- **Paleta:** `#0A4A82` `#1C7DC4` `#6FC3F0` `#F0F7FC` `#0E1B26`, tomada de la fachada
  (vidrio espejado azul + cartel blanco con logo azul).
  Para texto chico sobre blanco se usa `#1770B5`: `#1C7DC4` queda en 4.39:1 y no llega a AA.
- **Rendimiento:** un solo archivo, sin frameworks, sin imágenes en el flujo principal.
  La única request externa son las tipografías (Outfit + Inter) con `preconnect` y
  `display=swap`, y stack de fallback del sistema.
- **Accesibilidad:** un solo `<h1>`, jerarquía h2/h3 correcta, foco visible en todos los
  elementos interactivos, skip link, FAQ con `<details>` nativo (funciona sin JS),
  contraste AA verificado en todos los textos.
- **Movimiento:** fade-in con IntersectionObserver, anulado con `prefers-reduced-motion`
  y con un fallback en `<noscript>` para que el contenido se vea siempre.
- **SEO/AEO:** title y meta description con rubro + ciudad, Open Graph completo,
  JSON-LD `HomeAndConstructionBusiness` + `FAQPage`.

Probado en Chromium a 1440px y en emulación de iPhone 12, Pixel 5 y Galaxy S8 (360px),
sin scroll horizontal en ninguno.
