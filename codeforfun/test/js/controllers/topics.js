//【控制器】主题列表
App.TopicsController = Ember.ObjectController.extend({
    topics:[],
    nodename:"微趣",
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
            this.set('topics',App.Topics.findall(newone));
		},

		//查看下一页
		page: function(){
            var m=[];
            m=this.get('topics');
            var store=this.store;
            var old=store.getById('cachenode',1);
            var page=old.get('page');
            page++;
            store.push('cachenode',{
                id: old.get('id'),
                cur_node_id: old.get('cur_node_id'),
                per: old.get('per'),
                page: page,
                filter: old.get('filter'),
            });
            var newone=store.getById('cachenode',1);
            var newm=[];
            newm=App.Topics.findnextpage(m,newone);
            console.log('topics length= '+newm.length);
            this.set('topics',newm);
		},
		//喜欢某一个帖子
		likeTopic: function(topic_id){
            $.ajax({
                url: "http://api.aihuo360.com/v2/topics/"+topic_id+"/like",
            type: "PUT",
            crossDomain: true,
            async: false,
            dataType: "json",
            success:function(result){
                console.log('like success');
                return true;
            },
            error:function(xhr,status,error){
                console.log('like failed');
                return false;
            }
            });	
		},

		//讨厌某一个帖子
        dislikeTopic: function(topic_id){            
            $.ajax({
                url: "http://api.aihuo360.com/v2/topics/"+topic_id+"/unlike",
            type: "PUT",
            crossDomain: true,
            async: false,
            dataType: "json",
            success:function(result){
                console.log('unlike success');
                return true;
            },
            error:function(xhr,status,error){
                console.log('unlike failed');
                return false;
            }
            });	

		},
        //帖子详情
        seedetail:function(topic){
            console.log('controller seedetail'+topic.id);
            var store=this.store;
            store.push('cachetopic',{
                id: 1,
                cur_topic_id: topic.id,
                body: topic.body,
                nickname: topic.nickname,
                liked_count: topic.liked_count,
                disliked_count: topic.disliked_count,
                replies_count: topic.replies_count,
                created_at: topic.created_at,
                page: 1,
                per: 10,
            });
            this.transitionToRoute('topic');
        },
        createtopic:function(){
            this.transitionToRoute('createtopic');
        }
	}//End Action

});

