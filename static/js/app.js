const API = "";
let token         = localStorage.getItem("token") || "";
let selected      = {};       // { ingredient_id: { ingredient_id, weight_g, name } }
let allIngredients = [];      // полный список с сервера (для рецептов)
let editingDishId = null;     // id блюда в режиме редактирования

// ─────────────────────────────────────────────────
//  РЕЦЕПТЫ (определены по именам ингредиентов)
// ─────────────────────────────────────────────────
const RECIPES = [
  {
    emoji: "🍝",
    name: "Карбонара",
    desc: "Классическая итальянская паста с яйцом и сыром",
    tags: ["Паста", "Итальянская", "Быстро"],
    servings: 2,
    ingredients: [
      { name: "Макароны",            weight_g: 200 },
      { name: "Яйцо куриное",        weight_g: 120 },
      { name: "Сыр твёрдый",         weight_g: 60  },
      { name: "Масло сливочное",     weight_g: 20  },
      { name: "Чеснок",              weight_g: 10  },
      { name: "Перец чёрный молотый",weight_g: 3   },
    ],
  },
  {
    emoji: "🥗",
    name: "Греческий салат",
    desc: "Свежие овощи, сыр и оливковое масло",
    tags: ["Салат", "ЗОЖ", "Без готовки"],
    servings: 2,
    ingredients: [
      { name: "Томаты",              weight_g: 200 },
      { name: "Огурцы",              weight_g: 150 },
      { name: "Перец болгарский",    weight_g: 100 },
      { name: "Сыр твёрдый",         weight_g: 80  },
      { name: "Масло растительное",  weight_g: 30  },
      { name: "Лимон",               weight_g: 20  },
    ],
  },
  {
    emoji: "🍲",
    name: "Куриный суп",
    desc: "Лёгкий суп на курином бульоне с овощами",
    tags: ["Суп", "ЗОЖ", "Высокий белок"],
    servings: 4,
    ingredients: [
      { name: "Куриное филе",        weight_g: 400 },
      { name: "Картофель",           weight_g: 300 },
      { name: "Морковь",             weight_g: 100 },
      { name: "Лук репчатый",        weight_g: 80  },
      { name: "Соль",                weight_g: 5   },
    ],
  },
  {
    emoji: "🍳",
    name: "Омлет классический",
    desc: "Нежный яичный омлет — идеальный завтрак",
    tags: ["Завтрак", "Быстро", "Высокий белок"],
    servings: 1,
    ingredients: [
      { name: "Яйцо куриное",        weight_g: 180 },
      { name: "Молоко 3.2%",         weight_g: 60  },
      { name: "Масло сливочное",     weight_g: 15  },
    ],
  },
  {
    emoji: "🐟",
    name: "Лосось с овощами",
    desc: "Запечённый лосось с кабачком и томатами",
    tags: ["Рыба", "ЗОЖ", "Омега-3"],
    servings: 2,
    ingredients: [
      { name: "Лосось",              weight_g: 300 },
      { name: "Кабачок",             weight_g: 200 },
      { name: "Томаты",              weight_g: 150 },
      { name: "Масло растительное",  weight_g: 20  },
      { name: "Лимон",               weight_g: 30  },
      { name: "Чеснок",              weight_g: 8   },
    ],
  },
  {
    emoji: "🥣",
    name: "Овсянка с бананом",
    desc: "Сытная каша с натуральной сладостью банана",
    tags: ["Завтрак", "ЗОЖ", "Углеводы"],
    servings: 1,
    ingredients: [
      { name: "Овсянка",             weight_g: 80  },
      { name: "Молоко 3.2%",         weight_g: 200 },
      { name: "Банан",               weight_g: 120 },
      { name: "Мёд",                 weight_g: 15  },
    ],
  },
  {
    emoji: "🍄",
    name: "Гречка с грибами",
    desc: "Ароматная гречка с жареными шампиньонами",
    tags: ["Гарнир", "ЗОЖ", "Вегетарианское"],
    servings: 2,
    ingredients: [
      { name: "Гречка",              weight_g: 150 },
      { name: "Шампиньоны",          weight_g: 250 },
      { name: "Лук репчатый",        weight_g: 80  },
      { name: "Масло растительное",  weight_g: 20  },
      { name: "Соль",                weight_g: 4   },
    ],
  },
  {
    emoji: "🥩",
    name: "Говяжий стейк",
    desc: "Сочная говядина с чесночным маслом",
    tags: ["Мясо", "Высокий белок", "Кето"],
    servings: 1,
    ingredients: [
      { name: "Говядина (вырезка)",  weight_g: 250 },
      { name: "Масло сливочное",     weight_g: 20  },
      { name: "Чеснок",              weight_g: 10  },
      { name: "Перец чёрный молотый",weight_g: 2   },
    ],
  },
  {
    emoji: "🧆",
    name: "Творожная запеканка",
    desc: "Нежная запеканка — отличный источник белка",
    tags: ["Завтрак", "Высокий белок", "Десерт"],
    servings: 4,
    ingredients: [
      { name: "Творог 5%",           weight_g: 500 },
      { name: "Яйцо куриное",        weight_g: 120 },
      { name: "Сметана 20%",         weight_g: 100 },
      { name: "Мука пшеничная в/с",  weight_g: 60  },
      { name: "Сахар",               weight_g: 50  },
    ],
  },
];

