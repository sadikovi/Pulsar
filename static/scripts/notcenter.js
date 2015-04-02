var NotificationType = {
    Info    :   "INFO",
    Success :   "SUCCESS",
    Warning :   "WARNING",
    Error   :   "ERROR"
};

var Util = (function() {
    return {
        // create element
        createElement: function(tagname, id, aClass, text, parent) {
            var element = document.createElement(tagname);

            if (aClass != null && aClass != "")
                element.className = aClass;
            if (id != null && id != "")
                element.id = id;
            if (text != null && text != "")
                element.innerHTML = text;

            if (parent)
                parent.appendChild(element);

            return element;
        },

        /* add event listener and remove event listener */
        addEventListener: function(elem, evnt, handler) {
            if (elem.addEventListener)
                elem.addEventListener(evnt, handler, false);
            else if (elem.attachEvent) {
                elem.attachEvent("on"+evnt, handler);
            } else {
                elem["on" + evnt] = null;
            }
        },
        removeEventListener: function(elem, evnt, handler) {
            if (elem.removeEventListener) {
                elem.removeEventListener(evnt, handler, false);
            } else if (elem.detachEvent) {
                elem.detachEvent("on" + evnt, handler);
            } else {
                elem["on" + evnt] = null;
            }
        },

        /* add class to element and remove class from element */
        addClass: function(elem, classname) {
            if (!elem) {return;}
            var a = elem.className.split(" ");
            for (var i=0; i<a.length; i++)
                if (a[i] == classname)
                    return;

            elem.className += " " + classname;
        },
        removeClass: function(elem, classname) {
            if (!elem) {return;}
            var newclassname = "";
            var a = elem.className.split(" ");
            for (var i=0; i<a.length; i++)
                if (a[i] != classname)
                    newclassname += " " + a[i];
            elem.className = newclassname.replace(/^\s+|\s+$/gm,'');
        },
        hasClass: function(elem, classname) {
            if (!elem) {return;}
            var a = elem.className.split(" ");
            for (var i=0; i<a.length; i++)
                if (a[i] == classname)
                    return true;
            return false;
        }
    }
})();

