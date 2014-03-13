App.Cachenode = DS.Model.extend({
    cur_node_id: DS.attr(),
    page: DS.attr(),
    per: DS.attr(),
    filter: DS.attr()
});

App.Cachetopic = DS.Model.extend({
    cur_topic_id: DS.attr(),
    page: DS.attr(),
    per: DS.attr()
});
