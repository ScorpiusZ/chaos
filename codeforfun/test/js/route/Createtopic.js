App.CreatetopicRoute = Ember.Route.extend({
    model:function(){
        console.log('Createtopic model');
    },
    setupController:function(controller,model){
        console.log('Createtopic setupController');
    }
});
