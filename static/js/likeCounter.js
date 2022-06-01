// с сайта djangoproject функция для взятия csrf токена т к у нас login required на view
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(".btn_like").on('click', function (ev) {
    console.log('liked');
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'question_id=' + $this.data('data-id'),
        }
    )
    fetch(request).then(function (response) {
        console.log("response");
    })
})

$(".btn_dislike").on('click', function (ev) {
    console.log('disliked');
})