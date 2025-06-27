const vacancySelect = document.getElementById('vacancy-select');
const startInterviewBtn = document.getElementById('start-interview-btn');
const vacancyTitle = document.getElementById('vacancy-title');
const vacancyDescription = document.getElementById('vacancy-description');
const textarea = document.getElementById('answer');
const questionContainer = document.getElementById('question-container');
const vacancySelection = document.getElementById('vacancy-selection');
const questionText = document.getElementById('question-text');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const progressQuestions = document.getElementById('progress-questions');
const progressFill = document.getElementById('progress-fill');
const stepNumber1 = document.getElementById('step-number1');
const stepText1 = document.getElementById('step-text1');
const stepNumber2 = document.getElementById('step-number2');
const stepText2 = document.getElementById('step-text2');
const progressText = document.getElementById('progress-text');
const button = document.getElementById('button');

// Данные о вакансиях временно для теста функционала
// const vacancies = {
//     'frontend': {
//         title: 'Frontend разработчик',
//         description: 'Мы ищем фронтенд-разработчика с опытом работы с React от 2 лет. Обязательные навыки: JavaScript, React, Redux, HTML/CSS, работа с REST API.',
//         questions: [
//             'Расскажите о своем опыте работы с React. Какие проекты вы разрабатывали?',
//             'Как вы организуете управление состоянием в React-приложении?',
//             'Опишите процесс оптимизации производительности React-приложения.']
//     },
//     'backend': {
//         title: 'Backend разработчик',
//         description: 'Требуется бэкенд-разработчик с опытом работы с Node.js от 3 лет. Знание SQL/NoSQL баз данных, Docker, микросервисной архитектуры.',

//     }
// }

//начальное состояние страницы
let currentVacancy = null;
questionContainer.style.opacity =0;
let currentQuestionIndex = 0;
let answers = Array(3).fill('');

// let vacancies = {};

// document.addEventListener('DOMContentLoaded', function() {
//     const select = document.getElementById('vacancy-select');
//     const descriptionDiv = document.getElementById('vacancy-description');
    
//     select.addEventListener('change', function() {
//         const selectedValue = this.value;
//         if (selectedValue && vacanciesData[selectedValue]) {
//             descriptionDiv.innerHTML = vacanciesData[selectedValue].description;
//         } else {
//             descriptionDiv.innerHTML = '';
//         }
//     });
// });

//обрабатываю выбор вакансии
vacancySelect.addEventListener('change', function() {
    const selectedValue = this.value; //выбранная вакансия сохраняется
    startInterviewBtn.disabled = !selectedValue; //если не выбрана то кнопка не доступна для нажатия

    if (selectedValue) {
        currentVacancy = selectedValue;
        vacancyTitle.textContent = vacancies[selectedValue].title;
        vacancyDescription.textContent = vacancies[selectedValue].description;
        //если выбрана, то текущая вакансия=выбранная вакансия, заголовку вакансии присваивается название из массива вакансий и описание
        progressFill.style.width = "33%";
        stepNumber1.style.backgroundColor ="#e5937d";
        stepText1.style.fontSize = "20px";


    } else {
        vacancyTitle.textContent = 'Не выбрано';
        vacancyDescription.textContent = 'Пожалуйста, выберите вакансию из списка справа, чтобы начать собеседование.';
        progressFill.style.width = "0%";
        stepNumber1.style.backgroundColor ="#9d82f1";
        stepText1.style.fontSize = "18px";
    }
});


//начало тестирования
startInterviewBtn.addEventListener('click', function() {
    if (!vacancies[currentVacancy].questions || vacancies[currentVacancy].questions.length === 0) {
        alert('Для выбранной вакансии нет вопросов');
        return;
    }
    vacancySelection.style.display = 'none';
    questionContainer.style.display = 'block';
    progressText.textContent= 'шаг 2 из 3';
    progressFill.style.width = "66%";



    // Загружаю первый вопрос
    currentQuestionIndex = 0;
    questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
    progressQuestions.textContent = `Вопрос ${currentQuestionIndex + 1} из ${vacancies[currentVacancy].questions.length}`;


    // Анимация появления
    let opacity = 0;
    const interval = setInterval(() => {
        opacity += 0.1;
        questionContainer.style.opacity = opacity;
        if (opacity >= 1) {
            clearInterval(interval);
        }
    }, 10);

    stepNumber2.style.backgroundColor ="#e5937d";
    stepText2.style.fontSize = "20px";
    stepNumber1.style.backgroundColor ="#9d82f1";
    stepText1.style.fontSize = "18px";

});

if(currentQuestionIndex = 0){
    prevBtn.disabled = true;
} else{
    prevBtn.disabled = false;
}

prevBtn.addEventListener('click', function(){

    if (currentQuestionIndex > 0) {
        currentQuestionIndex -= 1;
        textarea.value= answers[currentQuestionIndex];
        questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
        progressQuestions.textContent = `Вопрос ${currentQuestionIndex + 1} из ${vacancies[currentVacancy].questions.length}`;
    }
    updateFinishButton();
});

nextBtn.addEventListener('click', function(){

    if (currentQuestionIndex < vacancies[currentVacancy].questions.length - 1) {
        currentQuestionIndex += 1;
        textarea.value= answers[currentQuestionIndex];
        questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
        progressQuestions.textContent = `Вопрос ${currentQuestionIndex + 1} из ${vacancies[currentVacancy].questions.length}`;
    }
    updateFinishButton();

});

function areAllQuestionsAnswered() {
    return answers.every(answer => answer.trim() !== '');
}
function updateFinishButton() {
    button.disabled = !areAllQuestionsAnswered();
}
textarea.addEventListener('input', function() {
    answers[currentQuestionIndex] = textarea.value;
    updateFinishButton();
});







