$(function() {
    let td = "";
    for (var i = 0; i < 5; i++) {
        for (var j = 0; j < 5; j++) {
            if (i == j) {
                td = td + "<td><input placeholder=1 disabled></td>";
            }
            if (i < j) {
                td = td + "<td><input></td>";
            }
            if (i > j) {
                td = td + "<td><input disabled></td>";
            }
        }
    }
    document.getElementById("demotd").innerHTML = td;

});

                                                