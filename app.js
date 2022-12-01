const submit = document.querySelector('button');

const stock = {};

function onSubmit(event){
    let stock_name = document.querySelector('#stock_name').value;
    let stock_quantity = document.querySelector('#stock_quantity').value;
    stock[stock_name] = stock_quantity;
    document.querySelector('#output').innerHTML = "";
    for (var key in stock){
        document.querySelector('#output').innerHTML += "<li>"+key+": "+stock[key]+"</li>";
    }
    
}

submit.addEventListener('click', onSubmit);