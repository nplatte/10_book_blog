
function TagClicked(tag_name, tag_group) {
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: 'posts/ajax-filter-call',
        type: 'POST',
        data: { tag: [tag_name, tag_group]},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (response){
            console.log('success');
            console.log(response);
        },
        error: function (xhr, textStatus, error) {
            console.log(error);
        }
    })
}