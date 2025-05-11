function selectOption(option) {
    if (option.classList.contains("selected")) {
        // If the option is already selected, deselect it
        option.classList.remove("selected");
        return;
    }
    // Deselect all options
    document.getElementById("optionA").classList.remove("selected");
    document.getElementById("optionB").classList.remove("selected");
    document.getElementById("optionC").classList.remove("selected");
    document.getElementById("optionD").classList.remove("selected");
    // Select the clicked option
    option.classList.add("selected");
}

function getQuestions() {
    fetch("/api/getAllQuestions")
        .then(response => response.json())
        .then(data => {
            data.forEach(question => {
                console.log(question);
            });
        })
        .catch(error => console.error('Error fetching questions:', error));
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("optionA").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionB").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionC").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionD").addEventListener("click", function () {
        selectOption(this);
    });
  });
  getQuestions();
