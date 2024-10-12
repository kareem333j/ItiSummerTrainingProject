let table_body = document.querySelector('table tbody');
let search = document.querySelector('.search');
// var returnBtn = document.querySelectorAll('.return-btn');

search.addEventListener('input', (e)=>{
    var text = e.target.value;
    let text_without_spacing = text.replace(/\s+/g, '');
    var value = text;

    if (text_without_spacing === '') {
        value = null;
    }
    const url = `/books/search/borrows/${value}`

    fetch(url)
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        handel_books(data.books);
    })
    .catch((err)=>{
        console.log(err);
    });
});

const handel_books = (list)=>{
    let table_rows = document.querySelectorAll('table .table-row');
    [...table_rows].map((e)=>{
        e.remove();
    });

    for(let i=0; i<list.length; i++){
        let tr = document.createElement('tr');
        for(let key in list[i]){
            let td = document.createElement('td')
            if(key == 'image'){
                td.innerHTML = `<img  width="50px" src='${list[i][key]}' alt='book_image'>`;
            }else{
                if(key == 'user'){
                    if(user_is_superuser == 'True'){
                        td.innerHTML = `<a href="/profile/${list[i].user_id}" class="text-light text-decoration-none">@${list[i][key]}</a>`;
                    }else{
                        td.innerHTML = `<button style="width: 80px;" data-book="${list[i].id}" class="btn btn-outline-info return-btn">return</button>`
                    }
                }
                else if(key == 'borrowed_dt'){
                    td.innerHTML = dateFormatter(list[i][key]);
                }
                else{
                    td.innerHTML = list[i][key];
                }
            }
            if(key != 'user_id'){
                tr.className = 'table-row';
                tr.appendChild(td);
            }
        }
        table_body.appendChild(tr);
    }


    returnBtn = document.querySelectorAll('.return-btn');
    actions();
}

actions();