---
name: taste
description: Criterio estético para interfaces — cómo hacer que algo se vea bien y no a plantilla generada. Usá esta skill siempre que estés construyendo o revisando UI visible: una landing, una pantalla de producto, un dashboard, un componente, un email. También cuando el usuario pida "que se vea bien", "más lindo", "más profesional", "le falta algo", "parece hecho con IA", o cuando pida una crítica o review de un diseño existente. Aplicala aunque no la pidan por nombre: si el resultado del trabajo lo va a mirar un ser humano, corresponde.
---

# Taste

Dos modos. **Construcción**: criterio que aplicás mientras escribís la UI.
**Crítica**: cuando te pasan algo hecho y piden una lectura.

El objetivo no es que la página sea impresionante. Es que se vea **decidida** —
que cada cosa esté donde está porque alguien lo eligió, no porque era el default.

---

## El olor a plantilla

Antes que nada, esto es lo que hay que evitar. Son los tics que delatan una UI
generada sin criterio, y aparecen juntos casi siempre:

- **Gradiente violeta → rosa** de fondo, o en el título, sin ninguna relación con la marca.
- **Emojis como íconos.** 🚀 en el hero, ✨ en los features, 💡 en el tip.
- **Tres cards idénticas** en fila porque tres es el número que queda lindo, no porque haya tres cosas.
- **Copy intercambiable**: "Elevate your workflow", "Seamless experience", "Built for the modern web".
  Si la frase sirve para un CRM, una barbería y un banco, no dice nada.
- **Glassmorphism sobre nada.** Blur y transparencia sin un fondo que justifique el efecto.
- **Todo redondeado a 16px y todo con sombra**, incluidos los elementos que no flotan.
- **Contadores animados** (`0 → 10.000 clientes`) en un negocio que no tiene 10.000 clientes.
- **Dark mode con azul saturado** sobre negro puro, ilegible.

La prueba: **tapá el logo y el texto. ¿Se puede saber de qué rubro es?**
Si no, la página no es de nadie.

---

## Modo construcción

### Tipografía
Es el 80% de la percepción de calidad y lo primero que se rompe.

- **Dos pesos por página, tres si hay una razón.** Un peso para títulos (600/700), uno para
  texto (400). El "medium" para todo lo intermedio es lo que hace que nada tenga jerarquía.
- **Una escala, no números al azar.** Ej: 12 / 14 / 16 / 20 / 24 / 32 / 48. Si aparece un
  `font-size: 17.5px` suelto, se nota aunque nadie sepa por qué.
- **Line-height inverso al tamaño.** Títulos 1.1–1.2, texto 1.5–1.7. Un H1 en 1.6 se desarma.
- **Letter-spacing negativo en títulos grandes** (-0.02em a -0.03em). Las tipografías se
  diseñan para texto; en 48px las letras quedan sueltas.
- **Ancho de línea 55–75 caracteres.** `max-width: 65ch` — pero ojo, `ch` usa la fuente del
  elemento, no la del body. Un `max-width: 36ch` en un contenedor con fuente chica colapsa
  el bloque entero.
- **Números tabulares** (`font-variant-numeric: tabular-nums`) en tablas, precios y contadores.

### Espaciado
- **Escala, no improvisación.** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96. Nada de `margin: 37px`.
- **El espacio agrupa.** Los elementos relacionados van más cerca entre sí que del resto.
  Un título separado de su párrafo por lo mismo que del bloque siguiente no se lee como un grupo.
- **Más aire del que parece necesario.** El error casi siempre es de menos, no de más.
- **Espaciado vertical asimétrico**: más arriba de un título que abajo. El título pertenece
  a lo que sigue, no a lo que vino antes.

### Color
- **El gris hace el trabajo.** Una UI buena es 90% neutros. El color de marca aparece en el
  CTA, en un acento, y poco más. Si todo es azul, nada es importante.
- **Nunca negro puro ni blanco puro** en superficies grandes. `#0E1B26` sobre `#F0F7FC`
  respira; `#000` sobre `#FFF` vibra.
- **Grises con temperatura.** Si la marca es azul, que los grises tengan azul. Un gris
  neutro `#808080` al lado de un azul de marca se ve sucio.
