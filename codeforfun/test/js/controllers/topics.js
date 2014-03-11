//【控制器】主题列表
App.TopicsController = Ember.ObjectController.extend({
	actions:{
		//查看最新、最热等
		filter: function(filter_v){
            var store=this.store;
            var old=store.getById('cachenode',1);
            this.store.push('cachenode',{
                id: old.get('id'),
                cur_node_id: old.get('cur_node_id'),
                per: old.get('per'),
                page: old.get('page'),
                filter: filter_v,
            });
            var newone=store.getById('cachenode',1);
            //console.log(App.Topics.findall(newone));
            this.set('model',App.Topics.findall(newone));
		},

		//查看下一页
		page: function(){
		},

		//喜欢某一个帖子
		likeTopic: function(topic_id){
		},

		//讨厌某一个帖子
		dislikeTopic: function(topic_id){
		}

	}//End Actions

});

