var ContentLoader = (function () {
    function ContentLoader() {
        console.log("loading content start");
        var actionLoader = new ConfigLoader(ELoad.services, "../config/poskytovane_sluzby.json");
        var announcmentLoader = new ConfigLoader(ELoad.announcement, "../config/oznameni.json");
    }
    return ContentLoader;
})();
var ELoad;
(function (ELoad) {
    ELoad[ELoad["services"] = 0] = "services";
    ELoad[ELoad["announcement"] = 1] = "announcement";
})(ELoad || (ELoad = {}));
var ConfigLoader = (function () {
    function ConfigLoader(_type, url) {
        this._type = _type;
        this._request = new XMLHttpRequest();
        this._request.addEventListener("readystatechange", this.responseHandler.bind(this));
        this._request.open("POST", url, true);
        this._request.send();
    }
    ConfigLoader.prototype.responseHandler = function () {
        if (this._request.readyState == 4 && this._request.status == 200) {
            // console.log("response: "+this._request.responseText);
            if (this._type == ELoad.services) {
                this.createActionItems(this._request.responseText);
            }
            else {
                this.createAnnouncementItems(this._request.responseText);
            }
        }
    };
    ConfigLoader.prototype.createActionItems = function (data) {
        var items = [];
        var services = JSON.parse(data).services;
        services.forEach(function (action) {
            var actionItem = new ActionItem(action["oblast"], action["sluzby"]);
            items.push(actionItem);
        });
        this.addItem(items);
    };
    ConfigLoader.prototype.createAnnouncementItems = function (data) {
        var items = [];
        var announcements = JSON.parse(data).oznameni;
        if (announcements.length && announcements.length > 0) {
            announcements.forEach(function (announcement) {
                var announcementItem = new AnnouncementItem(announcement["datum"], announcement["text"]);
                items.push(announcementItem);
            });
        }
        else {
            console.log("add mock");
            var date = new Date();
            var nodataItem = new AnnouncementItem(date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear(), "Žádná oznámení.");
            items.push(nodataItem);
        }
        this.addItem(items);
    };
    ConfigLoader.prototype.addItem = function (items) {
        var itemsContainer;
        if (this._type == ELoad.services) {
            itemsContainer = document.getElementById("services");
        }
        else {
            itemsContainer = document.getElementById("aItemContainer");
        }
        items.forEach(function (item) {
            //TODO efetk pridani
            itemsContainer.appendChild(item.item);
        });
    };
    return ConfigLoader;
})();
var ActionItem = (function () {
    function ActionItem(title, actions) {
        this.item = document.createElement("div");
        var heading = document.createElement("h4");
        heading.innerHTML = title;
        this.item.appendChild(heading);
        var actionList = document.createElement("ul");
        this.item.appendChild(actionList);
        actions.forEach(function (action) {
            var actionElement = document.createElement("li");
            actionElement.innerHTML = action;
            actionList.appendChild(actionElement);
        });
    }
    return ActionItem;
})();
var AnnouncementItem = (function () {
    function AnnouncementItem(date, text) {
        this.item = document.createElement("div");
        this.item.style.cssText = "width:100%;margig-bottom:10px;";
        var dateElement = document.createElement("div");
        dateElement.style.paddingRight = "5px";
        dateElement.innerHTML = date + " :";
        this.item.appendChild(dateElement);
        var textElement = document.createElement("div");
        textElement.innerHTML = text;
        this.item.appendChild(textElement);
    }
    return AnnouncementItem;
})();
//# sourceMappingURL=app.js.map