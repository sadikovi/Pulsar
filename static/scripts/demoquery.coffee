# content
content_id = "cbr-content-main"
container = document.getElementById content_id
return false unless container
# notifications
notcenter_id = "cbr-notification-content"
notcenter = document.getElementById notcenter_id
return false unless notcenter
# menu
menupanel_id = "cbr-menu"
menupanel = document.getElementById menupanel_id
return false unless menupanel
# extract dataset id
dataset_holder = document.getElementById "cbr-dataset-id"
# store dataset
dataset = dataset_holder.value

# create notification for loading
load = @notificationcenter.show @notificationcenter.type.Info, "Loading datasets...", -1, true, null, null, notcenter

rankByName = (rankname) ->
    # top ranks
    return "rank-o" if rankname == "O"
    return "rank-b" if rankname == "B"
    return "rank-a" if rankname == "A"
    # medium ranks
    return "rank-f" if rankname == "F"
    return "rank-g" if rankname == "G"
    return "rank-k" if rankname == "K"
    # low ranks
    return "rank-m" if rankname == "M"
    return "rank-l" if rankname == "L"
    return "rank-t" if rankname == "T"

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
        cls: "ui comments"
        children: [
            header =
                type: "h3"
                cls: "ui dividing header"
                title: "Elements"
        ]
    # collect elements
    for element in result.data.elements
        #features
        features = []
        for feature in element.features
            feat =
                type: "a"
                cls: "reply"
                title: "#{feature.name}: #{feature.value}"
            features.push feat
        # cluster attributes
        clustername = if element.cluster then element.cluster.name else "Undefined"
        clusterid = if element.cluster then element.cluster.id else ""
        rankcolor = rankByName element.rank.name
        # element
        element =
            type: "div"
            cls: "comment"
            children: [
                rank =
                    type: "a"
                    cls: "avatar"
                    children:
                        type: "div"
                        cls: "circular ui icon button #{rankcolor}"
                data =
                    type: "div"
                    cls: "content"
                    children: [
                        elementname =
                            type: "a"
                            id: "#{element.id}"
                            cls: "author"
                            title: "#{element.name}"
                        cluster =
                            type: "div"
                            cls: "metadata"
                            children:
                                type: "a"
                                cls: "reply"
                                id: "#{clusterid}"
                                title: "Cluster: #{clustername}"
                        desc =
                            type: "div"
                            cls: "text"
                            title: "#{element.desc}"
                        featurespanel =
                            type: "div"
                            cls: "actions"
                            children: features
                    ]
            ]
        map.children.push element
    # parse map
    @mapper.parseMapForParent map, container

    # build pulses
    map = []
    for pulse in result.data.pulses
        element = null
        if pulse.isstatic
            options = []
            # all option
            alloption =
                type: "option"
                title: "All"
            if not pulse.default
                alloption.selected = true
            options.push alloption
            # rest of the values
            for value in pulse.store
                valueelement =
                    type: "option"
                    title: "#{value}"
                if value == pulse.default
                    valueelement.selected = true
                options.push valueelement
            # element
            element =
                type: "div"
                cls: "pl-margin-top pl-margin-bottom"
                children: [
                    label =
                        type: "div"
                        cls: "ui label"
                        title: "#{pulse.name}"
                    select =
                        type: "select"
                        cls: "ui small dropdown"
                        children: options
                ]
        else
            element =
                type: "div"
                cls: "pl-margin-top pl-margin-bottom"
                children:
                    type: "div"
                    cls: "ui labeled small input"
                    children: [
                        label =
                            type: "div"
                            cls: "ui blue label"
                            title: "#{pulse.name}"
                        input =
                            type: "input"
                            inputtype: "text"
                            inputvalue: "#{pulse.default}"
                    ]
        map.push element
    # add search button
    searchbutton =
        type: "a"
        cls: "pl-button pl-button-primary"
        title: "Search"
    map.push searchbutton
    # parse map
    @mapper.parseMapForParent map, menupanel

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
