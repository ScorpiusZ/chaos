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
//记录当前是在哪个社区
var currentNodeId = null;
var currentNode = null;
//记录当前是最新、最热、我的等信息
var currentTopicsFilter = 'new';
//记录当前请求的页数
var topicsPage = 1;
//记录当前请求的每页的数目
var topicsPagePer = 20;
//当前是否在加载帖子列表
var isTopicsLoading = true;
//类：节点
App.Node = Ember.Object.extend({

});

App.Node.reopenClass({
    allNodes:[],
	findAll: function(){
		if(this.allNodes && this.allNodes.length>0)
		{
			return this.allNodes;
		}
		 var i = 0;
		 $.getJSON('http://api.aihuo360.com/v2/nodes').then(function(data){
			 data.nodes.map(function(node){
				var n = App.Node.create(node);
				// var n = store.createRecord(node);
				n.topicsLink = "index#/node/"+n.id+"/topics";
				n.iconLink = "images/fresh_article_cate_"+(i%6)+".png";
				// n.set('topicsLink' , "saxer#/node/"+n.id+"/topics");
				// n.set('iconLink' , "images/fresh_article_cate_"+(i%6)+".png");
				i++;
				App.Node.allNodes.pushObject(n);
			});
		});
		return this.allNodes;
	}
});



//类：帖子
App.Topics = Ember.Object.extend({

});

App.Topics.reopenClass({
    name:'Noname',
    Per:20,
    Page:1,
    filter:'new',
    isloading:false,
	findAll: function(node_id){
		var links = [];
		$.getJSON("http://api.aihuo360.com/v2/nodes/"+node_id+"/topics?"+
		 	      "page="+App.Topics.Page+"&device_id=00001393578531256&per_page="+App.Topics.Per
			      +"&filter="+App.Topics.filter).then(function(data){
			data.topics.forEach(function(t){
                links.pushObject(t);
            });
		});    

	  return links;
	}
});


//获取社区节点列表
App.ApplicationRoute = Ember.Route.extend({
});

App.WelcomeRoute = Ember.Route.extend({
	beforeModel: function(transition){
		console.log(new Date()+"before:"+transition);
	},

	model: function(){
		return App.Node.findAll();
	},

	afterModel: function(nodes,transition){
			console.log(new Date()+"after:"+nodes);
		if(nodes.length>0)
		{
			console.log(new Date()+"afterChange:"+nodes);
		}
},

	setupController: function(controller,model){
		this._super(controller,model);
		console.log(new Date()+"setupController:"+model);
	}

});


//【路由】获取帖子列表
App.TopicsRoute = Ember.Route.extend({

	model: function(params){
		return App.Topics.findAll(params.node_id);
	},

	afterModel: function(){
		// this.set('node',this.modelFor('application'));
		console.log('node:'+this.modelFor('application'));
	},

	setupController: function(controller,model){
		this._super(controller,model);
		console.log('noded:'+this.modelFor('application'));
	}
});
