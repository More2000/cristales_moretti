---
name: web-design-guidelines
description: Estándares verificables para interfaces web — HTML semántico, accesibilidad WCAG AA, responsive real, estados de carga/vacío/error, formularios, performance y Core Web Vitals. Usá esta skill siempre que construyas o revises cualquier UI web: una landing, una app, un componente, un formulario, un email. Es la capa de correctitud (lo que se puede verificar y falla objetivamente); para el criterio estético usá `taste`. Aplicala aunque el pedido no mencione accesibilidad ni performance, porque son justo las cosas que nadie pide y todos necesitan.
---

# Guías de diseño web

Esta skill cubre lo **verificable**: lo que pasa o no pasa un test.
El criterio visual —si algo se ve bien— está en `taste`.

Trabajá en este orden, porque cada nivel depende del anterior:
**semántica → accesibilidad → responsive → estados → performance.**

---

## HTML semántico

El elemento correcto trae gratis comportamiento, accesibilidad y teclado.

- `<button>` para acciones, `<a href>` para navegación. Un `<div onClick>` no recibe foco,
  no responde a Enter ni Space, y no se anuncia como control.
- Landmarks: `<header>`, `<nav>`, `<main>` (uno solo), `<section>` con nombre, `<footer>`.
- **Un solo `<h1>` por página** y jerarquía sin saltos (h2 → h3, nunca h2 → h4).
  Los títulos son el índice con el que se navega con lector de pantalla.
- Listas reales para cosas listadas; `<table>` con `<th scope>` para datos tabulares
  (nunca para maquetar).
- `<details>/<summary>` para acordeones y `<dialog>` para modales: resuelven foco y teclado solos.
- ARIA es el último recurso. Un atributo ARIA mal puesto es peor que ninguno.

---

## Accesibilidad (WCAG AA)

**Contraste** — el mínimo es 4.5:1 para texto normal y 3:1 para texto grande
(≥24px, o ≥18.66px en negrita) y para bordes de controles.
Calculalo, no lo estimes: los azules y verdes medios engañan al ojo.

**Teclado** — todo lo que se puede hacer con el mouse tiene que poder hacerse con teclado.
- Foco visible siempre. `:focus-visible` con contorno de 2–3px y `outline-offset`;
  nunca `outline: none` sin reemplazo.
- Orden de tabulación acorde al orden visual.
- Un modal atrapa el foco mientras está abierto y lo devuelve al cerrarse.
- Skip link al contenido principal como primer elemento enfocable.

**Imágenes y texto**
- `alt` que describa la función de la imagen en su contexto. Decorativa → `alt=""`.
- Un ícono sin texto necesita nombre accesible (`aria-label`). Ojo con los botones que ocultan
  su texto en mobile por CSS: quedan sin nombre.
- Nunca comuniques solo con color (un error tiene que decir por qué, no solo ponerse rojo).
- Zoom al 200% sin pérdida de contenido ni scroll horizontal.

**Movimiento** — respetá `prefers-reduced-motion` y nunca animes más de tres destellos por segundo.

---

## Responsive de verdad

Probar achicando la ventana del escritorio no alcanza: no reproduce el teclado virtual,
el área táctil ni el viewport real.

- **Mobile first.** Escribí el layout chico y ampliá con media queries, no al revés.
- Rango real: **320px hasta 1920px+**. El 320 es donde todo se rompe.
- **Objetivos táctiles de 44×44px mínimo**, con separación entre ellos.
- Nada de scroll horizontal. Cuando algo no entra (tablas, bloques de código, diagramas),
  que scrollee **dentro de su propio contenedor** con `overflow-x: auto`, no el body.
- Cuidado con el `padding` en shorthand: `padding: 40px 0` pisa el `padding-inline` que venía
  del contenedor y deja el contenido pegado al borde en mobile. En desktop no se nota.
