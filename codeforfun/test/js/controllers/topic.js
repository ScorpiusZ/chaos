App.TopicController = Ember.ObjectController.extend({

	actions:{
		//喜欢某一个帖子
		likeTopic: function(topic_id){
			 $.ajax({
		        url: "http://10.0.1.6/emberjs/topics.php/topics/"+topic_id+"/like",
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
			var m = this.get('model');
			m.set('liked_count' , m.liked_count+1);
			this.set('model',m);
		},

		//讨厌某一个帖子
		dislikeTopic: function(topic_id){
			 $.ajax({
		        url: "http://10.0.1.6/emberjs/topics.php/topics/"+topic_id+"/dislike",
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
			var m = this.get('model');
			m.set('disliked_count' , m.disliked_count+1);
			this.set('model',m);
		}
	}
});

