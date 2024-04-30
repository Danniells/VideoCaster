const convertButton = document.getElementById('convert-button');
const readMoreButton = document.getElementById('read-more');
const imageInstagram = document.querySelector ('.image-insta');
const imageEmail = document.querySelector ('.image-email');


const handleInstagramClick = () =>{
    window.open('https://www.linkedin.com/in/jean-peixoto-/', '_blank');
}

const handleEmailClick = () =>{
    window.open('https://www.linkedin.com/in/jean-peixoto-/', '_blank');
}

imageInstagram.addEventListener('click', handleInstagramClick);
imageEmail.addEventListener('click', handleEmailClick);



 convertButton.addEventListener('click', function() {
    window.location.href = 'converter.html'; 
});

readMoreButton.addEventListener('click', function() {
    window.location.href = 'sobre.html'; 
});
