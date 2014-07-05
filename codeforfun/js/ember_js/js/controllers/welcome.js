App.WelcomeController = Ember.ObjectController.extend({
    isloading:true,
    edituser:false,
    nodes:[],
    actions:{
        entercomunity: function(nodeid){
            console.log('Welcome controller entercomunity '+ nodeid);
            this.transitionToRoute('topics',nodeid);
        },
        usersetting:function(){
            this.set('edituser',true);
        },
        commitsetting:function(){
            var store=this.store;
            var nickname=this.get('username');
            this.set('edituser',false);
            var olduser=store.getById('user',1);
            console.log('username = '+nickname);
            this.store.push('user',{
                id:1,
                nickname: nickname,
                deviceid: olduser.get('deviceid'),
                sexy: olduser.get('sexy')
            });
        },
        loading:function(){
            console.log('WelcomeController actions loading');
            this.set('isloading',true);
        },
        loaded:function(){
            console.log('WelcomeController actions loaded')
            this.set('isloading',false);
        }
    }
});
