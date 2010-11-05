/*
 * Hub access library
 */

;Hub = (function() {
    var iframe = document.createElement("iframe");
    iframe.src = "http://hub/hub.html";
    document.firstChild.appendChild(iframe);
    var s_channel = Channel.build({
        window: iframe.contentWindow,
        origin: "*",
        scope: "hub"
    });
    return {
        saveBadge: function(badge, onsuccess) {
            s_channel.call({method: "badge_put", params: badge, success: onsuccess});
        },
        getBadges: function(filter, onsuccess) {
            s_channel.call({method: "badge_get", params: filter, success: onsuccess});
        }
    }
})();
