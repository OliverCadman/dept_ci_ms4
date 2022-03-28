$(document).ready(function() {
    /*
        Fills the Dashboard Landing Page's
        progress bar with a visual indicator of
        a user's progress.

        Gets progress percentage through data attribute
        of progress bar element in DOM.
    */
    fillProgressBar();

    function fillProgressBar(){
        /*
        Get the progress bar along with it's data attribute,
        and set it's width to the percentage of profile completedness.
        */
        const progressBar = document.getElementById("progress_bar_inner");
        const progressData = progressBar.getAttribute("data-progress");

        if (typeof(progressData) !== "undefined") {
            progressBar.style.width = `${progressData}%`;
        }
    }
});