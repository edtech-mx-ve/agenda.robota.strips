"use strict";

const form = document.querySelector("#plan-form");
const startSelect = document.querySelector("#start-zone");
const goalSelect = document.querySelector("#goal-zone");
const planButton = document.querySelector("#plan-button");
const playButton = document.querySelector("#play-button");
const pauseButton = document.querySelector("#pause-button");
const nextButton = document.querySelector("#next-button");
const resetButton = document.querySelector("#reset-button");

const statusBox = document.querySelector("#status");
const resultEmpty = document.querySelector("#result-empty");
const resultContent = document.querySelector("#result-content");
const resultMessage = document.querySelector("#result-message");
const planList = document.querySelector("#plan-list");
const metricMoves = document.querySelector("#metric-moves");
const metricExpanded = document.querySelector("#metric-expanded");
const goalState = document.querySelector("#goal-state");
const simulationBadge = document.querySelector("#simulation-badge");
const stepCounter = document.querySelector("#step-counter");
const gridMap = document.querySelector("#grid-map");

const traceEmpty = document.querySelector("#trace-empty");
const traceContent = document.querySelector("#trace-content");
const traceAction = document.querySelector("#trace-action");
const tracePre = document.querySelector("#trace-pre");
const traceAdd = document.querySelector("#trace-add");
const traceDel = document.querySelector("#trace-del");
const stateBefore = document.querySelector("#state-before");
const stateAfter = document.querySelector("#state-after");

let scenario = null;
let currentPlan = null;
let currentStep = 0;
let playbackTimer = null;

const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)",
).matches;

function setStatus(message, type = "") {
  statusBox.textContent = message;
  statusBox.className = `status ${type}`.trim();
}

function setPlanningBusy(isBusy) {
  planButton.disabled = isBusy;
  planButton.textContent = isBusy ? "Planificando…" : "Generar plan STRIPS";
}

function setSimulationControls(enabled) {
  const hasPlayablePlan = enabled && currentPlan && currentPlan.steps.length > 0;

  playButton.disabled = !hasPlayablePlan;
  nextButton.disabled = !hasPlayablePlan;
  resetButton.disabled = !enabled;
  pauseButton.disabled = true;
}

function populateSelect(select, zones, selected) {
  select.replaceChildren();

  for (const zone of zones) {
    const option = document.createElement("option");
    option.value = zone;
    option.textContent = `Celda ${zone}`;
    option.selected = zone === selected;
    select.append(option);
  }
}

function buildGrid(data) {
  gridMap.replaceChildren();

  for (const row of data.rows) {
    for (const col of data.cols) {
      const zone = `${row}${col}`;
      const cell = document.createElement("div");
      cell.className = "grid-cell";
      cell.dataset.zone = zone;
      cell.setAttribute("role", "gridcell");
      cell.setAttribute("aria-label", `Celda ${zone}`);
      cell.textContent = zone;
      gridMap.append(cell);
    }
  }
}

function zoneNodes() {
  return [...gridMap.querySelectorAll("[data-zone]")];
}

function findZone(zone) {
  return zoneNodes().find((node) => node.dataset.zone === zone);
}

function resetMapClasses() {
  for (const node of zoneNodes()) {
    node.classList.remove("start", "goal", "route", "robot");
    const marker = node.querySelector(".robot-marker");
    if (marker) {
      marker.remove();
    }
  }
}

function markZone(zone, className) {
  const node = findZone(zone);
  if (node) {
    node.classList.add(className);
  }
}

function placeRobot(zone) {
  for (const node of zoneNodes()) {
    node.classList.remove("robot");
    const existing = node.querySelector(".robot-marker");
    if (existing) {
      existing.remove();
    }
  }

  const node = findZone(zone);
  if (!node) {
    return;
  }

  node.classList.add("robot");

  const marker = document.createElement("span");
  marker.className = "robot-marker";
  marker.textContent = "R";
  marker.setAttribute("aria-label", `Robot en ${zone}`);
  node.append(marker);
}

function updateSelectionMap() {
  stopPlayback();
  resetMapClasses();
  markZone(startSelect.value, "start");
  markZone(goalSelect.value, "goal");
  placeRobot(startSelect.value);
}

function markRoute(data) {
  for (const step of data.steps) {
    markZone(step.origin, "route");
    markZone(step.destination, "route");
  }
}

function clearCurrentPlanHighlight() {
  for (const item of planList.querySelectorAll("li")) {
    item.classList.remove("current-step");
  }
}