// ─────────────────────────────────────────────────
//  AUTH
// ─────────────────────────────────────────────────

function authHeaders() {
  return { "Content-Type": "application/json", "Authorization": `Bearer ${token}` };
}

async function register() {
  const email    = document.getElementById("reg-email").value.trim();
  const username = document.getElementById("reg-username").value.trim();
  const password = document.getElementById("reg-password").value;
  if (!email || !username || !password) { toast("Заполните все поля", "warn"); return; }

  const res  = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password }),
  });
  const data = await res.json();
  if (res.ok) { toast("Аккаунт создан! Войдите.", "ok"); showSection("login"); }
  else        { toast(data.detail || "Ошибка регистрации", "err"); }
}

async function login() {
  const email    = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;
  const form     = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const res  = await fetch(`${API}/auth/login`, { method: "POST", body: form });
  const data = await res.json();
  if (res.ok) {
    token = data.access_token;
    localStorage.setItem("token", token);
    setAuthUI(true);
    showSection("constructor");
    loadIngredients();
  } else {
    toast(data.detail || "Неверный email или пароль", "err");
  }
}

function logout() {
  token = ""; localStorage.removeItem("token");
  selected = {}; editingDishId = null; allIngredients = [];
  setAuthUI(false);
  showSection("login");
}

function setAuthUI(loggedIn) {
  document.querySelectorAll(".auth-only").forEach(el => {
    el.classList.toggle("d-none", !loggedIn);
  });
  document.querySelectorAll(".guest-only").forEach(el => {
    el.classList.toggle("d-none", loggedIn);
  });
}

// ─────────────────────────────────────────────────
//  NAVIGATION
// ─────────────────────────────────────────────────

function showSection(id) {
  document.querySelectorAll(".section").forEach(s => s.classList.add("d-none"));
  document.getElementById("section-" + id).classList.remove("d-none");
  document.querySelectorAll(".nav-pill").forEach(b => b.classList.remove("active"));
  const btn = document.getElementById("nav-" + id);
  if (btn) btn.classList.add("active");
  if (id === "recipes") renderRecipes();
}

// ─────────────────────────────────────────────────
//  COOKING METHODS & MEDIUMS
// ─────────────────────────────────────────────────

let cookingMethods = [];
let cookingMediums = [];

