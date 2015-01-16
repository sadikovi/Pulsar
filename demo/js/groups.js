// Groups for classification
// has 3 groups with each group having 3 subgroups:
//      A: [A1, A2, A3]
//      B: [B1, B2, B3]
//      C: [C1, C2, C3]
// each group has rank that means how good the group is
var Groups = (function() {
    var Rates = { "GROUP_ACC": 0.20, "SUB_MIN": 0.25, "SUB_MAX": 0.6 };
    var groups = [
        { "name": "A1", "rank": 900 },
        { "name": "A2", "rank": 800 },
        { "name": "A3", "rank": 700 },

        { "name": "B1", "rank": 600 },
        { "name": "B2", "rank": 500 },
        { "name": "B3", "rank": 400 },

        { "name": "C1", "rank": 300 },
        { "name": "C2", "rank": 200 },
        { "name": "C3", "rank": 100 }
    ];

    return {
        getRates: function() {
            return Rates;
        },

        // return group for a particular value
        groupPriority: function(value, rValue) {
            var diff = rValue-value, accdiff = (1+Rates.GROUP_ACC)*rValue-value;
            var subgroup = function(val, min, max) {
                if (min === null || max === null) {
                    throw ("subgroup cannot be calculated");
                }

                if (val >= min && val <= max) {
                    var t = (val-min)*1.0/(max-min);
                    if (t <= Rates.SUB_MIN) {
                        return "1";
                    } else if (t > Rates.SUB_MIN && t <= Rates.SUB_MAX) {
                        return "2";
                    } else {
                        return "3";
                    }
                } else {
                    if (val <= (1+Rates.SUB_MIN)*min) {
                        return "1";
                    } else if (val > (1+Rates.SUB_MIN)*min && val <= (1+Rates.SUB_MAX)*min) {
                        return "2";
                    } else {
                        return "3";
                    }
                }
            }

            if (diff >= 0) {
                // assign group A
                return "A"+subgroup(value, 0, rValue);
            } else if (diff < 0 && accdiff >= 0) {
                // assign group B
                return "B"+subgroup(value, rValue, (1+Rates.GROUP_ACC)*rValue);
            } else {
                // assign group C
                return "C"+subgroup(value, (1+Rates.GROUP_ACC)*rValue, -1);
            }
        },

        getMainGroup: function(group) {
            if (group) {
                return (!group[0])?null:group[0];
            } else {
                return null;
            }
        },

        getSubgroupIndex: function(subgroup) {
            if (subgroup) {
                return (!subgroup.substring(1))?null:subgroup.substring(1);
            } else {
                return null;
            }
        }
    }
})();
