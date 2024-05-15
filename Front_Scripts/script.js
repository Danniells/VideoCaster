const convertButton = document.getElementById('convert-button-2');
const readMoreButton = document.getElementById('read-more');
const imageInstagram = document.querySelector ('.image-insta');
const imageEmail = document.querySelector ('.image-email');
const conversionForm = document.getElementById('conversion-form');
const urlInput = document.getElementById('url-input');
const convertButton2 = document.getElementById('convert-button-2');


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

convertButton2.addEventListener('click', async () => {
    const videoUrl = urlInput.value.trim();
    if (videoUrl) {
        try {
            // Call the Python script using AJAX or a similar approach
            const response = await fetch('/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ videoUrl }),
            });

            if (response.ok) {
                console.log('Video converted successfully!');
            } else {
                console.error('Error converting video:', response.statusText);
            }
        } catch (error) {
            console.error('Error converting video:', error);
        }
    } else {
        alert('Please enter a valid YouTube video URL');
    }
});

readMoreButton.addEventListener('click', function() {
    window.location.href = 'sobre.html'; 
});