async function loadCookingOptions() {
  const [mRes, eRes] = await Promise.all([
    fetch(`${API}/cooking/methods`),
    fetch(`${API}/cooking/mediums`),
  ]);
  cookingMethods = await mRes.json();
  cookingMediums = await eRes.json();

  const mSel = document.getElementById("cooking-method");
  if (!mSel) return;
  mSel.innerHTML = '<option value="">— без обработки —</option>' +
    cookingMethods.map(m => `<option value="${m.id}">${m.icon} ${m.name}</option>`).join("");

  const eSel = document.getElementById("cooking-medium");
  if (!eSel) return;
  eSel.innerHTML = '<option value="">— среда —</option>' +
    cookingMediums.map(e => `<option value="${e.id}">${e.icon} ${e.name}</option>`).join("");
}

function onMethodChange() {
  const sel  = document.getElementById("cooking-method");
  const methodId = parseInt(sel.value);
  const method = cookingMethods.find(m => m.id === methodId);
  const medRow = document.getElementById("medium-row");
  const hint   = document.getElementById("cooking-hint");

  if (!method) {
    medRow.classList.add("d-none");
    return;
  }

  medRow.classList.remove("d-none");

  // Подсказка с эффектом метода
  const wSign = method.weight_change_pct >= 0 ? "+" : "";
  let hintText = `Вес: ${wSign}${method.weight_change_pct}% | `;
  hintText += `Б: ×${method.protein_factor} | Ж: ×${method.fat_factor} | У: ×${method.carb_factor}`;
  if (method.absorbs_medium) {
    hintText += ` | Поглощение среды: ${method.medium_absorption_pct}%`;
  }
  hint.textContent = hintText;
}

function getCookingPayload() {
  const methodId = parseInt(document.getElementById("cooking-method")?.value) || null;
  const mediumId = parseInt(document.getElementById("cooking-medium")?.value) || null;
  const amount   = parseFloat(document.getElementById("medium-amount")?.value) || null;
  return {
    cooking_method_id: methodId || null,
    cooking_medium_id: (methodId && mediumId) ? mediumId : null,
    medium_amount_g:   (methodId && mediumId && amount) ? amount : null,
  };
}

// ─────────────────────────────────────────────────
//  INGREDIENTS
// ─────────────────────────────────────────────────

async function loadIngredients() {
  const search    = document.getElementById("ing-search")?.value   || "";
  const category  = document.getElementById("ing-category")?.value || "";
  const availOnly = document.getElementById("ing-available")?.checked ? "true" : "false";

  let url = `${API}/ingredients/?available_only=${availOnly}`;
  if (search)   url += `&search=${encodeURIComponent(search)}`;
  if (category) url += `&category=${encodeURIComponent(category)}`;

  const res   = await fetch(url);
  const items = await res.json();

  // Кешируем полный список (без фильтра) для матчинга рецептов
  if (!search && !category && availOnly === "false") allIngredients = items;

  const counter = document.getElementById("ing-count");
  if (counter) counter.textContent = `${items.length} продуктов`;
  renderIngredients(items);
}

function renderIngredients(items) {
  const container = document.getElementById("ingredients-list");
  if (!items.length) {
    container.innerHTML = `<div class="selected-empty" style="grid-column:1/-1">
      <div style="font-size:2rem;opacity:.3">🔎</div>Ничего не найдено</div>`;
    return;
  }
  container.innerHTML = items.map(ing => {
    const isSel = selected[ing.id] !== undefined;
    return `
    <div class="ing-card ${isSel ? "selected" : ""}" onclick="toggleIngredient(${ing.id}, this)">
      <div class="check-badge">✓</div>
      <div class="ing-name">${ing.name}</div>
      <div class="ing-cat">${ing.category}</div>
      <div class="ing-macros">
        <span class="macro-pill macro-cal">${ing.calories} ккал</span>
        <span class="macro-pill macro-p">Б ${ing.proteins}г</span>
        <span class="macro-pill macro-f">Ж ${ing.fats}г</span>
        <span class="macro-pill macro-c">У ${ing.carbs}г</span>
      </div>
      <div class="d-flex justify-content-between align-items-center">
        <span class="ing-avail ${ing.is_available ? "ok" : "out"}">
          ${ing.is_available ? "✓ В наличии" : "✗ Нет"}
        </span>
        <span class="ing-price">${ing.price_per_100g} ₽/100г</span>
      </div>
      ${isSel ? `<div class="ing-weight-row" onclick="event.stopPropagation()">
        <input type="number" value="${selected[ing.id].weight_g}" min="1"
               onchange="updateWeight(${ing.id}, this.value)">
        <span>г</span>
      </div>` : ""}
    </div>`;
  }).join("");
}

