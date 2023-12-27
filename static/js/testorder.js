$(document).ready(function(){
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
                    $('#appenddata').empty();
                    
                    // Iterate through each order in the response data
                    response.orders.forEach(function(order) {
                        // Append the order details to the ul element
                        $('#appenddata').append('<li>Order ID: ' + order.order_id + ', Date: <a href="#" class="order-detail-link" data-order-id="' + order.order_id + '">' + order.date + '</a>, Time: ' + order.time + ', Name: ' + order.name + ', Order By: ' + order.order_by + ', Called By: ' + order.called_by + ', Price: ' + order.price + '</li>');
                        // var orderListItem = $('<li>Order ID: ' + order.order_id + ', Date: <a href="#" class="order-detail-link" data-order-id="' + order.order_id + '">' + order.date + '</a>, Time: ' + order.time + ', Name: ' + order.name + ', Order By: ' + order.order_by + ', Called By: ' + order.called_by + ', Price: ' + order.price + '</li>');
                        // $appendData.append(orderListItem);
                    });
                    
                    console.log(response);
                },
                error: function(error){
                    console.error('Error:', error);
                    alert("An Error Occurred");
                }
            });
        }
    }, 7000); // Set the interval to 5000 milliseconds (5 seconds), adjust as needed

    // Function to check if a date is today
    function isToday(someDate) {
        const today = new Date();
        return someDate.getDate() === today.getDate() &&
               someDate.getMonth() === today.getMonth() &&
               someDate.getFullYear() === today.getFullYear();
    }

     // Event handler for order detail link click
     $('#appenddata').on('click', '.order-detail-link', function(event) {
        event.preventDefault(); // Prevent the default link behavior

        // Get the order_id from the data attribute
        var orderId = $(this).data('order-id');

        // Redirect to the order_detail view
        window.location.href = '/superviseur/order/' + orderId + '/';
    });
});
