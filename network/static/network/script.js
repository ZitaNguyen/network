document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {

        if (event.target.id === 'edit') {
            let postId = document.querySelector('#edit').dataset.id;
            let post = document.querySelector('#post');
            let postDetails = document.querySelector(`#post-${postId}`);
            let postContent = document.querySelector('#post-content');

            // Add textarea to edit post
            let updateContent = document.createElement('textarea');
            updateContent.className = 'form-control';
            updateContent.innerHTML = postContent.innerHTML;
            postDetails.style.display = 'none';
            post.appendChild(updateContent);

            // Create save button
            let saveButton = document.createElement('button');
            saveButton.innerHTML = 'Save';
            post.appendChild(saveButton);
            saveButton.className = 'btn btn-primary mt-3';

            // Update post content when click Save
            saveButton.addEventListener('click', () => {
                fetch(`/edit_post/${postId}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: updateContent.value
                    })
                })
                .then (function (response) {
                    if (response.status == 204) {
                        post.removeChild(updateContent)
                        post.removeChild(saveButton)
                        postDetails.style.display = 'block';
                        postContent.innerHTML = updateContent.value;
                    }
                })
            })
       }
    })

});
