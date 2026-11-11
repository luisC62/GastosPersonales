// ============================================================
// Control de gastos — código de la web
// Habla con el servidor API (main.py), que guarda los gastos
// en la base de datos misgastos.db.
// ============================================================

// Dirección donde escucha el servidor API. Hay que arrancarlo
// antes de abrir la página: uv run uvicorn main:app --reload
const URL_API = "http://127.0.0.1:8000";

// Elementos de la página que usa el código.
const formulario = document.querySelector("#formulario");
const campoFecha = document.querySelector("#fecha");
const campoCantidad = document.querySelector("#cantidad");
const campoTipo = document.querySelector("#tipo");
const campoDescripcion = document.querySelector("#descripcion");
const botonBorrar = document.querySelector("#boton-borrar");
const listaGastos = document.querySelector("#lista-gastos");
const aviso = document.querySelector("#aviso");
const sinGastos = document.querySelector("#sin-gastos");
const totalSemanal = document.querySelector("#total-semanal");
const rangoSemanal = document.querySelector("#rango-semanal");
const totalMensual = document.querySelector("#total-mensual");
const rangoMensual = document.querySelector("#rango-mensual");

// Gasto marcado en la lista (null si no hay ninguno marcado).
let gastoSeleccionado = null;

// Da formato de euros a un número: 12.5 -> "12,50 €".
const formatoEuros = new Intl.NumberFormat("es-ES", {
  style: "currency",
  currency: "EUR",
});

// Devuelve la fecha de hoy como "AAAA-MM-DD" usando la hora
// local del usuario (no toISOString, que trabaja con UTC).
function hoyLocal() {
  const hoy = new Date();
  const mes = String(hoy.getMonth() + 1).padStart(2, "0"); // getMonth() empieza en 0
  const dia = String(hoy.getDate()).padStart(2, "0");
  return `${hoy.getFullYear()}-${mes}-${dia}`;
}

