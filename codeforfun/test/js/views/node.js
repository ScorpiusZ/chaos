App.NodeItem = Ember.View.extend({
    itemid:null,
    click:function(){
        console.log('view on click'+this.itemid);
        this.get('controller').send('entercomunity',this.itemid);
    }
});
