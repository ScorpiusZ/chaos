App.Router.map(function(){
	this.resource('application');
    
    this.resource('welcome',{path :'/'});

    this.resource('topics',{path :'topics/:node_id'});

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
        var m=store.getById('nodes',n.get('cur_node_id'));
        console.log('node = ',m.get('name'));
        this.set('node',m);
        return App.Topics.findall(n);
	}
});
