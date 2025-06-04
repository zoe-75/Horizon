
$(document).ready(function(){
    var limit=3;
    var start=0
    var action='inactive'
    function load_post_data(limit, start){
        $.ajax({
            url: 'blog/',
            method: 'GET',
            data:{
                limit:limit,
                start:start
            },
            caches: false,
            success:function(response){
                $("#post-container").append(response);
                if(response==""){
                    $('#more-data').html("<button type='button' class='btn btn-info'>No post found</button>")
                      action='active';
                }else{
                    $('#more-data').html("<button type='button' class='btn btn-success'>Loading...</button>")
                      action='inactive';
                }
            }
        })
    }

    if(action=='inactive'){
        action='active',
        load_post_data(limit, start);
    } 
    $(window).scroll(function(){
        if($(window).scrollTop() + $(window).height() > $("#post-container").height() && action == 'inactive'){
            action='active';
            start = start + limit;
            setTimeout(function(){
                load_post_data(limit, start);
            }, 1000);
        }
    });
})