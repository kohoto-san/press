    <script type="text/javascript">

		$('.startups-wrapper').on('click', '.product-post-body', function() {
		//$('.product-post-body').click(function(){
			var url = "{% url 'hunt:post_detail' 'slug' %}";
			url = url.replace('slug', $(this).data('slug'))
			location.href = url;
		});


        var is_loading = false;
        var all_post = false;
        var page = 1;

        function loading(turn){
            // Когда посты загружены включить возможность загрузить ещё
            if(turn == 'on'){
                // $('#load_posts a').removeClass('disabled');
                $('.preloader-wrapper').hide();
                is_loading = false;
            }
            // Когда посты начали грузиться выключить возможность загрузить ещё
            else{
                // $('#load_posts a').addClass('disabled');
                $('.preloader-wrapper').show();
                is_loading = true;
            }
        }

		$( window ).load(function() {
            loading('off');
    		loadPosts();
		});

		function loadPosts(){

    		$.get("{% url 'hunt:load_posts' %}", {page: page, 'profile': "{{profile.pk}}" } )
                
        		.success(function( data ) {

            		var $container = $('.startups-wrapper');
        			if(data == 'empty'){
        				var newElems = "<h5>Кажется, здесь пусто.</h5>"
        			}
        			else{
            			var newElems = $( data );
        			}

            		$container.append(newElems);

                    page += 1;
                    loading('on');

        		}) // success || done
                
        		.fail(function() {
                    loading('on');
                    all_post = true;
        		    // $('#load_posts').prepend('<p>Упс...Кажется все посты уже загружены.</p>');
        		    // $('#load_posts a').addClass('disabled');
        		}); // fail
    
		} // function loadPosts

    </script>