var NotificationCenter = (function() {
    // default time to show notification (3 seconds)
    var time = 3000;

    return {
        // get type object for specified type
        getTypeObject: function(type) {
            if (NotificationType.Success == type) {
                return { nclass: "notification-success",
                laclass: "loading-indicator-success" };
            } else if (NotificationType.Warning == type) {
                return { nclass: "notification-warning",
                laclass: "loading-indicator-warning" };
            } else if (NotificationType.Error == type) {
                return { nclass: "notification-error",
                laclass: "loading-indicator-error" };
            } else {
                return { nclass: "", laclass: "" };
            }
        },

        // creates loading indicator
        createLoadingIndicator: function(typeObj, parent) {
            var main = Util.createElement("div", null, "notification-loading loading-indicator", null, parent);
            var spinner = Util.createElement("div", null, "loading-indicator-spinner", null, main);
            var mask = Util.createElement("div", null, "loading-indicator-mask", null, spinner);
            var maskCircle = Util.createElement("div", null, "loading-indicator-masked-circle " + typeObj.laclass, null, mask);
            return main;
        },

        // creates text node and adds text to it
        createTextNode: function(msg, parent) {
            return Util.createElement("div", null, "notification-content-cell", msg, parent);
        },

        // creates control panel with up to 2 buttons
        createControlPanel: function(ok, cancel, notification) {
            NotificationCenter.removeActionHandlers(notification);
            if (ok || cancel) {
                var a = Util.createElement("div", null, "notification-control-panel", null, notification.controlNode);
                if (ok) {
                    notification.controlNode.ok = Util.createElement("a", null, "notification-control", "Ok", a);
                    notification.controlNode.okHandler = function() {
                        if (notification.timeout) {
                            clearTimeout(notification.timeout);
                        }
                        NotificationCenter.hide(notification);
                        ok.call(this);
                    };
                    Util.addEventListener(notification.controlNode.ok, "click", notification.controlNode.okHandler);
                }

                if (cancel) {
                    notification.controlNode.cancel = Util.createElement("a", null, "notification-control", "Cancel", a);
                    notification.controlNode.cancelHandler = function() {
                        if (notification.timeout) {
                            clearTimeout(notification.timeout);
                        }
                        NotificationCenter.hide(notification);
                        cancel.call(this);
                    }
                    Util.addEventListener(notification.controlNode.cancel, "click", notification.controlNode.cancelHandler);
                }

                return a;
            } else {
                return null;
            }
        },

        // remove all action handlers
        removeActionHandlers: function(notification) {
            if (!notification || !notification.controlNode)
                return;

            if (notification.controlNode.okHandler) {
                Util.removeEventListener(notification.controlNode.ok, "click", notification.controlNode.okHandler);
            }
            if (notification.controlNode.cancelHandler) {
                Util.removeEventListener(notification.controlNode.cancel, "click", notification.controlNode.cancelHandler);
            }
        },

        setHideTimeout: function(notification, timeout) {
            if (notification.timeout) {
                clearTimeout(notification.timeout);
            }

            if (!timeout || timeout >= 0) {
                notification.timeout = setTimeout(function() {NotificationCenter.hide(notification);}, ((timeout)?timeout:time));
            }
        },

        change: function(notification, type, message, timeout, showLoad, okHandler, cancelHandler) {
            if (!notification) {
                throw ("Notification object is undefined");
            }

            var typeObj = NotificationCenter.getTypeObject(type);
            // change type
            notification.element.className = "notification"+" "+typeObj.nclass;
            // change message
            notification.textNode.innerHTML = message;
            // change loading
            notification.loadNode.innerHTML = "";
            if (showLoad)
                NotificationCenter.createLoadingIndicator(typeObj, notification.loadNode);
            // change okHandler and cancelHandler
            notification.controlNode.innerHTML = "";
            NotificationCenter.createControlPanel(okHandler, cancelHandler, notification);

            // change timeout
            NotificationCenter.setHideTimeout(notification, timeout);

            return false;
        },

        create: function(type, message, timeout, showLoad, okHandler, cancelHandler, parent) {
            var notification = {};
            var typeObj = NotificationCenter.getTypeObject(type);

            // build the html of the notification
            notification.parent = parent;
            notification.element = Util.createElement("div", null, "notification " + typeObj.nclass, null, parent);
            var table = Util.createElement("div", null, "notification-content-box", null, notification.element);

            // 0. spinner (loading indicator)
            notification.loadNode = Util.createElement("div", null, "notification-content-cell", null, table);
            if (showLoad) {
                NotificationCenter.createLoadingIndicator(typeObj, notification.loadNode);
            }

            // 1. text (message)
            notification.textNode = NotificationCenter.createTextNode(message, table);

            // 2. controls
            notification.controlNode = Util.createElement("div", null, "notification-content-cell", null, table);
            NotificationCenter.createControlPanel(okHandler, cancelHandler, notification);

            return notification;
        },

        show: function(type, message, timeout, showLoad, okHandler, cancelHandler, parent) {
            var t = NotificationCenter.create(type, message, timeout, showLoad, okHandler, cancelHandler, parent);
            NotificationCenter.setHideTimeout(t, timeout);
            NotificationCenter.fadeIn(t.element);
            return t;
        },

        hide: function(notification) {
            if (!notification.parent)
                throw ("Parent for notifications is undefined");

            if (!notification)
                return;

            NotificationCenter.removeActionHandlers(notification);
            NotificationCenter.fadeOut(notification.element, function() {
                notification.parent.removeChild(notification.element);
            });
        },

        /* fade out */
        fadeOut: function(element, callback) {
            var op = 1;
            element.style.opacity = op;
            var timer = setInterval(function () {
                if (op <= 0.1) {
                    clearInterval(timer);
                    Util.removeClass(element, "notification-on");
                    Util.addClass(element, "notification-off");
                    if (callback)
                        callback.call(this);
                }
                element.style.opacity = op;
                element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                op -= op * 0.1;
            }, 12);
        },

        /* fade in */
        fadeIn: function(element, callback) {
            var op = 0.1;
            element.style.opacity = op;
            Util.removeClass(element, "notification-off");
            Util.addClass(element, "notification-on");

            var timer = setInterval(function () {
                if (op >= 1) {
                    clearInterval(timer);
                    if (callback)
                        callback.call(this);
                }
                element.style.opacity = op;
                element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                op += op * 0.1;
            }, 12);
        }
    }
})();
