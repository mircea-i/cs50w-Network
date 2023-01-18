var buttons = document.querySelectorAll('.btn-light');
for (const button of buttons) {
    button.addEventListener('click', () => edit(button.dataset.value))
}
function edit(post) {

    const old_text = document.querySelector(`#post${post}`);

    // Create textarea for editing content and give it value
    const new_text = document.createElement('textarea');
    new_text.style.width = 'auto';
    new_text.cols = 75;
    new_text.rows = 3;
    new_text.innerHTML = old_text.innerHTML;
    new_text.classList.add('form-control');
    new_text.setAttribute('id', `new_post${post}`)

    // Replace post div with the textarea
    old_text.parentNode.replaceChild(new_text, old_text);

    // Create save button and replace edit with save
    edit_button = document.querySelector(`#button${post}`)
    const save_button = document.createElement('button');
    save_button.classList.add('btn', 'btn-success', 'btn-sm', 'align-self-end');
    save_button.setAttribute('id', `save${post}`)
    save_button.innerHTML = 'Save';
    edit_button.parentNode.replaceChild(save_button, edit_button);

    // Add listener to the new save button
    save_button.addEventListener('click', () => save(post))

    }

function save(post) {
    const post_content = document.querySelector(`#new_post${post}`).value;

    // POST new content to Django
    fetch (`/post/${post}`, {
        method: 'POST',
        headers: {'X-CSRFtoken': document.querySelector('[name=csrfmiddlewaretoken]').value},
        body: JSON.stringify({
            body: document.querySelector(`#new_post${post}`).value
        })
    })
    .then(response => console.log(response.json()))

    // Create edit button and replace save
    const save_button = document.querySelector(`#save${post}`);
    const edit_button = document.createElement('button');
    edit_button.classList.add('btn', 'btn-light', 'btn-sm', 'align-self-end');
    edit_button.setAttribute('id', `button${post}`);
    edit_button.setAttribute('data-value', `${post}`);
    edit_button.innerHTML = 'Edit';
    save_button.parentNode.replaceChild(edit_button, save_button);

    // Add event listener to the new edit button
    edit_button.addEventListener('click', () => edit(post));

    // Replace edit textarea with div
    const new_text = document.querySelector(`#new_post${post}`);
    const old_text = document.createElement('div');
    old_text.setAttribute('id', `post${post}`);
    old_text.innerHTML = post_content;
    new_text.parentNode.replaceChild(old_text, new_text);
    }