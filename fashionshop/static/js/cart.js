function updateShipCheck(){
    var price = document.getElementById('shipping_price')
    var value = price.getAttribute("value")
    
    if (value === '0.0'){
        var checkelement = document.getElementById('customRadio3')
        checkelement.setAttribute("checked", true)
    }
    if (value === '4.99'){
        var checkelement = document.getElementById('customRadio1')
        checkelement.setAttribute("checked", true)
    }
    if (value === '1.99'){
        var checkelement = document.getElementById('customRadio2')
        checkelement.setAttribute("checked", true)
    }

}
var clear = document.getElementsByClassName('clear-cart')
for(var i = 0; i < clear.length; i++){
    clear[i].addEventListener("click", function(){
        console.log("clear cart")
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            clearCart()
        }
    })
}
function clearCart(){
    console.log('User logged in, clear cart')
    var url = '/fashionshop/clear_cart'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'clear': true})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

var ship_price = document.getElementsByClassName('custom-control-input')
for(var i = 0; i < ship_price.length; i++){
    ship_price[i].addEventListener("click",function(){
        var price = this.dataset.value
        console.log('price:', price)
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            updateShippingPrice(price)
        }
    })
}


var updateBtns = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var item_id = this.dataset.item
        var action = this.dataset.action
        var size = this.dataset.size
        console.log('item_id:', item_id,  'action:', action, 'size', size)
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            console.log('User logged in, sending data')
            console.log('test')
            updateUserOrder(item_id, action, size)
        }
    }) 
}

var updateBtns = document.getElementsByClassName('update-cart-main')
console.log(updateBtns)
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var item_id = this.dataset.item
        var size = this.dataset.size;
        
        console.log('test')
        console.log('item_id:', item_id, 'size', size)
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            console.log('User logged in, sending data')
            updateUserOrderMain(item_id, size)
        }
    }) 
}


var updateBtns = document.getElementsByClassName('update-cart-signle')
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var item_id = this.dataset.item
        var size = this.dataset.size
        var qty = this.dataset.num
        console.log('item_id:', item_id, 'size', size, 'qty', qty)
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            console.log('User logged in, sending data')
            updateUserOrderSignle(item_id, size, qty)
        }
    }) 
}

function updateUserOrderSignle(item_id, size, qty){
    var url = '/fashionshop/update_item_signle'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'item_id': item_id, 'size':size, 'qty': qty})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function updateShippingPrice(price){
    console.log('User logged in, sending data')
    var url = '/fashionshop/update_ship'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'price': price})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function updateUserOrder(item_id, action, size){

    var url = '/fashionshop/update_item'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'item_id': item_id, 'action':action, 'size':size})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function updateUserOrderMain(item_id, size){

    var url = '/fashionshop/update_item_main'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'item_id': item_id, 'size':size})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

