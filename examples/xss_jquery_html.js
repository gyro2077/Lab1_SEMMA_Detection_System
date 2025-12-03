// jQuery .html() XSS
$(document).ready(function() {
    const userInput = $('#commentBox').val();
    // VULNERABLE: Direct HTML insertion
    $('#comments').html('<p>' + userInput + '</p>');
});
