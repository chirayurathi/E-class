const domain = 'meet.jit.si';
const options = {
    roomName: 'classroom'+classroom.data,
    parentNode: document.querySelector('#meet'),
    userInfo: {
        email: classroom.email,
        displayName: classroom.name
    }
};
const api = new JitsiMeetExternalAPI(domain, options);

api.addListener('videoConferenceLeft',()=>{
    window.location.href = window.location.origin + '/classroom/'+classroom.data+'/'
})