xhrPool = [];
var pageId = 1

// Makes an ajax request to our api to get Amazon Products
function requestAmazonProduct(pageID, isReset){
    $("#cardRowContainer").empty()

    if(isReset === true){
        $("#cardRow").empty()
        pageID = 1;
    }

    searchInput = $("#searchBarID").val()
    $.ajax({
        url: '/product-search/api/amazon/'+searchInput+ "/"+pageId,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            $.each(JSON.parse(response), function(index, responseData){
                var productTitle = responseData[1]
                var productASIN = responseData[2]

                $("#cardRowContainer").append(
                `<div class="card" style="min-height: 600px; max-height: 600px; width: 30%; margin-right: 2%; margin-top: 1%;overflow-y: auto;">
                    <img class="card-img-top" src=${responseData[0]} alt=${productTitle}>
                    <div class="card-body">
                        <p class="card-text">${productTitle}</p>
                        <p class="card-text">${productASIN}</p>
                        <p class="card-text">Price: ${responseData[4]}</p>
                        <div class="btn-group">
                            <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#productModal" onclick='setModalData("`+productASIN+`", "`+ productTitle + `")'>View</button>
                            <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                        </div>
                        <small class="text-muted">9 mins</small>
                    </div>
                </div>
                `)
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
                var productTitle = responseData[1]
                var productASIN = responseData[2]
                $("#cardRowContainer").append(
                `<div class="card" style="min-height: 600px; max-height: 600px; width: 30%; margin-right: 2%; margin-top: 1%;overflow-y: auto;">
                    <img class="card-img-top" src=${responseData[0]} alt=${productTitle}>
                    <div class="card-body">
                        <p class="card-text">${productTitle}</p>
                        <p class="card-text">${productASIN}</p>
                        <p class="card-text">Price: ${responseData[4]}</p>
                        <div class="btn-group">
                            <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#productModal" onclick='setModalData("`+productASIN+`", "`+ productTitle + `")'>View</button>
                            <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                        </div>
                        <small class="text-muted">9 mins</small>
                    </div>
                </div>
                `)
            })
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}


// Sets the modal data 
// Title
// Call targetAPICall function
    // Call rakutenAPICall function
async function setModalData(productASIN, productTitle){
    var productUPC = await requestAmazonProductUPC(productASIN)

    $("#modalProductTitle").html(productTitle + " |  List of Retailers")
    targetAPICall(productUPC, productTitle)
    ebayAPICall(productUPC, productTitle)
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

// Request target product based on productUPC
async function targetAPICall(productUPC, productTitle){
    var cashbackAmount = await rakutenAPICall("Target")
    $.ajax({
        url: '/product-search/api/target/'+productUPC+ "/"+productTitle,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            var response = JSON.parse(response)
            var sku = response['sku']
            var price = response['price']
            console.log(response['sku'])
            console.log(response['price'])
            if(price && sku !== undefined){
                $("#productModalBody tbody").append(`
                    <tr class="item" style="margin-left: 10%;">
                        <td><a href="https://www.target.com/p/h0seFNF/A-${sku}" target="_blank">Target</a></td>
                        <td>${price}</td>
                        <td>NO</td>
                        <td>${cashbackAmount}</td>
                    </tr>`)
            }
            else{
                $("#productModalBody tbody").append(`
                <tr class="item" style="margin-left: 10%;">
                    <td>Target</td>
                    <td>NOT_AVAILABLE</td>
                    <td>NOT_AVAILABLE</td>
                    <td>${cashbackAmount}</td>
                </tr>`)
            }
            
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}

// Request ebay product based on productUPC
async function ebayAPICall(productUPC, productTitle){

    // NEED TO ADD PRODUCT TITLE CHECK IN EBAY FILE[0]

    var cashbackAmount = await rakutenAPICall("eBay")
    $.ajax({
        url: '/product-search/api/ebay/'+ productUPC,
        method: "POST",
        beforeSend: function (jqXHR) {
            xhrPool.push(jqXHR);
        },
        success: function(response){
            var response = JSON.parse(response)
            if(response !== undefined){
                var productLink = response[0]['Link']
                var price = response[0]['Price']
                $("#productModalBody tbody").append(`
                    <tr class="item" style="margin-left: 10%;">
                        <td><a href="${productLink}" target="_blank">eBay</a></td>
                        <td>${price}</td>
                        <td>NO</td>
                        <td>${cashbackAmount}</td>
                    </tr>`)
            }
            else{
                $("#productModalBody tbody").append(`
                <tr class="item" style="margin-left: 10%;">
                    <td>eBay</td>
                    <td>NOT_AVAILABLE</td>
                    <td>NOT_AVAILABLE</td>
                    <td>${cashbackAmount}</td>
                </tr>`)
            }
            
        },
        error: function(response){
            console.log('ERROR_' + response)
        }
    });
}



// Once the user scrolls to the bottom it makes another call to requestAmazonProduct
// to fetch more products to display
$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
        console.log("BOTTOM OF PAGE MAKE AJAX REQ")
        pageID = pageID + 1;
        requestAmazonProduct(pageID, false)
    }
});

// Kill pending AJAX requests incase they are slow/timeout 
// Only functions when you close the modal
function killAjaxReq(){
    $.each(xhrPool, function(jqXHR) {
        $("#modalTable tbody").empty()
        console.log("Killed AJAX Requests")
        jqXHR.abort();
  });
}