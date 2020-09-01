(function($) {
  "use strict"; // Start of use strict
    
    var page_table = $('#page_table').DataTable({
       responsive: true
    });

    $(".delete-btn").on("click", function(e){
      var key = $(this).data('key');      
      
      bootbox.confirm("Are you sure to delete?", function(result) {
        if (result == true){
          window.location="/page/delete/" + key;
        }
      }); 

    });
 
})(jQuery); // End of use strict