- `100vh` en móvil incluye la barra del navegador: usá `100dvh`.
- `ch` se calcula con la fuente **del propio elemento**: un `max-width: 36ch` en un contenedor
  con fuente chica colapsa el bloque.
- Preferí `clamp()` y grillas que se adaptan (`auto-fit` + `minmax`) antes que acumular breakpoints.
- Respetá las áreas seguras (`env(safe-area-inset-*)`) en pantallas con notch.

---

## Los estados que siempre faltan

Toda vista que dependa de datos tiene cuatro estados, y en general se diseña uno solo:

1. **Cargando** — esqueleto con la forma del contenido real, no un spinner centrado.
   Evita el salto cuando llega el contenido.
2. **Vacío** — explicá qué va a aparecer ahí y ofrecé la acción para empezar.
   Un "No hay datos" a secas es una vía muerta.
3. **Error** — qué pasó, en lenguaje humano, y qué puede hacer la persona.
   Con opción de reintentar. Nunca el stack trace.
4. **Con datos** — incluida la versión con **demasiados** datos: nombres largos, 500 filas,
   textos que desbordan. Ahí es donde se rompe el layout.

Además: primera visita vs. usuario recurrente, sin permisos, offline, y el estado de
"acción en curso" (botón deshabilitado + feedback, para que nadie envíe dos veces).

---

## Formularios

- `<label>` asociado a cada campo. El placeholder **no es** una etiqueta: desaparece al escribir.
- `type` correcto (`email`, `tel`, `url`, `number`) para que el móvil muestre el teclado adecuado,
  y `autocomplete` con el token correcto.
- Errores **junto al campo**, no todos juntos arriba, y asociados con `aria-describedby`.
- Validá al salir del campo (`blur`), no en cada tecla: marcar en rojo mientras se escribe es hostil.
- No deshabilites el botón de envío hasta que el formulario sea válido — es mejor dejar enviar
  y mostrar qué falta, porque un botón gris sin explicación no dice qué corregir.
- Pedí solo lo que vas a usar. Cada campo baja la conversión.
- Validá siempre también en el servidor.

---

## Performance

Los umbrales que importan: **LCP < 2.5s**, **CLS < 0.1**, **INP < 200ms**.

- **CLS**: dimensiones explícitas en imágenes, video e iframes; espacio reservado para lo que
  carga después (banners, anuncios); nada que se inserte arriba del contenido ya visible.
- **LCP**: identificá el elemento más grande del primer viewport (suele ser la imagen del hero
  o el título) y priorizalo. Precargá solo eso.
- **Fuentes**: `font-display: swap`, `preconnect` al origen, self-hosting cuando se pueda,
  solo los pesos que usás, y stack de fallback del sistema.
- **Imágenes**: formatos modernos, `srcset`/`sizes` para servir el tamaño correcto,
  `loading="lazy"` en todo lo que esté debajo del pliegue (nunca en el LCP).
- **JavaScript**: es el recurso más caro por byte. Si algo se resuelve con CSS o HTML,
  no lo hagas con JS.
- Que la página funcione sin JS hasta donde sea razonable. Cuidado con animaciones de entrada
  que empiezan en `opacity: 0` y dependen de JS para volverse visibles: si el script no corre,
  el contenido nunca aparece. Poné el fallback en `<noscript>`.

---

## Antes de dar algo por terminado

- [ ] Un solo `<h1>`, jerarquía de títulos sin saltos
- [ ] Navegación completa por teclado con foco visible en todo
- [ ] Contraste AA verificado (calculado, no estimado)
- [ ] `alt` en todas las imágenes; nombre accesible en botones de solo ícono
- [ ] Probado a 320px y en un dispositivo móvil real o emulado, sin scroll horizontal
- [ ] Los cuatro estados resueltos, incluido "demasiados datos"
- [ ] Imágenes con dimensiones; sin saltos de layout
- [ ] `prefers-reduced-motion` respetado
- [ ] Funciona con JS desactivado, o degrada de forma visible y honesta