function toggleIngredient(id, cardEl) {
  if (selected[id]) { delete selected[id]; }
  else {
    const name = cardEl.querySelector(".ing-name").textContent.trim();
    selected[id] = { ingredient_id: id, weight_g: 100, name };
  }
  loadIngredients();
  renderSelectedPanel();
}

function updateWeight(id, val) {
  if (selected[id]) selected[id].weight_g = Math.max(1, parseFloat(val) || 100);
  renderSelectedPanel();
}

function removeIngredient(id) {
  delete selected[id];
  loadIngredients();
  renderSelectedPanel();
}

function renderSelectedPanel() {
  const panel = document.getElementById("selected-ingredients");
  const keys  = Object.keys(selected);
  if (!keys.length) {
    panel.innerHTML = `<div class="selected-empty">
      <div style="font-size:2rem;opacity:.3">🧺</div>
      Нажмите на ингредиент чтобы добавить</div>`;
    return;
  }
  panel.innerHTML = keys.map(id => `
    <div class="selected-item">
      <span class="si-name">${selected[id].name}</span>
      <input type="number" value="${selected[id].weight_g}" min="1"
             onchange="updateWeight(${id}, this.value)">
      <span class="si-unit">г</span>
      <button class="btn-icon btn-icon-danger" onclick="removeIngredient(${id})">✕</button>
    </div>`).join("");
}

// ─────────────────────────────────────────────────
//  RECIPES
// ─────────────────────────────────────────────────

function renderRecipes() {
  const grid = document.getElementById("recipes-grid");
  if (!grid) return;

  grid.innerHTML = RECIPES.map((r, idx) => {
    const tagHtml = r.tags.map((t, i) =>
      `<span class="recipe-tag ${i === 1 ? "tag-accent" : ""}">${t}</span>`).join("");
    const ingList = r.ingredients
      .map(i => `<strong>${i.name}</strong> ${i.weight_g}г`).join(" · ");
    return `
    <div class="recipe-card">
      <div class="recipe-card-header">
        <div class="recipe-emoji">${r.emoji}</div>
        <div class="recipe-name">${r.name}</div>
        <div class="recipe-desc">${r.desc}</div>
      </div>
      <div class="recipe-card-body">
        <div class="recipe-tags">${tagHtml}</div>
        <div class="recipe-ingredients">${ingList}</div>
        <div class="d-flex justify-content-between align-items-center small text-muted mb-3">
          <span>🍽 ${r.servings} порц.</span>
          <span>${r.ingredients.length} ингредиентов</span>
        </div>
        <button class="btn-recipe-load" onclick="loadRecipeIntoConstructor(${idx})">
          ✏️ Загрузить в конструктор
        </button>
      </div>
    </div>`;
  }).join("");
}

async function loadRecipeIntoConstructor(recipeIdx) {
  const recipe = RECIPES[recipeIdx];

  // Убедимся что у нас есть полный список ингредиентов
  if (!allIngredients.length) {
    const res = await fetch(`${API}/ingredients/`);
    allIngredients = await res.json();
  }

  // Матчим ингредиенты рецепта с базой
  selected = {};
  const notFound = [];

  for (const item of recipe.ingredients) {
    const ing = allIngredients.find(
      i => i.name.toLowerCase() === item.name.toLowerCase()
    );
    if (ing) {
      selected[ing.id] = { ingredient_id: ing.id, weight_g: item.weight_g, name: ing.name };
    } else {
      notFound.push(item.name);
    }
  }

  // Сбрасываем режим редактирования
  cancelEdit();
  editingDishId = null;

  // Заполняем поля
  document.getElementById("dish-name").value     = recipe.name;
  document.getElementById("dish-desc").value     = recipe.desc;
  document.getElementById("dish-servings").value = recipe.servings;

  showSection("constructor");
  loadIngredients();
  renderSelectedPanel();

  if (notFound.length) {
    toast(`Не найдены: ${notFound.join(", ")}`, "warn");
  } else {
    toast(`Рецепт «${recipe.name}» загружен — редактируйте и сохраняйте!`, "ok");
  }
}

