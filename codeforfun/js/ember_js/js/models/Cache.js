App.Cachenode = DS.Model.extend({
    cur_node_id: DS.attr(),
    page: DS.attr(),
    per: DS.attr(),
    filter: DS.attr()
});

App.Cachetopic = DS.Model.extend({
    cur_topic_id: DS.attr(),
    body: DS.attr(),
    nickname: DS.attr(),
    liked_count: DS.attr(),
    disliked_count: DS.attr(),
    replies_count: DS.attr(),
    created_at: DS.attr(),
    page: DS.attr(),
    per: DS.attr()
});
