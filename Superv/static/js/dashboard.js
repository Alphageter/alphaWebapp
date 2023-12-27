
$(document).ready(function(){
   // Define $tableBody - make sure to replace '#your-table-body-id' with the actual ID or selector of your table body
   var $tableBody = $('#my-table-body-id');

   // Attach click event to table rows
   $tableBody.on('click', 'tr', function() {
       // Get the order ID from the data attribute
       var orderId = $(this).data('order-id');

       // Construct the URL based on the order ID
       var orderDetailUrl = '/superviseur/order/' + orderId;

       // Redirect to the order detail page
       window.location.href = orderDetailUrl;
   });


    setInterval(function(){
        // Get the date from the data attribute
        var orderDate = $('#appenddata').data('order-date');
        
        // Parse the date using JavaScript Date object
        var parsedDate = new Date(orderDate);

        // Check if the parsed date is today's date
        if (isToday(parsedDate)) {
            $.ajax({
                url: getOrdersUrl,  // URL to your Django view
                type: 'GET',
                dataType: 'json',
                data: { date: orderDate },
                success: function(response){
                    
                    var $tableBody = $('#appenddata tbody');
                    $tableBody.empty();
                    
                    // Iterate through each order in the response data

                    response.orders.forEach(function(order) {
                        
                        // Format the date
                        var formattedDate = new Date(order.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                        

                        // Append the table row with a clickable link to the tbody
                        var tableRow = $('<tr data-order-id="' + order.order_id + '" style="cursor: pointer;"><td>' + formattedDate + '</td><td>' + order.time  + '</td><td>' + order.name + '</td><td>' + order.nbrarticle + '</td><td>' + order.price + '</td></tr>');
                       
                     

                        $tableBody.append(tableRow);
                    });

                  
                },
                error: function(error){
                    console.error('Error:', error);
                    alert("An Error Occurred");
                }
            });
        }
    }, 30*1000);

    // Function to check if a date is today
    function isToday(someDate) {
        const today = new Date();
        return someDate.getDate() === today.getDate() &&
               someDate.getMonth() === today.getMonth() &&
               someDate.getFullYear() === today.getFullYear();
    }

    // Event handler for order detail link click on the entire table row
   // Event handler for order detail link click on the entire table row
// $('#appenddata').on('click', 'tr', function(event) {
//     event.preventDefault(); // Prevent the default link behavior

//     // Get the order_id from the data attribute
//     var orderId = $(this).find('.order-detail-link').data('order-id');

//     // Redirect to the order_detail view
//     window.location.href = '/superviseur/order/' + orderId + '/';
// });
/* <a href="#" class="order-detail-link" data-order-id="' + order.order_id + '"></a> */

});

//////////////////////////////////////////////////////////////////////////////////////////////////////////

   

//for search form

document.addEventListener("DOMContentLoaded", function () {
    var rows = document.querySelectorAll("tr[data-href]");
    rows.forEach(function (row) {
        row.addEventListener("click", function () {
            window.location.href = row.dataset.href;
        });
    });
});


// Show or hide the scroll to top button based on scroll position
window.onscroll = function() {
var scrollToTopBtn = document.getElementById("scrollToTopBtn");

if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
scrollToTopBtn.style.display = "block";
} else {
scrollToTopBtn.style.display = "none";
}
};

// Scroll to the top of the page when the button is clicked
function scrollToTop() {
document.body.scrollTop = 0; // For Safari
document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
}