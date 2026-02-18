import librosa
import numpy as np
import soundfile as sf
import uuid
import tempfile


class VoiceObfuscator:


    def __init__(self, sr=16000):

        self.sr = sr


    def obfuscate(self, input_path):

        y, sr = librosa.load(input_path, sr=self.sr)


        pitch = np.random.uniform(-4, 4)

        y = librosa.effects.pitch_shift(
            y,
            sr=sr,
            n_steps=pitch
        )


        speed = np.random.uniform(0.9, 1.1)

        y = librosa.effects.time_stretch(
            y,
            rate=speed
        )


        noise = np.random.normal(
            0,
            0.002,
            len(y)
        )

        y += noise


        output = f"{tempfile.gettempdir()}/{uuid.uuid4()}.wav"


        sf.write(
            output,
            y,
            sr
        )


        return output
