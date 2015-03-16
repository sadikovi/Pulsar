/*
Copyright 2015 Ivan Sadikov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/


// pareto frontier
var pf = (function() {
    return {
        /* function to compare two elements for n features */
        compare: function(a, b, n) {
            var _less = true, _greater = true, _i = 0;
            for (_i=0; _i<n; _i++) {
                _less = _less && (a[_i] <= b[_i]);
                _greater = _greater && (a[_i] >= b[_i]);
            }
            return _less?-1:(_greater?1:0);
        },
        /* helper function to remove elements, returns new array */
        remove: function(a, indices) {
            var temp = [], _i = 0;
            for (_i=0; _i<indices.length; _i++) {
                a.splice(indices[_i], 1, null);
            }
            for (_i=0; _i<a.length; _i++) {
                if (a[_i] != null) { temp.push(a[_i]); }
            }
            return temp;
        },
        /* return groups of the pareto frontier
           using array "a" and number of element's features "n" */
        frontier: function(a, n) {
            if (a.length == 0) {
                throw ('Array is empty')
            }
            // copy array
            a = this.remove(a, []);
            // storage for groups of elements
            var storage = [];
            // sort data into buckets
            while (a.length > 0) {
                // add first element into group
                var group = [0];
                // for each element in array match with group
                for (var i=0; i<a.length; i++) {
                    var del = [], isPush = true, isDel = false, res = 0;
                    for (var j=0; j<group.length; j++) {
                        res = this.compare(a[i], a[group[j]], n);
                        if (res < 0) {
                            isPush = false;
                        } else if (res > 0) {
                            del.push(j);
                        }
                        isPush = isPush && true;
                    }
                    if (isPush) {
                        // add element to the group
                        group.push(i);
                        // remove any elements that have been replaced by it
                        group = this.remove(group, del);
                    }
                }
                // retrieve elements from indices of group
                var convGroup = [], temp = [], i=0;
                for (i=0; i<group.length; i++) {
                    convGroup.push(a[group[i]]);
                }
                // push to storage
                storage.push(convGroup);
                // remove elements from a
                a = this.remove(a, group);
            }
            return storage;
        }
    }
})();

(function() {
    // number of properties
    var n = 3;
    // array with properties
    var array = [
        [0.95, 0.80, 0.42],
        [0.94, 0.90, 0.21],
        [0.50, 0.75, 0.99],
        [0.39, 0.91, 0.12],
        [0.78, 0.90, 0.80],
        [0.23, 0.45, 0.12],
        [0.98, 0.81, 0.91],
        [0.91, 0.21, 0.87]
    ];
    // remove duplicate elements
    var hash = "", i = 0, j = 0, map = {}, temp = [];
    for (i=0; i<array.length; i++) {
        hash = "";
        for (j=0; j<n; j++)
            hash += array[i][j] + "";
        if (!map.hasOwnProperty(hash)) {
            map[hash] = true;
            temp.push(array[i]);
        }
    }
    array = temp;
    // get ranked groups
    var storage = pf.frontier(array, n);
    // display result
    console.log("Done!");
    console.log(array);
    console.log(storage);
})();
