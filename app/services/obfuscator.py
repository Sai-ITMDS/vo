"""
Enterprise Voice Obfuscation Engine
High intelligibility + Strong anti-voice-cloning protection
Production Ready
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

        # SAFE IDENTITY PROTECTION SETTINGS

        # Small pitch shift preserves clarity but breaks embeddings
        self.pitch_min = -2.0
        self.pitch_max = -1.0

        # VERY LOW NOISE (critical fix)
        self.noise_level = 0.00015

        # gentle spectral warp
        self.formant_strength = 0.08

        # pre-emphasis improves speech clarity
        self.pre_emphasis = 0.97


    # ============================================================
    # MAIN PIPELINE
    # ============================================================

    def obfuscate(self, input_path: str, output_dir: str) -> str:

        try:

            logger.info(f"Processing: {input_path}")

            y, sr = librosa.load(
                input_path,
                sr=self.target_sr,
                mono=True
            )

            # STEP 1 Clean noise
            y = self.noise_reduction(y, sr)

            # STEP 2 Speech enhancement
            y = self.pre_emphasize(y)

            # STEP 3 Normalize
            y = self.normalize(y)

            # STEP 4 Pitch shift (identity protection)
            y = self.pitch_shift(y, sr)

            # STEP 5 Formant protection
            y = self.formant_shift(y)

            # STEP 6 Add very small anti-cloning noise
            y = self.add_protection_noise(y)

            # STEP 7 Final normalize
            y = self.normalize(y)

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

            logger.info(f"Saved: {output_path}")

            return output_path

        except Exception as e:

            logger.error(f"Obfuscation failed: {str(e)}")

            raise


    # ============================================================
    # DSP FUNCTIONS
    # ============================================================


    def noise_reduction(self, y, sr):

        reduced = nr.reduce_noise(

            y=y,
            sr=sr,

            prop_decrease=0.6,

            stationary=True

        )

        return reduced


    def normalize(self, y):

        max_val = np.max(np.abs(y))

        if max_val > 0:

            y = y / max_val

        return y


    def pre_emphasize(self, y):

        return np.append(
            y[0],
            y[1:] - self.pre_emphasis * y[:-1]
        )


    def pitch_shift(self, y, sr):

        shift = np.random.uniform(

            self.pitch_min,
            self.pitch_max

        )

        logger.info(f"Pitch shift: {shift}")

        shifted = librosa.effects.pitch_shift(

            y,

            sr=sr,

            n_steps=shift,

            res_type="soxr_vhq"

        )

        return shifted


    def formant_shift(self, y):

        alpha = self.formant_strength

        b = [1 - alpha]

        a = [1, -alpha]

        return lfilter(b, a, y)


    def add_protection_noise(self, y):

        noise = np.random.normal(

            0,

            self.noise_level,

            len(y)

        )

        protected = y + noise

        return protected


# Singleton instance

obfuscator = VoiceObfuscator()
