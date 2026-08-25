---
name: react-view-transitions
description: View Transitions API en React y en la web — transiciones entre estados y entre páginas, view-transition-name, personalización de las animaciones, transiciones entre documentos, accesibilidad y performance. Usá esta skill cuando pidan animar un cambio de página o de vista, transiciones tipo app nativa, un elemento que se expande a pantalla completa, animar reordenamientos de listas, morphing entre miniatura y detalle, o cuando mencionen View Transitions, startViewTransition o navegaciones animadas.
---

# View Transitions

La API saca una foto del antes y del después, y anima entre las dos. Vos cambiás el DOM como
siempre; el navegador arma la transición. Eso es todo el modelo mental.

---

## Lo básico

```js
if (!document.startViewTransition) {
  actualizarDOM();               // fallback: cambio instantáneo, sin romper nada
} else {
  document.startViewTransition(() => actualizarDOM());
}
```

Por defecto ya hay un cross-fade de toda la página. Para que un elemento **se transforme**
en otro entre los dos estados, se le da el mismo nombre en ambos:

```css
.hero-imagen { view-transition-name: hero; }
```

**Solo un elemento puede tener un `view-transition-name` dado a la vez.** Si dos elementos
lo comparten en el mismo momento, la transición se cancela entera y sin error visible.
En listas, el nombre tiene que ser único por item:

```jsx
<img style={{ viewTransitionName: `producto-${id}` }} />
```

---

## En React

React aplica los cambios de estado de forma asíncrona, así que el callback tiene que ver el
DOM ya actualizado. Con `flushSync` se fuerza:

```jsx
import { flushSync } from "react-dom";

function navegar(nuevaVista) {
  if (!document.startViewTransition) return setVista(nuevaVista);
  document.startViewTransition(() => {
    flushSync(() => setVista(nuevaVista));
  });
}
```

`flushSync` fuerza un render sincrónico: usalo puntualmente para esto, no como herramienta general.

React tiene además un componente `<ViewTransition>` en sus builds experimentales que hace
esto sin `flushSync`; si el proyecto no está en experimental, el patrón de arriba es el camino.

Con un router, enganchá la transición en su hook de navegación. En el App Router de Next,
`useRouter` no expone un punto de enganche estable para esto: es más previsible envolver el
cambio de estado propio, o usar transiciones entre documentos (abajo).

---

## Personalizar la animación

La transición se expone como pseudo-elementos sobre la raíz:

```css
::view-transition-old(hero) { animation: 200ms ease-out both fade-out; }
::view-transition-new(hero) { animation: 300ms ease-out both fade-in; }

/* toda la página */
::view-transition-old(root),
::view-transition-new(root) { animation-duration: 250ms; }
```

- `view-transition-name` acepta cualquier identificador; `root` es el de la página completa.
- Para que un elemento **no** participe del cross-fade general, dale su propio nombre.
- Las animaciones corren sobre snapshots: animá `transform` y `opacity`.

---

## Entre páginas (sin JS)

Para sitios multipágina del mismo origen — un sitio estático, por ejemplo — alcanza con CSS:

```css
@view-transition { navigation: auto; }
```

Los elementos que compartan `view-transition-name` entre las dos páginas se transforman uno
en otro. Es la forma más barata de que un sitio común se sienta como una app.

---

## Accesibilidad

Innegociable, y son cuatro líneas:

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) { animation: none !important; }
}
```

Además: durante la transición el contenido son imágenes estáticas, así que no dependas de
ella para nada funcional, y mantené duraciones cortas (200–300ms). Una transición de 600ms
es encantadora la primera vez y molesta la décima.

---

## Performance

- El navegador **rasteriza** los elementos con nombre. Un subárbol enorme con
  `view-transition-name` es caro: nombrá el elemento puntual que se mueve, no el contenedor.
- Si el DOM tarda en actualizarse dentro del callback, la página queda congelada mientras tanto.
  Tené los datos listos antes de arrancar la transición.
- Las transiciones se cancelan si empieza otra: en navegación rápida es esperable y está bien.

---

## Cuándo usarlas y cuándo no

**Sí**: miniatura que se expande a detalle, cambio entre vista lista y grilla, apertura de un
panel o modal desde el elemento que lo dispara, navegación entre páginas hermanas.

**No**: para todo. Si cada cambio de estado de la app anima, la interfaz se siente lenta.
La transición sirve cuando comunica **de dónde vino** el elemento nuevo; si no hay
continuidad espacial que explicar, un cambio directo es mejor.

---

## Depurar

- **No pasa nada**: verificá que `document.startViewTransition` exista, y que el DOM haya
  cambiado realmente dentro del callback (en React, que esté el `flushSync`).
- **Parpadea en vez de transformarse**: los nombres no coinciden entre los dos estados,
  o hay dos elementos con el mismo nombre a la vez.
- **Se ve deformado**: los dos snapshots tienen relaciones de aspecto muy distintas.
  Ajustá con `object-fit` o animá un contenedor de proporción estable.
