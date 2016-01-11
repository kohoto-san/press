var page = 1;
var first_load = false;

$( window ).load(function() {
    loadPosts();
});

$('#load_posts').click(function(){
    loadPosts();
});


function loadPosts(){
            
    if( $(this).find('a').hasClass("disabled") == false){

        $.get( window.location.href, {page: page} )
                
            .success(function( data ) {

                var newElems = $( data );
                var $container = $('#content-posts-wrapper');

                $container.masonryImagesReveal( newElems );

                /*
                if ($container.data("masonry")) {
                    $container.append( newElems ).masonry( "appended", newElems );
                }
                else {
                    $container.append( data );
                }
                */

            }) // success || done
                
            .fail(function() {
                $('#load_posts').prepend('<p>Упс...Кажется все посты уже загружены.</p>')
                $('#load_posts a').addClass('disabled');
            }); // fail

    }    // hasClass

} // function loadPosts

(function( $ ){
    
    $.fn.masonryImagesReveal = function( $newElems ) {
        var msnry = this.data('masonry');
        var itemSelector = msnry.options.itemSelector;
        // hide by default
        $newElems.hide();
        // append to container
        this.append( $newElems );
        
        $newElems.imagesLoaded()
            .progress( function( imgLoad, image ) {
                // get item
                // image is imagesLoaded class, not <img>, <img> is image.img
                var $item = $( image.img ).parents( itemSelector );
                // un-hide item
                $item.show();
                // masonry does its thing
                msnry.appended( $item );

                if( !first_load ){
                    $('#content-posts-plug').css('display', 'none');
                    first_load = true;
                }

            })
            .always( function( instance ) {                
                page += 1;
            });
  
        return this;
    };

})( jQuery );
