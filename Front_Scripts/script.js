const convertButton = document.getElementById('convert-button-2');
const readMoreButton = document.getElementById('read-more');
const imageInstagram = document.querySelector ('.image-insta');
const imageEmail = document.querySelector ('.image-email');
const conversionForm = document.getElementById('conversion-form');
const urlInput = document.getElementById('url-input');


const handleInstagramClick = () =>{
    window.open('https://www.linkedin.com/in/jean-peixoto-/', '_blank');
}

const handleEmailClick = () =>{
    window.open('https://www.linkedin.com/in/jean-peixoto-/', '_blank');
}

imageInstagram.addEventListener('click', handleInstagramClick);
imageEmail.addEventListener('click', handleEmailClick);

convertButton.addEventListener('click', async (e) => {
    const videoUrl = urlInput.value.trim();
    if (videoUrl) {
        try {
            // Call the Go server using Fetch API
            const jsonData = { VideoUrl: videoUrl };
            console.log('JSON data:', jsonData);
            const response = await fetch('http://localhost:8080/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Video conversion requested successfully!');
                console.log('Converted audio file URL:', data.file_url);
                // Lidar com o download do arquivo convertido
                const downloadButton = document.getElementById('download');
                downloadButton.href = data.file_url;
                downloadButton.download = 'converted_audio.mp3';
            } else {
                console.error('Error requesting video conversion:', response.statusText);
            }
        } catch (error) {
            console.error('Error requesting video conversion:', error);
        }
    } else {
        alert('Please enter a valid YouTube video URL');
    }
});

readMoreButton.addEventListener('click', function() {
    window.location.href = 'sobre.html'; 
});
