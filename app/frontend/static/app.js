// ---------- navegação entre abas ----------
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((s) => s.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    if (btn.dataset.tab === "dashboard") carregarDashboard();
    if (btn.dataset.tab === "historico") carregarHistorico();
    if (btn.dataset.tab === "config") carregarConfig();
  });
});

function formToJson(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  if (data.datahora) data.datahora = data.datahora + ":00";
  else delete data.datahora;
  return data;
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// ---------- formulários de registro ----------

document.getElementById("form-refeicao").addEventListener("submit", async (e) => {
  e.preventDefault();
  await postJson("/api/refeicoes", formToJson(e.target));
  e.target.reset();
  alert("Refeição registrada.");
});

document.getElementById("form-glicemia").addEventListener("submit", async (e) => {
  e.preventDefault();
  await postJson("/api/glicemias", formToJson(e.target));
  e.target.reset();
  alert("Glicemia registrada.");
});

document.getElementById("form-dose").addEventListener("submit", async (e) => {
  e.preventDefault();
  await postJson("/api/doses", formToJson(e.target));
  e.target.reset();
  alert("Dose registrada.");
});

document.getElementById("form-calc").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = formToJson(e.target);
  const res = await postJson("/api/calcular_dose", body);
  document.getElementById("calc-resultado").textContent =
    `Bolus refeição: ${res.bolus_refeicao_ui} UI\n` +
    `Correção: ${res.correcao_ui} UI\n` +
    `Total sugerido: ${res.total_ui} UI\n\n${res.detalhes}`;
});

// ---------- dashboard ----------

let chartTIR, chartCurva, chartPadrao;

async function carregarDashboard() {
  const hoje = new Date().toISOString().slice(0, 10);
  document.getElementById("curva-data").value = hoje;
  document.getElementById("resumo-data").value = hoje;

  const tir = await (await fetch("/api/relatorios/tempo_no_alvo")).json();
  document.getElementById("tir-resumo").textContent =
    tir.total_leituras === 0
      ? "Sem leituras no período."
      : `Leituras: ${tir.total_leituras} | Média: ${tir.media} mg/dL | DP: ${tir.desvio_padrao}`;

  if (chartTIR) chartTIR.destroy();
  chartTIR = new Chart(document.getElementById("chart-tir"), {
    type: "doughnut",
    data: {
      labels: ["Abaixo do alvo", "No alvo", "Acima do alvo"],
      datasets: [{
        data: [tir.abaixo_pct, tir.no_alvo_pct, tir.acima_pct],
        backgroundColor: ["#dc2626", "#16a34a", "#f59e0b"],
      }],
    },
  });

  await carregarCurva(hoje);
  await carregarPadrao();
  await carregarResumo(hoje);

  document.getElementById("curva-data").onchange = (e) => carregarCurva(e.target.value);
  document.getElementById("resumo-data").onchange = (e) => carregarResumo(e.target.value);
}

async function carregarCurva(dataStr) {
  const pontos = await (await fetch(`/api/relatorios/curva/${dataStr}`)).json();
  if (chartCurva) chartCurva.destroy();
  chartCurva = new Chart(document.getElementById("chart-curva"), {
    type: "line",
    data: {
      labels: pontos.map((p) => p.datahora.slice(11, 16)),
      datasets: [{
        label: "Glicemia (mg/dL)",
        data: pontos.map((p) => p.valor_mgdl),
        borderColor: "#2563eb",
        tension: 0.3,
      }],
    },
    options: { scales: { y: { min: 40, max: 300 } } },
  });
}

