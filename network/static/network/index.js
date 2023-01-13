
function add_post() {     
    fetch('/new_post', {
        method: 'POST',
        // Attach the CSRF token to the request
        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
        // Put the post content in the request
        body: JSON.stringify({content: document.querySelector('#post-content').value})
        
    })
        .then(response => load_posts())
        
 
    }

    
function load_posts() {
    document.querySelector("#posts").innerHTML = '';
    fetch('/posts')
    .then(response => response.json())
    .then(posts =>
        {
            posts.forEach(post => {
                const element = document.createElement('div');
                element.classList.add('row', 'border', 'border-2', 'rounded', 'p-2', 'm-2');
                element.innerHTML = `
                    <div class='col'>${post.owner}</div>
                    <div class='col'>${post.content}</div>
                    <div class='col'>${post.creation}</div>`
                document.querySelector("#posts").appendChild(element);
            })
        })
    }
