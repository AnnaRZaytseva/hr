const vacancySelect = document.getElementById('vacancy-select');
const startInterviewBtn = document.getElementById('start-interview-btn');
const vacancyList = document.getElementById('vacancy-list');
const vacancyTitle = document.getElementById('vacancy-title');
const vacancyDescription = document.getElementById('vacancy-description');
const vacancyRequirements = document.getElementById('vacancy-requirements');
const textArea = document.getElementById('answer');
const questionContainer = document.getElementById('question-container');
const vacancySelection = document.getElementById('vacancy-selection');
const questionText = document.getElementById('question-text');

const nextBtn = document.getElementById('next');
const progressQuestions = document.getElementById('progress-questions');
const progressFill = document.getElementById('progress-fill');
const stepNumber1 = document.getElementById('step-number1');
const stepText1 = document.getElementById('step-text1');
const stepNumber2 = document.getElementById('step-number2');
const stepText2 = document.getElementById('step-text2');
const progressText = document.getElementById('progress-text');
const button = document.getElementById('button');

//начальное состояние страницы
let currentVacancy = null;
questionContainer.style.opacity =0;
let currentQuestionIndex = 0;

//обрабатываю выбор вакансии
vacancySelect.addEventListener('change', function() {

    const selectedValue = this.value; //выбранная вакансия сохраняется
    startInterviewBtn.disabled = !selectedValue; //если не выбрана то кнопка не доступна для нажатия

    if (selectedValue) {
        currentVacancy = selectedValue;
        vacancyTitle.textContent = vacancies[selectedValue].title;
        vacancyDescription.textContent = vacancies[selectedValue].description;
        vacancyRequirements.textContent = vacancies[selectedValue].requirements;
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
    if (!currentVacancy) return alert('Выберите вакансию');
    fetch('getq_first/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({vacancy_id: currentVacancy})
        
    })
    .then(r => r.json())
    .then(data => questionText.textContent = data.question || data.error)
    .catch(e => console.error(e));


    vacancySelection.style.display = 'none';
    questionContainer.style.display = 'block';
    progressText.textContent= 'шаг 2 из 3';
    progressFill.style.width = "66%";

    // fetch('/employee/getq_first/', { // Замените на ваш URL для получения вопроса
    //         method: 'POST',
    //         headers: {'Content-Type': 'application/json'},
    //         body: JSON.stringify({vacancy_id: currentVacancy})
    //     })
    //     .then(res => res.json())
    //     .then(data => {
    //         questionText.textContent = data.question || 'Начинаем собеседование';
    //         questionContainer.style.opacity = 1;
    //     })
    //     .catch(err => {
    //         console.error(err);
    //         vacancySelection.style.display = 'block';
    //         questionContainer.style.display = 'none';
    //     });

    currentQuestionIndex = 0;

    /*
    questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
    progressQuestions.textContent = `Вопрос ${currentQuestionIndex + 1} из ${vacancies[currentVacancy].questions.length}`;
    */

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

nextBtn.addEventListener('click', function() {

    const answer = textArea.value;

    fetch('/employee/vacancyinfo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: answer })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при отправке ответа: ' + response.status);
        }
        return response.json();
    })
    .then(data => {

        if (data.success) {
            return fetch('getq/');
        } else {
            console.error("Ошибка сервера при обработке ответа:", data);
            throw new Error("Ошибка сервера при обработке ответа"); //  Перебрасываем ошибку для обработки в .catch
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при получении следующего вопроса: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        textArea.value = '';
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
});

    fetch('getq/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.question == 'КОНЕЦ') {
                questionText.textContent = 'Собеседование закончено! Мы с вами свяжемся в ближайшее время.';
                textArea.value = '';
                nextBtn.disabled = true;
            } else {
                questionText.textContent = data.question;
                textArea.value = '';
                currentQuestionIndex += 1;
                progressQuestions.textContent = `Вопрос ${currentQuestionIndex + 1}`;
    }
        })
            .catch(error => {
                console.error('Error fetching initial question:', error);
        });

});

/*
function areAllQuestionsAnswered() {
    return answers.every(answer => answer.trim() !== '');
}
function updateFinishButton() {
    button.disabled = !areAllQuestionsAnswered();
}
*/

/*
textarea.addEventListener('input', function() {
    answers[currentQuestionIndex] = textArea.value;
    updateFinishButton();
});
*/




