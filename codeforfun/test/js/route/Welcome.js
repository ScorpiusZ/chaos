//获取node 列表
App.WelcomeRoute = Ember.Route.extend({
    model: function(params){
        console.log('WelcomeRoute model');
        if(params){
            console.log('WelcomeRoute model deviceid = '+params.device_id);
        }
        this.store.push('user',{
            id:1,
            nickname:"匿名用户",
            deviceid:params.device_id,
            sexy:"male"
        });

    },
    afterModel:function(){
        console.log('WelcomeRoute afterModel');
    },
    setupController:function(controller,model){
        var i = 0;
        var store=this.store;
        console.log('WelcomeRoute setupController');
        controller.set('isloading',true);
        $.getJSON('http://api.aihuo360.com/v2/nodes').then(function(data){
            data.nodes.map(function(node){
                var iconLink = "images/fresh_article_cate_"+(i%6)+".png";
                i++;
                store.push('nodes',{
                    id: node.id,
                    name: node.name,
                    summary: node.summary,
                    topics_count: node.topics_count,
                    iconLink : iconLink,
                });
            });
            controller.send('loaded');
        });
        controller.set('nodes',this.store.all('nodes'));
    }
});

