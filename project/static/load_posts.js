var page = 1;
var first_load = false;
var is_loading = false;

$( window ).load(function() {
    loading('off');
    loadPosts();
});

$('#load_posts').click(function(){
    if( !is_loading ){
        loading('off');
        loadPosts();
    }
});


function loading(turn){
    // Когда посты загружены включить возможность загрузить ещё
    if(turn == 'on'){
        $('#load_posts a').removeClass('disabled');
        is_loading = false;
    }
    // Когда посты начали грузиться выключить возможность загрузить ещё
    else{
        $('#load_posts a').addClass('disabled');
        is_loading = true;
    }

}


function loadPosts(){

    $.get( window.location.href, {page: page} )
                
        .success(function( data ) {

            var newElems = $( data );
            var $container = $('#content-posts-wrapper');

            $container.masonryImagesReveal( newElems );

            /*
            var $container = $('#content-posts-wrapper');
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

            /*
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
            */

            .always( function( instance ) {

                $newElems.show();
                msnry.appended( $newElems );

                if( !first_load ){
                    $('#content-posts-plug').css('display', 'none');
                    first_load = true;
                }

                page += 1;
                loading('on');
            });
  
        return this;
    };

})( jQuery );

// обрабатываем незагруженные изображения
$(function(){
    $('img').error(function(){
        $(this).attr('src', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
    });
});
