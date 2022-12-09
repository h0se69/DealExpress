xhrPool = [];
var pageId = 1

// Makes an ajax request to our api to get Amazon Products
function requestAmazonProduct(pageId, isReset){
    if(pageId === 1){
        $("#cardRowContainer").empty()
    }
    if(isReset === true){
        $("#cardRow").empty()
        pageId = 1;
    }
    searchInput = $("#searchBarID").val()
    if(searchInput === ""){
        searchInput = "electronics"
    }
    $.ajax({
        url: '/product-search/api/amazon/'+searchInput+ "/"+ pageId,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            $.each(JSON.parse(response), function(index, responseData){
                var asin = responseData[0]
                var title = responseData[1]
                var price = responseData[2]
                var imageURL = responseData[3]

                addProductCard(asin, title, price, imageURL)
            })
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}

//make ajax request to get best sellers page products
function requestBestSellerAmazonProducts(){
    $.ajax({
        url: '/product-search/api/amazon/bestsellers/',
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            $.each(JSON.parse(response), function(index, responseData){
                var asin = responseData[0]
                var title = responseData[1]
                var price = responseData[2]
                var imageURL = responseData[3]

                addProductCard(asin, title, price, imageURL)
            })
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}

function requestCategoryAmazonProducts(Category, pageId){
    $.ajax({
        url: '/product-search/api/amazon/'+Category+ "/"+ pageId,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            $.each(JSON.parse(response), function(index, responseData){
                var asin = responseData[0]
                var title = responseData[1]
                var price = responseData[2]
                var imageURL = responseData[3]

                addProductCard(asin, title, price, imageURL)
            })
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });

}

function addProductCard(asin, title, price, imageURL){
    $("#cardRowContainer").append(
        `<div class="card" style="min-height: 600px; max-height: 600px; width: 30%; margin-right: 2%; margin-top: 1%;overflow-y: auto;">
            <img class="card-img-top" src=${imageURL} alt=${title}_IMAGE>
            <div class="card-body">
                <p class="card-text">${title}</p>
                <p class="card-text">${asin}</p>
                <p class="card-text">Price: ${price}</p>
                <div class="btn-group">
                    <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#productModal" onclick='setModalData("`+asin+`", "`+ title +`", "` + price + `")'>View</button>
                    <button type="button" class="btn btn-sm btn-outline-secondary" onclick='passData("`+asin+`", "`+ title +`", "` + price + `")')>Add To Wishlist</button>
                </div>
                <br>
                <small class="text-muted">Checked at ${getCurrentTime()}</small>
            </div>
        </div>
    `)
}

function passData(Asin, Title, Price){
    var name = Title;
    var price = Price;
    var link = Asin;
    $.ajax(
    {
        method:'GET',
        url:'/addToWishlist' + "/" + name + "/" + price + "/" + link ,
        success:function(data) { 
            console.log(data)
            var reply=data;
            if(reply === "success"){
                alert("Saved to wishlist")
            }
            else{
                alert("Must be logged in")
            }
        }
    }
    )
}

// Sets the modal data 
// Title
// Call targetAPICall function
    // Call rakutenAPICall function
async function setModalData(Asin, Title, Price){
    $("#modalProductTitle").html(Title + "<br> <center>List of Retailers </center>")

    var productUPC = await requestAmazonProductUPC(Asin)
    addDealRow("Amazon", "", Price, "https://www.amazon.com/h0seFNF/dp/"+Asin, "NO", await rakutenAPICall("Amazon"))
    retailerAPICall(productUPC, Title, "Target")
    retailerAPICall(productUPC, Title, "eBay")
    // retailerAPICall(productUPC, Title, "BestBuy")
}

// Request product UPC
function requestAmazonProductUPC(productASIN){
    var apiResponse = null
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/api/get-upc/'+productASIN,
            method: "POST",
            beforeSend: function (jqXHR) {
                xhrPool.push(jqXHR);
            },
            success: function(response){
                // var response = JSON.parse(response)
                console.log("requestAmazonProductUPC: " + response['UPC'])
                apiResponse =  response['UPC']
                resolve(apiResponse)
            },
            error: function(response)
            {
                apiResponse =  response                
                resolve(apiResponse)
            }
        });
    });
}

function rakutenAPICall(retailer){
    var apiResponse = null
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: "/api/rakuten/get-cashback/" + retailer,
            method: "POST",
            beforeSend: function (jqXHR) {
                xhrPool.push(jqXHR);
            },
            success: function(response){
                apiResponse =  response['CashbackAmount']
                resolve(apiResponse)
            },
            error: function(response)
            {
                apiResponse =  "NONE_ER"                
                resolve(apiResponse)
            }
        });
    });
}

// Ajax Request to API for x Retailer and get data
async function retailerAPICall(productUPC, productTitle, retailerName){
    var cashbackAmount = await rakutenAPICall(retailerName)
    var urlTarget = '/product-search/api/' + retailerName + '/' + productUPC + "/"
    if(retailerName === "Target"){
        urlTarget = '/product-search/api/' + retailerName + '/' + productUPC + "/" + productTitle
    }
    $.ajax({
        url: urlTarget,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            var response = JSON.parse(response)
            var Title = response['Title']
            var Price = response['Price']
            var Link = response['Link']
            var onSale = "NO"
            addDealRow(retailerName, Title, Price, Link, onSale, cashbackAmount)
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}

// Add Deal Data to table *works with retailerAPICall*
function addDealRow(retailerName, Title, Price, Link, onSale, cashbackAmount){
    $("#productModalBody tbody").append(`
    <tr class="item" style="margin-left: 10%;">
        <td><a href=${Link} target="_blank">${retailerName}</a></td>
        <td>${Price && Link !== undefined ? Price: "NOT_AVAILABLE"}</td>
        <td>${Price && Link !== undefined ? onSale: "NOT_AVAILABLE"}</td>
        <td>${cashbackAmount}</td>
    </tr>`) 
}

// to fetch more products to display
function requestMoreProducts(){
    console.log(pageId)
    pageId = pageId + 1;
    console.log(pageId)
    console.log("space")
    requestAmazonProduct(pageId, false)
}

// Kill pending AJAX requests incase they are slow/timeout 
// Only functions when you close the modal
function killAjaxReq(){
    $.each(xhrPool, function(jqXHR) {
        $("#modalTable tbody").empty()
        console.log("Killed AJAX Requests")
        jqXHR.abort();
  });
}

function getCurrentTime(){
    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    if(today.getHours() > 11){
        return time + "PM"
    }
    else{
        return time + "AM"
    }
}