// Convierte "2026-11-09" en "9 nov 2026".
function formatearFecha(fechaISO) {
  // Se añade "T00:00" para que el navegador lea la fecha con la
  // zona horaria local y no cambie el día.
  const fecha = new Date(fechaISO + "T00:00");
  return fecha.toLocaleDateString("es-ES", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

// Muestra u oculta el mensaje de error que hay sobre el formulario.
function mostrarAviso(mensaje) {
  aviso.textContent = mensaje;
  aviso.classList.remove("oculto");
}

function ocultarAviso() {
  aviso.classList.add("oculto");
}

// Hace una petición al servidor API y devuelve su respuesta JSON.
// Si algo falla, lanza un error con un mensaje claro en español.
async function llamarAPI(ruta, opciones) {
  let respuesta;
  try {
    respuesta = await fetch(URL_API + ruta, opciones);
  } catch {
    // fetch falla así cuando el servidor no está arrancado.
    throw new Error(
      "No se ha podido conectar con el servidor. Arranca antes la API con el comando «uv run uvicorn main:app» y recarga la página."
    );
  }

  if (!respuesta.ok) {
    // El servidor ha contestado con un error.
    let mensaje = `El servidor ha respondido con un error (código ${respuesta.status}).`;
    try {
      const cuerpo = await respuesta.json();
      if (typeof cuerpo.detail === "string") {
        mensaje = cuerpo.detail;
      }
    } catch {
      // La respuesta no traía JSON: nos quedamos con el mensaje genérico.
    }
    throw new Error(mensaje);
  }

  return respuesta.json();
}

// Pinta la lista de gastos (el servidor ya los envía del más
// reciente al más antiguo).
function pintarGastos(gastos) {
  listaGastos.replaceChildren(); // vacía la lista
  gastoSeleccionado = null;
  actualizarBotonBorrar();
  sinGastos.classList.toggle("oculto", gastos.length > 0);

  for (const gasto of gastos) {
    listaGastos.append(crearGastoEnPantalla(gasto));
  }
}

// Crea el elemento de la lista para un gasto.
function crearGastoEnPantalla(gasto) {
  const elemento = document.createElement("button");
  elemento.type = "button";
  elemento.className = "gasto";
  elemento.dataset.id = gasto.id;
  elemento.setAttribute("aria-pressed", "false");
  elemento.addEventListener("click", () => alternarSeleccion(gasto, elemento));

  const texto = document.createElement("span");
  texto.className = "gasto-texto";

  const descripcion = document.createElement("span");
  descripcion.className = "gasto-descripcion";
  descripcion.textContent = gasto.descripcion;

  const meta = document.createElement("span");
  meta.className = "gasto-meta";

  const fecha = document.createElement("span");
  fecha.className = "gasto-fecha";
  fecha.textContent = formatearFecha(gasto.fecha);

  const tipo = document.createElement("span");
  tipo.className = "gasto-tipo";
  tipo.textContent = gasto.tipo;

  meta.append(fecha, tipo);
  texto.append(descripcion, meta);

  const cantidad = document.createElement("span");
  cantidad.className = "gasto-cantidad";
  cantidad.textContent = formatoEuros.format(gasto.cantidad);

  elemento.append(texto, cantidad);
  return elemento;
}

// Marca un gasto de la lista para poder borrarlo (o lo desmarca
// si ya estaba marcado).
function alternarSeleccion(gasto, elemento) {
  const anterior = listaGastos.querySelector(".seleccionado");
  if (anterior) {
    anterior.classList.remove("seleccionado");
    anterior.setAttribute("aria-pressed", "false");
  }

  if (elemento === anterior) {
    gastoSeleccionado = null;
  } else {
    elemento.classList.add("seleccionado");
    elemento.setAttribute("aria-pressed", "true");
    gastoSeleccionado = gasto;
  }

  actualizarBotonBorrar();
}

// El botón de borrar solo funciona cuando hay un gasto marcado.
function actualizarBotonBorrar() {
  botonBorrar.disabled = gastoSeleccionado === null;
}

// Descarga la lista de gastos del servidor y la pinta.
async function cargarGastos() {
  try {
    const gastos = await llamarAPI("/gastos");
    ocultarAviso();
    pintarGastos(gastos);
  } catch (error) {
    pintarGastos([]);
    mostrarAviso(error.message);
  }
}

// Descarga los totales de la semana y del mes en curso y los pinta.
async function cargarTotales() {
  try {
    const semana = await llamarAPI("/gastos/total-semanal");
    const mes = await llamarAPI("/gastos/total-mensual");

    totalSemanal.textContent = formatoEuros.format(semana.total);
    rangoSemanal.textContent = `${formatearFecha(semana.inicio)} – ${formatearFecha(semana.fin)}`;
    totalMensual.textContent = formatoEuros.format(mes.total);
    rangoMensual.textContent = `${formatearFecha(mes.inicio)} – ${formatearFecha(mes.fin)}`;
  } catch (error) {
    mostrarAviso(error.message);
  }
}

// Envío del formulario: guarda el gasto nuevo en el servidor.
formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault(); // evita que la página se recargue

  const gasto = {
    fecha: campoFecha.value,
    cantidad: Number(campoCantidad.value),
    tipo: campoTipo.value.trim(),
    descripcion: campoDescripcion.value.trim(),
  };

  try {
    const nuevo = await llamarAPI("/gastos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(gasto),
    });

    ocultarAviso();
    await cargarGastos();
    await cargarTotales();

    // Resalta el gasto recién creado para ver dónde ha entrado
    // en la lista (que va por fecha).
    const elemento = listaGastos.querySelector(`[data-id="${nuevo.id}"]`);
    if (elemento) {
      elemento.classList.add("nuevo");
      elemento.scrollIntoView({ block: "nearest" });
    }

    // Deja el formulario listo para el siguiente gasto.
    formulario.reset();
    campoFecha.value = hoyLocal();
    campoTipo.focus();
  } catch (error) {
    mostrarAviso(error.message);
  }
});

// Borra el gasto que esté marcado en la lista.
botonBorrar.addEventListener("click", async () => {
  if (!gastoSeleccionado) {
    return;
  }

  const seguro = window.confirm(
    `¿Eliminar el gasto «${gastoSeleccionado.descripcion}»?`
  );
  if (!seguro) {
    return;
  }

  try {
    await llamarAPI(`/gastos/${gastoSeleccionado.id}`, { method: "DELETE" });
    await cargarGastos();
    await cargarTotales();
  } catch (error) {
    mostrarAviso(error.message);
  }
});

// Al abrir la página: la fecha por defecto es hoy y se cargan
// la lista de gastos y los totales.
campoFecha.value = hoyLocal();
cargarGastos();
cargarTotales();
