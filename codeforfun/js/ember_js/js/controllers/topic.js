App.TopicController = Ember.ObjectController.extend({
    id: 123,
    body: 123,
    nickname: 123,
    liked_count: 123,
    disliked_count: 123,
    replies_count: 123,
    created_at: 123,
    replies:[],
    ismore:true,
    isloading:false,
    actions:{
        page: function(){
            this.set('isloading',true);
            var m=[];
            m=this.get('replies');
            var store=this.store;
            var old=store.getById('cachetopic',1);
            var page=old.get('page');
            page++;
            store.push('cachetopic',{
                id: 1,
                cur_topic_id: old.get('cur_topic_id'),
                body: old.get('body'),
                nickname: old.get('nickname'),
                liked_count: old.get('liked_count'),
                disliked_count: old.get('disliked_count'),
                replies_count: old.get('replies_count'),
                created_at: old.get('created_at'),
                page: page,
                per: 10,
            });
            var newone=store.getById('cachetopic',1);
            var newm=[];
            newm=App.Topic.getmorereply(m,newone);
            this.set('replies',newm);
        },
        loaded:function(){
            var cur_topic=this.store.getById('cachetopic',1);
            var replies=this.get('replies');
            console.log('TopicController actions loaded replies length='+replies.length+' loaded length = '+cur_topic.get('per')*cur_topic.get('page'));
            if(replies.length<cur_topic.get('per')*cur_topic.get('page')) {
                console.log('nomre');
                this.set('ismore',false);
            }
            this.set('isloading',false);
        },
        loading:function(){
            console.log('TopicController actions loading');
            this.set('isloading',true);
        }
    }
});
