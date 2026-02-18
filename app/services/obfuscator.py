"""
Enterprise Voice Obfuscator
Fully Instrumented Logging Version
"""

import librosa
import numpy as np
import soundfile as sf
import noisereduce as nr
import logging
import os
import uuid
import traceback

from scipy.signal import lfilter


logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def __init__(self):

        self.target_sr = 16000

        self.pitch_min = -2.0
        self.pitch_max = -1.0

        self.noise_level = 0.00015

        self.formant_strength = 0.08

        self.pre_emphasis = 0.97


    # ============================================================
    # MAIN
    # ============================================================

    def obfuscate(self, input_path: str, output_dir: str) -> str:

        logger.info("==========================================")
        logger.info("VOICE OBFUSCATION STARTED")
        logger.info(f"Input file: {input_path}")
        logger.info(f"Output dir: {output_dir}")

        try:

            # ----------------------------------------------------
            # LOAD
            # ----------------------------------------------------

            logger.info("Loading audio...")

            y, sr = librosa.load(

                input_path,

                sr=self.target_sr,

                mono=True

            )

            logger.info(f"Loaded successfully")
            logger.info(f"Sample rate: {sr}")
            logger.info(f"Samples: {len(y)}")
            logger.info(f"Duration: {len(y)/sr:.2f} sec")

            self.log_stats(y, "Original")


            # ----------------------------------------------------
            # STEP 1 Noise Reduction
            # ----------------------------------------------------

            logger.info("Step 1: Noise reduction")

            y = self.noise_reduction(y, sr)

            self.log_stats(y, "Noise reduced")


            # ----------------------------------------------------
            # STEP 2 Pre Emphasis
            # ----------------------------------------------------

            logger.info("Step 2: Speech enhancement")

            y = self.pre_emphasize(y)

            self.log_stats(y, "Enhanced")


            # ----------------------------------------------------
            # STEP 3 Normalize
            # ----------------------------------------------------

            logger.info("Step 3: Normalize")

            y = self.normalize(y)

            self.log_stats(y, "Normalized")


            # ----------------------------------------------------
            # STEP 4 Pitch Shift
            # ----------------------------------------------------

            logger.info("Step 4: Pitch shift")

            y = self.pitch_shift(y, sr)

            self.log_stats(y, "Pitch shifted")


            # ----------------------------------------------------
            # STEP 5 Formant Shift
            # ----------------------------------------------------

            logger.info("Step 5: Formant shift")

            y = self.formant_shift(y)

            self.log_stats(y, "Formant shifted")


            # ----------------------------------------------------
            # STEP 6 Protection Noise
            # ----------------------------------------------------

            logger.info("Step 6: Protection noise")

            y = self.add_protection_noise(y)

            self.log_stats(y, "Noise added")


            # ----------------------------------------------------
            # STEP 7 Final Normalize
            # ----------------------------------------------------

            logger.info("Step 7: Final normalize")

            y = self.normalize(y)

            self.log_stats(y, "Final")


            # ----------------------------------------------------
            # SAVE
            # ----------------------------------------------------

            filename = f"{uuid.uuid4()}.wav"

            output_path = os.path.join(

                output_dir,

                filename

            )

            logger.info(f"Saving to: {output_path}")

            sf.write(

                output_path,

                y,

                sr,

                subtype="PCM_16"

            )

            logger.info("SAVE SUCCESS")

            logger.info("VOICE OBFUSCATION COMPLETED")

            logger.info("==========================================")

            return output_path


        except Exception as e:

            logger.error("VOICE OBFUSCATION FAILED")

            logger.error(str(e))

            logger.error(traceback.format_exc())

            raise Exception("Processing failed")


    # ============================================================
    # LOG AUDIO STATS
    # ============================================================

    def log_stats(self, y, label):

        logger.info(

            f"{label} stats → "

            f"min: {np.min(y):.5f}, "

            f"max: {np.max(y):.5f}, "

            f"mean: {np.mean(y):.5f}"

        )


    # ============================================================
    # DSP
    # ============================================================

    def noise_reduction(self, y, sr):

        logger.info("Running noise reduction")

        return nr.reduce_noise(

            y=y,

            sr=sr,

            prop_decrease=0.6,

            stationary=True

        )


    def normalize(self, y):

        logger.info("Normalizing")

        max_val = np.max(np.abs(y))

        if max_val > 0:

            y = y / max_val

        return y


    def pre_emphasize(self, y):

        logger.info("Pre-emphasis")

        return np.append(

            y[0],

            y[1:] - self.pre_emphasis * y[:-1]

        )


    def pitch_shift(self, y, sr):

        shift = np.random.uniform(

            self.pitch_min,

            self.pitch_max

        )

        logger.info(f"Pitch shift value: {shift}")

        return librosa.effects.pitch_shift(

            y,

            sr=sr,

            n_steps=shift,

            res_type="soxr_vhq"

        )


    def formant_shift(self, y):

        logger.info("Formant shift")

        alpha = self.formant_strength

        b = [1 - alpha]

        a = [1, -alpha]

        return lfilter(b, a, y)


    def add_protection_noise(self, y):

        logger.info("Adding protection noise")

        noise = np.random.normal(

            0,

            self.noise_level,

            len(y)

        )

        return y + noise


# Singleton

obfuscator = VoiceObfuscator()
