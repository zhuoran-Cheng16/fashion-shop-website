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
        console.log('item_id:', item_id,  'action:', action)
        if(user === 'AnonymousUser'){
            console.log('AnonymousUser')
        }else{
            console.log('User logged in, sending data')
            updateUserOrder(item_id, action)
        }
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

function updateUserOrder(item_id, action){

    var url = '/fashionshop/update_item'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'item_id': item_id, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
