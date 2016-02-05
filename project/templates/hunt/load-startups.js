    <script type="text/javascript">

		$('.startups-wrapper').on('click', '.product-post-body', function() {
		//$('.product-post-body').click(function(){
			var url = "{% url 'hunt:post_detail' 'slug' %}";
			url = url.replace('slug', $(this).data('slug'))
			location.href = url;
		});

		$( window ).load(function() {
    		loadPosts();
		});

		var page = 1;

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

                    $('.preloader-wrapper').hide();
            		$container.append(newElems);

        		}) // success || done
                
        		.fail(function() {
        		    $('#load_posts').prepend('<p>Упс...Кажется все посты уже загружены.</p>')
        		    $('#load_posts a').addClass('disabled');
        		}); // fail
    
		} // function loadPosts

    </script>
