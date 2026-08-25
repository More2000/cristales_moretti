---
name: next-best-practices
description: Prácticas del App Router de Next.js — Server Components por defecto, data fetching sin cascadas, caché y revalidación, Server Actions seguras, streaming, metadata, imágenes y fuentes. Usá esta skill siempre que trabajes en un proyecto Next.js: crear o modificar rutas, layouts, páginas, route handlers o Server Actions, resolver problemas de caché o datos desactualizados, optimizar carga, o decidir qué corre en servidor y qué en cliente. Aplicala también si el pedido parece chico, porque las decisiones de servidor/cliente y de caché se pagan caro después.
---

# Next.js (App Router)

Dos ideas ordenan casi todo: **el servidor es el default**, y **la caché es explícita**.
Lo que se rompe suele venir de olvidar una de las dos.

---

## Servidor por defecto

Todo componente es Server Component hasta que alguien escribe `'use client'`.

`'use client'` va **en la hoja, no en la raíz**: en el componente que realmente necesita
estado, efectos, eventos o APIs del navegador. Ponerlo en el layout convierte toda la app
en cliente y se pierde el sentido del App Router.

Cuando un componente interactivo tiene que envolver contenido estático, pasalo como
`children` en vez de importarlo adentro — así el contenido sigue renderizando en servidor
(está desarrollado en `composition-patterns`).

Nunca importes en un componente cliente un módulo que lee secretos. Solo las variables con
prefijo `NEXT_PUBLIC_` llegan al navegador, y **todo lo que llega al navegador es público**.

---

## Datos: evitar la cascada

El error de performance más común del App Router es pedir datos en secuencia sin necesidad.

```jsx
// Cascada: el segundo fetch espera al primero sin depender de él
const user = await getUser(id);
const posts = await getPosts(id);

// Paralelo
const [user, posts] = await Promise.all([getUser(id), getPosts(id)]);
```

Otras cosas que ayudan:

- **Pedí los datos donde se usan.** No hace falta bajarlos por props desde el layout: varias
  peticiones iguales en el mismo render se deduplican.
- **No bloquees toda la página por un dato lento.** Aislá esa parte en su propio componente
  async dentro de un `<Suspense>` y dejá que el resto se muestre.
- `await` en el layout bloquea todas las rutas hijas: pensalo dos veces.

---

## Caché y revalidación

Es lo que más confunde, y casi siempre el bug es "cambié el dato y la página sigue vieja".

- Decidí explícitamente el comportamiento de cada fetch (cacheado, revalidado por tiempo,
  o siempre fresco) en vez de confiar en el default de la versión que estés usando: cambió
  entre versiones de Next.
- **Etiquetá lo que vas a invalidar** y revalidá por tag después de escribir. Es más preciso
  que revalidar rutas sueltas.
- Después de un Server Action que escribe, **revalidá antes de redirigir**, o el usuario
  aterriza en la versión vieja.
- Usar APIs dinámicas (`cookies()`, `headers()`, `searchParams`) vuelve dinámica la ruta.
  Si eso no era la intención, movelo al componente más chico posible.
- Para datos por usuario, cachear a nivel de ruta es peligroso: revisá que no se comparta
  entre sesiones.

Cuando algo "no se actualiza", revisá en orden: caché del fetch → caché de ruta →
caché del router en el cliente.

---

## Server Actions

Una Server Action es **un endpoint público**. Que se llame como una función local no cambia
que cualquiera puede invocarla con cualquier payload.

En toda action que escriba o lea algo sensible:

1. **Verificá la sesión adentro de la action.** No alcanza con haber ocultado el botón.
2. **Verificá permisos sobre el recurso concreto**, no solo que haya usuario logueado.
3. **Validá y parseá la entrada** con un esquema. Nunca confíes en los tipos de TypeScript
   para datos que llegan de afuera: se borran en runtime.
4. **Revalidá** lo que haya cambiado.
5. Devolvé errores como valor de retorno para mostrarlos en la UI, no como excepciones sueltas.

Actions para mutaciones desde la propia app. Route Handlers para webhooks, APIs públicas o
consumidores externos.

---

## Streaming y carga

- `loading.tsx` da un fallback a la ruta entera; `<Suspense>` a mano da control fino.
- El fallback debería tener **la forma del contenido** (un esqueleto), no un spinner centrado:
  evita el salto de layout cuando llega el contenido.
- Streaming sirve cuando parte de la página es rápida y parte lenta. Si todo es lento, no arregla nada.

---

## Metadata y SEO

- `metadata` estático cuando no depende de datos; `generateMetadata` cuando sí.
- Definí `metadataBase` para que las URLs de Open Graph queden absolutas — si son relativas,
  la preview al compartir no carga.
- `opengraph-image.tsx` genera la imagen social sin diseñarla a mano.
- Datos estructurados (JSON-LD) en un `<script type="application/ld+json">` dentro del
  componente de la página.
- `generateStaticParams` para prerenderizar rutas dinámicas conocidas.

---

## Imágenes y fuentes

- `next/image` **siempre con `width` y `height`** (o `fill` con un contenedor posicionado),
  para reservar el espacio y no mover el layout.
- `priority` solo en la imagen del LCP — la del hero. Ponerlo en varias es contraproducente.
- `sizes` correcto cuando la imagen es responsiva: sin eso se sirve la versión más grande.
- `next/font` se auto-hostea, elimina la request a Google y evita el flash de texto.
  Cargá solo los pesos que usás.

---

## Errores y no encontrados

- `error.tsx` es Client Component y recibe `reset()`. Ponelo cerca de lo que puede fallar,
  no solo en la raíz.
- `not-found.tsx` con `notFound()` para 404 reales, así el status HTTP es correcto para los buscadores.
- `global-error.tsx` cubre fallas del layout raíz.

---

## Señales

- `'use client'` en el layout raíz.
- Varios `await` seguidos que no dependen entre sí.
- Una Server Action sin chequeo de sesión adentro.
- `useEffect` + `fetch` para datos que podría traer el servidor.
- Datos que no se actualizan después de escribir (falta revalidar).
- Imágenes sin dimensiones.
