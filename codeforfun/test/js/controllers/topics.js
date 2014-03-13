//【控制器】主题列表
App.TopicsController = Ember.ObjectController.extend({
    node:null,
	actions:{
		//查看最新、最热等
		filter: function(filter_v){
            var store=this.store;
            var old=store.getById('cachenode',1);
            this.store.push('cachenode',{
                id: old.get('id'),
                cur_node_id: old.get('cur_node_id'),
                per: old.get('per'),
                page: 1,
                filter: filter_v,
            });
            var newone=store.getById('cachenode',1);
            //console.log(App.Topics.findall(newone));
            this.set('model',App.Topics.findall(newone));
		},

		//查看下一页
		page: function(){
            var m=[];
            m=this.get('model');
            var store=this.store;
            var old=store.getById('cachenode',1);
            var page=old.get('page');
            page++;
            this.store.push('cachenode',{
                id: old.get('id'),
                cur_node_id: old.get('cur_node_id'),
                per: old.get('per'),
                page: page,
                filter: old.get('filter'),
            });
            var newone=store.getById('cachenode',1);
            var newm=[];
            newm=App.Topics.findnextpage(m,newone);
            console.log('model length= '+newm.length);
            this.set('model',newm);
		},
		//喜欢某一个帖子
		likeTopic: function(topic_id){
		},

		//讨厌某一个帖子
		dislikeTopic: function(topic_id){
		},
        //帖子详情
        seedetail:function(topic){
            console.log('controller seedetail'+topic.id);
            var store=this.store;
            store.push('cachetopic',{
                id: 1,
                cur_topic_id: topic.id,
                page: 1,
                per: 20,
            });
            this.transitionToRoute('topic',topic);
        }
	}//End Action

});

