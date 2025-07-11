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
const stepNumber3 = document.getElementById('step-number3');
const stepText3 = document.getElementById('step-text3');
const progressText = document.getElementById('progress-text');
const button = document.getElementById('button');
const stepDiv1 = document.getElementById('step1');
const stepDiv2 = document.getElementById('step2');
const stepDiv3 = document.getElementById('step3');


//начальное состояние страницы
let currentVacancy = null;
questionContainer.style.opacity =0;
let currentQuestionIndex = 0;

let currentStep = 1;
function isMobile() {
    return window.matchMedia("(max-width: 767px)").matches;
}

// Создаем наблюдатель за изменением размеров
const resizeObserver = new ResizeObserver(entries => {
  for (let entry of entries) {
    const width = entry.contentRect.width;
    
    if (isMobile()) {
        if (currentStep === 1){
            stepDiv1.style.display="flex";
            stepDiv2.style.display="none";
            stepDiv3.style.display="none";
        }
        else if (currentStep === 2){
            stepDiv1.style.display="none";
            stepDiv2.style.display="flex";
            stepDiv3.style.display="none";
        }
        else if (currentStep === 3){
            stepDiv1.style.display="none";
            stepDiv2.style.display="none";
            stepDiv3.style.display="flex";
        }
    }
    else {
        stepDiv1.style.display="flex";
        stepDiv2.style.display="flex";
        stepDiv3.style.display="flex";
    }
  }
});

// Начинаем наблюдение за элементом (или за window)
resizeObserver.observe(document.documentElement);

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

        currentStep = 1;
        
    } else {
        vacancyTitle.textContent = 'Не выбрано';
        vacancyDescription.textContent = 'Пожалуйста, выберите вакансию из списка справа, чтобы начать собеседование.';
        progressFill.style.width = "0%";
        stepNumber1.style.backgroundColor ="#9d82f1";
        stepText1.style.fontSize = "18px";

        currentStep = 0;
    }
});


//начало тестирования
startInterviewBtn.addEventListener('click', function() {
    const selectedVacancy = vacancySelect.value;
    if (!selectedVacancy) return alert('Выберите вакансию');

    fetch('handle_interview/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ vacancy_id: selectedVacancy })
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка сети');
        return response.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.error);
        
        // Обновляем UI на основе данных сервера
        questionText.textContent = data.question;
        progressQuestions.textContent = `Вопрос ${data.progress.current}`;
        
        vacancySelection.style.display = 'none';
        questionContainer.style.display = 'block';
        progressText.textContent = 'Шаг 2 из 3';
        progressFill.style.width = "66%";
        
        // Анимация появления
        questionContainer.style.opacity = 0;
        let opacity = 0;
        const interval = setInterval(() => {
            opacity += 0.1;
            questionContainer.style.opacity = opacity;
            if (opacity >= 1) clearInterval(interval);
        }, 10);
        
        stepNumber2.style.backgroundColor = "#e5937d";
        stepText2.style.fontSize = "20px";
    })
    .catch(error => alert('Ошибка: ' + error.message));
});

nextBtn.addEventListener('click', function() {
    const answer = textArea.value.trim();
    if (!answer) return alert('Введите ответ');

    fetch('handle_interview/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ answer: answer })
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка сети');
        return response.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.error);

        if (data.status === 'completed') {
            // Завершение собеседования
            progressText.textContent = 'Шаг 3 из 3';
            progressFill.style.width = "100%";
            stepNumber3.style.backgroundColor ="#e5937d";
            stepText3.style.fontSize = "20px";

            
            textArea.style.display = 'none';
            nextBtn.style.display = 'none';
            progressQuestions.style.display = 'none';
            button.style.display = 'flex';

            fetch('end_interview/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) throw new Error(data.error);
                questionText.innerHTML = `Собеседование завершено. Ваши ответы сохранены, предварительные шансы попадания на очное собеседование - ${data.score_percentage}%.<br>После полной обработки мы свяжемся с вами по email.`;
            })
            .catch(error => {
                console.error('Analysis error:', error);
                alert('Analysis failed: ' + error.message);
            });

        } else {
            // Продолжаем собеседование
            questionText.textContent = data.question;
            textArea.value = '';
            progressQuestions.textContent = `Вопрос ${data.progress.current}`;
        }
    })
    .catch(error => alert('Ошибка: ' + error.message));
});

button.addEventListener('click', function() {



});