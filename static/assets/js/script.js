    
console.log("working fine");


const monthNames = [ "Jan", "Feb", "Mar", "April", "May", "June", "Juy", "Aug", "Sept", "Oct", "Nov", "Dec",];


$('#commentForm').submit(function(e){
    e.preventDefault();  

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + "," + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(), 
        method: $(this).attr("method"), 
        url: $(this).attr("action"),  
        dataType: "json", 
        
        success: function(response){
            console.log("Saved to the Db");

            if(response.bool == true){
                $("#review-resp").html("Review added successfully!") 
                $(".hide-comment-form").hide()

                let _html = '<div class="single-comment justify-content-between d-flex flex-column flex-sm-row mb-4 align-items-center">'

                _html += '<div class="thumb text-center mr-3 mb-3 mb-sm-0">'
                _html += '<img src="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-'
                _html += 'media-user-vector.jpg" alt="User Image" class="rounded-circle" width="50" height="50">'
                _html += '<a href="#" class="font-heading text-brand mt-2 d-block">' + response.context.user + '</a>'
                _html += '</div>'
                _html += '<div class="desc flex-grow-1">'
                                
                _html += '<div class="d-flex justify-content-between mb-2 align-items-center">'
                                    
                _html += '<div class="d-flex align-items-center mr-3">'
                _html += '<span class="text-muted">' + time + '</span>'
                _html += '</div>' 
                _html += '</div>'
                for(let i =1; i<=response.context.rating; i++){
                    
                    _html += '<i class ="fas fa-star text-warning"></i>'
                }
                  
                      
                _html += '<p class="mb-2">'
                _html += '<a href="#" class="reply text-decoration-none text-primary">Reply</a>'
                _html += '</p>'
                _html += '<p class="mb-0">' + response.context.review + ' </p>'

               
                _html +=  '</div> </div>'
                _html += '</div>'
                $(".comment-list").prepend(_html) 
            }
            
        }
    });
});



$(".add-to-cart-btn").on("click", function(){
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity  = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).val()

    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text()
    let product_pid = $(".product-pid-" + index).val()

    
    let product_image = $(".product-image-" + index).val()
    


    console.log("Quantity", quantity);
    console.log("Title", product_title);
    console.log("Price", product_price );
    console.log("Product ID", product_id);
    console.log("Product pid", product_pid);
    console.log("Product image", product_image);
    console.log("Current element", this_val);


    $.ajax({
        url: "/add-to-cart",
        data: {
            "id": product_id,
            "pid": product_pid,
            "image": product_image,
            "qty": quantity,
            "title": product_title,
            "price": product_price
        },
        dataType: "json",
        beforeSend: function(){
            console.log("Adding product to cart");
        },
        success: function(response){
            this_val.html("✔️")
            console.log("Added product to cart...");
            $(".cart-items-count").text(response.totalcartitems)

        }

    })
})
    


$(".delete-product").on("click", function() {
    let product_id = $(this).attr("data-product");  // Get the product ID from the button's data attribute
    let this_val = $(this);  // Reference to the clicked button
    console.log("product_id", product_id);  // For debugging

    // Confirm if the user wants to delete the item
    if (!confirm("Are you sure you want to remove this product from your cart?")) {
        return;  // Exit if the user cancels
    }

    $.ajax({
        url: "/delete-from-cart",  // URL for the delete request
        data: {"id": product_id},  // Send the product ID in the request
        dataType: "json",  // Expect a JSON response
        beforeSend: function() {
            this_val.hide();  // Hide the button while the request is being processed
        },
        success: function(response) {
            this_val.show();  // Show the delete button again after the request succeeds

            if (response.error) {
                // Handle any errors returned from the server
                alert(response.error);
                return;
            }

            // Update the cart item count and total amount
            $(".cart-items-count").text(response.totalcartitems);  // Update the cart item count
            $(".cart-total-amount").text("Ksh " + response.cart_total_amount.toFixed(2));  // Update the total amount

            // Update the cart items list with the returned HTML
            $("#cart-list").html(response.data);

            // Optionally, you can add logic to hide the cart container if it becomes empty
            if (response.totalcartitems === 0) {
                $("#cart-container").hide();  // Hide the cart container if empty
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);  // Log any error
            this_val.show();  // Ensure the button is shown again in case of error
            alert("An error occurred while deleting the product. Please try again.");
        }
    });
});



$(".update-product").on("click", function() {
    let product_id = $(this).attr("data-product"); 
    let this_val = $(this); 
    let product_quantity = $(".product-qty-"+product_id ).val()
    console.log("product_id", product_id);  
    console.log("product_qty", product_quantity);  

    $.ajax({
        url: "/update-cart", 
        data: {
            "id": product_id,
            "qty":product_quantity, 

        }, 
        dataType: "json",  
        beforeSend: function() {
            this_val.hide(); 
        },
        success: function(response) {
            this_val.show();  

            if (response.error) {
                
                alert(response.error);
                return;
            }

            // Update the cart item count and total amount
            $(".cart-items-count").text(response.totalcartitems);  // Update the cart item count
            $(".cart-total-amount").text("Ksh " + response.cart_total_amount.toFixed(2));  // Update the total amount

            // Update the cart items list with the returned HTML
            $("#cart-list").html(response.data);

            // Optionally, you can add logic to hide the cart container if it becomes empty
            if (response.totalcartitems === 0) {
                $("#cart-container").hide();  // Hide the cart container if empty
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);  // Log any error
            this_val.show();  
            alert("An error occurred while updating the product. Please try again.");
        }
    });
});


    



    // $(document).ready(function () {
        
    //     $(document).on("click", ".filter-checkbox", function() {
    //         console.log("A checkbox has been clicked");
    
    //         let filter_object = {};
    
    //         $(".filter-checkbox").each(function() {
    //             let filter_value = $(this).val();
    //             let filter_key = $(this).data("filter");
    
    //             console.log("filter key:", filter_key, "filter value:", filter_value);
    
               
    //             filter_object[filter_key] = Array.from(
    //                 document.querySelectorAll(`input[data-filter='${filter_key}']:checked`)
    //             ).map(function(element) {
    //                 return element.value;
    //             });
    //         });
    
    //         console.log("filter_object:", filter_object);
    
           
    //         $.ajax({
    //             url: "/filter-product",
    //             data: filter_object,
    //             dataType: "json",
    //             beforeSend: function() {
    //                 console.log("sending data.....");
    //             },
    //             success: function(response) {
    //                 console.log(response); 
    //                 $(".filtered-product").html(response.data); 
    //             }
    //         });
    //     });
    // });





   



    