function highlightPlanStep(index) {
  clearCurrentPlanHighlight();

  const item = planList.querySelector(`[data-step-index="${index}"]`);
  if (item) {
    item.classList.add("current-step");
  }
}

function fillList(element, values) {
  element.replaceChildren();

  for (const value of values) {
    const item = document.createElement("li");
    const code = document.createElement("code");
    code.textContent = value;
    item.append(code);
    element.append(item);
  }
}

function clearTrace() {
  traceEmpty.hidden = false;
  traceContent.hidden = true;
  traceAction.textContent = "—";
  tracePre.replaceChildren();
  traceAdd.replaceChildren();
  traceDel.replaceChildren();
  stateBefore.textContent = "—";
  stateAfter.textContent = "—";
}

function renderTrace(step) {
  traceEmpty.hidden = true;
  traceContent.hidden = false;

  traceAction.textContent = step.action;
  fillList(tracePre, step.preconditions);
  fillList(traceAdd, step.add_effects);
  fillList(traceDel, step.del_effects);
  stateBefore.textContent = step.state_before.join(", ");
  stateAfter.textContent = step.state_after.join(", ");
}


function preserveViewportDuringControl(action) {
  const scrollX = window.scrollX;
  const scrollY = window.scrollY;

  action();

  window.requestAnimationFrame(() => {
    window.scrollTo(scrollX, scrollY);
  });
}

function updateStepCounter() {
  const total = currentPlan ? currentPlan.steps.length : 0;
  stepCounter.textContent = `Paso ${currentStep} de ${total}`;
}

function renderPlan(data) {
  currentPlan = data;
  currentStep = 0;
  stopPlayback();

  resultEmpty.hidden = true;
  resultContent.hidden = false;
  resultMessage.textContent = data.message;
  metricMoves.textContent = String(data.plan.length);
  metricExpanded.textContent = String(data.expanded_states);
  planList.replaceChildren();

  goalState.textContent = data.goal_reached ? "Meta alcanzable" : "Sin solución";
  goalState.className = data.goal_reached ? "badge success" : "badge muted";

  resetMapClasses();
  markRoute(data);
  markZone(data.start, "start");
  markZone(data.goal, "goal");
  placeRobot(data.start);

  if (data.plan.length === 0) {
    const item = document.createElement("li");
    item.textContent = data.goal_reached
      ? "El robot ya se encuentra en la meta."
      : "No se encontró una secuencia de acciones.";
    planList.append(item);
  } else {
    for (const step of data.steps) {
      const item = document.createElement("li");
      item.dataset.stepIndex = String(step.index);
      item.textContent =
        `${step.index}. ${step.action} · ${step.origin} → ${step.destination}`;
      planList.append(item);
    }
  }

  clearTrace();
  updateStepCounter();

  if (data.goal_reached && data.steps.length > 0) {
    simulationBadge.textContent = "Listo para simular";
    simulationBadge.className = "badge";
    setSimulationControls(true);
  } else if (data.goal_reached) {
    simulationBadge.textContent = "Meta inicial";
    simulationBadge.className = "badge success";
    setSimulationControls(true);
  } else {
    simulationBadge.textContent = "Sin solución";
    simulationBadge.className = "badge muted";
    setSimulationControls(false);
  }
}

function advanceOneStep() {
  if (!currentPlan || currentPlan.steps.length === 0) {
    return;
  }

  if (currentStep >= currentPlan.steps.length) {
    stopPlayback();
    simulationBadge.textContent = "Simulación finalizada";
    simulationBadge.className = "badge success";
    return;
  }

  const step = currentPlan.steps[currentStep];

  currentStep += 1;

  placeRobot(step.destination);
  renderTrace(step);
  highlightPlanStep(step.index);
  updateStepCounter();

  simulationBadge.textContent = `Robot en ${step.destination}`;
  simulationBadge.className =
    currentStep === currentPlan.steps.length ? "badge success" : "badge";

  if (currentStep >= currentPlan.steps.length) {
    stopPlayback();
    playButton.disabled = true;
    nextButton.disabled = true;
    pauseButton.disabled = true;
    resetButton.disabled = false;
    setStatus("Simulación completada: meta alcanzada.", "success");
  }
}

function startPlayback() {
  if (!currentPlan || currentPlan.steps.length === 0) {
    return;
  }

  if (currentStep >= currentPlan.steps.length) {
    resetSimulation();
  }

  if (playbackTimer !== null) {
    return;
  }

  playButton.disabled = true;
  nextButton.disabled = true;
  pauseButton.disabled = false;
  resetButton.disabled = false;

  simulationBadge.textContent = "Reproduciendo";
  simulationBadge.className = "badge";

  advanceOneStep();

  if (currentStep >= currentPlan.steps.length) {
    return;
  }

  const intervalMs = prefersReducedMotion ? 1200 : 850;
  playbackTimer = window.setInterval(() => {
    advanceOneStep();
  }, intervalMs);
}

