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
const mainContent = document.getElementById('main-content');
const submitBtn = form.querySelector('.submit-btn');
const addform = document.getElementById('addvacancyForm');

// const Vacancies = [
//     {
//       id: 1,
//       title: 'Frontend-разработчик',
//       description: 'Разработка пользовательских интерфейсов для веб-приложений.',
//       requirements: 'Опыт работы с React, JavaScript, HTML/CSS. Понимание принципов REST API.',
//       responsibilities: 'Разработка новых компонентов. Оптимизация производительности. Участие в код-ревью.',
//       conditions: 'Гибкий график. Удаленная работа. Медицинская страховка.',
//       interviews: 12,
//       isActive: true
//     },
//     {
//       id: 2,
//       title: 'Backend-разработчик',
//       description: 'Разработка серверной части веб-приложений.',
//       requirements: 'Опыт работы с Python, Django/Flask, PostgreSQL. Знание Docker.',
//       responsibilities: 'Разработка API. Оптимизация запросов к БД. Написание unit-тестов.',
//       conditions: 'Офис в центре города. Гибкий график. Курсы за счет компании.',
//       interviews: 8,
//       isActive: false
//     }
//   ];

//начальное состояние
formContainer.style.display = 'none';
vacancies.style.display = 'none';

function returnHomePage(){
cardsBlock.style.display ='flex';
activitiesBlock.style.display = 'block';
logout.style.display = 'flex';
mainText.textContent = 'Здравствуйте, USERNAME';
subText.textContent = 'Добро пожаловать в личный кабинет'
hideForm();
hideForm1();
hideList();
let opacity = 0;
  const interval = setInterval(() => {
    opacity += 0.1;
    mainContent.style.opacity = opacity;
    if (opacity >= 1) {
      clearInterval(interval);
    }
  }, 10);

}

function hideHomePage(){
cardsBlock.style.display ='none';
activitiesBlock.style.display = 'none';
logout.style.display = 'none';
}

function hideForm(){
formContainer.style.display = 'none';
}

function hideForm1(){
formContainer1.style.display = 'none';
}

function hideList(){
vacancies.style.display ='none';
searchBar.style.display='none';
}

function resetForm() {
form.reset();
form.removeAttribute('data-edit-id');
submitBtn.textContent = 'Добавить вакансию';
const inputs = form.querySelectorAll('input, textarea');
  inputs.forEach(input => {
    input.classList.remove('error');
  });
}


menuItem1.addEventListener('click', function() {
returnHomePage();
});

menuItem2.addEventListener('click', function() {
hideHomePage();
hideList();
hideForm();
formContainer1.style.display = 'block';
mainText.textContent = 'Добавить новую вакансию';
subText.textContent = 'Пожалуйста, заполните поля ниже';



let opacity = 0;
  const interval = setInterval(() => {
    opacity += 0.1;
    formContainer.style.opacity = opacity;
    if (opacity >= 1) {
      clearInterval(interval);
    }
  }, 10);


});

menuItem3.addEventListener('click', function() {
hideHomePage();
hideForm();
hideForm1();
vacancies.style.display = 'block';
mainText.textContent = 'Список вакансий';
subText.textContent = 'Управление опубликованными вакансиями';
header.appendChild(searchBar);

let opacity = 0;
const vacanciesBlock = document.getElementById('vacancies');
vacanciesBlock.style.opacity = opacity;
vacanciesBlock.style.display = 'block';

const interval = setInterval(() => {
opacity += 0.1;
vacanciesBlock.style.opacity = opacity;
if (opacity >= 1) {
clearInterval(interval);
}
}, 5);

loadVacancies();
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

document.addEventListener('DOMContentLoaded', () => {
const progressCircle = document.querySelector('.progress-circle');
animateProgressCircle(70, progressCircle.parentElement);
});




function loadVacancies() {
vacanciesList.innerHTML = '';
  Vacancies.forEach(vacancy => {
    const vacancyItem = document.createElement('div');
    vacancyItem.className = 'vacancy-item';
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

    vacanciesList.appendChild(vacancyItem);
    const vacancyHeader = vacancyItem.querySelector('.vacancy-header');
    const vacancyContent = vacancyItem.querySelector('.vacancy-content');

    vacancyHeader.addEventListener('click', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.classList.contains('toggle-slider')) {
        return;
      }
      vacancyContent.classList.toggle('expanded');
    });

    const toggle = vacancyItem.querySelector('input[type="checkbox"]');
    toggle.addEventListener('change', function() {
      confirm(`Вакансия ${vacancy.id} теперь ${this.checked ? 'активна' : 'скрыта'}`);

    });

    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const vacancyId = parseInt(this.getAttribute('data-id'));
            editVacancy(vacancyId);
            searchBar.style.display = 'none';
        });
    });

    vacancyItem.querySelector('.delete-btn').addEventListener('click', function() {
      deleteVacancy(vacancy.id);
    });

    vacancyItem.querySelector('.report-btn').addEventListener('click', function() {
      showReport(vacancy.id);
    });
  });
}

