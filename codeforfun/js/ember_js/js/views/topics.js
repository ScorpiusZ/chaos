App.TopicsItem = Ember.View.extend({
    item:null,
    click:function(){
        console.log('view on click'+this.item);
        this.get('controller').send('seedetail',this.item);
    }
});
