# content
content_id = "cbr-content-main"
container = document.getElementById content_id
return false unless container
# notifications
notcenter_id = "cbr-notification-content"
notcenter = document.getElementById notcenter_id
return false unless notcenter
# extract dataset id
dataset_holder = document.getElementById "cbr-dataset-id"
# store dataset
dataset = dataset_holder.value

# create notification for loading
load = @notificationcenter.show @notificationcenter.type.Info, "Loading datasets...", -1, true, null, null, notcenter

success = (code, result) ->
    result = JSON.parse result
    msg = "Everything is loaded"
    @notificationcenter.change load, @notificationcenter.type.Success, msg, 10000, false, null, (()->)
    # display warnings received
    for item in result.messages
        @notificationcenter.show @notificationcenter.type.Warning, item, 10000, false, null, (()->), notcenter
    # build template
    map =
        type: "div"
        cls: "pl-grid"
        children: []
    # collect elements
    for element in result.data.elements
        #features
        features = []
        for feature in element.features
            f =
                type: "div"
                cls: "pl-display-inline-block pl-margin-small-left pl-margin-small-right"
                title: "#{feature.name}: #{feature.value}"
            features.push f
        # cluster attributes
        clustername = if element.cluster then element.cluster.name else "Undefined"
        clusterid = if element.cluster then element.cluster.id else ""
        # element
        element =
            type: "div"
            cls: "pl-width-1-1"
            children:
                type: "div"
                id: "#{element.id}"
                cls: "pl-panel pl-panel-box pl-margin-small-all"
                children: [
                    header =
                        type: "div"
                        cls: "pl-panel-title"
                        children: [
                            rank =
                                type: "span"
                                cls: "pl-margin-small-left pl-margin-small-right"
                                title: "rank: #{element.rank.name}"
                            title =
                                type: "span"
                                cls: "pl-margin-small-left pl-margin-small-right"
                                title: "#{element.name}"
                            cluster =
                                type: "a"
                                id: "#{clusterid}"
                                cls: "pl-margin-small-left pl-margin-small-right"
                                title: "#{clustername}"
                        ]
                    paragraph =
                        type: "div"
                        cls: "pl-text-muted"
                        title: "#{element.desc}"
                    features = features
                ]
        map.children.push element
    # parse map
    @mapper.parseMapForParent map, container

error = (code, result) ->
    result = JSON.parse result
    msg = if result.messages.length > 0 then result.messages[0] else "Something went wrong"
    @notificationcenter.change load, @notificationcenter.type.Error, msg, 10000, false, null, (()->)


sendQueryWithParameters = (dataset, query, issorted, iswarn) ->
    # prepare api parameters
    url = "/api/query?d=#{dataset}&q=#{query}&s=#{issorted}&w=#{iswarn}"
    method = "get"
    headers = {}
    payload = null
    # make api call
    @loader.sendrequest method, url, headers, payload, success, error

sendQueryWithParameters dataset, "", true, true
