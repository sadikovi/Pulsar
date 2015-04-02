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
load = @notificationcenter.show @notificationcenter.type.Info, "Loading datasets...", null, true, null, null, notcenter

success = (code, result) ->
    @notificationcenter.change load, @notificationcenter.type.Success, "Datasets are loaded", 3000, false, null, null
    # convert into json
    datasets = (JSON.parse result).data
    # create map
    map =
        type: 'div'
        cls: 'pl-grid'
        children: []
    # depending on datasets create panels
    if datasets.length > 0
        # create panels to display datasets
        for set in datasets
            group =
                type: 'div'
                cls: 'pl-width-1-3'
                children:
                    type: 'div'
                    cls: 'pl-panel pl-panel-box pl-margin-small-all'
                    children: [
                        title =
                            type: 'div'
                            cls: 'pl-panel-title pl-margin-small-bottom'
                            children:
                                type: 'a'
                                title: set.name
                                href: "/demo/#{set.id}"
                        paragraph =
                            type: 'div'
                            cls: 'pl-text-muted'
                            title: set.desc
                    ]
            map.children.push group
    else
        map.children =
            type: 'div'
            cls: 'pl-width-1-1'
            children:
                type: 'div'
                cls: 'pl-container pl-container-center pl-margin-large-top pl-text-center'
                title: nodatasetsmsg
    # parse map
    @mapper.parseMapForParent map, contcenter

error = (code, result) ->
    result = JSON.parse result
    msg = if result.messages.length > 0 then result.messages[0] else "Something went wrong"
    @notificationcenter.change load, @notificationcenter.type.Error, msg, 3000, false, null, null


url = "/api/datasets"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
