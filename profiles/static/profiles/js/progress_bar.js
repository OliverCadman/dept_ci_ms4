$(document).ready(function() {
    fillProgressBar();

    function fillProgressBar(){
        const progressBar = document.getElementById("progress_bar_inner");
        const progressData = progressBar.getAttribute("data-progress");

        if (typeof(progressData) !== "undefined") {
            progressBar.style.width = `${progressData}%`;
            progressBar.style.height = "10px"
            progressBar.style.backgroundColor = "blue";
        }
    }
})