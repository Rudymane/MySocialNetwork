document.addEventListener('DOMContentLoaded', function() {


    // Use buttons to toggle between views
    document.querySelector('#newpost-form').addEventListener('submit', submit_post);
    document.querySelector('#newcomment-form').addEventListener('submit', submit_comment);    
    document.querySelector('#nextpage').addEventListener('click', next_page); 
    document.querySelector('#previouspage').addEventListener('click', previous_page); 
    // document.querySelector('#currentposts-view').addEventListener('submit', edit_post(post['id']))
    // By default, load the inbox
    load_homepage();
});

// Start with first post
let counter = 10;

// Load posts 10 at a time
const quantity = 10;
console.log("hello")

function load_homepage(start=0, end=9) {
    
    
    
    document.querySelector('#newpost-view').style.display = 'block';
    document.querySelector('#newcomment-view').style.display = 'block';
    document.querySelector('#currentposts-view').style.display = 'block';
    document.querySelector('#nextpage-view').style.display = 'none';
    document.querySelector('#previouspage-view').style.display = 'none';

    const username = document.getElementById("profile-name").innerHTML
    const view = document.querySelector('#currentposts-view');
    const beginning = start
    const ending = end
    const parent= document.querySelector('#parentid').innerHTML
    console.log(parent)
    document.querySelector('#newpost-body').value = ''
    // retrieve the feed for those who the user is following
    if (username != "" && username != document.getElementById("user-name").value && username != "Following"){

        
        document.querySelector('#newpost-view').style.display = 'none';
        fetch(`/followfeed/?name=${username}`)
        .then(response => response.json())
        .then(follows => {
            
            // Create follow button
            followButton = document.createElement('button')
            followButton.className = "btn btn-primary center"
            followButton.setAttribute("id", "followbutton")
            followButton.innerHTML = "Follow"


            console.log(follows)
            // Change follow button's html depending on if the user follows the person or not
            follows.forEach(follow => {
                console.log(follow['name'])
                
                if (follow['name'].includes(username)){
                    
                    followButton.innerHTML = "Followed"
                }

            })
            // Update followers and following count 
            document.querySelector('#follow-section').appendChild(followButton)
            followButton.addEventListener('click', function() {
                
                if (document.getElementById("followbutton").innerHTML == "Followed"){
                    document.getElementById("followbutton").innerHTML = "Follow"
                    document.getElementById("the_followers").innerHTML -= 1
                }
                else{
                    document.getElementById("followbutton").innerHTML= "Followed"
                    document.getElementById("the_followers").innerHTML -= -1
                }
                
                // Send updated folling amount using PUT request
                fetch('/following/' + username, {
                    method: 'PUT',
                    body: JSON.stringify({follow : document.getElementById("followbutton").innerHTML})
            })
            })
            
        }) 
        

        
    }
    
    // retrieves 10 or less posts per page based on the "start","end","username", "parent" variables     
    fetch(`/feed?start=${beginning}&end=${ending}&username=${username}&parent=${parent}`)
    .then(response => response.json())
    .then(posts => {
        
        posts.forEach(post =>{
            console.log("this is each post",post)
            
            // display user posts
            let div = document.createElement('div')
            div.className = "a"
            div.innerHTML = `
                <div id="post-info${post['id']}">
                    <img src="/${post['profile']}" style="width:auto;height:30px; clip-path: circle();" />
                    <a href="/profile/${post['user']} ">${post['user']}</a>
                    <span class="timestamp"> ${post['timestamp']}</span>
                </div>
                <p id="body${post['id']}">${post['body']}</p>
                
                <span id="thumbs-up${post['id']}">
                </span>
                <span id="likescount${post['id']}">${post['likes']}</span>
                <span id="comment${post['id']}">
                </span>
                <br>
            `;

            // create like button
            likeButton = document.createElement('button')
            likeButton.className = "fa-solid fa-thumbs-up like"
            likeButton.style.color= "aqua"
            likeButton.setAttribute("id", "like"+post['id'])
            
            if(post['user_likes'].includes(post['users_id'])){
                likeButton.style.color= "aqua"
            }
            else {
                likeButton.style.color= "black"
            }
            // Update like button color on click
            likeButton.addEventListener('click', function() {
                
                if(document.getElementById("like"+post['id']).style.color == "black"){
                    console.log(document.getElementById("likescount"+post["id"]).innerHTML)
                    
                    document.getElementById("like"+post['id']).style.color =  "aqua"
                    document.getElementById("likescount"+post['id']).innerHTML = `
                    <span id="likescount${post['id']}">${post['likes'] +=1}</span>
                    `
                }
                else {
                    document.getElementById("like"+post['id']).style.color = "black"
                    document.getElementById("likescount"+post['id']).innerHTML = `
                    <span id="likescount${post['id']}">${post['likes'] -=1}</span>
                    `
                }
                console.log(document.getElementById("likescount"+post["id"]).innerHTML)
                fetch('/posts/' +post['id'], {
                    method: 'PUT',
                    body: JSON.stringify({like : document.getElementById("like"+post['id']).style.color
                    })
                })
            })

            // Create comment button
            commentButton = document.createElement('button')
            commentButton.className = "fa-sharp fa-solid fa-comments like"
            commentButton.setAttribute("id", "comment"+post['id'])
            commentButton.onclick = () => window.location = '/'+'comments/' +post['id'];

            // Create edit button
            editButton = document.createElement('button')
            editButton.className = "fa fa-pencil edit"
            editButton.addEventListener('click', function() {
        
                document.getElementById("body"+post['id']).innerHTML = `
                <textarea class="form-control" id="editpost-body" >${post['body']}</textarea>
                `
                // Create finish button to submit edit
                finishButton = document.createElement('button')
                finishButton.className = "btn btn-primary"
                finishButton.innerHTML = "Finish"
                finishButton.addEventListener('click', function() {
                    edit_post(post['id']);
                    document.getElementById("body"+post['id']).innerHTML = document.getElementById("editpost-body").value;
                    
                })
                document.getElementById("body"+post['id']).appendChild(finishButton)
            })
            
            view.append(div)
            document.getElementById("thumbs-up" +post['id']).appendChild(likeButton)
            document.getElementById("comment" +post['id']).appendChild(commentButton)
            if(post['users_id']== post["poster_id"]){
                document.getElementById("post-info" +post['id']).appendChild(editButton)
            }
        });
    })

    // Check if there are more posts on the next page
    fetch(`/feed?start=${beginning}&end=${ending + 1}&username=${username}&parent=${parent}`)
    .then(response => response.json())
    .then(posts =>{
        // display next button if there are more posts on the next page
        if(posts.length >10){
            document.querySelector('#nextpage-view').style.display = 'block';
        }
        else{
            document.querySelector('#nextpage-view').style.display = 'none';
        }
    })
    
    if(beginning == 0){
        document.querySelector('#previouspage-view').style.display = 'none'; 
    }
    else{
        document.querySelector('#previouspage-view').style.display = 'block'; 
    }
    
}

