# ICONS Engine

Herramienta web para crear, editar y jugar personajes de **ICONS** (*Assembled Edition*), usando los poderes del suplemento **Great Power**. Es una sola página HTML: no necesita servidor, ni instalar nada, ni conexión a internet.

Con ella podés:

- generar un héroe al azar con un clic, o crearlo paso a paso con dados físicos;
- editar la ficha completa y guardarla como `.json`;
- jugar en una mesa con varias fichas a la vez: tiradas, Determination, daño, condiciones con duración, iniciativa y ataques automáticos.

---

## Instalación

1. **Cloná el repositorio** (o bajalo como ZIP desde GitHub: *Code → Download ZIP*):

   ```bash
   git clone https://github.com/satepin/CLU-ICONS-Engine.git
   cd CLU-ICONS-Engine
   ```

2. **Abrí `index.html` en Chrome o Edge.** Doble clic alcanza. Si armaste la versión local con las descripciones, abrí `index.local.html`.

   > Para guardar las fichas en una carpeta se usa una función que hoy sólo tienen los navegadores basados en Chromium (Chrome, Edge, Brave, Opera). En Firefox o Safari la app funciona, pero las fichas quedan sólo en el navegador. En ese caso, usá **JSON** para exportarlas e importarlas.

3. **Elegí la carpeta de fichas.** En el panel *Héroes guardados*, tocá **📁 Elegir carpeta de fichas** y seleccioná la carpeta `heroes` del repositorio. El navegador pide permiso una vez; la app recuerda la carpeta para la próxima.

### Las carpetas de fichas

```
heroes/
├── global/   ← fichas compartidas: se suben al repositorio
└── local/    ← fichas privadas: git las ignora (sólo quedan en tu máquina)
```

- Las fichas **nuevas** se guardan en `heroes/local/`, así nada se sube por accidente.
- Para compartir una ficha, **arrastrala** en la lista de *Héroes guardados* hasta la carpeta `global`, o a una subcarpeta suya, por ejemplo `global/Jugadores`.
- Podés crear subcarpetas desde la app. Se muestran como grupos que se pueden colapsar.

---

## Uso rápido

### Crear un personaje

| Botón | Qué hace |
|---|---|
| **🎲 Generar héroe** | Tira todo al azar según las reglas del panel *Reglas*. |
| **🧭 Paso a paso** | Asistente a pantalla completa. Te muestra cada dado, qué significa cada resultado, y te deja elegir o tirar. Admite dados físicos y ↶ deshacer (Ctrl+Z). |

En el panel **Reglas** se configuran estas opciones:

- **Reglas balanceadas (FASERIP):**
  - abilities en pares verde y rojo, con 8 d6 o 8 d100 con tabla;
  - 8 puntos para poderes;
  - los poderes empiezan en 3;
  - una tienda donde se tira en la tabla d100, se suben poderes, se suman extras o limits, y se puede sacrificar un poder.
- **Límite de creación:** máximo para abilities, poderes y specialties. Por defecto, 7 / 7 / +3.
- **⏸ Decidir al final:** en el paso a paso, las decisiones que tocan estadísticas (qué par descartar, bonos de origen…) se pueden dejar para el final.

Todo se puede editar después en la ficha: abilities, poderes con sus extras y limits, specialties, qualities, equipo, vehículos y notas.

### Logros y mejoras

En la sección **🏆 Logros** de la ficha se registran los logros que va ganando el héroe: menores, moderados y mayores, con el evento que los otorgó y la fecha. Tiene tres pestañas:
- **Logros:** todos los logros y su estado (disponible, gastado o convertido).
- **Por evento:** cuántos logros de cada tipo dio cada evento.
- **Mejoras aplicadas:** el historial de mejoras, las proezas dominadas y los aportes al escenario.

**🛒 Gastar logros** abre una tienda paso a paso, como la de creación, con las mejoras de la Edición Recopilada:
- se elige qué logro gastar y qué mejora aplicar;
- convierte 4 menores en 1 moderado y 2 moderados en 1 mayor;
- ajusta la Determination (puede bajar hasta 0);
- se puede deshacer (Ctrl+Z) o cancelar sin tocar la ficha.

### Guardar y compartir

- **💾 Guardar** escribe `nombre-del-heroe.json` en la carpeta elegida. Si renombrás al personaje, el archivo se renombra solo.
- **📋 Ficha en texto** copia la ficha en texto plano. **⇄ JSON** exporta o importa una ficha suelta.
- Para compartir con el grupo: mové la ficha a `heroes/global/` y subila con git (ver más abajo).

