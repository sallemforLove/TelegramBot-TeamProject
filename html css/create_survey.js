document.addEventListener('DOMContentLoaded', function() {
    // Контейнер для всех вопросов
    const questionsContainer = document.getElementById('questions-container');
    
    // Кнопка добавления нового вопроса
    const addQuestionBtn = document.getElementById('add-question');
    
    // Обработчик для кнопки добавления вопроса
    addQuestionBtn.addEventListener('click', addNewQuestion);
    
    // Делегирование событий для кнопок удаления вопросов и добавления вариантов
    questionsContainer.addEventListener('click', function(e) {
        // Обработка клика по кнопке удаления варианта ответа
        if (e.target.classList.contains('delete-option')) {
            const optionBlock = e.target.closest('.option-block');
            const optionsContainer = optionBlock.parentElement;
            
            // Удаляем вариант, только если их больше 2
            if (optionsContainer.querySelectorAll('.option-block').length > 2) {
                optionBlock.remove();
            } else {
                alert('Должно быть хотя бы 2 варианта ответа');
            }
        }
        
        // Обработка клика по кнопке добавления варианта ответа
        if (e.target.classList.contains('add-option')) {
            const questionBlock = e.target.closest('.question-block');
            const optionsContainer = questionBlock.querySelector('.options-container');
            addNewOption(optionsContainer);
        }
    });
    
    // Функция добавления нового вопроса
    function addNewQuestion() {
        const questionBlock = document.createElement('div');
        questionBlock.className = 'question-block';
        
        questionBlock.innerHTML = `
            <div>
                <label>Вопрос:</label>
                <input type="text" class="question-input" required>
            </div>
            
            <div class="options-container">
                <div class="option-block">
                    <input type="text" placeholder="Вариант ответа" required>
                    <button class="delete-option">Удалить</button>
                </div>
                <div class="option-block">
                    <input type="text" placeholder="Вариант ответа" required>
                    <button class="delete-option">Удалить</button>
                </div>
            </div>
            
            <button class="add-option">+ Добавить вариант</button>
        `;
        
        questionsContainer.appendChild(questionBlock);
    }
    
    // Функция добавления нового варианта ответа
    function addNewOption(optionsContainer) {
        const optionBlock = document.createElement('div');
        optionBlock.className = 'option-block';
        
        optionBlock.innerHTML = `
            <input type="text" placeholder="Вариант ответа" required>
            <button class="delete-option">Удалить</button>
        `;
        
        optionsContainer.appendChild(optionBlock);
    }
    
    // Обработчик для кнопки создания опроса
    const createSurveyBtn = document.getElementById('create-survey');
    createSurveyBtn.addEventListener('click', function() {
        const surveyTitle = document.getElementById('survey-title').value.trim();
        const questionBlocks = document.querySelectorAll('.question-block');
        
        // Валидация названия опроса
        if (!surveyTitle) {
            alert('Введите название опроса');
            return;
        }
        
        // Валидация вопросов
        if (questionBlocks.length === 0) {
            alert('Добавьте хотя бы один вопрос');
            return;
        }
        
        // Валидация каждого вопроса и вариантов ответа
        for (let i = 0; i < questionBlocks.length; i++) {
            const questionInput = questionBlocks[i].querySelector('.question-input');
            const optionInputs = questionBlocks[i].querySelectorAll('.options-container input');
            
            if (!questionInput.value.trim()) {
                alert(`Введите текст вопроса #${i + 1}`);
                return;
            }
            
            // Проверка вариантов ответа
            const options = Array.from(optionInputs).map(input => input.value.trim());
            if (options.some(opt => !opt)) {
                alert(`Заполните все варианты ответа для вопроса #${i + 1}`);
                return;
            }
            
            // Проверка на уникальность вариантов
            const uniqueOptions = new Set(options);
            if (uniqueOptions.size !== options.length) {
                alert(`Уберите повторяющиеся варианты ответа в вопросе #${i + 1}`);
                return;
            }
        }
        
        // Если все проверки пройдены
        alert('Опрос успешно создан!');
        // Здесь можно добавить код для отправки данных на сервер
    });
});