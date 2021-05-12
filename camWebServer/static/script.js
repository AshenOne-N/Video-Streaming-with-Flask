$(function(){

    function update_info() {
        var $el = $('#qrinfo');
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function (data) {
                $el.text(data.message)
            }
        });
    }

    if ( $("#qrinfo").length > 0 ) {
       setInterval(update_info, 3000);
    }

});