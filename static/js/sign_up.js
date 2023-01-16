document.getElementsByClassName("ClientOn")[0].style.display = "none";
document.getElementsByClassName("ClientOn")[1].style.display = "none";
document.getElementById("SupplierAsUser").onclick = ()=>{
    document.getElementById("SupplierAsUser").checked=true
    document.getElementById("ClientAsUser").checked=false
    document.getElementsByClassName("ClientOn")[0].style.display = "none";
    document.getElementsByClassName("ClientOn")[1].style.display = "none";
    document.getElementsByClassName("SupplierOn")[0].style.display = "block";
    document.getElementsByClassName("SupplierOn")[1].style.display = "block";
}
document.getElementById("ClientAsUser").onclick = ()=>{
    document.getElementById("SupplierAsUser").checked=false
    document.getElementById("ClientAsUser").checked=true
    document.getElementsByClassName("SupplierOn")[0].style.display = "none";
    document.getElementsByClassName("SupplierOn")[1].style.display = "none";
    document.getElementsByClassName("ClientOn")[0].style.display = "block";
    document.getElementsByClassName("ClientOn")[1].style.display = "block";
}
