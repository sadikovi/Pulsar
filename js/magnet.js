/* script for magnet */
(function() {
    var A = {}; A.MagnetId = "magnet-roller"; A.MagnetModel = "magnet-roller"; A.MagnetLinkActive = "active";
    var C = {}; C.DataModel = "data-model"; C.MagnetOrder = "magnet-order";

    var magnet = document.getElementById(A.MagnetId);
    if (!magnet) { return false; }

    magnet.links = [];
    /** Magnet functions **/
    var createMagnetLinks = function(parent, elems) {
        for (var i=0; i<elems.length; i++) {
            var a = Util.createElement("div", null, "magnet-section", null, parent);
            if (i+1 < elems.length) {
                Util.createElement("div", null, "magnet-link", null, parent);
            }
            magnet.links.push(a);
        }
    };
    var updateMagnetLinks = function(links, elems) {
        for (var i=0; i<links.length; i++) {
            if (i<elems.length) {
                Util.addClass(links[i], A.MagnetLinkActive);
            } else {
                Util.removeClass(links[i], A.MagnetLinkActive);
            }
        }
    };
    /** Helper functions **/
    var hasAttribute = function(elem, attr) {
        return (elem.getAttribute(attr) != null && elem.getAttribute(attr).length > 0);
    };
    var getMagnetSections = function(parent, tag) {
        if (!parent || !tag) {
            throw ("Function parameters are undefined");
        }
        var r = [], a = parent.getElementsByTagName(tag);
        for (var i=0; i<a.length; i++) {
            if (hasAttribute(a[i], C.DataModel) && hasAttribute(a[i], C.MagnetOrder)) {
                r.push(a[i]);
            }
        }
        return r;
    };

    var isScrolledUp = function(elem) {
        if (!elem) { throw ("Element is not defined to check if it is scrolled up"); }
        return (elem.getBoundingClientRect().top < window.innerHeight/2);
    }

    /** flow process **/
    var sections = getMagnetSections(document, "div");
    if (sections.length == 0) { return false; }
    // create scrolling arrays
    var scrolledUp = [], scrolledDown = [];
    for (var i=0; i<sections.length; i++) {
        if (isScrolledUp(sections[i])) {
            scrolledUp.push(sections[i]);
        } else {
            scrolledDown.push(sections[i]);
        }
    }
    // set up scroll movement
    var isUp = {};
    isUp.lastScroll = 0;
    isUp.func = function() {
        var flag = document.documentElement.getBoundingClientRect().top > isUp.lastScroll;
        isUp.lastScroll = document.documentElement.getBoundingClientRect().top;
        return (flag)?false:true;
    }
    var toss = function() {
        var flag = isUp.func();
        if (flag && scrolledDown.length > 0) {
            var a = scrolledDown[0];
            if (isScrolledUp(a)) {
                scrolledUp.push(a);
                scrolledDown.splice(0, 1);
            }
        } else if (!flag && scrolledUp.length > 0) {
            var a = scrolledUp[scrolledUp.length-1];
            if (!isScrolledUp(a)) {
                scrolledDown.splice(0, 0, a);
                scrolledUp.splice(scrolledUp.length-1, 1);
            }
        }
        // update magnet links
        updateMagnetLinks(magnet.links, scrolledUp);
    }

    // create magnet links and update them
    createMagnetLinks(magnet, sections);
    updateMagnetLinks(magnet.links, scrolledUp);

    // add event listener to update magnet links
    Util.addEventListener(window, "scroll", function(e) { toss.call(this); });
})();
