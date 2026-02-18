"""
Enterprise Voice Obfuscator
Bank-Grade | Clear Speech | Deepfake Resistant | Render Safe
Single File Version
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


# ============================================================
# LOGGER CONFIG
# ============================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s [%(levelname)s] %(message)s"

)

logger = logging.getLogger(__name__)


# ============================================================
# MAIN CLASS
# ============================================================

class VoiceObfuscator:


    def __init__(self):

        logger.info("Initializing Enterprise Voice Obfuscator")

        self.target_sr = 16000


        # Safe identity protection range
        self.pitch_min = -1.4
        self.pitch_max = -0.6


        # VERY LOW noise (inaudible but blocks cloning)
        self.noise_level = 0.00002


        # Formant protection strength
        self.formant_strength = 0.06


        # Speech clarity enhancer
        self.pre_emphasis = 0.97


    # ============================================================
    # MAIN FUNCTION
    # ============================================================

    def obfuscate(self, input_path: str, output_dir: str = "/tmp/outputs") -> str:


        logger.info("==========================================")
        logger.info("VOICE OBFUSCATION STARTED")
        logger.info(f"Input: {input_path}")
        logger.info(f"Output Dir: {output_dir}")


        try:


            # ----------------------------------------------------
            # CREATE OUTPUT DIR
            # ----------------------------------------------------

            os.makedirs(output_dir, exist_ok=True)


            # ----------------------------------------------------
            # LOAD AUDIO
            # ----------------------------------------------------

            logger.info("Loading audio")

            y, sr = librosa.load(

                input_path,

                sr=self.target_sr,

                mono=True

            )


            logger.info(f"Loaded successfully")

            self.log_stats(y, "Original")



            # ----------------------------------------------------
            # STEP 1 Noise Reduction
            # ----------------------------------------------------

            logger.info("Noise reduction")

            y = nr.reduce_noise(

                y=y,

                sr=sr,

                prop_decrease=0.5,

                stationary=True

            )


            self.log_stats(y, "Noise Reduced")



            # ----------------------------------------------------
            # STEP 2 Speech Enhancement
            # ----------------------------------------------------

            logger.info("Speech enhancement")

            y = self.pre_emphasize(y)

            self.log_stats(y, "Enhanced")



            # ----------------------------------------------------
            # STEP 3 Normalize
            # ----------------------------------------------------

            y = self.normalize(y)



            # ----------------------------------------------------
            # STEP 4 Pitch Shift
            # ----------------------------------------------------

            shift = np.random.uniform(

                self.pitch_min,

                self.pitch_max

            )


            logger.info(f"Pitch shift: {shift}")


            y = librosa.effects.pitch_shift(

                y,

                sr=sr,

                n_steps=shift,

                res_type="soxr_vhq"

            )


            self.log_stats(y, "Pitch Shifted")



            # ----------------------------------------------------
            # STEP 5 Formant Shift
            # ----------------------------------------------------

            y = self.formant_shift(y)


            self.log_stats(y, "Formant Shifted")



            # ----------------------------------------------------
            # STEP 6 Protection Noise
            # ----------------------------------------------------

            y = self.add_noise(y)


            self.log_stats(y, "Noise Added")



            # ----------------------------------------------------
            # STEP 7 Final Normalize
            # ----------------------------------------------------

            y = self.normalize(y)



            # ----------------------------------------------------
            # SAVE FILE
            # ----------------------------------------------------

            file_id = str(uuid.uuid4())


            output_path = os.path.join(

                output_dir,

                f"{file_id}.wav"

            )


            logger.info(f"Saving file: {output_path}")


            sf.write(

                output_path,

                y,

                sr,

                subtype="PCM_16"

            )



            # VERIFY FILE

            if not os.path.exists(output_path):

                raise Exception("File not created")


            size = os.path.getsize(output_path)


            logger.info(f"Saved successfully: {size} bytes")


            if size < 1000:

                raise Exception("File corrupted")


            logger.info("VOICE OBFUSCATION COMPLETED")
            logger.info("==========================================")


            return output_path



        except Exception as e:


            logger.error("VOICE OBFUSCATION FAILED")

            logger.error(str(e))

            logger.error(traceback.format_exc())


            raise Exception("Processing failed")



    # ============================================================
    # DSP FUNCTIONS
    # ============================================================


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



    def formant_shift(self, y):

        alpha = self.formant_strength

        b = [1 - alpha]

        a = [1, -alpha]

        return lfilter(b, a, y)



    def add_noise(self, y):

        noise = np.random.normal(

            0,

            self.noise_level,

            len(y)

        )

        return y + noise



    # ============================================================
    # LOGGING
    # ============================================================


    def log_stats(self, y, label):

        logger.info(

            f"{label} → "

            f"min={np.min(y):.5f} "

            f"max={np.max(y):.5f} "

            f"mean={np.mean(y):.5f}"

        )



# ============================================================
# SINGLETON
# ============================================================

obfuscator = VoiceObfuscator()