function stopPlayback() {
  if (playbackTimer !== null) {
    window.clearInterval(playbackTimer);
    playbackTimer = null;
  }

  if (currentPlan && currentPlan.steps.length > 0) {
    const finished = currentStep >= currentPlan.steps.length;
    playButton.disabled = finished;
    nextButton.disabled = finished;
    pauseButton.disabled = true;
    resetButton.disabled = false;
  }
}

function resetSimulation() {
  stopPlayback();

  if (!currentPlan) {
    updateSelectionMap();
    return;
  }

  currentStep = 0;
  resetMapClasses();
  markRoute(currentPlan);
  markZone(currentPlan.start, "start");
  markZone(currentPlan.goal, "goal");
  placeRobot(currentPlan.start);

  clearTrace();
  clearCurrentPlanHighlight();
  updateStepCounter();

  simulationBadge.textContent =
    currentPlan.steps.length > 0 ? "Listo para simular" : "Meta inicial";
  simulationBadge.className =
    currentPlan.steps.length > 0 ? "badge" : "badge success";

  playButton.disabled = currentPlan.steps.length === 0;
  nextButton.disabled = currentPlan.steps.length === 0;
  pauseButton.disabled = true;
  resetButton.disabled = false;

  setStatus("Simulación reiniciada.", "success");
}

async function loadScenario() {
  try {
    const response = await fetch("/api/scenario", {
      headers: { Accept: "application/json" },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    scenario = await response.json();

    buildGrid(scenario);
    populateSelect(
      startSelect,
      scenario.zones,
      scenario.default_start,
    );
    populateSelect(
      goalSelect,
      scenario.zones,
      scenario.default_goal,
    );

    currentPlan = null;
    setSimulationControls(false);
    updateSelectionMap();

    setStatus(
      `Escenario 4×4 cargado: ${scenario.zones.length} celdas disponibles.`,
      "success",
    );
  } catch (error) {
    console.error("No se pudo cargar el escenario:", error);
    setStatus(
      "No se pudo cargar el escenario. Verifica que la API esté activa.",
      "error",
    );
    planButton.disabled = true;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const start = startSelect.value;
  const goal = goalSelect.value;

  if (!start || !goal) {
    setStatus("Selecciona una celda inicial y una celda objetivo.", "error");
    return;
  }

  stopPlayback();
  setPlanningBusy(true);
  setStatus("Calculando plan…");

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ start, goal }),
    });

    const data = await response.json();

    if (!response.ok) {
      const message =
        typeof data.detail === "string"
          ? data.detail
          : "La API rechazó la solicitud.";
      throw new Error(message);
    }

    renderPlan(data);
    setStatus(
      data.steps.length > 0
        ? "Plan generado. Usa los controles para simularlo."
        : data.message,
      "success",
    );
  } catch (error) {
    console.error("Error de planificación:", error);
    setStatus(`Error: ${error.message}`, "error");
  } finally {
    setPlanningBusy(false);
  }
});

startSelect.addEventListener("change", () => {
  currentPlan = null;
  currentStep = 0;
  resultEmpty.hidden = false;
  resultContent.hidden = true;
  simulationBadge.textContent = "Sin plan";
  simulationBadge.className = "badge muted";
  setSimulationControls(false);
  clearTrace();
  updateStepCounter();
  updateSelectionMap();
});

goalSelect.addEventListener("change", () => {
  currentPlan = null;
  currentStep = 0;
  resultEmpty.hidden = false;
  resultContent.hidden = true;
  simulationBadge.textContent = "Sin plan";
  simulationBadge.className = "badge muted";
  setSimulationControls(false);
  clearTrace();
  updateStepCounter();
  updateSelectionMap();
});

playButton.addEventListener("click", () => preserveViewportDuringControl(startPlayback));
pauseButton.addEventListener("click", () => preserveViewportDuringControl(() => {
  stopPlayback();
  simulationBadge.textContent = `Pausado · paso ${currentStep}`;
  simulationBadge.className = "badge muted";
}));
nextButton.addEventListener("click", () => preserveViewportDuringControl(advanceOneStep));
resetButton.addEventListener("click", () => preserveViewportDuringControl(resetSimulation));

loadScenario();
