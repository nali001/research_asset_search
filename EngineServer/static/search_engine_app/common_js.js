// =================== Common JS functions ======================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

    localStorage.setItem("channel", object_type);
    channel_id = '#'+object_type+'_channel'
    sessionStorage.removeItem("parsed_augment_terms");
    // Update the href attribute of the <a> element
    $(channel_id).attr("href",url);

    sessionStorage.setItem("searchValue", searchValue);
    
    add_to_query_history(searchValue);
    
}    

function selectObject(event, operation) {
    new_item = event.target

    if (operation=='select') {
        // Post the selected item to server to get reformulated query
        
        getReformulatedQuery(new_item.dataset.type, new_item.dataset.docid)
        .then(data => {
            console.log(data);

            // document.getElementById('searchbox2').value = reformed_query;
            document.getElementById('task_button').innerText = data.task;
            document.getElementById('method_button').innerText = data.method;
            document.getElementById('dataset_button').innerText = data.dataset;
            
            // Save the data object to session storage
            sessionStorage.setItem("parsed_augment_terms", JSON.stringify(data));

            // Save the selected item to local storage
            var item_data = {
                'type': new_item.dataset.type,
                'id': 'item'+new_item.dataset.docid, 
                'docid': new_item.dataset.docid, 
                'name': new_item.dataset.name, 
                'url': new_item.dataset.url, 
                'parsed_augment_terms': data,
            }
        
            add_to_bookmark(item_data);
            refresh_bookmarks();
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
        //save the original query
        sessionStorage.setItem("originalQuery", query);
        // save the reformulated query
        sessionStorage.setItem("reformulatedQuery", data.reformed_query);

        console.log(data.reformed_query);
        // return data.reformed_query;
        return data;

    })
    .catch(error => {
        console.error('Error:', error);
        return query;
    });
}

function augment_query(title) {
    // var current_query = sessionStorage.getItem("originalQuery");
    var current_query = document.getElementById('searchbox2').value;
    var parsed_augment_terms = JSON.parse(sessionStorage.getItem("parsed_augment_terms"));

    if (parsed_augment_terms == null) {
        console.log('No parsed_augment_terms in session storage');
        return;
    }

    if (parsed_augment_terms[title].length > 0) {
        var new_query = current_query + ' ' + parsed_augment_terms[title];
    }
    else {
        var new_query = current_query;
    }

    document.getElementById('searchbox2').value = new_query; 
    
}

function remove_augment_term(title) {
    var original_query =  document.getElementById('searchbox2').value; //sessionStorage.getItem("originalQuery");
    var parsed_augment_terms = JSON.parse(sessionStorage.getItem("parsed_augment_terms"));

    var new_query = original_query.replace(parsed_augment_terms[title], '');

    document.getElementById('searchbox2').value = new_query; 

    return parsed_augment_terms[title]
}

function handleAugmentOptionClick(event) {
    target_item = event.target
    if(target_item.tagName == 'SPAN') {
        target_item = target_item.parentElement;
        target_span = event.target;
    }
    else{
        target_span = target_item.getElementsByTagName('span')[0];
        if (target_span == undefined) {
            target_span = target_item;
        }
    }

    title = target_item.dataset.title.toLowerCase();
    action = target_item.dataset.action;
    
    if (sessionStorage.getItem("parsed_augment_terms") == null) {
        console.log('No parsed_augment_terms in session storage');
        return;
    }
    
    // cases include 'augment', 'cancel' 
    switch (action) {
        case 'augment':
            // Add the selected item to query string
            augment_query(title);
            target_item.dataset.action = 'cancel';
            kept_value = target_span.innerText;            
            target_span.innerText = 'Cancel';
            // change the target_span color to yellow
            target_item.style.color = "yellow";
            target_item.setAttribute('kept-value', kept_value);
            break;
        case 'cancel':
            // Remove the selected item from query string
            terms = remove_augment_term(title);
            target_item.dataset.action = 'augment';            
            target_span.innerText = terms;
            target_item.style.color = "";
            target_item.setAttribute('kept-value', "Cancel");
            break;
        default:
            console.log('No action is taken');
    }

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

function generateId (len) {
    const dec2hex = function(dec) {
        return ('0' + dec.toString(16)).substr(-2)
    };

    let arr = new Uint8Array((len || 30) / 2);
    window.crypto.getRandomValues(arr);
    return Array.from(arr, dec2hex).join('')
}


/**
 * Start User Study. Create user-id for this participant, and store it in the session storage.
 * @returns userid: the user id of the registered user, or error message
 */
function start_user_study() {
    if(localStorage.getItem("userId") == null) {
        userId = generateId();
        localStorage.setItem("userId", userId);
    }

    userId = localStorage.getItem("userId");

    sessionId = generateId();
    sessionStorage.setItem("sessionId", sessionId);

    return userId, sessionId;
}

/**
 * Get user study task. Choose the condition for this study (0: W/o Entity Recognition, 1: W/ Entity Recognition), and research question for this user.
 */
function get_user_study_task() {
    userId = localStorage.getItem("userId");
    sessionId = sessionStorage.getItem("sessionId");

    var url = "/user_study/task_assignment/";

    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            'userId': userId,
            'sessionId': sessionId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        console.log(data);
        taskId = data['taskId'];
        task = data['task'];
        condition = data['condition'];
        sessionStorage.setItem("taskId", taskId);
        sessionStorage.setItem("task", task);
        sessionStorage.setItem("condition", condition);
        sessionStorage.setItem("taskData", JSON.stringify(data));
        return data;
    })
    .catch(error => {
        console.error('Error:', error);
        return error;
    });
}


