var vm = avalon.define({
    $id: "list",
    keyword: "",
    $load: function() {
        console.log("load");
        $.ajax({
            url: "/list",
            type: "GET",
            data: {"keyword": vm.keyword},
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        }).done(function(data) {
            vm.reply_list = data;
        });
    },
    $add: function() {
        console.log("start add");
        var keyword = $("#add-keyword").val();
        var content = $("#add-content").val();
        $.post("/add", {"keyword": keyword, "content": content}, function(data) {
            console.log("add finished");
            $("#add-section").addClass("hidden");
            vm.$load();
        });
    },
    $fork: function () {
        console.log("start delete")
        var replyid = $(this).attr("replyid");
        $.post("/delete", {"replyid": replyid}, function (data) {
            vm.$load();
        })
    },
    $update: function() {
        console.log("start update");
        var replyid = $("#edit-replyid").val();
        var keyword = $("#edit-keyword").val();
        var content = $("#edit-content").val();
        $.post("/add", {"replyid": replyid, "keyword": keyword, "content": content}, function(data) {
            console.log("update finished")
            $("#edit-section").addClass("hidden");
            vm.$load();
        })
    },
    reply_list: [],
});

$(function() {
    avalon.scan();
    vm.$load();
})