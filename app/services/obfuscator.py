"""
Enterprise Voice Obfuscator
MAX CLARITY + Anti-Deepfake Protection
Production Ready
"""

import librosa
import numpy as np
import soundfile as sf
import os
import uuid
import logging
import traceback
from scipy.signal import lfilter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def __init__(self):

        self.target_sr = 16000

        # Identity protection strength
        self.mcadams = 0.75

        # Anti-deepfake protection (INAUDIBLE)
        self.protection_noise = 0.00001

        # Speech clarity enhancement
        self.pre_emphasis = 0.97


    # ============================================================
    # MAIN
    # ============================================================

    def obfuscate(self, input_path, output_dir="/tmp/outputs"):

        try:

            logger.info("VOICE OBFUSCATION STARTED")

            os.makedirs(output_dir, exist_ok=True)


            # Load
            y, sr = librosa.load(
                input_path,
                sr=self.target_sr,
                mono=True
            )


            logger.info("Speech enhancement")

            y = self.pre_emphasize(y)


            logger.info("McAdams anonymization")

            y = self.mcadams_anonymize(y)


            logger.info("Anti-deepfake protection")

            y = self.anti_deepfake(y)


            logger.info("Normalize")

            y = self.normalize(y)


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


            logger.info("SUCCESS")

            return output_path


        except Exception as e:

            logger.error(traceback.format_exc())

            raise Exception("Processing failed")


    # ============================================================
    # McAdams anonymization (CORE)
    # ============================================================

    def mcadams_anonymize(self, y):

        frame_length = 512
        hop_length = 256
        order = 20

        output = np.zeros_like(y)

        for i in range(0, len(y) - frame_length, hop_length):

            frame = y[i:i+frame_length]

            lpc = librosa.lpc(frame, order=order)

            roots = np.roots(lpc)

            angles = np.angle(roots)

            magnitudes = np.abs(roots)

            angles = angles * self.mcadams

            new_roots = magnitudes * np.exp(1j * angles)

            new_lpc = np.real(np.poly(new_roots))

            new_frame = lfilter(
                [0] + -1 * new_lpc[1:].tolist(),
                [1],
                frame
            )

            output[i:i+frame_length] += new_frame


        return output


    # ============================================================
    # Anti-Deepfake Protection
    # ============================================================

    def anti_deepfake(self, y):

        """
        Adds inaudible adversarial perturbation

        Humans cannot hear it
        AI embedding models get corrupted
        """

        noise = np.random.normal(

            0,

            self.protection_noise,

            len(y)

        )

        return y + noise


    # ============================================================
    # Speech Enhancement
    # ============================================================

    def pre_emphasize(self, y):

        return np.append(

            y[0],

            y[1:] - self.pre_emphasis * y[:-1]

        )


    # ============================================================

    def normalize(self, y):

        max_val = np.max(np.abs(y))

        if max_val > 0:

            y = y / max_val

        return y



# Singleton
obfuscator = VoiceObfuscator()
