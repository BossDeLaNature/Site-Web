let quizData = []; // Tableau pour stocker les questions du quiz
let currentQuestionIndex = 0; // Index de la question actuelle
// Charger les données JSON
fetch('Excel/Question-Chapitre-II.json')
    .then(response => response.json())
    .then(data => {
        quizData = data;
        showQuestion(currentQuestionIndex);
    })
    .catch(error => console.error('Erreur:', error));

    // Fonction pour afficher une question
    function showQuestion(index) {
        const quizContainer = document.getElementById('quiz-container');
        quizContainer.innerHTML = ''; // Vider le contenu précédent

        const questionNumber = document.createElement('h3');
        questionNumber.textContent = `Question ${quizData[index]['Numero']} (${quizData[index]['Question']})`;
        quizContainer.appendChild(questionNumber);

        const question = document.createElement('h2');
        question.textContent = quizData[index]['Proposition'];
        quizContainer.appendChild(question);

        const trueButton = document.createElement('button');
        trueButton.className = 'btn btn-success'
        trueButton.textContent = 'Vrai';
        trueButton.addEventListener('click', () => checkAnswer(true, quizData[index]['Reponse'], quizData[index]['Justification']));
        quizContainer.appendChild(trueButton);

        const falseButton = document.createElement('button');
        falseButton.className = 'btn btn-danger'
        falseButton.textContent = 'Faux';
        falseButton.addEventListener('click', () => checkAnswer(false, quizData[index]['Reponse'], quizData[index]['Justification']));
        quizContainer.appendChild(falseButton);
    }

    // Fonction pour vérifier la réponse
    function checkAnswer(selectedAnswer, correctAnswer, justification) {
      let numeroquestion = quizData[currentQuestionIndex]['Numero'].toString();
      let imagesource = 'media/dias/'.concat(numeroquestion, '.png')
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = '<button type="button"  data-bs-toggle="modal" data-bs-target="#exampleModal" data-whatever="@mdo"> <img src="media/dias/1.png" class="w-100" alt="Responsive image"/> </button>';
        if (selectedAnswer === correctAnswer) {
            alert(`Correct! Justification: ${justification}`);
        } else {
            alert(`Faux! Justification: ${justification}`);
        }
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    }


    // Gérer le bouton "Next Question"
    document.getElementById('next-question').addEventListener('click', () => {
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = ''; // Vider le contenu précédent

        currentQuestionIndex++;
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    });
