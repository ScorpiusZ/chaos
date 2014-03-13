App.Topic = DS.Model.extend({
    body: DS.attr(),
    nickname: DS.attr(),
    liked_count: DS.attr(),
    disliked_count: DS.attr(),
    replies_count: DS.attr(),
    created_at: DS.attr(),
});

