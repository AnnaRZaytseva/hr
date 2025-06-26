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

// Р”Р°РЅРЅС‹Рµ Рѕ РІР°РєР°РЅСЃРёСЏС… РІСЂРµРјРµРЅРЅРѕ РґР»СЏ С‚РµСЃС‚Р° С„СѓРЅРєС†РёРѕРЅР°Р»Р°
const vacancies = {
    'frontend': {
        title: 'Frontend СЂР°Р·СЂР°Р±РѕС‚С‡РёРє',
        description: 'РњС‹ РёС‰РµРј С„СЂРѕРЅС‚РµРЅРґ-СЂР°Р·СЂР°Р±РѕС‚С‡РёРєР° СЃ РѕРїС‹С‚РѕРј СЂР°Р±РѕС‚С‹ СЃ React РѕС‚ 2 Р»РµС‚. РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ РЅР°РІС‹РєРё: JavaScript, React, Redux, HTML/CSS, СЂР°Р±РѕС‚Р° СЃ REST API.',
        questions: [
            'Р Р°СЃСЃРєР°Р¶РёС‚Рµ Рѕ СЃРІРѕРµРј РѕРїС‹С‚Рµ СЂР°Р±РѕС‚С‹ СЃ React. РљР°РєРёРµ РїСЂРѕРµРєС‚С‹ РІС‹ СЂР°Р·СЂР°Р±Р°С‚С‹РІР°Р»Рё?',
            'РљР°Рє РІС‹ РѕСЂРіР°РЅРёР·СѓРµС‚Рµ СѓРїСЂР°РІР»РµРЅРёРµ СЃРѕСЃС‚РѕСЏРЅРёРµРј РІ React-РїСЂРёР»РѕР¶РµРЅРёРё?',
            'РћРїРёС€РёС‚Рµ РїСЂРѕС†РµСЃСЃ РѕРїС‚РёРјРёР·Р°С†РёРё РїСЂРѕРёР·РІРѕРґРёС‚РµР»СЊРЅРѕСЃС‚Рё React-РїСЂРёР»РѕР¶РµРЅРёСЏ.']
    },
    'backend': {
        title: 'Backend СЂР°Р·СЂР°Р±РѕС‚С‡РёРє',
        description: 'РўСЂРµР±СѓРµС‚СЃСЏ Р±СЌРєРµРЅРґ-СЂР°Р·СЂР°Р±РѕС‚С‡РёРє СЃ РѕРїС‹С‚РѕРј СЂР°Р±РѕС‚С‹ СЃ Node.js РѕС‚ 3 Р»РµС‚. Р—РЅР°РЅРёРµ SQL/NoSQL Р±Р°Р· РґР°РЅРЅС‹С…, Docker, РјРёРєСЂРѕСЃРµСЂРІРёСЃРЅРѕР№ Р°СЂС…РёС‚РµРєС‚СѓСЂС‹.',

    }
}


//РЅР°С‡Р°Р»СЊРЅРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ СЃС‚СЂР°РЅРёС†С‹
let currentVacancy = null;
questionContainer.style.opacity =0;
let currentQuestionIndex = 0;
let answers = Array(3).fill('');



//РѕР±СЂР°Р±Р°С‚С‹РІР°СЋ РІС‹Р±РѕСЂ РІР°РєР°РЅСЃРёРё
vacancySelect.addEventListener('change', function() {
    const selectedValue = this.value; //РІС‹Р±СЂР°РЅРЅР°СЏ РІР°РєР°РЅСЃРёСЏ СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ
    startInterviewBtn.disabled = !selectedValue; //РµСЃР»Рё РЅРµ РІС‹Р±СЂР°РЅР° С‚Рѕ РєРЅРѕРїРєР° РЅРµ РґРѕСЃС‚СѓРїРЅР° РґР»СЏ РЅР°Р¶Р°С‚РёСЏ

    if (selectedValue) {
        currentVacancy = selectedValue;
        vacancyTitle.textContent = vacancies[selectedValue].title;
        vacancyDescription.textContent = vacancies[selectedValue].description;
        //РµСЃР»Рё РІС‹Р±СЂР°РЅР°, С‚Рѕ С‚РµРєСѓС‰Р°СЏ РІР°РєР°РЅСЃРёСЏ=РІС‹Р±СЂР°РЅРЅР°СЏ РІР°РєР°РЅСЃРёСЏ, Р·Р°РіРѕР»РѕРІРєСѓ РІР°РєР°РЅСЃРёРё РїСЂРёСЃРІР°РёРІР°РµС‚СЃСЏ РЅР°Р·РІР°РЅРёРµ РёР· РјР°СЃСЃРёРІР° РІР°РєР°РЅСЃРёР№ Рё РѕРїРёСЃР°РЅРёРµ
        progressFill.style.width = "33%";
        stepNumber1.style.backgroundColor ="#e5937d";
        stepText1.style.fontSize = "20px";


    } else {
        vacancyTitle.textContent = 'РќРµ РІС‹Р±СЂР°РЅРѕ';
        vacancyDescription.textContent = 'РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РІС‹Р±РµСЂРёС‚Рµ РІР°РєР°РЅСЃРёСЋ РёР· СЃРїРёСЃРєР° СЃРїСЂР°РІР°, С‡С‚РѕР±С‹ РЅР°С‡Р°С‚СЊ СЃРѕР±РµСЃРµРґРѕРІР°РЅРёРµ.';
        progressFill.style.width = "0%";
        stepNumber1.style.backgroundColor ="#9d82f1";
        stepText1.style.fontSize = "18px";
    }
});


//РЅР°С‡Р°Р»Рѕ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ
startInterviewBtn.addEventListener('click', function() {
    if (!vacancies[currentVacancy].questions || vacancies[currentVacancy].questions.length === 0) {
        alert('Р”Р»СЏ РІС‹Р±СЂР°РЅРЅРѕР№ РІР°РєР°РЅСЃРёРё РЅРµС‚ РІРѕРїСЂРѕСЃРѕРІ');
        return;
    }
    vacancySelection.style.display = 'none';
    questionContainer.style.display = 'block';
    progressText.textContent= 'С€Р°Рі 2 РёР· 3';
    progressFill.style.width = "66%";



    // Р—Р°РіСЂСѓР¶Р°СЋ РїРµСЂРІС‹Р№ РІРѕРїСЂРѕСЃ
    currentQuestionIndex = 0;
    questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
    progressQuestions.textContent = `Р’РѕРїСЂРѕСЃ ${currentQuestionIndex + 1} РёР· ${vacancies[currentVacancy].questions.length}`;


    // РђРЅРёРјР°С†РёСЏ РїРѕСЏРІР»РµРЅРёСЏ
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
        progressQuestions.textContent = `Р’РѕРїСЂРѕСЃ ${currentQuestionIndex + 1} РёР· ${vacancies[currentVacancy].questions.length}`;
    }
    updateFinishButton();
});

nextBtn.addEventListener('click', function(){

    if (currentQuestionIndex < vacancies[currentVacancy].questions.length - 1) {
        currentQuestionIndex += 1;
        textarea.value= answers[currentQuestionIndex];
        questionText.textContent = vacancies[currentVacancy].questions[currentQuestionIndex];
        progressQuestions.textContent = `Р’РѕРїСЂРѕСЃ ${currentQuestionIndex + 1} РёР· ${vacancies[currentVacancy].questions.length}`;
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







