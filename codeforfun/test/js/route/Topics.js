App.Topics = Ember.Object.extend({
});

App.Topics.reopenClass({
    findall:function(params){
        var links=[];
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')
            +"/topics?"+"page="+params.get('page')
            +"&device_id=00001393578531256&per_page="+params.get('per') 
            +"&filter="+params.get('filter')+"").then(function(data){
                data.topics.forEach(function(t) {
                    links.pushObject(t);
                });
            });
        return links;
    },
    findnextpage:function(olddata,params){
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')
            +"/topics?"+ "page="+params.get('page')
            +"&device_id=00001393578531256&per_page="+params.get('per') 
            +"&filter="+params.get('filter')+"").then(function(data){
                data.topics.forEach(function(t) {
                    olddata.pushObject(t);
                });
            });
        return olddata;
    }
});

//获取帖子列表
App.TopicsRoute = Ember.Route.extend({
	model: function(params){
        console.log('model');
        var store=this.store;
        var node=store.getById('nodes',params.node_id);
        store.push('cachenode',{
            id: 1,
            cur_node_id: params.node_id,
            page: 1,
            per: 20,
            filter: "new",
        });
        var n=store.getById('cachenode',1);
        //return App.Topics.findall(n);
	},
    setupController: function(controller,model){
        console.log('setupController');
        var store=this.store;
        var cur_node=store.getById('cachenode',1);
        var node=store.getById('nodes',cur_node.get('cur_node_id'));
        console.log('node name '+node.get('name'));
        controller.set('nodename',node.get('name'));
        var n=store.getById('cachenode',1);
        controller.set('topics',App.Topics.findall(n));
    }
});

