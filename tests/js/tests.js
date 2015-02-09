var unittest_groups_1 = function() {
    var t = Groups.groupPriority(50, 200);
    return TestEngine.assert(t, "A1");
}
var unittest_groups_2 = function() {
    var t = Groups.groupPriority(100, 200);
    return TestEngine.assert(t, "A2");
}
var unittest_groups_3 = function() {
    var t = Groups.groupPriority(350, 480);
    return TestEngine.assert(t, "A3");
}
var unittest_groups_4 = function() {
    var t = Groups.groupPriority(210, 200);
    return TestEngine.assert(t, "B1");
}
var unittest_groups_5 = function() {
    var t = Groups.groupPriority(220, 200);
    return TestEngine.assert(t, "B2");
}
var unittest_groups_6 = function() {
    var t = Groups.groupPriority(240, 200);
    return TestEngine.assert(t, "B3");
}
var unittest_groups_7 = function() {
    var t = Groups.groupPriority(300, 200);
    return TestEngine.assert(t, "C1");
}
var unittest_groups_8 = function() {
    var t = Groups.groupPriority(350, 200);
    return TestEngine.assert(t, "C2");
}
var unittest_groups_9 = function() {
    var t = Groups.groupPriority(600, 200);
    return TestEngine.assert(t, "C3");
}

var unittest_groups_10 = function() {
    var t = true;
    t = t && TestEngine.assert(Groups.getMainGroup("A1"), "A");
    t = t && TestEngine.assert(Groups.getMainGroup("B1"), "B");
    t = t && TestEngine.assert(Groups.getMainGroup("C1"), "C");
    t = t && TestEngine.assert(Groups.getMainGroup("A2"), "A");
    t = t && TestEngine.assert(Groups.getMainGroup("B3"), "B");
    t = t && TestEngine.assert(Groups.getMainGroup("C3"), "C");
    return t;
}

var unittest_groups_11 = function() {
    var t = true;
    t = t && TestEngine.assert(Groups.getSubgroupIndex("A1"), "1");
    t = t && TestEngine.assert(Groups.getSubgroupIndex("B2"), "2");
    t = t && TestEngine.assert(Groups.getSubgroupIndex("C3"), "3");
    return t;
}

var UnitTests = [

{ "num": 1, "desc": "Groups Priority test of group A1", "func": unittest_groups_1 },
{ "num": 2, "desc": "Groups Priority test of group A2", "func": unittest_groups_2 },
{ "num": 3, "desc": "Groups Priority test of group A3", "func": unittest_groups_3 },
{ "num": 4, "desc": "Groups Priority test of group B1", "func": unittest_groups_4 },
{ "num": 5, "desc": "Groups Priority test of group B2", "func": unittest_groups_5 },
{ "num": 6, "desc": "Groups Priority test of group B3", "func": unittest_groups_6 },
{ "num": 7, "desc": "Groups Priority test of group C1", "func": unittest_groups_7 },
{ "num": 8, "desc": "Groups Priority test of group C2", "func": unittest_groups_8 },
{ "num": 9, "desc": "Groups Priority test of group C3", "func": unittest_groups_9 },
{ "num": 10, "desc": "Test of the getting main group for subgroups", "func": unittest_groups_10 },
{ "num": 11, "desc": "Test of receiving subgroup index", "func": unittest_groups_11 }

];
