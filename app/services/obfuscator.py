"""
MAX CLARITY Voice Obfuscator
McAdams Coefficient Method
Production Grade
"""

import librosa
import numpy as np
import soundfile as sf
import os
import uuid
import logging
import traceback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceObfuscator:

    def __init__(self):

        self.target_sr = 16000

        # McAdams coefficient
        # 0.6–0.8 = BEST clarity + anonymization
        self.mcadams = 0.7


    # ============================================================
    # MAIN
    # ============================================================

    def obfuscate(self, input_path, output_dir="/tmp/outputs"):

        try:

            logger.info("Loading audio")

            os.makedirs(output_dir, exist_ok=True)

            y, sr = librosa.load(
                input_path,
                sr=self.target_sr,
                mono=True
            )


            logger.info("Running McAdams anonymization")

            y_anonymized = self.mcadams_anonymize(y)


            logger.info("Normalizing")

            y_anonymized = self.normalize(y_anonymized)


            output_path = os.path.join(
                output_dir,
                f"{uuid.uuid4()}.wav"
            )


            sf.write(
                output_path,
                y_anonymized,
                sr,
                subtype="PCM_16"
            )


            logger.info("SUCCESS")

            return output_path


        except Exception as e:

            logger.error(str(e))
            logger.error(traceback.format_exc())

            raise Exception("Processing failed")


    # ============================================================
    # McAdams Method
    # ============================================================

    def mcadams_anonymize(self, y):

        frame_length = 512
        hop_length = 256
        order = 20

        output = np.zeros_like(y)

        for i in range(0, len(y) - frame_length, hop_length):

            frame = y[i:i+frame_length]

            lpc = librosa.lpc(frame, order)

            roots = np.roots(lpc)

            angles = np.angle(roots)

            magnitudes = np.abs(roots)

            angles = angles * self.mcadams

            new_roots = magnitudes * np.exp(1j * angles)

            new_lpc = np.real(np.poly(new_roots))

            new_frame = librosa.lfilter(
                [0] + -1 * new_lpc[1:].tolist(),
                [1],
                frame
            )

            output[i:i+frame_length] += new_frame


        return output


    # ============================================================

    def normalize(self, y):

        max_val = np.max(np.abs(y))

        if max_val > 0:

            y = y / max_val

        return y



obfuscator = VoiceObfuscator()
