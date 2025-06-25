const vacancySelect = document.getElementById('vacancy-select');
const startInterviewBtn = document.getElementById('start-interview-btn');
const vacancyTitle = document.getElementById('vacancy-title');
const vacancyDescription = document.getElementById('vacancy-description');
//начальное состояние страницы
let currentVacancy = null; //начальный выбор вакансии отсутсвует
//обрабатываю выбор вакансии
vacancySelect.addEventListener('change', function() {
            const selectedValue = this.value; //выбранная вакансия сохраняется
            startInterviewBtn.disabled = !selectedValue; //если не выбрана то кнопка не доступна для нажатия

            if (selectedValue) {
                currentVacancy = selectedValue;
                vacancyTitle.textContent = vacancies[selectedValue].title;
                vacancyDescription.textContent = vacancies[selectedValue].description;
                //если выбрана, то текущая вакансия=выбранная вакансия, заголовку вакансии присваивается название из массива вакансий и описание
            } else {
                vacancyTitle.textContent = 'Выберите вакансию';
                vacancyDescription.textContent = 'Пожалуйста, выберите вакансию из списка справа, чтобы начать собеседование.';
            }
        });


// Данные о вакансиях временно для теста функционала
        const vacancies = {
            'frontend': {
                title: 'Frontend разработчик',
                description: 'Мы ищем фронтенд-разработчика с опытом работы с React от 2 лет. Обязательные навыки: JavaScript, React, Redux, HTML/CSS, работа с REST API.',
            },
            'backend': {
                title: 'Backend разработчик',
                description: 'Требуется бэкенд-разработчик с опытом работы с Node.js от 3 лет. Знание SQL/NoSQL баз данных, Docker, микросервисной архитектуры.',

            }
        }