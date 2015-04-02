class Mapper
    constructor: ->

    # just creates element and assigns to parent
    createElement: (type, parent) ->
        t = document.createElement type
        parent.appendChild t

    # parses map for parent specified
    # does not do anything, if map or parent is undefined
    parseMapForParent: (map, parent) ->
        # mappers
        mprs =
            type: 'type'
            cls: 'cls'
            title: 'title'
            href: 'href'
            children: 'children'
        # return of something is wrong
        return false unless map and parent
        # map can be object or array
        if mprs.type of map
            # create object and add to parent
            c = @.createElement map[mprs.type], parent
            c.className = map[mprs.cls] unless mprs.cls not of map
            c.innerHTML = map[mprs.title] unless mprs.title not of map
            c.href = map[mprs.href] unless mprs.href not of map
            @parseMapForParent map[mprs.children], c if mprs.children of map
        else
            @parseMapForParent item, parent for item in map

# create global mapper
@mapper ?= new Mapper
