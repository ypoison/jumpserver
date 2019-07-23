function DyAPIUpdateAttr(props) {
    // props = {url: .., body: , success: , error: , method: ,}
    props = props || {};
    var user_success_message = props.success_message;
    var default_success_message = gettext('Update is successful!');
    var user_fail_message = props.fail_message;
    var default_failed_message = gettext('An unknown error occurred while updating..');
    var flash_message = props.flash_message || true;
    if (props.flash_message === false){
        flash_message = false;
    }
    $(".splash").show();
    $.ajax({
        url: props.url,
        type: props.method || "PATCH",
        data: props.body,
        contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json"
    }).done(function(data, textStatue, jqXHR) {
        if (flash_message) {
            var msg = "";
            if (user_success_message) {
                msg = user_success_message;
            } else if (jqXHR.responseJSON.msg) {
                msg = jqXHR.responseJSON.msg
            }
            if (msg === "") {
                msg = default_success_message;
            }
            $(".splash").hide();
            toastr.success(msg);
        }
        if (typeof props.success === 'function') {
            return props.success(data);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (flash_message) {
            var msg = "";
            if (user_fail_message) {
                msg = user_fail_message;
            } else if (jqXHR.responseJSON) {
                if (jqXHR.responseJSON.error) {
                    msg = jqXHR.responseJSON.error
                } else if (jqXHR.responseJSON.msg) {
                    msg = jqXHR.responseJSON.msg
                }
            }
            if (msg === "") {
                msg = default_failed_message;
            }
            $(".splash").hide();
            toastr.error(msg);
        }
        if (typeof props.error === 'function') {
            $(".splash").hide();
            console.log(jqXHR);
            return props.error(jqXHR.responseText, jqXHR.status);
        }
    });
  // return true;
}

function DySwalAjax(obj, name, url, method, data, redirectTo) {
    function doMethod() {
        var body = data
        if (!body){
            var body = {};
        }
        var success = function() {
            if (method == 'DELETE') {
                // swal('Deleted!', "[ "+name+"]"+" has been deleted ", "success");
                if (!redirectTo) {
                    $(obj).parent().parent().remove();
                } else {
                    window.location.href = redirectTo;
                }
            }
        };
        var fail = function() {
            // swal("错误", "删除"+"[ "+name+" ]"+"遇到错误", "error");
            swal(gettext('Error'), "[ "+name+" ]" + "遇到错误.", "error");
        };
        DyAPIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: method,
            success: success,
            error: fail
        });
    }
    swal({
        title: gettext('Are you sure?'),
        text: " [" + name + "] ",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: gettext('Cancel'),
        confirmButtonColor: "#ed5565",
        confirmButtonText: gettext('Confirm'),
        closeOnConfirm: true,
    }, function () {
        doMethod()
    });
}
