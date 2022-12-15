document.addEventListener('DOMContentLoaded', function() {
    load_posts()
    function load_posts() {
        document.querySelector("#posts").innerHTML = '';
        fetch('/posts')
        .then(response => response.json())
        .then(posts =>
            {
                posts.forEach(post => {
                    const element = document.createElement('div');
                    element.classList.add('row', 'border', 'border-2', 'rounded', 'p-2', 'm-2');
                    element.innerHTML = post.content;
                    document.querySelector("#posts").appendChild(element);
                })
            })
        

    }
})