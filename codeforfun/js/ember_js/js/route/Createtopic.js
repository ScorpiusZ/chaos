App.CreatetopicRoute = Ember.Route.extend({
    model:function(){
        console.log('Createtopic model');
    },
    setupController:function(controller,model){
        console.log('Createtopic setupController');
        var store=this.store;
        var user=store.getById('user',1);
        if(user) {
            controller.set('nickname',user.get('nickname'));
        }
    }
});
