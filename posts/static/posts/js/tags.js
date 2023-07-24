
function TagClicked(tag_name, tag_group) {
    UpdateTagColor(tag_name);
    GetPostFilterData(tag_name);
}

function UpdateTagColor(tag) {
    const id_name = 'fake_tag_'.concat(tag);
    tag = document.getElementById(id_name);
    if (tag.classList.contains("nonactive_tag")) {
        tag.classList.remove('nonactive_tag');
        tag.classList.add('active_tag')
    } 
    
}

function GetPostFilterData(tag) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: 'posts/ajax-filter-call',
        type: 'POST',
        data: { tag: tag},
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