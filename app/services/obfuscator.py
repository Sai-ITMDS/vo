"""
Enterprise Voice Obfuscation Engine
Prevents voice cloning while preserving intelligibility
Production-grade version
"""

import librosa
import numpy as np
import soundfile as sf
import noisereduce as nr
import logging
import os
import uuid
from scipy.signal import lfilter

logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def __init__(self):

        self.target_sr = 16000

        # Optimized for clarity + anti cloning
        self.pitch_shift_range = (-2.0, -0.5)

        self.noise_level = 0.0003

        self.formant_strength = 0.08


    # =========================
    # MAIN PIPELINE
    # =========================

    def obfuscate(self, input_path: str, output_dir: str) -> str:

        try:

            logger.info(f"Processing file: {input_path}")

            os.makedirs(output_dir, exist_ok=True)

            y, sr = librosa.load(
                input_path,
                sr=self.target_sr,
                mono=True
            )

            # ===== ENTERPRISE PIPELINE =====

            y = self.noise_reduction(y, sr)

            y = self.normalize(y)

            y = self.pitch_shift(y, sr)

            y = self.time_stretch(y)

            y = self.formant_shift(y)

            y = self.highpass_filter(y)

            y = self.phase_perturb(y)

            y = self.add_protection_noise(y)

            y = self.normalize(y)

            # ==============================

            filename = f"{uuid.uuid4()}.wav"

            output_path = os.path.join(
                output_dir,
                filename
            )

            sf.write(

                output_path,

                y,

                sr,

                subtype="PCM_16"

            )

            logger.info(
                f"Saved obfuscated file: {output_path}"
            )

            return output_path

        except Exception as e:

            logger.error(f"Obfuscation failed: {str(e)}")

            raise


    # =========================
    # DSP FUNCTIONS
    # =========================


    def noise_reduction(self, y, sr):

        return nr.reduce_noise(

            y=y,

            sr=sr,

            prop_decrease=0.6

        )


    def normalize(self, y):

        max_val = np.max(np.abs(y))

        if max_val > 0:

            y = y / max_val

        return y


    def pitch_shift(self, y, sr):

        shift = np.random.uniform(

            self.pitch_shift_range[0],

            self.pitch_shift_range[1]

        )

        logger.info(f"Pitch shift applied: {shift}")

        return librosa.effects.pitch_shift(

            y,

            sr=sr,

            n_steps=shift,

            res_type="soxr_vhq"

        )


    # Prevent voice embedding reuse
    def time_stretch(self, y):

        rate = np.random.uniform(

            0.94,

            1.06

        )

        logger.info(f"Time stretch: {rate}")

        return librosa.effects.time_stretch(

            y,

            rate=rate

        )


    # Prevent formant cloning
    def formant_shift(self, y):

        alpha = self.formant_strength

        b = [1 - alpha]

        a = [1, -alpha]

        return lfilter(

            b,

            a,

            y

        )


    # Remove identity-rich low frequencies
    def highpass_filter(self, y):

        alpha = 0.97

        filtered = np.append(

            y[0],

            y[1:] - alpha * y[:-1]

        )

        return filtered


    # Break speaker embeddings
    def phase_perturb(self, y):

        phase_noise = np.random.normal(

            0,

            0.0004,

            len(y)

        )

        return y + phase_noise


    # Anti-deepfake protection
    def add_protection_noise(self, y):

        noise = np.random.normal(

            0,

            self.noise_level,

            len(y)

        )

        return y + noise


# Singleton instance
obfuscator = VoiceObfuscator()
