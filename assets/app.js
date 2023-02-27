
document.addEventListener("click", (e) => {

    console.log(e.target)

    if (e.target.id === "openNav") {
        openNav()
    }
    if (e.target.className === "closebtn") {
        closeNav()
    }
})

// const hola = document.getElementById("upload-data")
// btnAbrir.addEventListener("click", openNav)

function openNav() {
    document.getElementById("mySidebar").style.width = "300px";
    document.getElementById("header").style.marginLeft = "300px";
    // document.getElementById("contenedor").style.marginLeft = "250px";
    // document.getElementById("alggo").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("header").style.marginLeft = "0";
    // document.getElementById("contenedor").style.marginLeft = "0";
    document.getElementById("alggo").style.marginLeft = "3rem";
}

