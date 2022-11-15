document.addEventListener('DOMContentLoaded', function() {

    // Edit post and toggle like
    document.addEventListener('click', event => {
        element = event.target;

        if (element.id.startsWith('edit-')) {
            let postId = element.dataset.id;
            let post = document.querySelector(`#post-${postId}`);
            let postDetails = document.querySelector(`#post-details-${postId}`);
            let postContent = document.querySelector(`#post-content-${postId}`);

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

       if (element.id.startsWith('heart-')) {
            let postId = element.dataset.id;
            let fan = document.querySelector(`.fan-${postId}`);

            // Update fan list
            fetch(`/toggle_like/${postId}`, {
                method: 'PUT'
            })
            .then (function (response) {
                if (response.status == 204) {
                    if (element.dataset.action == "like") {
                        totalFan = parseInt(fan.textContent);
                        fan.innerHTML = '';
                        fan.innerHTML = `
                            <i class="bi bi-heart-fill" id="heart-fill" data-id="${postId}" data-action="unlike"></i> ${totalFan + 1}
                        `;
                    }
                    if (element.dataset.action == "unlike") {
                        totalFan = parseInt(fan.textContent);
                        fan.innerHTML = '';
                        fan.innerHTML = `
                            <i class="bi bi-heart" id="heart-empty" data-id="${postId}" data-action="like"></i> ${totalFan - 1}
                        `;
                    }
                }
            })
       }

    })

});
