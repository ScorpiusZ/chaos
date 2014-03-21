App.Topic = Ember.Object.extend({
});
var route;
App.Topic.reopenClass({
    getmorereply:function(olddata,topic){
        $.getJSON('http://api.aihuo360.com/v2/topics/' +topic.get('cur_topic_id')
                  +'/replies'+'?page='+topic.get('page')
                  +'&per_page='+topic.get('per')).then(function(data){
                      data.replies.forEach(function(t) {
                          olddata.pushObject(t);
                      });
                      route.get('controller').send('loaded');
                  });
                  return olddata;
    },
    getreply:function(topic){
        var links=[];
        $.getJSON('http://api.aihuo360.com/v2/topics/'+topic.get('cur_topic_id')
                  +'/replies'+'?page='+topic.get('page')
                  +'&per_page='+topic.get('per')).then(function(data){
                      data.replies.forEach(function(t){
                          links.pushObject(t);
                      });
                      route.get('controller').send('loaded');
                  });
                  return links;
    },
});
//帖子详情
App.TopicRoute = Ember.Route.extend({
    model: function(topic){
        route=this;
        console.log('TopicRoute model');
    },
    setupController: function(controller,model){
        console.log('TopicRoute setupController');
        var store=this.store;
        var cur_topic=store.getById('cachetopic',1);
        controller.set('isloading',true);
        controller.set('replies',App.Topic.getreply(cur_topic));
        console.log('get replies'+cur_topic.get('body'));
        controller.set('id', cur_topic.get('id'));
        controller.set('body', cur_topic.get('body'));
        controller.set('nickname', cur_topic.get('nickname'));
        controller.set('liked_count', cur_topic.get('liked_count'));
        controller.set('disliked_count', cur_topic.get('disliked_count'));
        controller.set('replies_count', cur_topic.get('replies_count'));
        controller.set('created_at', cur_topic.get('created_at'));
    },
});

