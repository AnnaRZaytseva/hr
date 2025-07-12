// Полный рабочий скрипт с исправлениями для корректной работы UI вакансий

const formContainer = document.getElementById('form-container');
const formContainer1 = document.getElementById('form-container1');
const menuItem1 = document.getElementById('item1');
const menuItem2 = document.getElementById('item2');
const menuItem3 = document.getElementById('item3');
const cardsBlock = document.getElementById('cards');
const activitiesBlock = document.getElementById('activities');
const header = document.getElementById('header');
const mainText = document.getElementById('main-text');
const subText = document.getElementById('sub-text');
const logout = document.getElementById('logout');
const reset = document.getElementById('reset1');
const vacancies = document.getElementById('vacancies');
const searchBar = document.getElementById('search-bar');
const search = document.getElementById('search');
const vacanciesList = document.getElementById('vacancies-list');
const form = document.getElementById('vacancyForm');
const addform = document.getElementById('addvacancyForm');
const mainContent = document.getElementById('main-content');
const submitBtn = form.querySelector('.submit-btn');
const reports = document.getElementById('reports');
const reportList = document.getElementById('report-list');

function returnHomePage() {
  cardsBlock.style.display = 'flex';
  activitiesBlock.style.display = 'block';
  if (logout) logout.style.display = 'flex';
  mainText.textContent = `Здравствуйте, ${user_name}!`;
  subText.textContent = 'Добро пожаловать в личный кабинет';
  hideForm();
  hideForm1();
  hideList();
  hideReports();
  let opacity = 0;
  const interval = setInterval(() => {
    opacity += 0.1;
    mainContent.style.opacity = opacity;
    if (opacity >= 1) clearInterval(interval);
  }, 10);
}

function hideHomePage() {
  cardsBlock.style.display = 'none';
  activitiesBlock.style.display = 'none';
  if (logout) logout.style.display = 'none';
}

function hideForm() {
  formContainer.style.display = 'none';
}

function hideForm1() {
  formContainer1.style.display = 'none';
}

function hideList() {
  vacancies.style.display = 'none';
  searchBar.style.display = 'none';
}
function hideReports() {
  reports.style.display = 'none';
}

function resetForm() {
  form.reset();
  form.removeAttribute('data-edit-id');
  submitBtn.textContent = 'Опубликовать вакансию';
  form.querySelectorAll('input, textarea').forEach(input => input.classList.remove('error'));
}

menuItem1.addEventListener('click', returnHomePage);

menuItem2.addEventListener('click', function () {
  hideHomePage();
  hideList();
  hideForm();
  hideReports();
  formContainer1.style.display = 'block';
  mainText.textContent = 'Добавить новую вакансию';
  subText.textContent = 'Пожалуйста, заполните поля ниже';
  let opacity = 0;
  const interval = setInterval(() => {
    opacity += 0.1;
    formContainer1.style.opacity = opacity;
    if (opacity >= 1) clearInterval(interval);
  }, 10);
});

menuItem3.addEventListener('click', function () {
  hideHomePage();
  hideForm();
  hideForm1();
  hideReports();
  vacancies.style.display = 'block';
  mainText.textContent = 'Список вакансий';
  subText.textContent = 'Управление опубликованными вакансиями';
  header.appendChild(searchBar);

  let opacity = 0;
  vacancies.style.opacity = opacity;
  const interval = setInterval(() => {
    opacity += 0.1;
    vacancies.style.opacity = opacity;
    if (opacity >= 1) clearInterval(interval);
  }, 5);

  loadVacancies();
});

document.addEventListener('DOMContentLoaded', () => {
  const progressCircle = document.querySelector('.progress-circle');
  animateProgressCircle(Math.round(avg_score_percentage), progressCircle.parentElement);
});

function animateProgressCircle(percent, element) {
  const circle = element.querySelector('.progress-fill');
  const text = element.querySelector('.progress-text');
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const targetOffset = circumference - (percent / 100) * circumference;
  circle.style.transition = 'stroke-dashoffset 1.5s ease-out';
  circle.style.strokeDashoffset = targetOffset;
  let current = 0;
  const interval = setInterval(() => {
    text.textContent = `${current}%`;
    current++;
    if (current > percent) clearInterval(interval);
  }, 15);
}

