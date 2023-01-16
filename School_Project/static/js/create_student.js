const API_URL = "http://127.0.0.1:8000/api/v1/students";
console.log(JSON.stringify($('#id_course').val()));
//console.log($('.update-btn'));
 $('#update-btn').click(function () {
    const data ={
        "id":$("#id_input").val(),
        "firstname":$("#id_firstname").val(),
        "surname":$("#id_surname").val(),
        "age":$("#id_age").val(),
        "email":$("#id_email").val(),
        "group":$("#id_group").val(),
        "course": $('#id_course').val(),
        //"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
        //

    };
    console.log("PATCH")
    console.log(JSON.stringify(data))
    //console.log(JSON.parse(data))

    $.ajax({
        type: "PUT",
    //    contentType="application/json"
    //    dataType: "json",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/"+data.id+"/",
        data: data,
        success: function(data){
        console.log("PATCH-done"+data.course)
        }
    })


});

$("#get-btn").click(function (){
    const data ={
        "id":$("#id_input").val(),

    };
    console.log("GET"+data.id);
    console.log($('#id_course').val());
    $.getJSON(API_URL+"/"+data.id,function(dataJson){
    console.log(dataJson);
    $("#id_firstname").val(dataJson.firstname)
    $("#id_surname").val(dataJson.surname)
    $("#id_age").val(dataJson.age)
    $("#id_email").val(dataJson.email)
    $("#id_group").val(dataJson.group)
    $("#id_course").val(dataJson.course)


    });
});
$('#delete-btn').click(function(){
    const data ={
    "id":$("#id_input").val(),
    }
    console.log("DELETE")
    console.log(data)
    $.ajax({
        type: "DELETE",
        dataType: "json",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/"+data.id,
        success: function(data){
        console.log("DELETE-done");
        $("#id_firstname").val(null);
        $("#id_surname").val(null);
        $("#id_age").val(null);
        $("#id_email").val(null);
        $("#id_group").val(null);
        $("#id_course").val(null);
        }
    })
});

$('#create-btn').click(function(){
    const data ={
        "firstname":$("#id_firstname").val(),
        "surname":$("#id_surname").val(),
        "age":$("#id_age").val(),
        "email":$("#id_email").val(),
        "group":$("#id_group").val(),
        "course":'#id_course').val(),
    };
    console.log("POST");
    console.log(data);
    $.ajax({
        type: "POST",
        dataType: "json",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/",
        data: data,
        success: function(data){
        console.log("POST-done")
        }
    })
    });
