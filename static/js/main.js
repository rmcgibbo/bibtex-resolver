$(document).ready(function() {

    $('#searchform').submit( function(event){
      // prevent default browser behaviour
      event.preventDefault();
      var data = $('#searchform').serialize();
      $('#results').text('working...');
      var jqxhr = $.get("/api", data, function(e) {
        console.log(e);
        $('#results').text(e);
      });

    });

});