function loadVacancies() {
  vacanciesList.innerHTML = '';
  Vacancies.forEach(vacancy => {
    const vacancyItem = document.createElement('div');
    vacancyItem.className = 'vacancy-item';
    vacancyItem.dataset.id = vacancy.id;
    vacancyItem.innerHTML = `
      <div class="vacancy-header">
        <div class="vacancy-title">${vacancy.title}</div>
        <div class="vacancy-stats">
          <div class="interview-count">Собеседований: ${vacancy.interviews}</div>
          <label class="vacancy-toggle">
            <input type="checkbox" ${vacancy.isActive ? 'checked' : ''}>
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>
      <div class="vacancy-content">
        <div class="vacancy-section">
          <h4>Описание</h4>
          <div class="vacancy-section-content">${vacancy.description}</div>
        </div>
        <div class="vacancy-section">
          <h4>Требования</h4>
          <div class="vacancy-section-content">${vacancy.requirements}</div>
        </div>
        <div class="vacancy-section">
          <h4>Обязанности</h4>
          <div class="vacancy-section-content">${vacancy.responsibilities}</div>
        </div>
        <div class="vacancy-section">
          <h4>Условия</h4>
          <div class="vacancy-section-content">${vacancy.conditions}</div>
        </div>
        <div class="vacancy-actions">
          <button class="action-btn edit-btn" data-id="${vacancy.id}">Изменить</button>
          <button class="action-btn delete-btn" data-id="${vacancy.id}">Удалить</button>
          <button class="action-btn report-btn" data-id="${vacancy.id}">Отчет</button>
        </div>
      </div>
    `;

    const vacancyHeader = vacancyItem.querySelector('.vacancy-header');
    const vacancyContent = vacancyItem.querySelector('.vacancy-content');
    vacancyHeader.addEventListener('click', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.classList.contains('toggle-slider')) return;
      vacancyContent.classList.toggle('expanded');
    });

    vacancyItem.querySelector('.edit-btn').addEventListener('click', function () {
      editVacancy(vacancy.id);
      searchBar.style.display = 'none';
    });

    vacancyItem.querySelector('.delete-btn').addEventListener('click', function () {
      handleDeleteVacancy(vacancy.id, vacancyItem);
    });

    vacancyItem.querySelector('.report-btn').addEventListener('click', function () {
      showReport(vacancy.id);
    });

    const toggle = vacancyItem.querySelector('input[type="checkbox"]');
    toggle.addEventListener('change', async (e) => {
      const response = await fetch('update-vacancy-status/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vacancy_id: vacancy.id,
          is_active: e.target.checked
        })
      });
      if (!response.ok) e.target.checked = !e.target.checked;
    });

    vacanciesList.appendChild(vacancyItem);
  });
}

function handleDeleteVacancy(vacancyId, vacancyElement) {
  if (!confirm('Вы уверены, что хотите удалить вакансию?')) return;
  fetch('delete-vacancy/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vacancy_id: vacancyId })
  })
    .then(response => {
      if (!response.ok) throw new Error(`Ошибка: ${response.status}`);
      vacancyElement.remove();
      showNotification('Вакансия успешно удалена', 'success');
    })
    .catch(error => {
      console.error('Ошибка при удалении:', error);
      showNotification('Не удалось удалить вакансию', 'error');
    });
}

async function editVacancy(id) {
  const found = Vacancies.find(v => v.id === id);
  hideHomePage();
  hideList();
  hideReports();
  formContainer.style.display = 'block';
  mainText.textContent = 'Редактирование вакансии';
  subText.textContent = 'Внесите необходимые изменения';
  resetForm();
  form.setAttribute('data-edit-id', id);
  form.title.value = found.title;
  form.description.value = found.description;
  form.requirements.value = found.requirements;
  form.responsibilities.value = found.responsibilities;
  form.conditions.value = found.conditions;
  const newForm = form.cloneNode(true);
  form.parentNode.replaceChild(newForm, form);
  newForm.addEventListener('submit', async function (e) {
    if (!confirm('Вы уверены, что хотите изменить вакансию?')) window.location.reload();  
    e.preventDefault();
    const editId = parseInt(this.getAttribute('data-edit-id'));
    const index = Vacancies.findIndex(v => v.id === editId);
    if (index !== -1) {
      Vacancies[index] = {
        ...Vacancies[index],
        title: this.title.value,
        description: this.description.value,
        requirements: this.requirements.value,
        responsibilities: this.responsibilities.value,
        conditions: this.conditions.value
      };
      await fetch('update-vacancy/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vacancy_id: id,
          title: this.title.value,
          description: this.description.value,
          requirements: this.requirements.value,
          responsibilities: this.responsibilities.value,
          conditions: this.conditions.value
        })
      });
      loadVacancies();
      menuItem3.click();
    }
  });
}

