App.Router.map(function(){
	this.resource('application');
    
    this.resource('welcome',{path :'/'});

    this.resource('topics',{path :'topics/:node_id'});

    //this.resource('topic');
    this.resource('topic',{path :'topic/:topic'});

});

//格式化时间，显示 X分钟之前 类似这样的格式
Ember.Handlebars.helper('format-date' , function(date){
	return moment(date).fromNow();
});

//显示文字中的html标签
var showDown = new Showdown.converter();
Ember.Handlebars.helper('format-markdown' , function(input) {
	return new Handlebars.SafeString(showDown.makeHtml(input));
});

//显示表情
var facial = new Facial.expression();
Ember.Handlebars.helper('facial' , function(input) {
	var facialedText = facial.showFacial(input);
	return new Handlebars.SafeString(showDown.makeHtml(facialedText));
});



App.ApplicationRoute = Ember.Route.extend({
});

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

App.Topics = Ember.Object.extend({
});

App.Topics.reopenClass({
    findall:function(params){
        var links=[];
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')+"/topics?"+
            "page="+params.get('page')+"&device_id=00001393578531256&per_page="+params.get('per')
            +"&filter="+params.get('filter')+"").then(function(data){
                data.topics.forEach(function(t) {
                    links.pushObject(t);
                });
            });
        return links;
    },
    findnextpage:function(olddata,params){
        $.getJSON("http://api.aihuo360.com/v2/nodes/"+params.get('cur_node_id')+"/topics?"+
            "page="+params.get('page')+"&device_id=00001393578531256&per_page="+params.get('per')
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
        var store=this.store;
        store.push('cachenode',{
            id: 1,
            cur_node_id: params.node_id,
            page: 1,
            per: 20,
            filter: "new",
        });
        var n=store.getById('cachenode',1);
        return App.Topics.findall(n);
	}
});

App.Topic = Ember.Object.extend({
});

App.Topic.reopenClass({
    gettopic:function(topic_id){
        return $.getJSON('http://api.aihuo360.com/v2/topics/'+topic_id).then(function(data){
    return data;
    });
    },
    getreply:function(topic_id){
        var links=[];
        $.getJSON('http://api.aihuo360.com/v2/topics/'+topic_id+'/replies').then(function(data){
    data.replies.forEach(function(t){
        links.pushObject(t);
        });
    });
            return links;
    },
});
//帖子详情
App.TopicRoute = Ember.Route.extend({
    model: function(topic){
        console.log('TopicRoute model'+topic);
    },
    setupController: function(controller,model){
        console.log('setupController');
        var store=this.store;
        var cur_topic=store.getById('cachetopic',1);
        //var topic=store.getById('topic',cur_topic.get('cur_topic_id'));
        //controller.get('topic');
        controller.set('replies',App.Topic.getreply(cur_topic.get('cur_topic_id')));
        //console.log('get replies'+topic.get('body'));
        //controller.set('id', topic.get('id'));
        //controller.set('body', topic.get('body'));
        //controller.set('nickname', topic.get('nickname'));
        //controller.set('liked_count', topic.get('liked_count'));
        //controller.set('disliked_count', topic.get('disliked_count'));
        //controller.set('replies_count', topic.get('replies_count'));
        //controller.set('created_at', topic.get('created_at'));
        //controller.set('topic',topic);
        console.log('get topic');
    },
    afterModel:function(){
    }
});

App.Reply = Ember.Route.extend({
    model:function(){
        console.log('Reply model');
    },
    setupController: function(controller,model){
    }
});
