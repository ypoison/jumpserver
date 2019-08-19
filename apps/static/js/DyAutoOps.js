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
            toastr.success(msg);
        }
        $(".splash").hide();
        if (typeof props.success === 'function') {
            return props.success(data);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        var msg = "";
        if (user_fail_message) {
            msg = user_fail_message;
        } else if (jqXHR.responseJSON) {
            if (jqXHR.responseJSON.error) {
                msg = jqXHR.responseJSON.error
            } else if (jqXHR.responseJSON.msg) {
                msg = jqXHR.responseJSON.msg
            }
        }if (msg === "") {
            msg = default_failed_message;
        }
        toastr.error(msg);
        $(".splash").hide();
        if (typeof props.error === 'function') {
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

//云管中心拿oss列表函数
function GetOss(url, selected_source, source_type, selected_source_type) {
    if ($("#id_source_type").val() === 'oss') {
        var the_url = url
        var success = function (ret) {
            $("#id_sources").parent().html(
                '<select name="sources" class="form-control" title="" id="id_sources"> </select>'
            )
            if (ret.code != 0) {
                var data = ret['msg'];
                $.each(data, function (key, val) {
                    if (val === selected_source) {
                        $("#id_sources").append("<option value =" + val + " selected>" + val + "</option>")
                    } else {
                        $("#id_sources").append("<option value =" + val + " >" + val + "</option>")
                    }
                })
            }
        }
        DyAPIUpdateAttr({
            url: the_url, method: 'GET', success: success
        })
    } else {
        if (!selected_source){
            var selected_source = '1.1.1.1:20,2.1.1.1:30'
        }
        if (source_type === selected_source_type) {
            $("#id_sources").parent().html(
                '<input type="text" name="sources" value="' + selected_source + '" placeholder="1.1.1.1:20,2.1.1.1:30" ' +
                'maxlength="128" class="form-control" title="20为主，30为备；如：1.1.1.1:20,2.1.1.1:30；source1.dymis.com:20,source2.dymis.com:30" ' +
                'required="" id="id_sources">' +
                '<div class="help-block">20为主，30为备；如：1.1.1.1:20,2.1.1.1:30；source1.dymis.com:20,source2.dymis.com:30</div>'
            )
        } else {
            $("#id_sources").parent().html(
                '<input type="text" name="sources" placeholder="1.1.1.1:20,2.1.1.1:30" ' +
                'maxlength="128" class="form-control" title="20为主，30为备；如：1.1.1.1:20,2.1.1.1:30；source1.dymis.com:20,source2.dymis.com:30" ' +
                'required="" id="id_sources">' +
                '<div class="help-block">20为主，30为备；如：1.1.1.1:20,2.1.1.1:30；source1.dymis.com:20,source2.dymis.com:30</div>'
            )
        }
    }
}

//UTC转北京时间
function formatUTC(utc_datetime) {
    var beijing_datetime = new Date(+new Date(utc_datetime) + 8 * 3600 * 1000).toISOString().replace(/T/g, ' ').replace(/\.[\d]{3}Z/, '');
    return beijing_datetime;
}
