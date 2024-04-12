document.addEventListener("DOMContentLoaded", function() {
    // Seleciona o botão de converter
    var convertButton = document.getElementById("convert-button");

    // Adiciona um ouvinte de evento para o clique no botão
    convertButton.addEventListener("click", function() {
        // Obtém o valor do input da URL
        var url = document.getElementById("url-input").value;

        // Verifica se a URL não está vazia
        if (url.trim() === "") {
            alert("Por favor, insira a URL do YouTube");
            return;
        }

        // Envia a URL para o servidor para conversão
        fetch("http://localhost:8000/file/download-youtube", { // /converter
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => {
            if (response.ok) {
                // Se a resposta do servidor estiver OK, inicia o download do arquivo MP3
                response.blob().then(blob => {
                    var url = window.URL.createObjectURL(blob);
                    var a = document.createElement("a");
                    a.href = url;
                    a.download = "audio.mp3";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                });
            } else {
                // Se houver um erro na resposta do servidor, exibe uma mensagem de erro
                response.text().then(message => {
                    alert("Erro: " + message);
                });
            }
        })
        .catch(error => {
            // Se houver um erro ao fazer a solicitação, exibe uma mensagem de erro
            alert("Erro ao converter o vídeo: " + error);
        });
    });
});
