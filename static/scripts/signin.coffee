# data mapping
datamap =
    title: "signin-title"
    subtitle: "signin-subtitle"
    info: "signin-info"
    controls: "signin-controls"

# not authenticated data map
notauth =
    title: {classname: "", title: "Sign in with Google account"}
    subtitle: {classname: "", title: "We will also have to add you to the white list to play with demo"}
    info: {classname: "pl-text-muted", title: "Your email address will not be shared and will be used to log in to the website only"}
    controls: [
        {type: "a", classname: "pl-button pl-button-success", action: "/login", title: "Okay, let me in"},
        {type: "div", classname: "pl-display-inline-block pl-margin-small-all", title: ""},
        {type: "a", classname: "pl-button pl-button-danger", action: "/", title: "No, I don't trust you, guys"}
    ]

# not in whitelist data map
forbidden =
    title: {classname: "pl-text-success", title: "Request has been sent"}
    subtitle: {classname: "", title: "We will add you and send confirmation email as soon as possible"}
    info: {classname: "pl-text-muted", title: "Your email address will not be shared and will be used to log in to the website only"}
    controls: [
        {type: "a", classname: "pl-button", action: "mailto:ivan.sadikov@lincolnuni.ac.nz", title: "Didn't get email?"},
        {type: "div", classname: "pl-display-block pl-margin-all", title: ""},
        {type: "a", classname: "pl-button", action: "/logout", title: "I give up, log me out"}
    ]

# already has an access
# not in whitelist data map
hasaccess =
    title: {classname: "pl-text-success", title: "You have access"}
    subtitle: {classname: "", title: "Click below to try demo"}
    info: {classname: "pl-text-muted", title: "Having troubles to log in? Send an email"}
    controls: [
        {type: "a", classname: "pl-button pl-button-primary", action: "/demo", title: "Try demo"},
        {type: "div", classname: "pl-display-block pl-margin-all", title: ""},
        {type: "a", classname: "pl-button pl-button-link pl-link-muted", action: "mailto:ivan.sadikov@lincolnuni.ac.nz", title: "Send email"}
    ]

# util and processing functions
typeIsArray = Array.isArray or (value) -> return {}.toString.call(value) is '[object Array]'

changeItem = (item, element) ->
    [element.className, element.innerHTML] = [item.classname, item.title]
    element.href = item.action if element.tagName is "A"

buildItem = (item, element) ->
    result = document.createElement item.type
    changeItem item, result
    element.appendChild result

mapObjectToElement = (object, element, key) ->
    data = if key of object then object[key] else null
    return false if data is null or element is null
    # process data
    if typeIsArray data
        buildItem item, element for item in data
    else
        changeItem data, element

applyDatamap = (datamap, object) ->
    for key, value of datamap
        element = document.getElementById value
        mapObjectToElement object, element, key

# request processing functions
success = (code, result) ->
    applyDatamap datamap, hasaccess

error = (code, result) ->
    object = if code is 403 then forbidden else notauth
    applyDatamap datamap, object


url = "/api/accountinfo"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
