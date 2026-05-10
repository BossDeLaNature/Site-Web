let quizData = []; // Tableau pour stocker les questions du quiz
let currentQuestionIndex = 0; // Index de la question actuelle
// Charger les données JSON
fetch('Excel/digestif.json')
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
        trueButton.className = 'btn btn-success btn-lg'
        trueButton.textContent = 'Vrai';
        trueButton.addEventListener('click', () => checkAnswer(true, quizData[index]['Reponse'], quizData[index]['Justification']));
        quizContainer.appendChild(trueButton);

        const falseButton = document.createElement('button');
        falseButton.className = 'btn btn-danger btn-lg'
        falseButton.textContent = 'Faux';
        falseButton.addEventListener('click', () => checkAnswer(false, quizData[index]['Reponse'], quizData[index]['Justification']));
        quizContainer.appendChild(falseButton);
    }

    // Fonction pour vérifier la réponse
    function checkAnswer(selectedAnswer, correctAnswer, justification) {
      let numeroquestion = quizData[currentQuestionIndex]['Numero'].toString();
      let imagesource = 'media/dias/digestif/'.concat(numeroquestion, '.png')
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = '<button type="button"  data-bs-toggle="modal" data-bs-target="#exampleModal" data-whatever="@mdo"> <img src="'.concat(imagesource,'" class="w-100" alt="Responsive image"/> </button>');
      const modalContainer = document.getElementById('modal-container');
      modalContainer.innerHTML = '<img src="'.concat(imagesource,'" class="img-fluid" alt="Responsive image"/>');
      const reponseContainer = document.getElementById('reponse-container');
      reponseContainer.innerHTML = '';
      const justifContainer = document.getElementById('justif-container');
      justifContainer.innerHTML = '';
      const refContainer = document.getElementById('ref-container');
      refContainer.innerHTML = quizData[currentQuestionIndex]['Reference'];


        if (selectedAnswer === correctAnswer) {
          var audio = new Audio('media/sound/Correct.mp3');
          audio.play();
          const yihaa = document.createElement('h3');
          yihaa.textContent = 'Correct :)';
          reponseContainer.appendChild(yihaa);
          justifContainer.innerHTML = justification;
        } else {
          var audio = new Audio('media/sound/Wrong.mp3');
          audio.play();
          const yihaa = document.createElement('h3');
          yihaa.textContent = 'Dommage :(';
          reponseContainer.appendChild(yihaa);
          justifContainer.innerHTML = justification;
        }
        if (currentQuestionIndex < quizData.length) {
            showQuestion(currentQuestionIndex);
        } else {
            alert('Quiz terminé!');
        }
    }


    //Menu déroulant
    function Menuderoulant(){
      for (let pas = 0; pas <quizData.length ; pas++) {
        const menuContainer = document.getElementById('menu-container');
        const choixButton = document.createElement('button');
        choixButton.className = 'btn btn-success'
        choixButton.textContent = 'Question '.concat(quizData[pas]['Numero'].toString());
        choixButton.addEventListener('click', () => Ajoutquestion(pas));
        menuContainer.appendChild(choixButton);
      }
    };

    document.getElementById("dropdownMenuButton").addEventListener('click', () => {
      const menuContainer = document.getElementById('menu-container');
      menuContainer.innerHTML = '';
      Menuderoulant();

    });

    // Gérer le bouton "Next Question"
    document.getElementById('next-question').addEventListener('click', () => {
      const imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = ''; // Vider le contenu précédent
      const modalContainer = document.getElementById('modal-container');
      modalContainer.innerHTML = ''; // Vider le contenu précédent
      const reponseContainer = document.getElementById('reponse-container');
      reponseContainer.innerHTML = '';
      const refContainer = document.getElementById('ref-container');
      refContainer.innerHTML = '';
      const justifContainer = document.getElementById('justif-container');
      justifContainer.innerHTML = '';

        if (currentQuestionIndex+1 < quizData.length) {
          currentQuestionIndex++;
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
      const refContainer = document.getElementById('ref-container');
      refContainer.innerHTML = '';
      const justifContainer = document.getElementById('justif-container');
      justifContainer.innerHTML = '';
      if (currentQuestionIndex === 0){}
      else {
        currentQuestionIndex--;
      }
      if (currentQuestionIndex < quizData.length) {
          showQuestion(currentQuestionIndex);
      }

    });
