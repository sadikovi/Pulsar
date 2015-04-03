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

# classes for panels
panels = [
    'pl-panel-box-success'
    'pl-panel-box-warning'
    'pl-panel-box-error',
    'pl-panel-box-info',
    ''
]
norepmap =
    latest: null
# random uniform element from list
choice = (list, norepmap=false) ->
    return false if list.length == 0
    min = 0
    max = list.length - 1
    a = list[Math.floor(Math.random() * (max - min) + min)]
    if a == norepmap.latest
        a = choice list, norepmap
    else
        norepmap.latest = a
    a


success = (code, result) ->
    @notificationcenter.change load, @notificationcenter.type.Success, "Datasets are loaded", null, false, null, null
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
                cls: 'pl-width-1-1'
                children:
                    type: 'div'
                    cls: 'pl-container pl-container-center pl-panel-box-width-medium'
                    children:
                        type: 'div'
                        cls: 'pl-panel pl-panel-box pl-margin-small-all'
                        children: [
                            title =
                                type: 'div'
                                cls: 'pl-panel-title pl-margin-small-bottom'
                                children: [
                                    explore =
                                        type: 'a'
                                        cls: 'pl-button pl-button-primary'
                                        title: "Explore #{set.name}"
                                        href: "/demo/#{set.id}"
                                ]
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
    @notificationcenter.change load, @notificationcenter.type.Error, msg, null, false, null, null


url = "/api/datasets"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
