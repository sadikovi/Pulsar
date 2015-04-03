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
        element =
            type: "div"
            cls: "pl-width-1-1"
            children:
                type: "div"
                id: "#{element.id}"
                cls: "pl-panel pl-panel-box pl-margin-small-all"
                children: [
                    title =
                        type: "div"
                        cls: "pl-panel-title"
                        title: "#{element.name}"
                    paragraph =
                        type: "div"
                        cls: "pl-text-muted"
                        title: "#{element.desc}"
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
