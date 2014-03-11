App.Album = DS.Model.extend({
  title: DS.attr(),
  artist: DS.attr(),
  songCount: DS.attr()
});

App.ApplicationRoute = Ember.Route.extend({
  model: function() {
    this.store.push('album', {
      id: "asdas1",
      title: "Fewer Moving Parts",
      artist: "David Bazan",
      songCount: 10
    });
    this.store.push('album', {
      id: "2",
      title: "Calgary b/w I Can't Make You Love Me/Nick Of Time",
      artist: "Bon Iver",
      songCount: 2
    });
  }
});
