document.getElementById("login-button").onclick = (e)=>{
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
                console.log(xhr.responseText)
            }
        })
        xhr.open("POST","http://127.0.0.1:8000/login/")
        xhr.setRequestHeader('content-type','application/json')
        xhr.setRequestHeader("X-CSRFToken",csrftoken)
        xhr.withCredentials = false
        xhr.send(JSON.stringify(data))
    })
}