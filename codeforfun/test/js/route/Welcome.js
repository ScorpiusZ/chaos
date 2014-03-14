//获取node 列表
App.WelcomeRoute = Ember.Route.extend({
    model: function(){
        var i = 0;
        var store=this.store;
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
    });
           return this.store.all('nodes');
    },
});

