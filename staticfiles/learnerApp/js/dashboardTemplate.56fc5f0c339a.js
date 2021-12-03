let button = document.querySelector('.sideNav button');
button.onclick = ()=>{
    document.getElementsByClassName('sideNav')[0].classList.toggle('activeNav')
    document.getElementsByClassName('dashboard')[0].classList.toggle('activeNav')
}

if(window.innerWidth<700){
    document.getElementsByClassName('sideNav')[0].classList.remove('activeNav')
    document.getElementsByClassName('dashboard')[0].classList.remove('activeNav')
}
