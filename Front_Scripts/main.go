package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"

	"github.com/gorilla/handlers"
)

func main() {
	http.HandleFunc("/convert", convertHandler)

	// Adicione o seguinte código para permitir solicitações de qualquer origem
	headers := handlers.AllowedHeaders([]string{"Content-Type"})
	methods := handlers.AllowedMethods([]string{"POST"})
	origins := handlers.AllowedOrigins([]string{"*"})
	http.ListenAndServe(":8080", handlers.CORS(headers, methods, origins)(http.DefaultServeMux))
}

func convertHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Requisição recebida")
	log.Println("Request body:", r.Body)
	if r.Method != "POST" {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}

	var data struct {
		VideoUrl string `json:"VideoUrl"`
	}

	fmt.Println("Request body:", string(body))
	err = json.Unmarshal(body, &data)

	if err != nil {
		http.Error(w, "Error unmarshalling JSON", http.StatusBadRequest)
		return
	}

	videoUrl := data.VideoUrl
	if videoUrl == "" {
		http.Error(w, "Missing videoUrl field in JSON", http.StatusBadRequest)
		return
	}

	fileUrl, err := convertVideo(videoUrl)

	if err != nil {
		http.Error(w, "Error converting video", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"file_url": fileUrl})
}

func convertVideo(videoUrl string) (string, error) {
	fmt.Println("Processing video URL:", videoUrl)

	// Verificar se o comando youtube-dl está instalado
	cmd := exec.Command("youtube-dl", "-h")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err != nil {
		return "", fmt.Errorf("youtube-dl command not found: %v\n%s", err, stderr.String())
	}

	// Download video using youtube-dl
	cmd = exec.Command("youtube-dl", "-f", "bestaudio", "-o", "-", videoUrl)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err = cmd.Run()
	if err != nil {
		return "", fmt.Errorf("Error downloading video: %v\n%s", err, stderr.String())
	}

	// Print the output of the youtube-dl command to the console
	fmt.Println("youtube-dl output:", stdout.String())

	// Verificar se o comando ffmpeg está instalado
	cmd = exec.Command("ffmpeg", "-h")
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err = cmd.Run()
	if err != nil {
		return "", fmt.Errorf("ffmpeg command not found: %v\n%s", err, stderr.String())
	}

	// Convert audio to MP3 using ffmpeg
	audioData := stdout.Bytes()
	cmd = exec.Command("ffmpeg", "-i", "-", "-vn", "-ab", "128k", "audio.mp3")
	cmd.Stdin = bytes.NewBuffer(audioData)
	var ffmpegStderr bytes.Buffer
	cmd.Stderr = &ffmpegStderr

	err = cmd.Run()
	if err != nil {
		return "", fmt.Errorf("Error converting audio: %v\n%s", err, ffmpegStderr.String())
	}

	// Print the output of the ffmpeg command to the console
	fmt.Println("ffmpeg output:", ffmpegStderr.String())

	// Save the converted audio to a file
	fileUrl := "/Front_Scripts/converted-audio.mp3"
	err = ioutil.WriteFile(fileUrl, audioData, 0644)
	if err != nil {
		return "", fmt.Errorf("Error saving converted audio: %v", err)
	}

	// Verificar se o arquivo foi salvo com sucesso
	if _, err := os.Stat(fileUrl); os.IsNotExist(err) {
		return "", fmt.Errorf("File %s does not exist", fileUrl)
	}

	// Print the output of the ioutil.WriteFile() function to the console
	fmt.Println("Converted audio saved to:", fileUrl)

	return fileUrl, nil
}