- **Contraste verificado, no estimado.** El ojo miente con los azules y verdes medios.
  Un `#1C7DC4` sobre blanco parece contrastado y da 4.39:1 — no llega a AA para texto chico.
  Calculalo.
- **Máximo tres colores de acento**, y que uno domine.

### Jerarquía y layout
- **Una sola cosa importante por pantalla.** Si hay dos CTAs del mismo peso visual, no hay CTA.
- **Alineá a una grilla.** Los bordes izquierdos de todo lo que se apila tienen que coincidir.
  El desalineado de 3px es lo que hace que algo "se vea raro" sin que se sepa por qué.
- **Densidad acorde al uso.** Un dashboard que se mira 8 horas por día quiere densidad alta.
  Una landing que se mira 20 segundos quiere aire.
- **Rompé la grilla a propósito, una vez.** Un elemento que se sale de la caja da vida.
  Dos, es caos.

### Bordes, sombras y profundidad
- **La sombra indica elevación, no decoración.** Si el elemento no flota sobre otro, no lleva sombra.
- **Sombras en capas y sutiles.** Una sombra real son dos: un contacto corto y difuso
  (`0 1px 2px rgba(0,0,0,.06)`) y una ambiental larga (`0 8px 24px rgba(0,0,0,.07)`).
  Una sola sombra de `0 4px 12px rgba(0,0,0,.3)` se ve a videojuego de 2009.
- **Radio consistente y escalado.** Si las cards son 14px, los botones adentro no pueden ser 14px:
  el radio interior va más chico que el exterior.
- **Borde de 1px antes que sombra.** En UI densa el borde separa mejor y pesa menos.

### Movimiento
- **150–250ms para casi todo.** Menos de 100ms no se percibe; más de 400ms molesta a la tercera vez.
- **Easing con salida, no lineal.** `cubic-bezier(.4,0,.2,1)`. Lo lineal se ve mecánico.
- **Animá `transform` y `opacity`.** Todo lo demás dispara layout y se traba.
- **La animación explica algo o no va.** Un fade-in al hacer scroll está bien una vez por sección;
  seis elementos entrando en secuencia es un preloader disfrazado.
- **`prefers-reduced-motion` siempre.** No es opcional y son tres líneas.

### Copy
El texto es diseño. Un layout impecable con copy genérico se ve genérico.

- **Específico sobre superlativo.** "Cortamos el vidrio a la medida que traigas" gana a
  "Soluciones integrales en vidrio".
- **Los botones dicen qué pasa.** "Pedir presupuesto", no "Enviar". "Borrar los 3 archivos", no "OK".
- **Escribí como habla el negocio.** Un taller no dice "optimizamos su experiencia".

---

## Modo crítica

Cuando te pidan revisar algo existente, no listes todo lo que está mal. Ordená por
lo que más cambia la percepción y sé concreto: cada falla con su corrección.

```
## Veredicto
[Una línea honesta. Qué impresión da y por qué.]

## Lo que falla
1. [Alto] Jerarquía tipográfica — el H1 (600) y el texto (500) compiten,
   la página se lee como un bloque plano.
   → Bajar el texto a 400 y subir el H1 a 700.

2. [Medio] El azul de marca está en 6 lugares distintos, así que el CTA no destaca.
   → Dejarlo solo en el botón principal; el resto en gris.

3. [Bajo] Radio de 16px en las cards y 16px en los botones internos.
   → Botones a 8px.

## Lo que está bien
[Nombralo. Sirve para saber qué no tocar.]
```

Reglas de la crítica:
- **Máximo 5 problemas.** Una lista de 20 no se acciona.
- **Nunca "mejorá el espaciado".** Decí qué valor y dónde.
- **Separá gusto de error.** "Yo iría con más aire" es una opinión; "el contraste da 3.1:1
  y no pasa AA" es un hecho. Marcá cuál es cuál.

---

## Cuándo romper todo esto

Estas reglas producen UI sólida y correcta. No producen UI memorable.
Cuando el proyecto pide personalidad — una marca con carácter, un portfolio, algo editorial —
elegí **una** cosa para llevar al extremo: tipografía enorme, un color agresivo, una grilla rota,
densidad brutal. Una. El resto se mantiene disciplinado, y por eso esa decisión se lee como
decisión y no como error.
