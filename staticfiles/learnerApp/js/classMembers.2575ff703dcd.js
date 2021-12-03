forms = document.querySelectorAll('form')
document.querySelectorAll('form button')
.forEach((btn,index)=>{
    console.log(index)
    btn.onclick = (e)=>{
    if(!forms[index].classList.contains("active")){
        e.preventDefault()
        forms[index].classList.add('active')
    }
}})