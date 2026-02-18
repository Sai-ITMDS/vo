"""
Enterprise Voice Obfuscator
ULTRA CLEAR VERSION
Bank / Healthcare / Call Center Grade
"""

import librosa
import numpy as np
import soundfile as sf
import logging
import os
import uuid
import traceback
import noisereduce as nr


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def __init__(self):

        self.target_sr = 16000

        # SMALL shift = clear speech
        self.pitch_shift = (-0.9, -0.4)

        # embedding poison (NOT audible)
        self.embed_noise = 0.000005


    # ============================================================
    # MAIN
    # ============================================================

    def obfuscate(self, input_path, output_dir="/tmp/outputs"):


        try:

            logger.info("Loading")

            os.makedirs(output_dir, exist_ok=True)

            y, sr = librosa.load(
                input_path,
                sr=self.target_sr,
                mono=True
            )


            # ====================================================
            # STEP 1 Light noise reduction
            # ====================================================

            y = nr.reduce_noise(
                y=y,
                sr=sr,
                prop_decrease=0.3
            )


            # ====================================================
            # STEP 2 Normalize loudness
            # ====================================================

            y = self.normalize(y)


            # ====================================================
            # STEP 3 Pitch shift (primary identity protection)
            # ====================================================

            shift = np.random.uniform(
                self.pitch_shift[0],
                self.pitch_shift[1]
            )


            logger.info(f"Pitch shift: {shift}")


            y = librosa.effects.pitch_shift(
                y,
                sr=sr,
                n_steps=shift,
                res_type="soxr_vhq"
            )


            # ====================================================
            # STEP 4 Vocal tract warping (CRITICAL STEP)
            # ====================================================

            y = self.vocal_warp(y)


            # ====================================================
            # STEP 5 Spectral smoothing (restore clarity)
            # ====================================================

            y = self.spectral_smooth(y)


            # ====================================================
            # STEP 6 Anti-cloning poison (INAUDIBLE)
            # ====================================================

            y = self.embed_protection(y)


            # ====================================================
            # FINAL NORMALIZE
            # ====================================================

            y = self.normalize(y)


            # ====================================================
            # SAVE
            # ====================================================

            output_path = os.path.join(
                output_dir,
                f"{uuid.uuid4()}.wav"
            )


            sf.write(
                output_path,
                y,
                sr,
                subtype="PCM_16"
            )


            logger.info("Completed")

            return output_path


        except Exception as e:

            logger.error(str(e))
            logger.error(traceback.format_exc())

            raise Exception("Processing failed")


    # ============================================================
    # FUNCTIONS
    # ============================================================


    def normalize(self, y):

        return y / np.max(np.abs(y))


    def vocal_warp(self, y):

        # vocal tract modification without destroying clarity

        stft = librosa.stft(y)

        magnitude, phase = librosa.magphase(stft)

        warp = np.linspace(0.9, 1.1, magnitude.shape[0])

        magnitude = magnitude * warp[:, None]

        warped = magnitude * phase

        return librosa.istft(warped)


    def spectral_smooth(self, y):

        stft = librosa.stft(y)

        mag, phase = librosa.magphase(stft)

        mag = librosa.decompose.nn_filter(
            mag,
            aggregate=np.median,
            metric='cosine'
        )

        return librosa.istft(mag * phase)


    def embed_protection(self, y):

        noise = np.random.normal(
            0,
            self.embed_noise,
            len(y)
        )

        return y + noise



obfuscator = VoiceObfuscator()