// like or dislike post when clicked on
function like_post(){
    if(document.getElementById("c-like").style.color == "black"){
        console.log(document.getElementById("c-likescount").innerHTML)
        
        document.getElementById("c-like").style.color =  "aqua"
        document.getElementById("c-likescount").innerHTML -= (-1)
        
    }
    else {
        document.getElementById("c-like").style.color = "black"
        document.getElementById("c-likescount").innerHTML -= 1
    }

    fetch('/posts/' + document.getElementById("parentid").innerHTML, {
        method: 'PUT',
        body: JSON.stringify({like : document.getElementById("c-like").style.color
        })
    })
}  

// submits post from the values entered in '#newpost-body'
function submit_post() {
    event.preventDefault();
    document.getElementById('currentposts-view').innerHTML = '';
    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#newpost-body').value
        })
    })
    
    .then(response => load_homepage());

}

// Adds a comment to the post
function submit_comment() {
    event.preventDefault();
    const parent= document.querySelector('#parentid').innerHTML
    const posted_comment = document.querySelector('#newcomment-body').value
    document.getElementById('currentposts-view').innerHTML = '';
    document.querySelector('#newcomment-body').value ="";

    // Use POST request to make new comment
    fetch('/newcomment', {
        method: 'POST',
        body: JSON.stringify({
            body: posted_comment,
            parent: parent
        })
    })
    .then(response => load_homepage());

}

// Use PUT request to edit post
function edit_post(post_id){
    fetch('/edit_post/' + post_id, {
        method: 'PUT',
        body: JSON.stringify({
            body: document.querySelector('#editpost-body').value
        })
    })
    
    
}

// Update start and end to show content on next page
function next_page() {
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    
    document.getElementById('currentposts-view').innerHTML = '';
    load_homepage(start, end);
}

// Update start and end to show content on previous page
function previous_page() {
    const start = counter - quantity -10 ;
    const end = counter -1 -10;
    if (end < 9){
        end = 9;
    }
    counter = end + 1;
    
    document.querySelector('#previouspage-view').style.display = 'none';
    document.getElementById('currentposts-view').innerHTML = '';
    load_homepage(start, end);
}


var names = [];
function ul(value){
    
    fetch('/search/')
    .then(response => response.json())
    .then(people=>{
        names = people

    })
    
    var n= names.length; // Length of datalist names  
    console.log("this is names", names)
    document.getElementById('datalist').innerHTML = '';
        // Datalist needs to be empty at start or else the same name will be repeated
        
        l=value.length;
        
    for (var i = 0; i<n; i++) {
    
        if(((names[i].toLowerCase()).indexOf(value.toLowerCase()))>-1)
        {
            // Seeing if user input string is in names[i]
            var node = document.createElement("option");
            var val = document.createTextNode(names[i]);
            node.appendChild(val);

            document.getElementById("datalist").appendChild(node);
                // Updates datalist with the names available with current search
            }
        }
}

// Search the name of the person searched for
function lookup() {
    window.location = '/'+'profile/' +document.getElementById("lookup").value;
}