// ─────────────────────────────────────────────────
//  EDIT MODE
// ─────────────────────────────────────────────────

async function startEditDish(dishId) {
  const res  = await fetch(`${API}/dishes/${dishId}`, { headers: authHeaders() });
  if (!res.ok) { toast("Не удалось загрузить блюдо", "err"); return; }
  const dish = await res.json();

  // Убедимся что ингредиенты загружены
  if (!allIngredients.length) {
    const r2 = await fetch(`${API}/ingredients/`);
    allIngredients = await r2.json();
  }

  editingDishId = dishId;
  selected = {};
  for (const di of dish.ingredients) {
    const ing = di.ingredient;
    selected[ing.id] = { ingredient_id: ing.id, weight_g: di.weight_g, name: ing.name };
  }

  document.getElementById("dish-name").value     = dish.name;
  document.getElementById("dish-desc").value     = dish.description || "";
  document.getElementById("dish-servings").value = dish.servings;

  // Показываем баннер
  document.getElementById("edit-banner").classList.remove("d-none");
  document.getElementById("edit-dish-name-label").textContent = dish.name;
  document.getElementById("builder-title").textContent = "Редактирование";
  document.getElementById("save-btn").textContent = "💾 Сохранить изменения";

  showSection("constructor");
  loadIngredients();
  renderSelectedPanel();
  toast(`Редактирование «${dish.name}»`, "ok");
}

function cancelEdit() {
  editingDishId = null;
  const banner = document.getElementById("edit-banner");
  if (banner) banner.classList.add("d-none");
  const title = document.getElementById("builder-title");
  if (title) title.textContent = "Моё блюдо";
  const btn = document.getElementById("save-btn");
  if (btn) btn.textContent = "⚡ Рассчитать и сохранить";
}

// ─────────────────────────────────────────────────
//  SAVE (CREATE or UPDATE)
// ─────────────────────────────────────────────────

async function saveDish() {
  const name        = document.getElementById("dish-name").value.trim();
  const description = document.getElementById("dish-desc").value.trim();
  const servings    = parseInt(document.getElementById("dish-servings").value) || 1;

  if (!name)                         { toast("Введите название блюда", "warn"); return; }
  if (!Object.keys(selected).length) { toast("Добавьте хотя бы один ингредиент", "warn"); return; }

  const ingredients = Object.values(selected).map(i => ({
    ingredient_id: i.ingredient_id,
    weight_g:      i.weight_g,
  }));

  const isEdit = editingDishId !== null;
  const url    = isEdit ? `${API}/dishes/${editingDishId}` : `${API}/dishes/`;
  const method = isEdit ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: authHeaders(),
    body: JSON.stringify({ name, description, servings, ingredients, ...getCookingPayload() }),
  });

  if (res.ok) {
    const dish = await res.json();
    toast(isEdit ? "Блюдо обновлено!" : "Блюдо сохранено!", "ok");
    cancelEdit();
    await showNutrition(dish.id, "constructor");
  } else {
    const err = await res.json();
    toast(err.detail || "Ошибка при сохранении", "err");
  }
}

// ─────────────────────────────────────────────────
//  NUTRITION
// ─────────────────────────────────────────────────

async function showNutrition(dishId, context) {
  const res = await fetch(`${API}/dishes/${dishId}/nutrition`, { headers: authHeaders() });
  if (!res.ok) return;
  const n = await res.json();

  if (context === "dishes") {
    renderNutritionPanel(n, document.getElementById("dishes-nutrition-panel"));
  } else {
    const panel = document.getElementById("nutrition-result");
    panel.classList.remove("d-none");
    renderNutritionMainPanel(n);
  }
}

