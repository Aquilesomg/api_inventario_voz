import os
import whisper
import tempfile
from gtts import gTTS
import subprocess
import warnings

# Suprimir advertencias de Whisper sobre FP16
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

class VoiceService:
    def __init__(self):
        # Verificar que FFmpeg esté disponible
        self._check_ffmpeg()
        # Cargar el modelo Whisper
        self.model = whisper.load_model("medium")
        
    def _check_ffmpeg(self):
        """Verifica si FFmpeg está instalado y accesible"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise RuntimeError(
                "FFmpeg no encontrado. Por favor instálalo desde:\n"
                "https://ffmpeg.org/download.html\n"
                "Y asegúrate de agregarlo al PATH de tu sistema"
            )

    def _convert_to_wav(self, input_path):
        """
        Convierte cualquier archivo de audio a WAV mono 16kHz (compatible con Whisper)
        :param input_path: Ruta del archivo original
        :return: Ruta del archivo WAV temporal generado
        """
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        output_path = output_file.name
        output_file.close()

        command = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ac", "1",       # Convertir a mono
            "-ar", "16000",   # Frecuencia de muestreo 16kHz
            output_path
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_path

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio a texto usando Whisper
        :param audio_path: Ruta del archivo de audio
        :return: Texto transcrito
        """
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

            # Convertimos a WAV seguro
            wav_path = self._convert_to_wav(audio_path)

            # Transcribimos el archivo WAV
            result = self.model.transcribe(wav_path)

            # Eliminamos archivo temporal convertido
            os.remove(wav_path)

            return result["text"]
        except Exception as e:
            raise RuntimeError(f"Error al transcribir audio: {str(e)}")

    def text_to_speech(self, text, lang="es", slow=False):
        """
        Convierte texto a voz usando gTTS
        :param text: Texto a convertir
        :param lang: Idioma (default: español)
        :param slow: Habla más lento (default: False)
        :return: Ruta al archivo de audio generado
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts = gTTS(text=text, lang=lang, slow=slow)
                tts.save(fp.name)
                return fp.name
        except Exception as e:
            raise RuntimeError(f"Error al generar audio: {str(e)}")

# Instancia global del servicio
voice_service = VoiceService()