// Функции для действий с вакансиями
function findVacancyById(id) {
    return Vacancies.find(vacancy => vacancy.id === id);
}

// Функция для редактирования вакансии
function editVacancy(id) {
    const foundVacancy = findVacancyById(id);
    //Показываем форму
    hideHomePage();
    hideList();
    formContainer.style.display = 'block';
    mainText.textContent = 'Редактирование вакансии';
    subText.textContent = 'Внесите необходимые изменения';
    resetForm();

    // Заполняем поля формы
    document.getElementById('title').value = foundVacancy.title;
    document.getElementById('description').value = foundVacancy.description;
    document.getElementById('requirements').value = foundVacancy.requirements;
    document.getElementById('responsibilities').value = foundVacancy.responsibilities;
    document.getElementById('conditions').value = foundVacancy.conditions;

     form.setAttribute('data-edit-id', id);

     const submitBtn = form.querySelector('.submit-btn');
     submitBtn.textContent = 'Сохранить изменения';

      const newForm = form.cloneNode(true);
      form.parentNode.replaceChild(newForm, form);

      newForm.addEventListener('submit', function(e) {
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

          alert('Изменения сохранены!');
          loadVacancies(); // Перезагружаем список
          menuItem3.click(); // Переключаемся на список вакансий
        }
      });

}



function deleteVacancy(id) {
  if (confirm('Вы уверены, что хотите удалить эту вакансию?')) {
    console.log(`Удаление вакансии ${id}`);

    loadVacancies();
  }
}

function showReport(id) {
  console.log(`Показ отчета по вакансии ${id}`);

  alert(`Отчет по вакансии #${id} будет отображен здесь`);
}


search.addEventListener('click', function() {
  const searchTerm = document.getElementById('searchVacancy').value.toLowerCase();
  const vacanciesItems = document.querySelectorAll('.vacancy-item');
  vacanciesItems.forEach(vacancy => {
    const title = vacancy.querySelector('.vacancy-title').textContent.toLowerCase();
    if (title.includes(searchTerm)) {
      vacancy.style.display = 'block';
    } else {
      vacancy.style.display = 'none';
    }
  });
});


//добавление вакансии
// addform.addEventListener('submit', function(e) {
//   e.preventDefault();

//   const title = this.elements.title1.value;
//   const description = this.elements.description1.value;
//   const requirements = this.elements.requirements1.value;
//   const responsibilities = this.elements.responsibilities1.value;
//   const conditions = this.elements.conditions1.value;

//   addNewVacancy(this);
//   this.reset();

//   menuItem3.click();
//   loadVacancies();
// });

// function addNewVacancy(form) {
//   const title = form.title1.value;
//   const description = form.description1.value;
//   const requirements = form.requirements1.value;
//   const responsibilities = form.responsibilities1.value;
//   const conditions = form.conditions1.value;

//   const newVacancy = {
//     id: Vacancies.length > 0 ? Math.max(...Vacancies.map(v => v.id)) + 1 : 1,
//     title,
//     description,
//     requirements,
//     responsibilities,
//     conditions,
//     interviews: 0,
//     isActive: true
//   };

//   Vacancies.push(newVacancy);
//   alert('Новая вакансия успешно добавлена!');
// }