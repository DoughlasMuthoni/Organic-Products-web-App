    
    console.log("working fine");

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




   



    


