---
name: composition-patterns
description: Cómo componer componentes de React que aguanten cambios — children sobre configuración, componentes compuestos, inversión de control, variantes en vez de sopa de booleanos, y el borde server/client. Usá esta skill cuando diseñes la API de un componente, cuando uno esté creciendo en props o condicionales, cuando haya prop drilling, cuando aparezca la duda de dividir o abstraer un componente, o al armar un design system o librería de UI.
---

# Patrones de composición

Casi todo componente que se vuelve difícil de mantener siguió el mismo camino: nació simple,
le fueron agregando props para cada caso nuevo, y terminó siendo un archivo de condicionales.

La salida casi siempre es la misma: **dejar de configurar y empezar a componer.**

---

## `children` antes que props de configuración

```jsx
// Se rompe en cuanto alguien quiere un ícono al lado del título
<Card title="Ventas" subtitle="Este mes" icon={<Chart/>} action={<Button/>} footer="..." />

// Aguanta cualquier caso
<Card>
  <Card.Header>
    <Chart /> <h3>Ventas</h3>
  </Card.Header>
  <Card.Body>…</Card.Body>
</Card>
```

La pregunta útil: **¿esta prop describe *qué es* el componente, o *qué hay adentro*?**
Lo que es (`variant`, `size`, `disabled`) va como prop. Lo que hay adentro va como children.

---

## Componentes compuestos

Un componente padre que comparte estado implícito con hijos que se pueden acomodar libremente.
Es el patrón de `<select>/<option>`, y de casi todas las librerías de UI buenas.

```jsx
<Tabs defaultValue="datos">
  <Tabs.List>
    <Tabs.Trigger value="datos">Datos</Tabs.Trigger>
    <Tabs.Trigger value="config">Configuración</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="datos">…</Tabs.Panel>
</Tabs>
```

El estado vive en `Tabs` y viaja por contexto interno. Quien lo usa reordena, envuelve o
intercala lo que quiera sin que vos hayas previsto ese caso.

Cuándo conviene: cuando hay varias partes que van juntas pero cuyo orden y envoltura no
querés fijar. Cuándo no: para un componente de una sola pieza, es sobreingeniería.

---

## Variantes, no booleanos acumulados

```jsx
// Cuatro booleanos = 16 combinaciones, la mayoría sin sentido
<Button primary secondary large disabled />

// Estados imposibles eliminados por diseño
<Button variant="primary" size="lg" />
```

Si dos props no pueden ser verdaderas a la vez, son una sola prop con valores.

---

## Inversión de control

Cuando un componente empieza a acumular props tipo `onBeforeX`, `shouldY`, `renderZ`,
está pidiendo que le devuelvas el control a quien lo usa.

- **`children` como función** cuando quien consume necesita el estado interno para decidir el markup.
- **Prop de render** (`renderItem`) para listas donde el item lo decide el consumidor.
- **`asChild` / polimorfismo**: el componente aporta comportamiento y estilo, y quien lo usa
  decide el elemento final (un `<a>`, un `<Link>`, un `<button>`). Evita duplicar `Button`,
  `ButtonLink` y `ButtonAnchor`.
- **Custom hooks**: si lo que se comparte es lógica y no markup, un hook (`useDisclosure`,
  `useSelection`) compone mucho mejor que un componente.

---

## Prop drilling: cuándo importa

Pasar props tres niveles no es un problema en sí. El problema es pasar props por componentes
**a los que no les incumben**.

Antes de crear un contexto, probá composición: si el que tiene el dato renderiza el que lo
necesita y se lo pasa como `children`, los niveles intermedios desaparecen.

```jsx
// Layout ya no necesita saber nada de user
<Layout sidebar={<Profile user={user} />}>
  <Feed user={user} />
</Layout>
```

Contexto para lo que es genuinamente ambiental y cambia poco: tema, idioma, sesión, config.
Recordá que **todo consumidor re-renderiza cuando el valor cambia** — partí los contextos por
frecuencia de cambio, y no metas en el mismo objeto el estado que cambia en cada tecla junto
al que cambia una vez por sesión.

---

## El borde server/client

En React Server Components, `'use client'` marca el punto donde empieza el bundle del cliente:
todo lo que ese componente importa se va con él.

La regla que más rinde: **poné `'use client'` lo más abajo posible en el árbol**, y cuando un
componente interactivo tiene que envolver contenido estático, pasalo como `children` en vez de
importarlo adentro.

```jsx
// El acordeón es cliente; el contenido sigue siendo server y no viaja al bundle
<ClientAccordion>
  <ServerContenidoPesado />
</ClientAccordion>
```

Un componente cliente puede *recibir* Server Components como children, pero no *importarlos*.

---

## Cuándo NO abstraer

- **Regla de tres**: duplicar dos veces está bien. A la tercera aparece el patrón real.
  Abstraer con un solo caso de uso produce la abstracción equivocada.
- **Duplicación incidental vs real**: dos bloques que hoy se ven iguales pero cambian por
  motivos distintos no son duplicación. Unirlos los va a llenar de flags después.
- Si el componente compartido ya tiene tres props que sirven para prender y apagar partes,
  probablemente había que dejarlos separados.

---

## Señales

- Más de 8 props en un componente de presentación.
- Props que se llaman `showX` / `hideY` / `withZ`.
- Un `renderXxx` por cada zona del componente: eso ya era `children`.
- Un componente que sabe de dónde vienen sus datos *y* cómo se ven.
- `'use client'` en el layout raíz.
