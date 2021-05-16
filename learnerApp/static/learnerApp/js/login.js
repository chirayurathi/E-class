document.getElementById("login-button").onclick = (e)=>{
    e.preventDefault();
    e.preventDefault();
    xhr = new XMLHttpRequest()
    data = {
        username:document.getElementById("email").value,
        password:document.getElementById("password").value
    }
    cookieStore.get('csrftoken')
    .then(cookie=>{
        let csrftoken = cookie.value
        xhr.addEventListener("readystatechange",()=>{
            if(xhr.readyState===4){
                let response = JSON.parse(xhr.responseText)
                e.preventDefault();
                console.log(response.message)
                if(response.message === "success"){
                    window.location.replace(window.location.origin + '/dashboard/')
                    console.log('here')
                }
            }
        })
        xhr.open("POST","http://127.0.0.1:8000/login/")
        xhr.setRequestHeader('content-type','text/plain')
        xhr.setRequestHeader("X-CSRFToken",csrftoken)
        xhr.withCredentials =false
        xhr.send(JSON.stringify(data))
    })
}