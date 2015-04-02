container_id = 'content-main'
container = document.getElementById container_id
return false unless container


# not authenticated data map
notauth = [
    frame =
        type: 'div'
        cls: 'pl-text-center'
        children: [
            htitle =
                type: 'h2'
                title: 'Sign in with Google account'
            hsubtitle =
                type: 'div'
                title: 'We will also have to add you to the white list to play with demo'
            info =
                type: 'small'
                cls: 'pl-text-muted'
                title: 'Your email address will not be shared and will be used to log in to the website only'
        ]
    controls =
        type: 'div'
        cls: 'pl-margin-large-top pl-text-center'
        children: [
            ok =
                type: 'a'
                title: 'Okay, let me in'
                cls: 'pl-button pl-button-success'
                href: '/login'
            divr =
                type: 'div'
                cls: 'pl-display-inline-block pl-margin-small-all'
            cancel =
                type: 'a'
                title: 'No, I don\'t trust you, guys'
                cls: 'pl-button pl-button-danger'
                href: '/'
        ]
]

# not in whitelist data map
forbidden = [
    frame =
        type: 'div'
        cls: 'pl-text-center'
        children: [
            htitle =
                type: 'h2'
                cls: 'pl-text-success'
                title: 'Request has been sent'
            hsubtitle =
                type: 'div'
                title: 'We will add you and send confirmation email as soon as possible'
            info =
                type: 'small'
                cls: 'pl-text-muted'
                title: 'Your email address will not be shared and will be used to log in to the website only'
        ]
    controls =
        type: 'div'
        cls: 'pl-margin-large-top pl-text-center'
        children: [
            ok =
                type: 'a'
                title: 'Didn\'t get email?'
                cls: 'pl-button'
                href: 'mailto:ivan.sadikov@lincolnuni.ac.nz'
            divr =
                type: 'div'
                cls: 'pl-display-inline-block pl-margin-small-all'
            cancel =
                type: 'a'
                title: 'I give up, log me out'
                cls: 'pl-button'
                href: '/logout'
        ]
]

# already has an access
# not in whitelist data map
hasaccess = [
    frame =
        type: 'div'
        cls: 'pl-text-center'
        children: [
            htitle =
                type: 'h2'
                cls: 'pl-text-success'
                title: 'You have access'
            hsubtitle =
                type: 'div'
                title: 'Click below to try demo'
            info =
                type: 'small'
                cls: 'pl-text-muted'
                title: 'Having troubles to log in? Send an email'
        ]
    controls =
        type: 'div'
        cls: 'pl-margin-large-top pl-text-center'
        children: [
            ok =
                type: 'a'
                title: 'Try demo'
                cls: 'pl-button pl-button-primary'
                href: '/demo'
            divr =
                type: 'div'
                cls: 'pl-display-block pl-margin-all'
            cancel =
                type: 'a'
                title: 'Send email'
                cls: 'pl-button pl-button-link pl-link-muted'
                href: 'mailto:ivan.sadikov@lincolnuni.ac.nz'
        ]
]

# request processing functions
success = (code, result) ->
    @mapper.parseMapForParent hasaccess, container

error = (code, result) ->
    object = if code is 403 then forbidden else notauth
    @mapper.parseMapForParent object, container


url = "/api/accountinfo"
method = "get"
headers = {}
payload = null
# make api call
@loader.sendrequest method, url, headers, payload, success, error
