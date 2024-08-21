
function deleteAddress(id, rowName) {
    if (confirm("Are you sure you want to delete " + rowName)) {
        // if user says yes to confirm

        // post id of row in database so can be removed from database
        $.ajax({ 
            url: '/addressDelete', 
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(id), 
        
        // if successfully posted, reload page to show changes
        success: function(response) {
            location.reload();
        },
        error: function(error) { 
            alert(error); 
        } 
        });
    }

    // other error just pass
    else {
        pass
    }
}

// basket 
function addToBasket(itemID, itemName, itemCost) {
    let quantity = parseInt(prompt("Please enter the quantity"), 10);
    // check it is not null and is a int
    if (quantity != null && Number.isInteger(quantity) == true) {
        // post id of row in database so can be removed from database
        $.ajax({ 
            url: '/addToBasket', 
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify({"itemID": itemID, "itemQuantity": quantity, "itemName": itemName, "itemCost": itemCost}), 
        
        // if successfully posted, reload icon to show basket number
        success: function(response) {
            location.reload();
            alert(response);
        },
        error: function(error) { 
            alert(error); 
        } 
        });
    }

    else {
        alert("Cancelled / enter a valid number");
    }
}

function deleteBasketItem(id, rowName) {
    if (confirm("Are you sure you want to delete " + rowName)) {
        // if user says yes to confirm

        // post id of row in database so can be removed from database
        $.ajax({ 
            url: '/basketDelete', 
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(id), 
        
        // if successfully posted, reload page to show changes
        success: function(response) {
            location.reload();
        },
        error: function(error) { 
            alert(error); 
        } 
        });
    }

    // other error just pass
    else {
        pass
    }
}

function checkout(totalNumOfRows) {
    // if nothing in basket then cant checkout
    if (totalNumOfRows == 0) {
        alert("No items in basket, cannot checkout")
    }
    // show checkout page
    else {
        window.location.href = "/checkout"
    }
}

function checkoutAddress(addressID) {
    // when select button is clicked post id to python
    $.ajax({ 
        url: '/checkoutFinalised', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify(addressID), 
    
    // if successfully posted, go to orders page
    success: function(response) {
        window.location.href = "/orders"
    },
    error: function(error) { 
        alert(error); 
    } 
    });
}


// advanced feature
// products search by tags
$(document).ready(function(){
    var tags=[];
    
    function getTags(){
        // get all the tags from database
        $.getJSON('/tags', function(data, status, xhr){
            // add them all to the array
            for (var i = 0; i < data.length; i++ ) {
                tags.push(data[i].tagName);
            }
    });
    };
    
    // call get tags
    getTags();
    
    // autocomplete the search box
    $('#productTag').autocomplete({
        source: tags, 
        });
    });


    