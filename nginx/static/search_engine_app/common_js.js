// =================== Common JS functions ======================
function updateURL(event, object_type) {
    var searchValue = document.getElementById("searchbox2").value; 
    var nodeDistance = 3

    if (object_type=='notebook') {
        var url = "../../notebooksearch/notebook_search?query=" + searchValue + "&page=1&filter=&facet="; 
    }
    else if (object_type=='dataset') {
        var url = "../../datasetsearch/dataset_search?query=" + searchValue + "&page=1&filter=&facet=";
    }
    else if (object_type=='graph') {
        var url = "../../graphvisualization/graph_visualization?query=" + searchValue + "&distance=" + nodeDistance;
    }

    channel_id = '#'+object_type+'_channel'

    // Update the href attribute of the <a> element
    $(channel_id).attr("href",url);

    sessionStorage.setItem("searchValue", searchValue);
    
}    

function selectObject(event, operation) {
    new_item = event.target

    if (operation=='select') {
        // Post the selected item to server to get reformulated query
        
        getReformulatedQuery(new_item.dataset.type, new_item.dataset.docid)
        // .then(reformed_query => {
        //     console.log(reformed_query);
        //     sessionStorage.setItem("reformulatedQuery", reformed_query);
        //     // document.getElementById('searchbox2').value = reformed_query;
        //     document.getElementById('task_button').value = reformed_query;
        //     document.getElementById('method_button').value = reformed_query;
        //     document.getElementById('dataset_button').value = reformed_query;

        // })
        .then(data => {
            console.log(data);
            sessionStorage.setItem("reformulatedQuery", data.reformed_query);
            // document.getElementById('searchbox2').value = reformed_query;
            document.getElementById('task_button').innerText = data.task;
            document.getElementById('method_button').innerText = data.method;
            document.getElementById('dataset_button').innerText = data.dataset;

        })
        .catch(error => console.error(error));

        // Clear other other selected item first
        var selected_item = document.getElementById("selected_item");
        console.log(selected_item)
        if (selected_item) {
            toggleSelection(selected_item, 'cancel', 'delete'); 
        }

        // Set new item to cancel status
        toggleSelection(new_item, 'select', 'add'); 

    }

    else if (operation=='cancel') {
        toggleSelection(new_item, 'cancel', 'delete'); 

        // Restore original query
        var original_query = sessionStorage.getItem("searchValue");
        document.getElementById('searchbox2').value = original_query; 
    }

}

function getReformulatedQuery(object_type, docid) {
    var url = `../select_${object_type}/`; 
    var query = sessionStorage.getItem("searchValue")
    var newEntity = {"query": query, "object_type": object_type, "docid": docid}; 

    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(newEntity)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        console.log(data.reformed_query);
        // return data.reformed_query;
        return data;

    })
    .catch(error => {
        console.error('Error:', error);
        return query;
    });
}


function modifyMyCart() {
    // Modify icon display
    $("#MyCartIcon").addClass('fa-bounce'); 
    setTimeout(function() {
        $("#MyCartIcon").removeClass('fa-bounce');
        }, 3000);

    // Modify item number
    cnt = document.querySelectorAll("#MyCart li").length - 1;
    $('#MyCartCount').text(cnt);

}

function modifyCartItems(data) {
    if (data['operation'] == 'add') {
        var ul = document.getElementById("MyCart");
        var li = document.createElement("li");
        var icon = "";
        if (data['type'] == 'notebook') {
            icon = '<i style="font-size:10pt; font-weight: bold; padding-right:5px;" class="ti-file"></i>';
        }
        else if (data['type'] == 'dataset') {
            icon = '<i style="font-size:10pt; font-weight: bold; padding-right:5px;" class="ti-server"></i>';
        }
        else if (data['type'] == 'Webpages') {
            icon = '<i style="font-size:10pt; font-weight: bold; padding-right:5px;" class="ti-world"></i>';
        }
        else if (data['type'] == 'WebAPIs') {
            icon = '<i style="font-size:10pt; font-weight: bold; padding-right:5px;" class="ti-control-shuffle"></i>';
        }

        var data_name = data['name']
        const maxLength = 36
        if (data_name.length > maxLength) {
            data["name"] = data_name.substring(0, maxLength) + '...';
        }
        data['operation'] == 'delete'; 
        li.innerHTML = '<div class="media">' +
            icon +
            '<div class="media-body">' +
            '<h5 class="notification-user"><a target="_blank" href="' + data['url'] + '">' + data['name'] + '</a> </h5>' +
            '</div>' +
            '<a href="#" onclick="modifyCartItems(' + data + ');"' +
            'style="font-size:8pt;  display:inline-block;"> <i class="ti-close"></i>' +
            '</a>' +
            '</div>';
        li.setAttribute("id", data['id']); // added line
        ul.appendChild(li);
    }
    else if (data['operation'] == 'delete') {
        $('#' + data['id']).remove();
    }
    modifyMyCart(); 
}