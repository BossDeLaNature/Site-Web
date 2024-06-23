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

    function Ajoutquestion(pas) {
      currentQuestionIndex = pas;
      showQuestion(pas);
    }


    // Fonction pour afficher une question
    function showQuestion(index) {
        const quizContainer = document.getElementById('quiz-container');
        quizContainer.innerHTML = ''; // Vider le contenu précédent

        const questionNumber = document.createElement('h5');
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
      imageContainer.innerHTML = '<button type="button"  data-bs-toggle="modal" data-bs-target="#exampleModal" data-whatever="@mdo"> <img src="'.concat(imagesource,'" class="w-100" alt="Responsive image"/> </button>');
      const modalContainer = document.getElementById('modal-container');
      modalContainer.innerHTML = '<img src="'.concat(imagesource,'" class="img-fluid" alt="Responsive image"/>');
      const reponseContainer = document.getElementById('reponse-container');
      reponseContainer.innerHTML = '';
      const refContainer = document.getElementById(ref-container);
      refContainer.innerHTML = quizData[currentQuestionIndex]['Reference'];


        if (selectedAnswer === correctAnswer) {
          var audio = new Audio('media/sound/Correct.mp3');
          audio.play();
          reponseContainer.innerHTML = 'Correct :) Justification : '.concat(justification);
        } else {
          var audio = new Audio('media/sound/Wrong.mp3');
          audio.play();
          reponseContainer.innerHTML = 'Dommage :( Justification : '.concat(justification);
        }
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    }


    //Menu déroulant
    function Menuderoulant(){
      let diviseur = 0;
      for (diviseur; diviseur < Math.floor(quizData.length-1/10);diviseur++){
        const ligne = document.createElement('row');
        for (let pas = 0; pas < 10; pas++) {
          const quizContainer = document.getElementById('menu-container');
          const choixButton = document.createElement('button');
          choixButton.className = 'btn btn-success'
          choixButton.textContent = 'Question '.concat(quizData[pas]['Numero'].toString());
          choixButton.addEventListener('click', () => Ajoutquestion(pas));
          ligne.appendChild(choixButton);
        }
        quizContainer.appendChild(ligne);
      }
      for (let pas = 0; pas <quizData.length%10 ; pas++) {
        const quizContainer = document.getElementById('menu-container');
        const choixButton = document.createElement('button');
        choixButton.className = 'btn btn-success'
        choixButton.textContent = 'Question '.concat(quizData[pas]['Numero'].toString());
        choixButton.addEventListener('click', () => Ajoutquestion(pas));
        ligne.appendChild(choixButton);
      }
    }

    document.addEventListener("DOMContentLoaded", Menuderoulant())

    // Gérer le bouton "Next Question"
    document.getElementById('next-question').addEventListener('click', () => {
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = ''; // Vider le contenu précédent
      const modalContainer = document.getElementById('modal-container');
      modalContainer.innerHTML = ''; // Vider le contenu précédent
      const reponseContainer = document.getElementById('reponse-container');
      reponseContainer.innerHTML = '';
      const refContainer = document.getElementById(ref-container);
      refContainer.innerHTML = '';

        currentQuestionIndex++;
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    });

    // Gérer le bouton "Previous Question"
    document.getElementById('previous-question').addEventListener('click', () => {
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = ''; // Vider le contenu précédent
      const modalContainer = document.getElementById('modal-container');
      modalContainer.innerHTML = ''; // Vider le contenu précédent
      const reponseContainer = document.getElementById('reponse-container');
      reponseContainer.innerHTML = '';
        currentQuestionIndex--;
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    });
