// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// overlay menu
function openNav() {
    document.getElementById("myNav").classList.toggle("menu_width");
    document.querySelector(".custom_menu-btn").classList.toggle("menu_btn-style");
}


/** google_map js **/

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// lightbox gallery
$(document).on("click", '[data-toggle="lightbox"]', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});


function updatePreview() {
    var metal = document.getElementById("metal").value;
    var stone = document.getElementById("stone").value;
    var size = document.getElementById("size").value;

    // Image Mapping
    var imageMap = {
        "gold-diamond": "https://raymondleejewelers.net/wp-content/uploads/2019/06/IMG_1220.jpg",
        "gold-ruby": "https://www.meenajewelers.com/thumbFull/images/9_22K_gold_necklace_1362.jpg",
        "gold-emerald": "https://th.bing.com/th/id/OIP.-7qv33rKsJGT8nBuSp_WrAHaDd?rs=1&pid=ImgDetMain",
        "silver-diamond": "https://i.pinimg.com/originals/05/a3/ee/05a3ee2e33b63d85bc3f5b97eda43e36.jpg",
        "silver-ruby": "https://th.bing.com/th/id/OIP.xCmsh2CYyHsYLz720W9e0QHaGk?rs=1&pid=ImgDetMain",
        "silver-emerald": "https://th.bing.com/th/id/OIP.AAZOvjTfrh-qzzVN3ai3vAHaHa?rs=1&pid=ImgDetMain",
        "platinum-diamond": "https://th.bing.com/th/id/OIP.rppLM5RPJfQXRH5neDLkNQHaHa?rs=1&pid=ImgDetMain",
        "platinum-ruby": "https://a.1stdibscdn.com/ruby-diamond-gold-bracelet-for-sale/j_4943/1535729711038/FV1309_V1_master.jpg?disable=upscale&auto=webp&quality=60&width=800",
        "platinum-emerald": "https://a.1stdibscdn.com/diamond-ruby-platinum-tennis-necklace-for-sale/j_5603/j_153360821649192574185/j_15336082_1649192574708_bg_processed.jpg"
    };

    // Price Mapping
    var priceMap = {
        "gold-diamond": 500,
        "gold-ruby": 450,
        "gold-emerald": 480,
        "silver-diamond": 400,
        "silver-ruby": 350,
        "silver-emerald": 370,
        "platinum-diamond": 600,
        "platinum-ruby": 550,
        "platinum-emerald": 580
    };

    // Update Image
    var selectedImage = imageMap[`${metal}-${stone}`] || "https://upload.wikimedia.org/wikipedia/commons/d/da/Gold-jewellery-jewel-henry-designs-terabass.jpg";
    document.getElementById("previewImage").src = "" + selectedImage;

    // Update Price
    var selectedPrice = priceMap[`${metal}-${stone}`] || 300;
    document.getElementById("priceTag").innerHTML = "Price: $" + selectedPrice;
}
