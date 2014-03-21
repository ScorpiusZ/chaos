App.Topics = Ember.Object.extend({
});

var route;

App.Topics.reopenClass({
    findall:function(params,device_id){
        var links=[];
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')
                  +"/topics?"+"page="+params.get('page')
                  +"&device_id="+device_id+"&per_page="+params.get('per') 
                  +"&filter="+params.get('filter')+"").then(function(data){
                      data.topics.forEach(function(t) {
                          links.pushObject(t);
                      });
                      route.get('controller').send('loaded');
                  });
                  return links;
    },
    findnextpage:function(olddata,params,device_id){
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')
                  +"/topics?"+ "page="+params.get('page')
                  +"&device_id="+device_id+"&per_page="+params.get('per') 
                  +"&filter="+params.get('filter')+"").then(function(data){
                      data.topics.forEach(function(t) {
                          olddata.pushObject(t);
                      });
                      route.get('controller').send('loaded');
                  });
                  return olddata;
    }
});

//获取帖子列表
App.TopicsRoute = Ember.Route.extend({
    model: function(params){
        console.log('TopicsRoute model');
        route=this;
        var node=this.store.getById('nodes',params.node_id);
        this.store.push('cachenode',{
            id: 1,
            cur_node_id: params.node_id,
            page: 1,
            per: 20,
            filter: "new",
        });
    },
    setupController: function(controller,model){
        console.log('TopicsRoute setupController');
        var store=this.store;
        var cur_node=store.getById('cachenode',1);
        var node=store.getById('nodes',cur_node.get('cur_node_id'));
        controller.set('nodename',node.get('name'));
        var user=store.getById('user',1);
        console.log('set isloading true');
        controller.set('isloading',true);
        controller.set('topics',App.Topics.findall(cur_node,user.get('deviceid')));
    }
});

