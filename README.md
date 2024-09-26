
## **AI Dialog Application**

### **Overview**
This Python application provides a simple and interactive interface for conversing with an AI. It utilizes various libraries and APIs to achieve a seamless user experience.

### **Features**
* **Voice-based interaction:** Users can interact with the AI by speaking directly into their microphone.
* **Real-time speech-to-text:** The spoken input is converted into text using speech recognition technology.
* **AI-generated responses:** The text is processed by a local GPT model, which generates a comprehensive response.
* **Contextual understanding:** AI has the ability to understand context.
* **Text-to-speech output:** The AI's response is converted into natural-sounding speech and played back to the user.
* **User-friendly GUI:** A simple graphical user interface (GUI) is provided using PySimpleGui.

### **How it works**
1. **Start the application:** Run `python main.py` to start the application.
2. **Speak into the microphone:** Click the "Start Talk" button and speak your query.
3. **Speech-to-text conversion:** The spoken audio is recorded and converted into text using the `speech_recognition` library.
4. **AI processing:** The text is processed by a local GPT model to generate a response.
5. **Text-to-speech conversion:** The AI's response is converted into an audio file using the ElevenLabs API.
6. **Audio playback:** The generated audio is played back to the user using Pygame.

### **Prerequisites**
* **Python:** Ensure you have Python installed (version 3.6 or later).
* **API keys:**
    * **ElevenLabs:** Obtain an API key from ElevenLabs and set it in the `.env` file.
    * **PySimpleGUI:** You may need to provide a key after the first run.

### **Installation**
1. **Clone the repository:**
   ```bash
   git clone https://your-repository-url.git
   ```
2. **Create Virtual Environment:**
   ```bash
   pip -m venv venv
   ```
2. **Install dependencies::**
   ```bash
   pip install -r requirements.txt
   ```
   
### **Interact with the AI:**
* **Click the "Start Talk" button.**
* **Speak your query.**
* **The AI will respond.**

### **Additional notes**
* **Customization:** Feel free to customize the application by modifying the code.
* **Improvements:** Consider adding features like:
* **Voice cloning:** Use ElevenLabs' voice cloning feature.
* **Multiple languages:** Support different languages.


*this README has made with IA*
