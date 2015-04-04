# ids of the fields in DOM
notcenter_id = "cbr-notification-content"
content_id = "cbr-content-main"
# no datasets message
nodatasetsmsg = "No datasets to explore :-|"

notcenter = document.getElementById notcenter_id
# notification is not found
return "Notification is not found" unless notcenter

contcenter = document.getElementById content_id
# content center is not found
return "Content center is not found" unless contcenter

# create notification for loading
load = @notificationcenter.show @notificationcenter.type.Info, "Loading datasets...", -1, true, null, null, notcenter

success = (code, result) ->
    @notificationcenter.change load, @notificationcenter.type.Success, "Datasets are loaded", null, false, null, null
    # convert into json
    datasets = (JSON.parse result).data
    # create map
    map = []
    # depending on datasets create panels
    if datasets.length > 0
        # create panels to display datasets
        for set in datasets
            group =
                type: "div"
                cls: "item"
                children: [
                    image =
                        type: "div"
                        cls: "ui tiny image pl-text-center"
                        children:
                            type: "i"
                            cls: "star big icon"
                    content =
                        type: "div"
                        cls: "content"
                        children: [
                            header =
                                type: "span"
                                cls: "header"
                                title: "#{set.name}"
                            desc =
                                type: "div"
                                cls: "description"
                                children:
                                    type: "p"
                                    title: "#{set.desc}"
                            extra =
                                type: "div"
                                cls: "extra"
                                children:
                                    type: "a"
                                    cls: "pl-button pl-button-primary"
                                    title: "Explore"
                                    href: "demo/#{set.id}"
                        ]
                ]
            map.push group
    else
        map =
            type: 'div'
            cls: 'pl-container pl-container-center pl-margin-large-top pl-text-center'
            title: nodatasetsmsg

    # parse map
    @mapper.parseMapForParent map, contcenter

error = (code, result) ->
    result = JSON.parse result
    msg = if result.messages.length > 0 then result.messages[0] else "Something went wrong"
    @notificationcenter.change load, @notificationcenter.type.Error, msg, null, false, null, null


url = "/api/datasets"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
