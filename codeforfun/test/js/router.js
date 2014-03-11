App.Router.map(function(){
	this.resource('application');
    
    this.resource('welcome',{path :'/'});

    this.resource('topics',{path :'topics/:node_id'});
    //this.resource('topics', { path: 'node/:node_id/topics' });

	//this.resource('topic' ,{ path: 'topics/:topic_id' } , function(){
		//this.resource('replies' , { path: 'replies/:topic_id' } );
	//});

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
        return	$.getJSON("http://api.aihuo360.com/v2/nodes/"+params.cur_node_id+"/topics?"+
            "page="+params.page+"&device_id=00001393578531256&per_page="+params.per
            +"&filter="+params.filter ).then(function(data){
                return data.topics
            })
    },
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
        var n=store.all('cachenode');
        console.log('cache:'+n.cur_node_id);
        return App.Topics.findall(n)
	},
});