function showReport(vacancyId) {
  hideList();
  reports.style.display = 'block';
  mainText.textContent = 'Отчёты';
  // subText.textContent = 'Просмотр результатов собеседований';
  reportList.innerHTML = '';

  let opacity = 0;
  reports.style.opacity = opacity;
  const interval = setInterval(() => {
    opacity += 0.1;
    reports.style.opacity = opacity;
    if (opacity >= 1) clearInterval(interval);
  }, 5);


  fetch('get-vacancy-report/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vacancy_id: vacancyId })
  })
    .then(response => {
      if (!response.ok) throw new Error(`Ошибка: ${response.status}`);
      return response.json();
    })
    .then(data => {
      if (!data.report_info || data.report_info.length === 0) {
        reportList.innerHTML = '<div class="no-data">Нет данных по этой вакансии</div>';
        return;
      }
      
      data.report_info.forEach(user => {
        const reportItem = document.createElement('div');
        reportItem.className = 'report-item';
        subText.textContent = `Просмотр результатов собеседований по вакансии ${user.vacancy_title}`;
reportItem.innerHTML = `
  <div class="report-header">
    <div class="report-main">

      <div class="report-user">${user.fullname}</div>
    </div>
    <div class="report-stats">
      <div class="interview-per">${user.per}</div>
    </div>
  </div>
  <div class="report-content">
    <div class="report-section">
      <h4>Связь с пользователем</h4>
      <div class="report-section-content">${user.email}</div>
    </div>
    <div class="report-section">
      <h4>Заключенеи системы</h4>
      <div class="report-section-content">${user.ai_result}</div>
    </div>

    ${user.qa_pairs.map((qa, index) => `
      <div class="qa-pair">
        <div class="report-section">
          <h4>Вопрос ${index + 1}</h4>
          <div class="report-section-content">
            ${qa.question}
          </div>
        </div>
        <div class="report-section">
          <h4>Ответ</h4>
          <div class="report-section-content">
            ${qa.answer}
          </div>
        </div>
      </div>
    `).join('')}
  </div>
`;
        
        const reportHeader = reportItem.querySelector('.report-header');
        const reportContent = reportItem.querySelector('.report-content');
        reportHeader.addEventListener('click', () => {
          reportContent.classList.toggle('expanded');
        });
        
        reportList.appendChild(reportItem);
      });
    })
    .catch(error => {
      console.error('Ошибка при получении отчета:', error);
      reportList.innerHTML = `<div class="error">Ошибка загрузки: ${error.message}</div>`;
    });
}

search.addEventListener('click', function () {
  const searchTerm = document.getElementById('searchVacancy').value.toLowerCase();
  document.querySelectorAll('.vacancy-item').forEach(v => {
    const title = v.querySelector('.vacancy-title').textContent.toLowerCase();
    v.style.display = title.includes(searchTerm) ? 'block' : 'none';
  });
});

addform.addEventListener('submit', async function (e) {
  e.preventDefault();
  const response = await fetch('add-vacancy/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: this.title.value,
      description: this.description.value,
      requirements: this.requirements.value,
      responsibilities: this.responsibilities.value,
      conditions: this.conditions.value
    })
  });
  const data = await response.json();
  if (data.status === 'success') {
    this.reset();
    sessionStorage.setItem('shouldClick', 'true');
    window.location.reload();
  } else {
    alert('Ошибка при добавлении');
  }
});

window.addEventListener('load', () => {
  if (sessionStorage.getItem('shouldClick')) {
    sessionStorage.removeItem('shouldClick');
    menuItem3.click();
  }
});
