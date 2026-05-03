import subprocess
import re
import threading
import time


def _run_powershell(script):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        timeout=30,
    )


def voice_features_supported():
    try:
        result = _run_powershell(
            "Add-Type -AssemblyName System.Speech; Write-Output 'OK'"
        )
        return result.returncode == 0 and "OK" in result.stdout
    except Exception:
        return False


_voice_lock = threading.Lock()
_active_voice_thread = None
_active_voice_process = None
_stop_voice_event = threading.Event()


def list_available_voices():
    if not voice_features_supported():
        return []

    script = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }"
    )
    try:
        result = _run_powershell(script)
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def get_default_voice_name():
    voices = list_available_voices()
    for preferred in ("Zira", "Hazel", "Sonia", "Heera", "female"):
        for voice in voices:
            if preferred.lower() in voice.lower():
                return voice
    return voices[0] if voices else None


def _prepare_speech_text(text):
    cleaned = text
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
    cleaned = re.sub(r"`(.*?)`", r"\1", cleaned)
    cleaned = re.sub(r"^\s*[-*]\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.replace("|", ". ")
    cleaned = cleaned.replace(":", ". ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:3500]


def chunk_speech_text(text, max_chunk_length=260):
    cleaned = _prepare_speech_text(text)
    if not cleaned:
        return []

    sentence_parts = re.split(r"(?<=[.!?])\s+", cleaned)
    chunks = []
    current_chunk = ""

    for part in sentence_parts:
        if not part:
            continue
        proposed = f"{current_chunk} {part}".strip() if current_chunk else part
        if len(proposed) <= max_chunk_length:
            current_chunk = proposed
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = part

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def speak_text(text, voice_name=None, rate=-2, volume=100):
    if not voice_features_supported():
        return False, "Voice output is not available on this system."

    safe_text = _prepare_speech_text(text).replace("'", "''")
    voice_name = voice_name or get_default_voice_name()

    voice_line = ""
    if voice_name:
        safe_voice = voice_name.replace("'", "''")
        voice_line = (
            "$matchingVoice = $synth.GetInstalledVoices() | "
            "ForEach-Object { $_.VoiceInfo.Name } | "
            f"Where-Object {{ $_ -like '*{safe_voice}*' }} | Select-Object -First 1; "
            "if ($matchingVoice) { $synth.SelectVoice($matchingVoice) }; "
        )

    script = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$synth.Rate = {int(rate)}; "
        f"$synth.Volume = {int(volume)}; "
        f"{voice_line}"
        f"$synth.Speak('{safe_text}');"
    )

    try:
        result = _run_powershell(script)
        if result.returncode != 0:
            return False, (result.stderr or "Voice output failed.").strip()
        return True, "Voice output played."
    except Exception as exc:
        return False, str(exc)


def _build_speech_script(text, voice_name=None, rate=-2, volume=100):
    safe_text = _prepare_speech_text(text).replace("'", "''")
    voice_name = voice_name or get_default_voice_name()

    voice_line = ""
    if voice_name:
        safe_voice = voice_name.replace("'", "''")
        voice_line = (
            "$matchingVoice = $synth.GetInstalledVoices() | "
            "ForEach-Object { $_.VoiceInfo.Name } | "
            f"Where-Object {{ $_ -like '*{safe_voice}*' }} | Select-Object -First 1; "
            "if ($matchingVoice) { $synth.SelectVoice($matchingVoice) }; "
        )

    return (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$synth.Rate = {int(rate)}; "
        f"$synth.Volume = {int(volume)}; "
        f"{voice_line}"
        f"$synth.Speak('{safe_text}');"
    )


def stop_speaking():
    global _active_voice_process

    _stop_voice_event.set()
    with _voice_lock:
        process = _active_voice_process
        if process and process.poll() is None:
            try:
                process.terminate()
            except Exception:
                pass
        _active_voice_process = None

    return True, "Voice playback stopped."


def _speak_text_interruptible(text, voice_name=None, rate=-2, volume=100):
    global _active_voice_process

    if not voice_features_supported():
        return False, "Voice output is not available on this system."

    script = _build_speech_script(text, voice_name=voice_name, rate=rate, volume=volume)

    try:
        process = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        with _voice_lock:
            _active_voice_process = process

        while process.poll() is None:
            if _stop_voice_event.is_set():
                try:
                    process.terminate()
                except Exception:
                    pass
                break
            time.sleep(0.05)

        stdout, stderr = process.communicate()
        with _voice_lock:
            if _active_voice_process is process:
                _active_voice_process = None

        if _stop_voice_event.is_set():
            return False, "Voice playback stopped."
        if process.returncode not in (0, None):
            return False, (stderr or stdout or "Voice output failed.").strip()
        return True, "Voice output played."
    except Exception as exc:
        with _voice_lock:
            _active_voice_process = None
        return False, str(exc)


def speak_text_async(text, voice_name=None, rate=-2, volume=100, chunked=False):
    global _active_voice_thread

    def _worker():
        _stop_voice_event.clear()
        if chunked:
            chunks = chunk_speech_text(text)
            for chunk in chunks:
                if _stop_voice_event.is_set():
                    break
                _speak_text_interruptible(
                    chunk,
                    voice_name=voice_name,
                    rate=rate,
                    volume=volume,
                )
        else:
            _speak_text_interruptible(
                text,
                voice_name=voice_name,
                rate=rate,
                volume=volume,
            )

    with _voice_lock:
        if _active_voice_process and _active_voice_process.poll() is None:
            try:
                _active_voice_process.terminate()
            except Exception:
                pass
        _stop_voice_event.clear()
        thread = threading.Thread(target=_worker, daemon=True)
        _active_voice_thread = thread
        thread.start()

    return True, "Voice output started."


def listen_once(timeout_seconds=8):
    if not voice_features_supported():
        return False, "Voice input is not available on this system."

    script = f"""
Add-Type -AssemblyName System.Speech;
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine;
$recognizer.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar));
$recognizer.SetInputToDefaultAudioDevice();
$result = $recognizer.Recognize([TimeSpan]::FromSeconds({int(timeout_seconds)}));
if ($result -and $result.Text) {{
    Write-Output $result.Text
}} else {{
    Write-Output '__NO_SPEECH__'
}}
"""

    try:
        result = _run_powershell(script)
        if result.returncode != 0:
            return False, (result.stderr or "Voice input failed.").strip()

        transcript = result.stdout.strip()
        if transcript == "__NO_SPEECH__":
            return False, "I could not hear a clear voice input."
        if not transcript:
            return False, "No voice input captured."
        return True, transcript
    except Exception as exc:
        return False, str(exc)
