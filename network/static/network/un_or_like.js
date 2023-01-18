function un_or_like(post) {

    fetch (`/un_or_like/${post}`, {
        method: 'POST',
        headers: {'X-CSRFtoken': document.querySelector('[name=csrfmiddlewaretoken]').value},
        body: JSON.stringify({
            content: post
        })
    })
    .then((response) => {

        if(response.ok) {

            response.json().then(data => {

            const button = document.querySelector(`#like${post}`);

            if (button.classList.contains('btn-success')) {
                button.classList.remove('btn-success', 'fa-thumbs-up');
                button.classList.add('btn-danger', 'fa-thumbs-down');
                document.getElementById(`likes${post}`).innerHTML = `x ${data.data}`;
            }
            else {
                button.classList.remove('btn-danger','fa-thumbs-down');
                button.classList.add('btn-success', 'fa-thumbs-up');
                document.getElementById(`likes${post}`).innerHTML = `x ${data.data}`;
            }
        })
    }              
    })
}