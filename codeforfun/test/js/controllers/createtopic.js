App.CreatetopicController = Ember.ObjectController.extend({
    nickname:"匿名用户",
    actions:{
        publish: function(){
            var store=this.store;
            var cur_node=store.getById('cachenode',1);
            console.log('CreatetopicController publish');
            var content=this.get('content');
            console.log('url = api.aihuo360.com/v2/nodes/'+cur_node.get('cur_node_id')+'/topics');
            console.log('content = '+content);
            var usr=store.getById('user',1);
            console.log('nickname = '+usr.get('nickname'));
        }
    }
});