async function carregarPadrao() {
  const padrao = await (await fetch("/api/relatorios/padrao_diario")).json();
  if (chartPadrao) chartPadrao.destroy();
  chartPadrao = new Chart(document.getElementById("chart-padrao"), {
    type: "bar",
    data: {
      labels: padrao.map((p) => `${p.hora}h`),
      datasets: [
        { label: "Média", data: padrao.map((p) => p.media), backgroundColor: "#2563eb" },
        { label: "Máx", data: padrao.map((p) => p.max), backgroundColor: "#f59e0b" },
        { label: "Mín", data: padrao.map((p) => p.min), backgroundColor: "#16a34a" },
      ],
    },
  });
}

async function carregarResumo(dataStr) {
  const r = await (await fetch(`/api/relatorios/resumo_diario/${dataStr}`)).json();
  const insulina = Object.entries(r.insulina_por_tipo)
    .map(([tipo, ui]) => `${tipo}: ${ui} UI`)
    .join(", ") || "—";
  document.getElementById("resumo-resultado").textContent =
    `Carboidratos: ${r.carboidratos_totais_g} g\n` +
    `Insulina total: ${r.insulina_total_ui} UI (${insulina})\n` +
    `Glicemia média: ${r.glicemia_media ?? "—"} mg/dL (min ${r.glicemia_min ?? "—"} / max ${r.glicemia_max ?? "—"})\n` +
    `Leituras no dia: ${r.n_leituras}`;
}

// ---------- histórico ----------

async function carregarHistorico() {
  const refeicoes = await (await fetch("/api/refeicoes")).json();
  const tbodyR = document.querySelector("#tabela-refeicoes tbody");
  tbodyR.innerHTML = refeicoes
    .map((r) => `<tr><td>${r.datahora}</td><td>${r.descricao}</td><td>${r.carboidratos_g}</td><td>${r.origem}</td></tr>`)
    .join("");

  const glicemias = await (await fetch("/api/glicemias")).json();
  const tbodyG = document.querySelector("#tabela-glicemias tbody");
  tbodyG.innerHTML = glicemias
    .map((g) => `<tr><td>${g.datahora}</td><td>${g.valor_mgdl}</td><td>${g.contexto}</td></tr>`)
    .join("");

  const doses = await (await fetch("/api/doses")).json();
  const tbodyD = document.querySelector("#tabela-doses tbody");
  tbodyD.innerHTML = doses
    .map((d) => `<tr><td>${d.datahora}</td><td>${d.tipo}</td><td>${d.insulina}</td><td>${d.unidades}</td></tr>`)
    .join("");
}

// ---------- configuração ----------

const LABELS_CONFIG = {
  basal_dose_ui: "Dose basal (Glargina, UI)",
  razao_ic_g_por_ui: "Razão I:C (g de carbo por 1 UI)",
  fator_sensibilidade_mgdl_por_ui: "Fator de sensibilidade (mg/dL por 1 UI)",
  meta_glicemia_mgdl: "Meta de glicemia (mg/dL)",
  faixa_alvo_min_mgdl: "Faixa alvo — mínimo (mg/dL)",
  faixa_alvo_max_mgdl: "Faixa alvo — máximo (mg/dL)",
  correcao_inicio_mgdl: "Glicemia a partir da qual corrige (mg/dL)",
  correcao_reducao_abaixo_mgdl: "Glicemia abaixo da qual reduz bolus (mg/dL)",
};

async function carregarConfig() {
  const cfg = await (await fetch("/api/config")).json();
  const form = document.getElementById("form-config");
  form.innerHTML = "";
  for (const [chave, rotulo] of Object.entries(LABELS_CONFIG)) {
    if (!(chave in cfg)) continue;
    const label = document.createElement("label");
    label.innerHTML = `${rotulo}<input type="number" step="0.1" name="${chave}" value="${cfg[chave]}">`;
    form.appendChild(label);
  }
  const btn = document.createElement("button");
  btn.textContent = "Salvar configurações";
  btn.type = "submit";
  form.appendChild(btn);

  form.onsubmit = async (e) => {
    e.preventDefault();
    await postJson("/api/config", formToJson(form));
    alert("Configurações atualizadas.");
  };
}