function renderNutritionMainPanel(n) {
  const totalKcal = n.proteins * 4 + n.fats * 9 + n.carbs * 4 || 1;
  const pPct = Math.round(n.proteins * 4 / totalKcal * 100);
  const fPct = Math.round(n.fats    * 9 / totalKcal * 100);
  const cPct = Math.round(n.carbs   * 4 / totalKcal * 100);

  // Блок до/после
  const hasCooking = !!n.cooking_method_name;
  const effectBadge  = document.getElementById("cooking-effect-badge");
  const beforeAfter  = document.getElementById("before-after");
  const caloriesSimple = document.getElementById("calories-simple");

  if (hasCooking) {
    effectBadge.classList.remove("d-none");
    effectBadge.textContent = `🔥 ${n.cooking_effect}`;
    beforeAfter.classList.remove("d-none");
    caloriesSimple.classList.add("d-none");
    document.getElementById("raw-calories").textContent = n.raw_calories;
    document.getElementById("nutr-calories").textContent = n.calories;
  } else {
    effectBadge.classList.add("d-none");
    beforeAfter.classList.add("d-none");
    caloriesSimple.classList.remove("d-none");
    document.getElementById("nutr-calories-simple").textContent = n.calories;
  }

  document.getElementById("nutr-proteins-label").textContent = `${n.proteins} г`;
  document.getElementById("nutr-fats-label").textContent     = `${n.fats} г`;
  document.getElementById("nutr-carbs-label").textContent    = `${n.carbs} г`;
  document.getElementById("bar-p").style.width = pPct + "%";
  document.getElementById("bar-f").style.width = fPct + "%";
  document.getElementById("bar-c").style.width = cPct + "%";
  document.getElementById("nutr-cost").textContent   = `${n.total_cost} ₽`;
  document.getElementById("nutr-weight").textContent = `${n.total_weight_g} г`;

  const psRow = document.getElementById("nutr-per-serving-row");
  if (n.per_serving) {
    psRow.style.display = "";
    document.getElementById("nutr-per-serving").textContent =
      `${n.per_serving.calories} ккал · ${n.per_serving.cost} ₽`;
  }

  const avEl = document.getElementById("nutr-available");
  avEl.className   = "avail-badge " + (n.all_available ? "ok" : "out");
  avEl.textContent = n.all_available
    ? "✓ Все ингредиенты доступны"
    : "✗ Недоступны: " + n.unavailable_ingredients.join(", ");

  renderChart(n);
}

function renderNutritionPanel(n, container) {
  const totalKcal = n.proteins * 4 + n.fats * 9 + n.carbs * 4 || 1;
  const pPct = Math.round(n.proteins * 4 / totalKcal * 100);
  const fPct = Math.round(n.fats    * 9 / totalKcal * 100);
  const cPct = Math.round(n.carbs   * 4 / totalKcal * 100);

  container.innerHTML = `
  <div class="nutr-panel">
    <h6>Расчёт КБЖУ</h6>
    <div class="nutr-big">
      <div class="value">${n.calories}</div>
      <div class="label">ккал · всего</div>
    </div>
    <div class="macro-bars">
      <div class="macro-bar-row">
        <div class="macro-bar-label"><span style="color:#2471a3">Белки</span><span>${n.proteins} г</span></div>
        <div class="macro-bar-track"><div class="macro-bar-fill bar-p" style="width:${pPct}%"></div></div>
      </div>
      <div class="macro-bar-row">
        <div class="macro-bar-label"><span style="color:#d68910">Жиры</span><span>${n.fats} г</span></div>
        <div class="macro-bar-track"><div class="macro-bar-fill bar-f" style="width:${fPct}%"></div></div>
      </div>
      <div class="macro-bar-row">
        <div class="macro-bar-label"><span style="color:#1e8449">Углеводы</span><span>${n.carbs} г</span></div>
        <div class="macro-bar-track"><div class="macro-bar-fill bar-c" style="width:${cPct}%"></div></div>
      </div>
    </div>
    <div class="nutr-row"><span class="nkey">Стоимость</span><span class="nval">${n.total_cost} ₽</span></div>
    <div class="nutr-row"><span class="nkey">Вес блюда</span><span class="nval">${n.total_weight_g} г</span></div>
    <div class="nutr-row"><span class="nkey">На порцию</span>
      <span class="nval">${n.per_serving.calories} ккал · ${n.per_serving.cost} ₽</span></div>
    <div class="mt-2">
      <span class="avail-badge ${n.all_available ? "ok" : "out"}">
        ${n.all_available ? "✓ Все ингредиенты доступны" : "✗ Недоступны: " + n.unavailable_ingredients.join(", ")}
      </span>
    </div>
  </div>`;
}

