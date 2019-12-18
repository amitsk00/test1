
var myStr = " .. ....";
var z_name = "";
var z_price = "";
var z_descr = "";

function showResult() {
    var para = document.createElement("p");
    para.innerText = myStr;
    document.getElementById("z_results").appendChild(para);
}

function valPrice() {

    let strErrPrice = "";

    if (typeof z_price != 'number') {
        strErrPrice += "Price is not a number.";
        isValid = false;
        document.getElementById("z_price").focus();
    }

    if (z_price < 1) {
        strErrPrice += " Price too low.";
        isValid = false;
        document.getElementById("z_price").focus();
    }
    if (z_price == 0) {
        strErrPrice += " Price is needed.";
        isValid = false;
        document.getElementById("z_price").focus();
    }

    z_price_error.innerText = strErrPrice;
}

function validateData() {

    var isValid = true;

    console.log(document.getElementById("z_name").innerHTML);

    z_name = document.getElementById("z_name").innerText;
    z_price = document.getElementById("z_price").innerText;
    z_descr = document.getElementById("z_descr").innerText;

    console.log("Name is " + z_name);

    z_name_error = document.getElementById("z_name_error");
    z_price_error = document.getElementById("z_price_error");
    z_descr_error = document.getElementById("z_descr_error");

    if (z_name === "") {
        z_name_error.innerText = "Name is needed";
        isValid = false;
        document.getElementById("z_name").focus();
    }

    valPrice();

    // call other functions to check data


    if (isValid === true) {
        myStr += "validation success, PHP will be called";
        // PHP called for backend execution
        /*
        $.ajax({
            url: "mytest1.php",
            type: "POST",
            success: function (result) {
                alert(result)
            }
        }) */
    }
    else {
        myStr += "validation failed, check the errors";
    }

    console.log(myStr);
    document.getElementById("z_final").innerHTML = myStr;
    document.getElementById("z_final").innerText = myStr;

    document.querySelector("p2").innerHTML = myStr;

}

var currStr = "From JavaScript";
currStr = "<p> " + currStr + " at -" + new Date() + " </p>";
console.log(myStr);
document.querySelector("footer").innerHTML = currStr;

