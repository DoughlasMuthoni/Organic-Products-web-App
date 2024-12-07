    
    console.log("working fine");

    $("#comment-form").submit(function(e){
        e.preventDefault();  
    
        $.ajax({
            data: $(this).serialize(),  
            method: $(this).attr("method"),  
            url: $(this).attr("action"), 
            dataType: "json",  
    
            success: function(response) {
                console.log("comments saved in db");
    
               
                if (response.bool == true) {
                
                    $("#review-res").html("Review added successfully!!")
                    $(".hide-comment-form").hide()
                    
                    setTimeout(function() {
                        $("#review-res").fadeOut();
                    }, 7000);
    
                    $("#hide-comment-form").hide();
                }
            },
    
            error: function(xhr, status, error) {
                console.log("Error: " + error);
            }
        });
    });
    
    $(document).ready(function () {
        // Delegate click event to handle dynamically added checkboxes
        $(document).on("click", ".filter-checkbox", function() {
            console.log("A checkbox has been clicked");
    
            let filter_object = {};
    
            $(".filter-checkbox").each(function() {
                let filter_value = $(this).val();
                let filter_key = $(this).data("filter");
    
                // Log the filter values and keys to make sure they're correct
                console.log("filter key:", filter_key, "filter value:", filter_value);
    
                // Get the checked checkboxes for each filter
                filter_object[filter_key] = Array.from(
                    document.querySelectorAll(`input[data-filter='${filter_key}']:checked`)
                ).map(function(element) {
                    return element.value;
                });
            });
    
            console.log("filter_object:", filter_object);
    
            // Make the AJAX call
            $.ajax({
                url: "/filter-product",
                data: filter_object,
                dataType: "json",
                beforeSend: function() {
                    console.log("sending data.....");
                },
                success: function(response) {
                    console.log(response); // Log the response to ensure it's correct
                    $(".filtered-product").html(response.data); // Update the filtered product list
                }
            });
        });
    });




    $(".add-to-cart-btn").on("click", function() {
        let this_val = $(this);
        let index = this_val.attr("data-index")
        
        let quantity = $(".product-quantity-" + index).val(); 
        let product_title = $(".product-title-" + index).val(); 
        let product_id = $(".product-id-" + index).val(); 
        let product_price = $(".current-product-price-" + index).text();
        let product_pid = $(".product-pid-" + index).val(); 
        let product_image = $(".product-image-" + index).val(); 
       
        
       
    
        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("ID:", product_id);
        console.log("Pid:", product_pid);
        console.log("Image:", product_image);
        console.log("Index:", index);
        console.log("Current Element:", this_val);
    
        // Send AJAX request to server
    $.ajax({
    url: "/add-to-cart",
    method: "GET",  
    data: {
        "id": product_id,
        "pid": product_pid,
        "image": product_image,
        "qty": quantity,
        "title": product_title,
        "price": product_price
    },
    dataType: "json",
    beforeSend: function() {
        this_val.prop("disabled", true);
        console.log("Adding to cart...");
    },
    
    success: function(response) {
        this_val.html('✅')
        console.log("Added product to cart ")
        $(".cart-items-count").text(response.totalcartitems)
    },
    error: function(xhr, status, error) {
        alert("An error occurred while adding the item to the cart.");
        console.log("Error:", error);
        this_val.prop("disabled", false);
    }
});
});


    


