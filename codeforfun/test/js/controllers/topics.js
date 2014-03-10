//【控制器】主题列表
App.TopicsController = Ember.ObjectController.extend({
    node: null,

	actions:{
		//查看最新、最热等
		filter: function(filter_v){
			App.Topic.findNodeById(currentNodeId);
			this.set('node',currentNode);
			this.set('isFilterNew',filter_v=="new"?true:false);
			this.set('isFilterAll',filter_v=="all"?true:false);
			this.set('isFilterHot',filter_v=="hot"?true:false);
			this.set('isFilterMine',filter_v=="mine"?true:false);

			currentTopicsFilter = filter_v;//当前的filter值改变
			topicsPage = 1;//初始化帖子列表的页数
			this.set('model' , App.Topic.findAll(currentNodeId,filter_v));
		},

		//查看下一页
		page: function(){
			App.Topic.findNodeById(currentNodeId);
			this.set('node',currentNode);
			topicsPage++;//帖子列表数加1
			this.set('model' , App.Topic.findNextPage(this.get('model'),currentNodeId,currentTopicsFilter));
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
		            // likeTopicSuccess(topic_id);
		            return true;
		        },
		        error:function(xhr,status,error){
		            alert("顶失败："+status);
		            return false;
		        }
		    });	

			 //FIXME:请求失败的时候就不要更新了
			var models = this.get('model');
			models.forEach(function(t){
				if(t.id == topic_id)
				{
					t.set('liked_count' , t.liked_count+1);
				}
			});
			this.set('model',models);
		},

		//讨厌某一个帖子
		dislikeTopic: function(topic_id){
			 $.ajax({
		        url: "http://api.aihuo360.com/v2/topics/"+topic_id+"/dislike",
		        type: "PUT",
		        crossDomain: true,
		        async: false,
		        dataType: "json",
		        success:function(result){
		            // likeTopicSuccess(topic_id);
		        },
		        error:function(xhr,status,error){
		            alert("踩失败："+status);
		        }
		    });	

			 //FIXME:请求失败的时候就不要更新了
			var models = this.get('model');
			models.forEach(function(t){
				if(t.id == topic_id)
				{
					t.set('disliked_count' , t.disliked_count+1);
				}
			});
			this.set('model',models);
		}

	}//End Actions

});

