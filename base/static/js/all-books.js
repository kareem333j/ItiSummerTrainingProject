let table_body = document.querySelector('table tbody');
let search = document.querySelector('.search');
var deleteBtn = document.querySelectorAll('.delete-book-btn');
var borrowBtn = document.querySelectorAll('.borrow-btn');
var returnBtn = document.querySelectorAll('.return-btn');
var infoBtn = document.querySelectorAll('.btn-info');


search.addEventListener('input', (e)=>{
    var text = e.target.value;
    let text_without_spacing = text.replace(/\s+/g, '');
    var value = text;

    if (text_without_spacing === '') {
        value = null;
    }
    const url = `/books/search/books/${value}`

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
                td.innerHTML = `<img  width="50px" src='${ list[i][key]}' alt='book_image'>`;
            }else{
                if(key == 'author'){
                    td.innerHTML = `@${list[i][key]}`;
                }
                else if(key == 'stock'){
                    td.innerHTML = `x${list[i][key]}`;
                }
                else{
                    td.innerHTML = list[i][key];
                }
            }
            if(key != 'borrowed'){
                if(parseInt(list[i]['stock']) <= parseInt(0)){
                    tr.className = 'table-row zero';
                }else{
                    tr.className = 'table-row';
                }
                tr.appendChild(td);
            }
        }
        let td = document.createElement('td');
        if(user_is_superuser != 'True'){
            if(list[i]['borrowed'] == true){
                td.innerHTML = `
                    <div class="d-flex gap-1">
                        <button style="width: 80px;" data-book="${list[i].id}" class="btn btn-outline-info return-btn">return</button>
                        <a class="btn btn-info" href="/books/all/${list[i].id}/info"><i class="fa-solid fa-circle-info"></i></a>
                    </div>
                `
            }else{
                if(parseInt(list[i]['stock']) <= parseInt(0)){
                    td.innerHTML = `
                        <div class="d-flex gap-1">
                            <button style="width: 80px;cursor:no-drop" class="btn btn-secondary">finished</button>
                            <a class="btn btn-info" href="/books/all/${list[i].id}/info"><i class="fa-solid fa-circle-info"></i></a>
                        </div>
                    `
                }
                else{
                    td.innerHTML = `
                        <div class="d-flex gap-1">
                            <button style="width: 80px;" data-book="${list[i].id}" class="btn btn-outline-info borrow-btn">borrow</button>
                            <a class="btn btn-info" href="/books/all/${list[i].id}/info"><i class="fa-solid fa-circle-info"></i></a>
                        </div>
                    `
                }
            }
        }else{
            td.innerHTML = `
                <div class="d-flex gap-1">
                    <a class="btn btn-primary" href="/books/${list[i].id}/edit"><i class="fa-solid fa-pen-to-square"></i></a>
                    <button data-book="${list[i].id}" class="btn btn-danger delete-book-btn" href="#"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
        }

        
        tr.appendChild(td);
        table_body.appendChild(tr);
    }

    deleteBtn = document.querySelectorAll('.delete-book-btn');
    borrowBtn = document.querySelectorAll('.borrow-btn');
    returnBtn = document.querySelectorAll('.return-btn');
    actions();
}

actions();
