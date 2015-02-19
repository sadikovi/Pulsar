class Selector(object):
    """
        Selector class performs filtering of the coming data. For example, if
        there are @GroupsMap, @ResultsMap, and @PropertiesMap coming into the
        class, then on the other end those maps will be modified + algorithm is
        added. Thus, there are four instances to manage.


        GroupsMap--------|                    |----> GroupsMap'
        ResultsMap-------|  --> Selector -->  |----> ResultsMap'
        PropertiesMap----|                    |----> PropertiesMap'
                                              |----> Algorithm

        To do this, selector receives DML queries to perform on those maps. For
        instance, to filter groups by id:
    """
