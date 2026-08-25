---
name: react-best-practices
description: Prácticas actuales de React (19+) — manejo de estado, cuándo un efecto sobra, keys, memoización en la era del compilador, Actions, Suspense y límites de error. Usá esta skill siempre que escribas, revises o refactorices componentes de React, hooks o lógica de estado, aunque el pedido sea chico ("agregá un input", "arreglá este componente"). Aplicala especialmente si aparece useEffect, useMemo, useCallback, estado duplicado o listas renderizadas, porque ahí es donde se concentran los errores caros.
---

# React, en la práctica

El principio que ordena casi todo: **la UI es una función del estado.** La mayoría de los
bugs de React vienen de tener más estado del necesario, o del mismo dato guardado en dos lados.

---

## Estado: lo mínimo posible

### Derivá, no sincronices
Si un valor se puede calcular a partir de props o de otro estado, calculalo durante el render.
No lo guardes.

```jsx
// Mal: dos fuentes de verdad y un frame donde no coinciden
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);
useEffect(() => { setCount(items.length) }, [items]);

// Bien
const [items, setItems] = useState([]);
const count = items.length;
```

Si el cálculo es realmente caro (miles de items, no cientos), ahí sí `useMemo` — pero medí antes.

### Resetear estado con `key`, no con efectos
Cuando un componente tiene que volver a cero porque cambió su contexto, cambiale la `key`.
React desmonta y monta de nuevo, y el estado se va solo.

```jsx
// Mal: efecto que limpia a mano y corre un render tarde
useEffect(() => { setDraft("") }, [userId]);

// Bien
<Editor key={userId} />
```

### Un estado, no cinco booleanos
`isLoading`, `isError`, `isSuccess`, `isEmpty` permiten estados imposibles
(cargando y con error a la vez). Usá una máquina simple:

```jsx
const [status, setStatus] = useState("idle"); // idle | loading | success | error
```

### Colocá el estado donde se usa
Subilo solo hasta el ancestro común más cercano de quienes lo necesitan. Estado global para
algo que usan dos hermanos es deuda: re-renderiza de más y acopla todo.

---

## `useEffect`: casi siempre sobra

Un efecto sirve para **sincronizar con un sistema externo a React**: una suscripción, un
`addEventListener`, un timer, una API del navegador, una librería no-React. Nada más.

No va efecto para:

| En vez de un efecto que… | Hacé esto |
|---|---|
| calcula un valor derivado | calculalo en el render |
| responde a un click o submit | ponelo en el handler del evento |
| resetea estado al cambiar una prop | `key` |
| avisa al padre que algo cambió | llamá al callback en el handler |
| busca datos al montar | Server Component, o una librería de data fetching |

La regla mental: **¿esto pasó por algo que hizo el usuario, o porque el componente apareció
en pantalla?** Si fue el usuario, va en el handler.

Cuando sí escribís un efecto:
- Devolvé siempre la limpieza (unsubscribe, clearTimeout, abort).
- Asumí que va a correr dos veces en desarrollo (StrictMode). Si eso rompe algo, el efecto
  está mal, no StrictMode.
- Un efecto, una responsabilidad. No agrupes cosas no relacionadas por compartir dependencias.

---

## Memoización en la era del compilador

Con **React Compiler** activado, `useMemo` / `useCallback` / `memo` escritos a mano
en general sobran: el compilador memoiza por vos y lo hace mejor. Escribí el componente
limpio y dejá que compile.

Sin compilador, memoizá con intención, no por reflejo:
- `useCallback` solo si la función se pasa a un hijo memoizado o es dependencia de un efecto.
- `memo` en el borde de un subárbol caro que recibe props estables, no en cada componente.
- Memoizar todo tiene costo propio (comparaciones + memoria) y suele empatar o perder.

Lo que sí importa siempre: **no crear objetos y arrays nuevos en el render** si van a bajar
como props a algo memoizado, y **no definir componentes adentro de otros componentes**
(se desmonta y remonta todo en cada render).

---

## Keys

- Una `key` estable y única entre hermanos, del dato: `item.id`.
- **El índice sirve solo si la lista nunca se reordena, filtra ni recibe inserciones.**
  Con índice, borrar el primer item hace que el estado interno de cada fila se corra una posición.
- Nunca `key={Math.random()}`: remonta todo en cada render y pierde foco y scroll.

---

## React 19: lo que cambió y conviene usar

- **`ref` es una prop normal.** `forwardRef` ya no hace falta para componentes nuevos.
- **Actions**: `useActionState` para el ciclo pending/error/resultado de un envío,
  `useFormStatus` para que un hijo sepa si el form está enviando, `useOptimistic` para
  mostrar el resultado antes de que confirme el servidor.
- **`use()`** lee una promesa o un contexto, y a diferencia de los hooks se puede llamar
  condicionalmente.
- **Metadata en el componente**: `<title>`, `<meta>` y `<link>` renderizados adentro se
  elevan al `<head>` solos.
- **`ref` con función de limpieza**: el callback ref puede devolver su cleanup.

---

## Suspense y errores

- Un `<Suspense>` **por unidad de carga independiente**, con un fallback que tenga la forma
  aproximada del contenido real. Un spinner tapando toda la página anula el streaming.
- Un `fallback` que cambia mucho de tamaño respecto del contenido final genera salto de layout.
- Los Error Boundaries van **cerca de lo que puede fallar**, para que el resto de la página
  sobreviva. Uno solo en la raíz convierte cualquier error en pantalla en blanco.
- Los boundaries no atrapan errores de handlers ni de código asíncrono: eso se maneja donde ocurre.

---

## Formularios

- **No controles lo que no necesitás controlar.** Un input no controlado con `defaultValue`
  y lectura en el submit alcanza para la mayoría de los casos y no re-renderiza en cada tecla.
- Controlado cuando necesitás validación en vivo, formateo mientras se escribe o estado
  compartido con otra parte de la UI.
- Validá también del lado del servidor. La validación del cliente es UX, no seguridad.

---

## Señales de que algo va mal

- Un `useEffect` con `setState` adentro y sin sistema externo involucrado.
- El mismo dato en dos `useState`.
- Props que atraviesan cuatro niveles sin que nadie las use en el camino
  (mirá `composition-patterns`: pasar `children` suele resolverlo mejor que un contexto).
- Un componente de 400 líneas con ocho hooks: casi siempre son dos componentes.
- `useMemo` en todo, incluidos strings y números.
- `key={index}` en una lista con botón de borrar.
