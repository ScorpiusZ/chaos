App.WelcomeController = Ember.ObjectController.extend({
    edituser:false,
	actions:{
        entercomunity: function(nodeid){
            console.log('Welcome controller entercomunity '+ nodeid);
            this.transitionToRoute('topics',nodeid);
        },
        usersetting:function(){
            this.set('edituser',true);
        },
        commitsetting:function(){
            var nickname=this.get('username');
            this.set('edituser',false);
            console.log('username = '+nickname);
            this.store.push('user',{
                nickname: nickname,
                deviceid: "00001393578531256",
                sexy: male
            });
        }
	}
});
