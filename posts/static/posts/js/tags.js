
function TagClicked(tag_name, tag_group) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: 'posts/ajax-filter-call',
        type: 'POST',
        data: { tag: tag_name},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (response){
            response = JSON.parse(response);
            const post_list = document.getElementById('post_list');
            var new_post_list = document.createElement('div');
            new_post_list.setAttribute('id', 'post_list');
            function addPost(new_post) {
                var new_post_element = document.createElement('a');
                new_post_element.setAttribute('class', 'post');
                new_post_element.textContent = 'test'
                new_post_list.appendChild(new_post_element);
            }
            response.forEach(addPost);
            post_list.replaceWith(new_post_list);
        },
        error: function (xhr, textStatus, error) {
            console.log('NAH');
        }
    })
}
