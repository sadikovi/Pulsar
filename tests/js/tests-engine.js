var TestEngine = (function() {
    var id = "pulsar-tests";
    var table = null;
    var conditionRes = { "pass": "Pass", "fail": "Fail" };

    return {
        getTable: function() {
            if (table==null) {
                table = document.getElementById(id);
            }
            return table;
        },

        addAction: function(handler) {
            var btn = document.getElementById(id+"-run");
            if (btn) {
                if (btn.addEventListener) {
                    btn.addEventListener("click", handler, false);
                } else if (elem.attachEvent) {
                    btn.attachEvent("onclick", handler);
                }
            }
            return false;
        },

        validateTable: function() {
            return !!TestEngine.getTable();
        },

        clearTable: function() {
            if (TestEngine.validateTable()) {
                TestEngine.getTable().innerHTML = "";
            }
        },

        fillTable: function(tests) {
            if (!tests || !tests.length) {
                throw ("Tests are not an array");
            }

            if (!TestEngine.validateTable(id)) {
                throw ("Test table is not defined");
            }

            // clear table
            TestEngine.clearTable();

            for (var i=0; i<tests.length; i++) {
                var test = tests[i];
                TestEngine.buildTestRecord(test.num, test.desc, test.res, test.comment, TestEngine.getTable());
            }
        },

        buildTestRecord: function(num, desc, res, comment, parent) {
            var record = document.createElement("tr");
            TestEngine.buildConditionField(res, record, function(value, el) {
                if (value == conditionRes.pass) {
                    el.className = "label label-success";
                } else if (value == conditionRes.fail) {
                    el.className = "label label-danger";
                }
                return false;
            });
            TestEngine.buildTestField(num, record);
            TestEngine.buildTestField(desc, record);
            TestEngine.buildTestField(comment, record);
            parent.appendChild(record);
            return record;
        },

        buildTestField: function(value, parent) {
            var td = document.createElement("td");
            var sp = document.createElement("span");
            sp.innerHTML = value;
            td.appendChild(sp);
            td.className = "test-item";
            if (parent) {
                parent.appendChild(td);
            }
            return td;
        },

        buildConditionField: function(value, parent, func) {
            var t = TestEngine.buildTestField(value, parent);
            func.call(this, value, t);
        },

        buildTests: function() {
            var results = [];
            if (UnitTests && UnitTests.length) {
                for (var i=0; i<UnitTests.length; i++) {
                    var unittest = UnitTests[i];
                    var r = TestEngine.buildTest(unittest);
                    results.push(r);
                }
            } else {
                throw ("Unit tests do not exist!");
            }

            return results;
        },

        buildTest: function(unittest) {
            try {
                var t = unittest.func.call(this);
                if (t) {
                    return TestEngine.testResult(unittest.num, unittest.desc, true, "");
                } else {
                    return TestEngine.testResult(unittest.num, unittest.desc, false, "False is returned, test failed.");
                }
            } catch (e) {
                return TestEngine.testResult(unittest.num, unittest.desc, false, e.message||e);
            }
        },

        testResult: function(num, desc, isPassed, comment) {
            return { "num":num, "desc": desc, "res": (isPassed)?conditionRes.pass:conditionRes.fail, "comment":comment };
        },

        /* test functionality*/
        assert: function(res, outcome) {
            if (res === outcome) {
                return true;
            } else {
                throw ("Result: [" + res + "], expected: [" + outcome + "]");
            }
        }
    }
})();



// add action to the button
TestEngine.addAction(function(e) {
    var results = TestEngine.buildTests();
    TestEngine.fillTable(results);
});
