/*
 * Hub access library
 */

;Hub = (function() {
    let iframe = document.createElement("iframe");
    var s_channel = Channel.build({
        window: iframe.contentWindow,
        origin: "*",
        scope: "hub"
    });
    return {
        saveBadge: function(badge, onsuccess) {
            s_channel.call("badge_put", badge, onsuccess);
        },
        getBadges: function(filter, onsuccess) {
            s_channel.call("badge_get", filter, onsuccess)
        }
    }
})();