function renderChart(n) {
  const ctx = document.getElementById("nutrition-chart").getContext("2d");
  if (window._chart) window._chart.destroy();
  window._chart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Белки", "Жиры", "Углеводы"],
      datasets: [{
        data: [n.proteins * 4, n.fats * 9, n.carbs * 4],
        backgroundColor: ["#2471a3", "#d68910", "#27ae60"],
        borderWidth: 0,
      }],
    },
    options: {
      cutout: "68%",
      plugins: { legend: { position: "bottom", labels: { font: { size: 11 }, padding: 10 } } },
    },
  });
}

// ─────────────────────────────────────────────────
//  MY DISHES
// ─────────────────────────────────────────────────

async function loadMyDishes() {
  if (!token) return;
  const res    = await fetch(`${API}/dishes/`, { headers: authHeaders() });
  if (!res.ok) return;
  const dishes = await res.json();
  const container = document.getElementById("my-dishes-list");

  if (!dishes.length) {
    container.innerHTML = `<div class="empty-state">
      <div class="empty-icon">🍽</div>
      <p>Вы ещё не создали ни одного блюда</p></div>`;
    return;
  }

  container.innerHTML = dishes.map(d => `
    <div class="dish-card">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <div class="dish-name">${d.name}</div>
          <div class="dish-meta">${d.ingredients.length} ингр. · ${d.servings} порц.</div>
        </div>
        <div class="d-flex gap-1">
          <button class="btn-icon" onclick="showNutrition(${d.id},'dishes')" title="КБЖУ">📊</button>
          <button class="btn-icon" onclick="startEditDish(${d.id})" title="Редактировать">✏️</button>
          <button class="btn-icon btn-icon-danger" onclick="deleteDish(${d.id})" title="Удалить">✕</button>
        </div>
      </div>
    </div>`).join("");
}

async function deleteDish(id) {
  if (!confirm("Удалить блюдо?")) return;
  await fetch(`${API}/dishes/${id}`, { method: "DELETE", headers: authHeaders() });
  toast("Блюдо удалено", "ok");
  loadMyDishes();
  document.getElementById("dishes-nutrition-panel").innerHTML = "";
}

// ─────────────────────────────────────────────────
//  TOAST
// ─────────────────────────────────────────────────

function toast(msg, type = "ok") {
  const colors = { ok: "#27ae60", err: "#e74c3c", warn: "#f39c12" };
  const t = document.createElement("div");
  t.textContent = msg;
  Object.assign(t.style, {
    position: "fixed", bottom: "24px", right: "24px", zIndex: 9999,
    background: colors[type] || colors.ok, color: "#fff",
    padding: "12px 20px", borderRadius: "10px",
    fontSize: "0.88rem", fontWeight: "500",
    boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
    transition: "opacity 0.3s",
  });
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; setTimeout(() => t.remove(), 300); }, 2800);
}

// ─────────────────────────────────────────────────
//  INIT
// ─────────────────────────────────────────────────

window.onload = () => {
  if (token) {
    setAuthUI(true);
    showSection("constructor");
    loadIngredients();
    loadCookingOptions();
  } else {
    setAuthUI(false);
    showSection("login");
  }
};
