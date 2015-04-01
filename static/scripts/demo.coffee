notcenter_id = "cbr-notification-content"
notcenter = document.getElementById notcenter_id
if notcenter is null
    console.log "Notification center is not found"
    return false

content_id = "cbr-content-main"
contentcenter = document.getElementById content_id
if contentcenter is null
    console.log "Content center is not found"
    return false

# no datasets message
nomsg = "No datasets to explore :-|"
# create notification for loading
load = NotificationCenter.show NotificationType.Info, "Load datasets...", -1, true, null, null, notcenter

success = (code, result) ->
    msg = "Datasets are loaded"
    NotificationCenter.change load, NotificationType.Success, msg, 3000, false, null, null
    # convert into json
    datasets = (JSON.parse result).data
    # create grid
    grid = document.createElement "div"
    grid.className = "pl-grid"
    contentcenter.appendChild grid
    # depending on datasets create panels
    if datasets.length > 0
        # create panels to display datasets
        for set in datasets
            group = document.createElement "div"
            group.className = "pl-width-1-3"
            grid.appendChild group

            panel = document.createElement "div"
            panel.className = "pl-panel pl-panel-box pl-margin-small-all"
            group.appendChild panel

            titlediv = document.createElement "div"
            titlediv.className = "pl-panel-title pl-margin-small-bottom"
            panel.appendChild titlediv

            title = document.createElement "a"
            [title.href, title.className, title.innerHTML] = ["/demo/#{set.id}", "", set.name]
            titlediv.appendChild title

            paragraph = document.createElement "div"
            [paragraph.className, paragraph.innerHTML] = ["pl-text-muted", set.desc]
            panel.appendChild paragraph
    else
        # create one panel telling that there is no datasets
        group = document.createElement "div"
        group.className = "pl-width-1-1"
        grid.appendChild group
        panel = document.createElement "div"
        [panel.className, panel.innerHTML] = ["pl-container pl-container-center pl-margin-large-top pl-text-center", nomsg]
        group.appendChild panel


changeItem = (item, element) ->
    [element.className, element.innerHTML] = [item.classname, item.title]
    element.href = item.action if element.tagName is "A"

buildItem = (item, element) ->
    result = document.createElement item.type
    changeItem item, result
    element.appendChild result


error = (code, result) ->
    result = JSON.parse result
    msg = if result.messages.length > 0 then result.messages[0] else "Something went wrong"
    NotificationCenter.change load, NotificationType.Error, msg, 3000, false, null, null


url = "/api/datasets"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
