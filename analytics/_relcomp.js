(function() {
    // array must be sorted
    //var a = [120, 122, 130, 250, 300];
    //var a = [1, 2, 2.2, 3, 3.2, 4, 5];
    var a = [2.31, 2.32, 2.35, 2.36, 2.40, 2.41, 3];
    var m = 2;

    var alpha = function() {
        return 1;
    }

    var beta = function(a, k, d) {
        if (k<0 || k>1) { throw ("k must be in [0, 1]"); }
        if (k == 0) {
            return 1/(1 + d*Math.exp(1-a));
        } else if (k == 1) {
            return 0;
        } else {
            return 1/(1 + Math.exp(a/(1-k) + d + 1));
        }
    }

    var k = function(r, rmax, rm, da) {
        if (r <= rm) {
            //return r*1.0/rm;
            return -(r*r)/(rm*rm) + 2*r/rm;
        } else {
            //return (r-rmax)*1.0 / (rm-rmax);
            return Math.exp(0.2*(rm-r)/da);
        }
    }

    var delta = function(dr, da) {
        return dr / da;
    }

    var dr = function(r, rm, i, m) {
        return (m==i)?0:Math.abs((r-rm)/(m-i))*Math.exp(Math.abs(m-i));
    }

    var da = function(array) {
        var dai = 0, _i=0;
        for (_i=1; _i<array.length; _i++) {
            dai += array[_i] - array[_i-1];
        }
        return dai/(array.length-1);
    }

    var map = {};
    for (var _i=0; _i<a.length; _i++) {
        var ki = k(a[_i], a[a.length-1], a[m], da(a));
        var ai = alpha();
        var di = delta(dr(a[_i], a[m], _i, m), da(a));
        var bi = beta(ai, ki, di);
        console.log(a[_i] + "-> " + bi);
        rank = ai*ki + bi;
        map[""+a[_i]] = Math.floor(rank*1000)/1000
    }

    console.log(map);
})();
