import subprocess
import platform

class AudioNotifier:
    @staticmethod
    def play_alert_sound(sound_name="Glass"):
        """Plays a native macOS system sound or notification chime."""
        if platform.system() == "Darwin":  # macOS
            # Available macOS sounds: Glass, Ping, Purr, Sosumi, Bottle, Funk
            sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
            subprocess.run(["afplay", sound_path])
        else:
            print("🔊 *Alert Ringtone Triggered!*")
