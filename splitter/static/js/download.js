document.addEventListener('DOMContentLoaded', function () {
    var downloadButton = document.getElementById('downloadBtn');
    var folder_name = document.body.getAttribute('data-id');
    downloadButton.addEventListener('click', function() {
            // document.getElementById('top-label').textContent = folder_name
            fetch("/download_file/", {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({'folder_name': folder_name})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = folder_name + '.zip'; // or any other name you want
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                location.href = '/'
            })
            .catch(error => console.error(error))
        });
    }
)


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie contains the CSRF token
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}