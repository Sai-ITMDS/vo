import os
import uuid
import logging
import librosa
import soundfile as sf
import numpy as np

logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def obfuscate(self, input_path: str, output_dir="outputs"):

        os.makedirs(output_dir, exist_ok=True)


        # KEEP ORIGINAL SAMPLE RATE
        y, sr = librosa.load(
            input_path,
            sr=None,
            mono=True
        )


        # normalize
        y = y / np.max(np.abs(y))


        # Small pitch shift
        y = librosa.effects.pitch_shift(
            y,
            sr=sr,
            n_steps=3
        )


        # slight formant effect via resample trick
        y2 = librosa.resample(
            y,
            orig_sr=sr,
            target_sr=int(sr * 1.1)
        )

        y = librosa.resample(
            y2,
            orig_sr=int(sr * 1.1),
            target_sr=sr
        )


        y = y / np.max(np.abs(y))


        output_path = os.path.join(
            output_dir,
            f"{uuid.uuid4()}.wav"
        )


        sf.write(
            output_path,
            y,
            sr
        )


        return output_path



obfuscator = VoiceObfuscator()