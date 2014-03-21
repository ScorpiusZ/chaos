App.Router.map(function(){
    this.resource('application');

    this.resource('welcome',{path :'/:device_id'});

    this.resource('topics',{path :'topics/:node_id'});

    this.resource('topic');
    //this.resource('topic',{path :'topic/:topic'});

    this.resource('createtopic');

});

//格式化时间，显示 X分钟之前 类似这样的格式
Ember.Handlebars.helper('format-date' , function(date){
    return moment(date).fromNow();
});

//显示文字中的html标签
var showDown = new Showdown.converter();
Ember.Handlebars.helper('format-markdown' , function(input) {
    return new Handlebars.SafeString(showDown.makeHtml(input));
});

//显示表情
var facial = new Facial.expression();
Ember.Handlebars.helper('facial' , function(input) {
    var facialedText = facial.showFacial(input);
    return new Handlebars.SafeString(showDown.makeHtml(facialedText));
});


