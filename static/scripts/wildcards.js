const wcFields = document.querySelectorAll('.wildcard')

wcFields.forEach(wcField => {
    const searchField = wcField.querySelector('.wildcard-pick input');
    const list = wcField.querySelector('.wildcard-dropdown-list');
    const imageField = wcField.querySelector('.wildcard-pick-image');
    const wcModel = wcField.dataset.model;
    const wcType = wcField.dataset.type;


    searchField.addEventListener('click', () => {
        list.classList.remove('hidden');
    })

    const options = list.querySelectorAll('.dropdown-item');

    searchField.addEventListener("input", () => {
        const value = searchField.value.toLowerCase();

        options.forEach(option => {
            const nameSpan = option.querySelector('span');
            const name = nameSpan.textContent.toLowerCase();
            option.style.display = name.startsWith(value) ? "flex": "none";
        })
    })


    options.forEach(option => {
        option.addEventListener('click', () => {
            const optionName = option.querySelector('span').textContent;
            const optionImgUrl = option.querySelector('img').src;
            searchField.value = optionName;

            imageField.innerHTML = '';
            const newImage = document.createElement('img');
            newImage.src = optionImgUrl;
            imageField.appendChild(newImage);
            list.classList.add('hidden');

            const predictStatusEls = wcField.querySelectorAll('.predict-status');
            predictStatusEls[0].classList.add('hidden');
            predictStatusEls[2].classList.add('hidden');
            predictStatusEls[1].classList.remove('hidden');

            fetch('/submit-wildcard/', {
                method: 'POST',
                header: {
                    'Content-Type': 'application/json',
                    'x-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    model: wcModel,
                    type: wcType,
                    option: optionName,
                })
            })
            .then(response => response.json())
            .then(data => {
                return new Promise(resolve => {
                    setTimeout(() => resolve(data), 500);
                })
            })
            .then(data => {
                if (data.success) {
                    predictStatusEls[1].classList.add('hidden');
                    predictStatusEls[2].classList.remove('hidden');
                } else {
                    alert('Error: ' + data.error);
                }
                
            })
        })
    })
})



function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
         }
      }
   }
   return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    Object.entries(userWildcards).forEach(([key, value]) => {
        if (!value) return; 
        const fields = document.querySelectorAll(`[data-model="${key}"]`)
        fields.forEach(field => {
            const input = field.querySelector('input');
            if (input) input.value = value.name;

            const imageField = field.querySelector('.wildcard-pick-image');
            if (imageField && value.img_url) {
                imageField.innerHTML = '';
                const img = document.createElement('img');
                img.src = value.img_url;
                img.alt = value.name;
                imageField.appendChild(img);
            }

            const endDate = new Date(2025, 5, 27, 22, 0, 0);
            const now = new Date();
            

            const predictStatusEls = field.querySelectorAll('.predict-status');
            predictStatusEls[0].classList.add('hidden');
            predictStatusEls[1].classList.add('hidden');
            predictStatusEls[2].classList.remove('hidden');
            if (now >= endDate) {
                input.disabled = true;

                predictStatusEls[2].classList.add('hidden');
                predictStatusEls[3].classList.remove('hidden');
            }
        })
    })
    const endDate = new Date(2025, 5, 27, 22, 0, 0);
    const now = new Date();

    if (now >= endDate) {
        const fields = document.querySelectorAll('.wildcard');
        
        fields.forEach(field => {
            const input = field.querySelector('input');
            input.disabled = true;

            const predictStatusEls = field.querySelectorAll('.predict-status');
            predictStatusEls[0].classList.add('hidden');
            predictStatusEls[1].classList.add('hidden');
            predictStatusEls[2].classList.add('hidden');
            predictStatusEls[3].classList.remove('hidden');
        })
    }
})