
        var left_height = 0;
        var right_height = 0;
        var current_collumn = 0;
        var page = 1;

        var card_width = 0;

        if( $(window).width() >= 992 ){
            var columns = 2;
        }
        else{
            var columns = 1;
        }

        $( window ).load(function() {
            
            card_width = $('.card-post:eq(0)').outerWidth();

            if( $(window).width() >= 992 ){
                var wrapper_width = (card_width * columns) + $('#home-sidebar-share').outerWidth();
                $('#content-posts-wrapper').css('width',  wrapper_width);
                $('#content-posts-wrapper').parent().css('width',  wrapper_width);
            }
            /*
            else{
                var wrapper_width = card_width * columns;
            }
            */

            loadPosts();
        });
        

        function posCardsCover(){

            var left_height_meta = left_height;
            var right_height_meta = right_height;

            $('#content-posts-plug').css('display', 'block');

            $('#content-posts-plug').children().each(function( index ) {
                positionCard( $(this) );
            });

            cardsShow();

            left_height = left_height_meta;
            right_height = right_height_meta;
        }


        function posCards($cards){

            //var cards_html = $($.parseHTML(cards_str));
            //var cards_html = $('<div/>').html(cards_str).contents();
            //alert(cards_html);



            //$('.card-post-disabled').each(function( index ) {
            $cards.find('.card-post-disabled').each(function( index ) {
                positionCard( $(this), index );
            });

            cardsShow();

            $('#content-posts-plug').css('display', 'none');
        }

        function positionCard($elem, index){

            var height = 0;
            var top = 0;

            if( $elem.parent().is('#content-posts-plug') == false ){
                $('#content-posts-wrapper').append($elem);
            }

            var current_height = $elem.height();

            $elem.css('left', current_collumn * card_width);

            if(current_collumn == 0){
                $elem.css('top', left_height);
                current_height += left_height;

                left_height = current_height;
            }
            else{
                $elem.css('top', right_height);
                current_height += right_height;

                right_height = current_height;
            }

            if( $elem.parent().is('#content-posts-plug') == false ){
                $elem.removeClass('card-post-disabled');
            }

            current_collumn += 1;

            if(current_collumn == columns){
                current_collumn = 0;
            }

        }

        function cardsShow(){

            if(left_height >= right_height){
                $('#content-posts-wrapper:parent').css('height', left_height);
            }
            else{
                $('#content-posts-wrapper:parent').css('height', right_height);
            }
        }


        $('#load_posts').click(function(){
            loadPosts();
        });


        function loadPosts(){
            
            if( $(this).find('a').hasClass("disabled") == false){

                $.get( window.location.href, {page: page} )
                
                    .done(function( data ) {

                        if( $(window).width() >= 992 && page == 1){
                            //posCardsCover();
                        }
                        
                        //$('#content-posts-wrapper').append(data);
                        
                        var data_object = $('<div></div>').append(data);
                        
                        if( $(window).width() >= 992 ){
                            setTimeout(function(){ posCards(data_object); }, 2000);
                            //posCards(data_object);
                        }
                        else{

                            $('#content-posts-plug').css('display', 'none');
                            $('.card-post-disabled').removeClass('card-post-disabled');
                        }
                        

                        page += 1;

                    }) // done
                
                    .fail(function() {
                        $('#load_posts').prepend('<p>Упс...Кажется все посты уже загружены.</p>')
                        $('#load_posts a').addClass('disabled');
                    }); // fail

            }    // hasClass

        } // function loadPosts