function start_study_session(event) {
    window.location.href = "/user_study/guide/";

}

/**
 * This is a function to handle the user information submission when registering. 
 * @param {*} event 
 * @returns userid: the user id of the registered user, or error message
 */
async function sumit_user_information(event) {
    event.preventDefault();

    userId = localStorage.getItem("userId");
    sessionId = sessionStorage.getItem("sessionId");
    if(userId == null || sessionId == null){ 
        userId, sessionId = start_user_study();
    }

    var topicBlocks = event.target.getElementsByClassName('topic-block');
    topics = [];
    if (topicBlocks.length > 0) {
        topics = Array.from(topicBlocks).map(topicBlock => {
            return topicBlock.lastChild.innerText.trim();
        });
    }

    var user_info = {
        'registerUserName': event.target.elements.registerUserName.value,
        'registerUserEmail': event.target.elements.registerUserEmail.value,
        'registerUserEducation': event.target.elements.registerUserEducation.value,
        'registerResearchTopics': topics.join('\n'),
        'userId': userId,
        'sessionId': sessionId
    }

    var url = "../../user_study/information_survey/";

    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(user_info)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        console.log(data);
        sessionStorage.setItem("userInformation", JSON.stringify(user_info));
        assigned_condition = data['assigned_condition']       
        sessionStorage.setItem("assigned_condition", assigned_condition);

        return data;
    })
    .catch(error => {
        console.error('Error:', error);
        return error;
    });
}


function post_questionnaire(event){

}


function getCurrentTime() {
    var now = new Date();
    var date = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var year = now.getFullYear().toString().substr(-2);
    var hours = ("0" + now.getHours()).slice(-2);
    var minutes = ("0" + now.getMinutes()).slice(-2);
    
    // var formattedDate = date + "-" + month + "-" + year + " " + hours + ":" + minutes;
    var formattedDate = date + "-" + month + " " + hours + ":" + minutes;
    return formattedDate;
}



{/* <i class="fa-solid fa-database"></i> */}
function add_to_query_history(query) {
    console.log("add_to_query_history");

    var currentTime = getCurrentTime();

    var channel = localStorage.getItem("channel");
    if (!channel) {
        channel = "notebook";
    }

    query_item = {
        "channel": channel,
        "query": query,
        "time": currentTime
    }
    
    var queryHistory = localStorage.getItem("query_history");
    if (queryHistory) {
        queryHistory = JSON.parse(queryHistory);
        queryHistory["queries"].unshift(query_item);
    } else {
        queryHistory =  {"queries": [query_item]};
    }
    localStorage.setItem("query_history", JSON.stringify(queryHistory));
}


