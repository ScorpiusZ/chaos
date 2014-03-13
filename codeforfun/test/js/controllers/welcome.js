App.WelcomeController = Ember.ObjectController.extend({
	actions:{
        entercomunity: function(nodeid){
            console.log('Welcome controller entercomunity '+ nodeid);
            this.transitionToRoute('topics',nodeid);
        }
	}
});
