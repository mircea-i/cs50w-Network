document.addEventListener('DOMContentLoaded', function() {
    if (auth === true) {
    document.querySelector('#new-post').addEventListener('submit', event => {
        event.preventDefault();
        new_post();
        })
    }
    //load_posts();


    function new_post() {
        
        fetch('/new_post', {
            method: 'POST',

            // Attach the CSRF token to the request
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },

            // Put the post content in the request
            body: JSON.stringify({
                content: document.querySelector('#post-content').value
            })
        })
        .then(document.querySelector('#post-content').value = '')
        then(response => load_posts())
        console.log('posted')
    }

    
})