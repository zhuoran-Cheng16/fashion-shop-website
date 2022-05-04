function getList(id) {
    $.ajax({
        url: "/fashionshop/all_review/" + id,
        dataType: "json",
        success: updateList,
        error: updateError
    });
}

function getHighestRating(id) {
    console.log("enter rating")
    $.ajax({
        url: "/fashionshop/get-highest-rating/" + id,
        dataType: "json",
        success: updateList,
        error: updateError
    });
}

function getLowestRating(id) {
    $.ajax({
        url: "/fashionshop/get-lowest-rating/" + id,
        dataType: "json",
        success: updateList,
        error: updateError
    });
}

function getStarRating(id,rating_num) {
    $.ajax({
        url: "/fashionshop/get-star-rating/" + id+"/" + rating_num,
        dataType: "json",
        success: updateList,
        error: updateError
    });
}
function getPicture(id) {
    $.ajax({
        url: "/fashionshop/get-picture/" + id,
        dataType: "json",
        success: updateList,
        error: updateError
    });
}


function updateList(items) {
    console.log("Enter function updateList in JS")
   
    // Removes items from todolist if they not in items
        $("div").each(function() {
            if(this.id.startsWith("id_item_")){
                this.remove()
            }
        })
    let count = 0
    // Adds each new todolist item to the list (only if it's not already here)
    $(items).each(function () {
        let my_id = "id_item_" + this.id
        if (document.getElementById(my_id) == null) {
            count++;
            
            let info =  '<div class="comment-box" id="id_item_' + this.id + '">'
                + '<div id="textbox">'
                + '<p style= "font-weight:bold">'
                + this.review_title + ' - ' + this.nickname + '</p>'
                + '<p class="mb-0" style="font-weight:bold">'
                + this.time + '</p></div>'
                + ' <div id="textbox"> <p style = "font-weight:bold">'
                + this.rating + '</p>' 
            if (this.review_picture !=''){
                console.log("enter if loop")
                info+= '<a class="gallery_img" href="/static/review_images'+this.review_picture+ '" >'
                + ' <img class="img-thumbnail" alt="No Image" width="120" height="336" src= "/static/review_images'+this.review_picture+'" ></img></a>'
            }
              
            info+='</div>'
                + ' <p>' + this.review + '</p>'
                +'<hr class = "style-eight">'
                + '</div>'
            
            $("#todo-list").append(info)
            console.log(this.review_picture)
        }
    })
    $(document).ready(function(){

        $("#id_comment_entry_num").text(count +" entry(s) found.");
      
    });


}


function updateError(xhr) {

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    $("#error").html(message);
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
}