### Fichas vinculadas

Los poderes **Alter Ego**, **Servant**, **Gestalt** y los **vehículos** crean fichas propias, vinculadas entre sí con botones de acceso directo:

- en la mesa, un botón cambia entre las formas de un Alter Ego;
- otro junta los componentes en la forma Gestalt o los separa;
- los grupos de servants genéricos se manejan desde una sola ficha.
- en un servant, los extras de un mismo poder cuestan 1, 2, 3… puntos del pool (regla de la mesa, como la tienda de las reglas balanceadas).

### Jugar

**🎭 Modo jugar** abre la ficha en formato compacto:

- tocá una ability o un poder y luego **Tirar**;
- elegí el modo de la tirada: contra oposición, contra dificultad fija, o **sólo dado + modificador**;
- Determination Points normales y temporales, esfuerzo determinado, qualities;
- Stamina, daño con Resistance, condiciones con duración en páginas;
- **Wizardry, Magic, Gadgets y las Mimicry** pueden volverse otro poder un rato. Sin *Instant* ni *Mastery*, el cambio tarda una página. En el modo edición se guardan **copias**: qué poder, con qué extras y limits, y si queda copiada **a largo plazo**, en cuyo caso arranca activa. Regla de la mesa: una copia no cambia el costo de Determination, así que **cada extra se compensa con un limit**; una copia descompensada no se puede usar. Una copia de Servant, Alter Ego o Gestalt puede crear su ficha vinculada, y el vínculo queda aunque se deje de copiar.
- Un **ítem misceláneo** puede **conferir un poder** mientras está equipado. Se equipa o se quita desde el modo jugar o desde la mesa.

Arriba se elige el **dado de juego** (d8 por defecto, o d6) y si usás **dados físicos**: en ese caso la app te pide cada resultado.

### La mesa

La pestaña **🗂 Mesa** muestra todas las fichas abiertas como tarjetas. Se pueden ampliar, minimizar y reordenar arrastrándolas.

- **Tirada grupal:** la misma tirada para las fichas seleccionadas (o todas). Incluye abilities, poderes, rasgos de vehículos e iniciativa.
- **Acciones:** daño, curación, PD, condiciones y **Siguiente página ▶**, que descuenta las duraciones en toda la mesa.
- **⏱ Iniciativa:**
  - Tira Coordination o Super-Speed, el más alto; los vehículos tiran Speed.
  - Si hay fichas seleccionadas, sólo entran ellas. Para sumar a alguien después, usá ➕, el desplegable, o arrastrá su tarjeta a la lista.
  - La lista se reordena arrastrando. La tarjeta de quien le toca se resalta. Al terminar la ronda, la página avanza sola.
- **⚔ Ataque automático:**
  - Elegí al atacante con el ⚔ de su tarjeta y seleccioná los blancos.
  - La app tira la reacción de cada blanco (esquivar, bloquear…) y aplica la tabla de resultados: daño, derribo, aturdimiento, condiciones y anulación de poderes.
  - Admite esfuerzos combinados y tiene ↶ deshacer.

---

## Subir fichas al repositorio

```bash
git pull                      # traé lo último del grupo
git add heroes/global
git commit -m "Fichas: agrego a Imparable"
git push
```

Lo que está en `heroes/local/` nunca se sube.

---

## Para desarrollar

El código fuente está en `src/`:

- `src/template.html` — la app: HTML, CSS y JavaScript en un solo archivo, con el marcador `/*DATA*/`.
- `src/powers_data.js` — la lista de poderes de Great Power: nombres, tipos, páginas y nombres de extras y limits. **No incluye el texto del libro**: la app muestra “ver Great Power, p. X”.
- `build.py` — arma `index.html` reemplazando el marcador por los datos.

### Versión local con las descripciones completas

Si tenés el libro, podés guardar una versión de los datos con las descripciones en `fuentes/powers_data_full.js`, con el mismo formato que `src/powers_data.js`. Al correr `build.py` se arma además **`index.local.html`**, con el texto completo en la referencia y en el paso a paso. Tanto `fuentes/` como `index.local.html` están en `.gitignore`: nunca se suben.

Después de editar algo en `src/`:

```bash
python3 build.py
```

y recargá `index.html` en el navegador.

---

## Aviso

ICONS es un juego de Ad Infinitum Adventures (Steve Kenson). Este proyecto es una herramienta de fans, sin fines de lucro, y no incluye los manuales: para jugar necesitás tus propios libros. La carpeta `fuentes/` y cualquier `.pdf` están excluidos del repositorio.