function refresh_query_history(){
    query_history = localStorage.getItem('query_history');
    if (query_history) {
        query_history = JSON.parse(query_history)['queries'];
        query_history.forEach(function(query){
            channel = query["channel"];
            channel_icon = "";
            if (channel == "dataset"){
                channel_icon = '<i class="fa-solid fa-database" style="color: #74C0FC;"></i>';
            }
            else if (channel == "notebook"){
                channel_icon = '<i class="fa-regular fa-file" style="color: #74C0FC;"></i>';
            }
            else{
                channel_icon = '<i class="fa-solid fa-diagram-project" style="color: #74C0FC;"></i>';
            }

            $('#query-history-list').append('<a href="#" class="list-group-item list-group-item-action py-2 lh-sm" aria-current="true" ><div class="d-flex w-100 align-items-center justify-content-between" >' + channel_icon +  '&nbsp;&nbsp;<small class="mb-1 small" >'+query["query"] +'</small><small class="text-body-secondary">' + query["time"] +'</small></div></a>');
        });
    }
}    

function add_to_bookmark(item) {
    console.log("add_to_bookmark");

    var currentTime = getCurrentTime();
    item["time"] = currentTime;
    var bookmarks = localStorage.getItem("bookmarks");
    if (bookmarks) {
        bookmarks = JSON.parse(bookmarks);
        bookmarks["items"].unshift(item);
    } else {
        bookmarks =  {"items": [item]};
    }

    localStorage.setItem("bookmarks", JSON.stringify(bookmarks));

    refresh_bookmarks();
}

function add_one_bookmark(bookmark){

    channel = bookmark["type"];
    channel_icon = "";
    if (channel == "dataset"){
        channel_icon = '<i class="fa-solid fa-database" style="color: #74C0FC;"></i>';
    }
    else if (channel == "notebook"){
        channel_icon = '<i class="fa-regular fa-file" style="color: #74C0FC;"></i>';
    }
    else{
        channel_icon = '<i class="fa-solid fa-diagram-project" style="color: #74C0FC;"></i>';
    }

    asset_name = bookmark["name"];
    asset_url = bookmark["url"];
    parsed_augment_terms = bookmark["parsed_augment_terms"]
    augment_terms = '<p> Task<i class="fa-solid fa-lightbulb"></i>:' + parsed_augment_terms["task"] + ' <br> Method <i class="fa-solid fa-microscope"></i>: ' + parsed_augment_terms["method"] +  ' <br> Dataset<i class="fa-solid fa-dna"></i>: ' + parsed_augment_terms["dataset"] + "</p>";
    var task_condition = sessionStorage.getItem("condition");

    if (task_condition == '0') {
        $('#saved-bookmark-list').append('<div class="list-group-item list-group-item-action py-2 lh-sm" aria-current="true" ><div class="d-flex w-100 align-items-center justify-content-between" >' + channel_icon +  '&nbsp;&nbsp; <a href="'+ asset_url +'" class="mb-1 small" > ' + asset_name + '</a> <small class="text-body-secondary">' + bookmark["time"] +'</small></div> </div>');
    }
    else {
        $('#saved-bookmark-list').append('<div class="list-group-item list-group-item-action py-2 lh-sm" aria-current="true" ><div class="d-flex w-100 align-items-center justify-content-between" >' + channel_icon +  '&nbsp;&nbsp; <a href="'+ asset_url +'" class="mb-1 small" > ' + asset_name + '</a> <small class="text-body-secondary">' + bookmark["time"] +'</small></div> <div class="col-10 mb-1 small">' + augment_terms +' </div> </div>');
    }
}

function refresh_bookmarks(){
    $('#saved-bookmark-list').html('');

    bookmarks = localStorage.getItem('bookmarks');        
    if (bookmarks) {
        bookmarks = JSON.parse(bookmarks)['items'];
        bookmarks.forEach(function(bookmark){add_one_bookmark(bookmark);});
    }
}

