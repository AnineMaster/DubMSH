import os
import sys

# --- 1. Clone OmniVoice Repository and Install Dependencies ---
omnivoice_repo_path = "/content/OmniVoice"
if not os.path.exists(omnivoice_repo_path):
    print("Cloning OmniVoice repository...")
    !git clone https://github.com/k2-fsa/OmniVoice.git
else:
    print("OmniVoice repository already exists. Skipping clone.")

# Install core dependencies with pydub effects dependency
print("Installing core Python dependencies...")
!pip install -q pysrt pydub transformers faster-whisper ctranslate2 demucs

# Install OmniVoice itself from source
print("Installing OmniVoice from source...")
!pip install -q -e {omnivoice_repo_path}/

if omnivoice_repo_path not in sys.path:
    sys.path.insert(0, omnivoice_repo_path)
    print(f"Added {omnivoice_repo_path} to sys.path.")

print("\n--- Setup Complete ---\n")


# --- 2. Write Corrected subtitle.py with WHISPER LARGE-V3 & 100+ Language Code Mapper ---
subtitle_content_to_write = '''# File: /content/OmniVoice/omnivoice/subtitle.py
print("Loading /content/OmniVoice/omnivoice/subtitle.py with Whisper Large-V3 & Multilingual Mapper")

from faster_whisper import WhisperModel
import torch
import os

# Comprehensive Whisper ISO-639-1 Language Code Map (100+ Languages)
WHISPER_LANG_MAP = {
    "english": "en", "hindi": "hi", "urdu": "ur", "spanish": "es", "french": "fr", "german": "de",
    "italian": "it", "portuguese": "pt", "russian": "ru", "chinese": "zh", "japanese": "ja",
    "korean": "ko", "arabic": "ar", "turkish": "tr", "vietnamese": "vi", "polish": "pl",
    "dutch": "nl", "indonesian": "id", "bengali": "bn", "marathi": "mr", "tamil": "ta",
    "telugu": "te", "gujarati": "gu", "punjabi": "pa", "kannada": "kn", "malayalam": "ml",
    "nepali": "ne", "sinhala": "si", "thai": "th", "persian": "fa", "swedish": "sv",
    "norwegian": "no", "danish": "da", "finnish": "fi", "hebrew": "he", "ukrainian": "uk",
    "romanian": "ro", "hungarian": "hu", "greek": "el", "catalan": "ca", "czech": "cs",
    "slovak": "sk", "bulgarian": "bg", "croatian": "hr", "serbian": "sr", "slovenian": "sl",
    "lithuanian": "lt", "latvian": "lv", "estonian": "et", "macedonian": "mk", "albanian": "sq",
    "georgian": "ka", "armenian": "hy", "azerbaijani": "az", "kazakh": "kk", "uzbek": "uz",
    "kyrgyz": "ky", "tajik": "tg", "turkmen": "tk", "mongolian": "mn", "amharic": "am",
    "somali": "so", "swahili": "sw", "yoruba": "yo", "hausa": "ha", "igbo": "ig",
    "zulu": "zu", "xhosa": "xh", "shona": "sn", "malagasy": "mg", "welsh": "cy",
    "irish": "ga", "scottish gaelic": "gd", "basque": "eu", "galician": "gl", "latin": "la",
    "esperanto": "eo", "sanskrit": "sa", "bhojpuri": "bho", "maithili": "mai", "dogri": "doi",
    "konkani": "kok", "manipuri": "mni", "santhali": "sat", "sindhi": "sd", "odia": "or",
    "kashmiri": "ks"
}

_whisper_model = None

def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if torch.cuda.is_available() else "int8"
        print(f"Initializing Whisper Large-V3 on {device} ({compute_type})...")
        _whisper_model = WhisperModel(
            "Systran/faster-whisper-large-v3", 
            device=device, 
            compute_type=compute_type
        )
        print("Whisper Large-V3 loaded successfully.")
    return _whisper_model

def get_clean_lang_code(language_input):
    """Converts display names like 'English' or 'Hindi' to ISO-639-1 code ('en', 'hi')"""
    if not language_input:
        return None
        
    cleaned = str(language_input).strip().lower()
    
    # Check if it is already a 2-letter ISO code
    if len(cleaned) == 2:
        return cleaned
        
    # Return mapped code or None (None triggers Auto detection)
    return WHISPER_LANG_MAP.get(cleaned, None)

def subtitle_maker(audio_path, language=None):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = _get_whisper_model()
    
    # Standardize language string to valid code
    lang_code = get_clean_lang_code(language)

    try:
        print(f"Transcribing voice with Whisper Large-V3 (Resolved code: {lang_code})...")
        segments, info = model.transcribe(audio_path, language=lang_code)
        
        transcription_text = " ".join([seg.text for seg in segments]).strip()
        print(f"ASR Output: '{transcription_text}'")

        mock_results = ["", "", "", "", "", "", "", transcription_text]
        return mock_results
    except Exception as e:
        print(f"Error during Whisper Large-V3 transcription: {e}")
        raise

# Display codes
LANGUAGE_CODE = {
    "English": "en", "Hindi": "hi", "Urdu": "ur", "Spanish": "es", "French": "fr", 
    "German": "de", "Auto": None
}
'''

os.makedirs('/content/OmniVoice/omnivoice/', exist_ok=True)
subtitle_file_path = '/content/OmniVoice/omnivoice/subtitle.py'
with open(subtitle_file_path, 'w', encoding='utf-8') as f:
    f.write(subtitle_content_to_write)
    print(f"'{subtitle_file_path}' has been overwritten with Whisper Large-V3 & Code Mapper.\n")


# --- 3. Create Mock hf_mirror.py ---
hf_mirror_content = '''# File: /content/MENAVOICE-/hf_mirror.py
import os

def download_model(repo_id, download_folder, redownload=False, workers=6, use_snapshot=False):
    print(f"Mocking download_model for {repo_id}. Returning local path: {download_folder}")
    os.makedirs(download_folder, exist_ok=True)
    return download_folder
'''

os.makedirs('/content/MENAVOICE-/', exist_ok=True)
hf_mirror_file_path = '/content/MENAVOICE-/hf_mirror.py'
with open(hf_mirror_file_path, 'w', encoding='utf-8') as f:
    f.write(hf_mirror_content)
    print(f"'{hf_mirror_file_path}' has been created.\n")


# --- 4. Write app.py (With Demucs v4 HTDemucs_FT integration & Progress Bar) ---
gradio_code_modified = '''import os
import sys
import logging
import tempfile
from typing import Any, Dict
import gc
import subprocess
import glob

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import gradio as gr
import numpy as np
import torch
import scipy.io.wavfile as wavfile
import re
import uuid
import pysrt
from pydub import AudioSegment
from pydub.effects import normalize

temp_audio_dir="./Omni_Audio"
os.makedirs(temp_audio_dir, exist_ok=True)

from omnivoice.subtitle import subtitle_maker

try:
    from omnivoice.subtitle import LANGUAGE_CODE as WHISPER_LANGUAGE_CODE
except ImportError:
    WHISPER_LANGUAGE_CODE = None

from omnivoice import OmniVoice, OmniVoiceGenerationConfig
from omnivoice.utils.lang_map import LANG_NAMES, lang_display_name

# Model Loading
print("Loading model from k2-fsa/OmniVoice to cuda ...")
from hf_mirror import download_model

try:
    model = OmniVoice.from_pretrained(
            "k2-fsa/OmniVoice",
            device_map="cuda",
            dtype=torch.float16,
            load_asr=False,
        )
except Exception as e:
    omnivoice_model_path = download_model(
            "k2-fsa/OmniVoice",
            download_folder="./OmniVoice_Model",
            redownload=False,
            workers=6,
            use_snapshot=False,
        )
    model = OmniVoice.from_pretrained(
            omnivoice_model_path,
            device_map="cuda",
            dtype=torch.float16,
            load_asr=False,
        )
sampling_rate = model.sampling_rate
print("Model loaded successfully!")

# --- Auto Transcription Helper ---
def _auto_transcribe_voice(audio_path, lang):
    if not audio_path:
        return gr.update(value="", placeholder="Kripya reference audio upload karein...")
    try:
        print(f"Whisper Large-V3 auto-transcribing: {audio_path}")
        whisper_lang = lang if lang != "Auto" else None
        whisper_results = subtitle_maker(audio_path, whisper_lang)
        if whisper_results and len(whisper_results) > 7:
            transcribed_text = whisper_results[7].strip()
            print(f"Transcribed successfully: '{transcribed_text}'")
            return gr.update(value=transcribed_text)
    except Exception as e:
        print(f"Auto-transcription error: {e}")
        return gr.update(value="", placeholder="Transcription failed. Aap manually likh sakte hain.")

# --- SRT to Cloned Audio Function ---
def srt_to_audio_gradio(srt_file, srt_text_paste, ref_audio, ref_text, language, steps, guidance_scale):
    srt_content = None
    if srt_file:
        with open(srt_file.name, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    elif srt_text_paste and srt_text_paste.strip():
        srt_content = srt_text_paste.strip()

    if not srt_content or not ref_audio:
        return None, "Kripya SRT content aur Reference Audio dono provide karein."

    if not ref_text or not ref_text.strip():
        return None, "Reference Text khali hai."

    temp_dir = "./temp_gradio_segments"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        print("="*60)
        print("VERIFICATION: Sending reference text to model:")
        print(f"--> '{ref_text.strip()}'")
        print("="*60)

        voice_clone_prompt = model.create_voice_clone_prompt(ref_audio=ref_audio, ref_text=ref_text.strip())

        if srt_file: 
            subs = pysrt.open(srt_file.name)
        else: 
            subs = pysrt.from_string(srt_content)

        audio_segments = []

        gen_config = OmniVoiceGenerationConfig(
            num_step=int(steps),
            guidance_scale=float(guidance_scale),
            denoise=True,
            preprocess_prompt=True,
            postprocess_output=True,
        )

        for index, sub in enumerate(subs):
            text = sub.text.strip()
            if not text:
                continue

            temp_segment_path = os.path.join(temp_dir, f"seg_{index}.wav")
            kw = dict(
                text=text,
                language=language if language != "Auto" else None,
                generation_config=gen_config,
                voice_clone_prompt=voice_clone_prompt
            )

            audio = model.generate(**kw)
            waveform = (audio[0] * 32767).astype(np.int16)
            wavfile.write(temp_segment_path, sampling_rate, waveform)

            seg_audio = AudioSegment.from_wav(temp_segment_path)
            seg_audio = normalize(seg_audio)

            audio_segments.append({
                "start": sub.start.ordinal,
                "audio": seg_audio
            })

            del audio, waveform
            torch.cuda.empty_cache()
            gc.collect()

        if not audio_segments:
            return None, "Koi audio segment generate nahi ho paya."

        final_duration = subs[-1].end.ordinal + 2000
        merged_audio = AudioSegment.silent(duration=final_duration)

        for item in audio_segments:
            merged_audio = merged_audio.overlay(item["audio"], position=item["start"])

        out_wav_path = os.path.join(temp_audio_dir, f"srt_cloned_{uuid.uuid4().hex[:6]}.wav")
        merged_audio.export(out_wav_path, format="wav")

        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

        return out_wav_path, f"Done! Perfect voice cloning complete using text: '{ref_text[:30]}...'"
    except Exception as e:
        return None, f"Error: {e}"


# --- 5. ADVANCED DUBBING PIPELINE (With Demucs v4 HTDemucs_FT & Live Progress Bar) ---
def srt_dynamic_dubbing_gradio(
    srt_file, srt_text_paste, media_file, source_lang, target_lang, steps, guidance_scale, use_demucs,
    progress=gr.Progress(track_tqdm=True)
):
    srt_content = None
    if srt_file:
        with open(srt_file.name, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    elif srt_text_paste and srt_text_paste.strip():
        srt_content = srt_text_paste.strip()

    if not srt_content or not media_file:
        return None, "Kripya SRT file aur original Video/Audio upload karein."

    temp_dir = "./temp_dubbing_segments"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        progress(0, desc="Extracting original audio track from media...")
        original_audio = AudioSegment.from_file(media_file.name)
        total_audio_length = len(original_audio)

        # OPTIONAL DEMUCS V4 HTDEMUCS_FT SEPARATION
        no_vocals_audio = None
        if use_demucs:
            progress(0.05, desc="Running Extreme Demucs HTDemucs_FT separation...")
            demucs_out_dir = "/content/demucs_out"
            
            cmd = [
                "demucs", 
                "-n", "htdemucs_ft", 
                "--two-stems", "vocals", 
                "-o", demucs_out_dir, 
                media_file.name
            ]
            print(f"Executing Demucs: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            
            no_vocals_files = glob.glob(f"{demucs_out_dir}/htdemucs_ft/**/no_vocals.wav", recursive=True)
            if no_vocals_files:
                bgm_path = no_vocals_files[0]
                print(f"Demucs background music found: {bgm_path}")
                no_vocals_audio = AudioSegment.from_wav(bgm_path)
            else:
                print("Warning: Demucs output files not found. Falling back to non-demucs mode.")
                use_demucs = False

        if srt_file:
            subs = pysrt.open(srt_file.name)
        else:
            subs = pysrt.from_string(srt_content)

        audio_segments = []

        gen_config = OmniVoiceGenerationConfig(
            num_step=int(steps),
            guidance_scale=float(guidance_scale),
            denoise=True,
            preprocess_prompt=True,
            postprocess_output=True,
        )

        for index, sub in enumerate(progress.tqdm(subs, desc="Processing dynamic segments")):
            text = sub.text.strip()
            start_ms = sub.start.ordinal
            end_ms = sub.end.ordinal
            duration = end_ms - start_ms
            
            if not text:
                continue

            print("-" * 50)
            print(f"Processing Dubbing Segment {index+1}/{len(subs)} ({sub.start} --> {sub.end})")
            
            # --- SMART 5-SECOND EXPANSION ---
            ref_slice_path = os.path.join(temp_dir, f"ref_slice_{index}.wav")
            if duration < 5000:
                deficit = 5000 - duration
                pad_backward = deficit // 2
                pad_forward = deficit - pad_backward
                new_start = max(0, start_ms - pad_backward)
                new_end = min(total_audio_length, end_ms + pad_forward)
                if new_start == 0:
                    new_end = min(total_audio_length, 5000)
                if new_end == total_audio_length:
                    new_start = max(0, total_audio_length - 5000)
                
                print(f"Expanding short clip window to 5s: [{new_start/1000:.2f}s -> {new_end/1000:.2f}s]")
                audio_slice = original_audio[new_start:new_end]
            else:
                audio_slice = original_audio[start_ms:end_ms]

            audio_slice.export(ref_slice_path, format="wav")

            # Whisper Transcription (Passing raw text string - resolved inside subtitle.py)
            ref_text = ""
            try:
                whisper_results = subtitle_maker(ref_slice_path, source_lang)
                if whisper_results and len(whisper_results) > 7:
                    ref_text = whisper_results[7].strip()
                    print(f"ASR Padded Output: '{ref_text}'")
            except Exception as e:
                print(f"Warning: Segment transcription failed: {e}")

            if not ref_text:
                ref_text = "speech" 

            voice_clone_prompt = model.create_voice_clone_prompt(ref_audio=ref_slice_path, ref_text=ref_text)

            temp_segment_path = os.path.join(temp_dir, f"seg_{index}.wav")
            kw = dict(
                text=text,
                language=target_lang if target_lang != "Auto" else None,
                generation_config=gen_config,
                voice_clone_prompt=voice_clone_prompt
            )

            audio = model.generate(**kw)
            waveform = (audio[0] * 32767).astype(np.int16)
            wavfile.write(temp_segment_path, sampling_rate, waveform)

            seg_audio = AudioSegment.from_wav(temp_segment_path)
            seg_audio = normalize(seg_audio)

            audio_segments.append({
                "start": start_ms,
                "end": end_ms,
                "audio": seg_audio
            })

            del audio, waveform
            torch.cuda.empty_cache()
            gc.collect()

        progress(0.95, desc="Timeline merging and background music sync in progress...")

        # --- ADVANCED TIMELINE MERGING (UNTOUCHED GAPS) ---
        final_dubbed_audio = AudioSegment.silent(duration=total_audio_length)
        current_time = 0

        subs_sorted = sorted(audio_segments, key=lambda x: x["start"])

        for item in subs_sorted:
            seg_start = item["start"]
            seg_end = item["end"]
            cloned_audio = item["audio"]

            if seg_start > current_time:
                gap_original = original_audio[current_time:seg_start]
                final_dubbed_audio = final_dubbed_audio.overlay(gap_original, position=current_time)

            if use_demucs and no_vocals_audio is not None:
                bgm_slice = no_vocals_audio[seg_start:seg_end]
                dubbed_scene = bgm_slice.overlay(cloned_audio, position=0)
            else:
                original_slice = original_audio[seg_start:seg_end]
                ducked_slice = original_slice - 20  
                dubbed_scene = ducked_slice.overlay(cloned_audio, position=0)

            final_dubbed_audio = final_dubbed_audio.overlay(dubbed_scene, position=seg_start)
            current_time = seg_end

        if current_time < total_audio_length:
            last_gap_original = original_audio[current_time:total_audio_length]
            final_dubbed_audio = final_dubbed_audio.overlay(last_gap_original, position=current_time)

        out_wav_path = os.path.join(temp_audio_dir, f"dubbed_output_{uuid.uuid4().hex[:6]}.wav")
        final_dubbed_audio.export(out_wav_path, format="wav")

        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists("/content/demucs_out"):
            shutil.rmtree("/content/demucs_out", ignore_errors=True)

        return out_wav_path, "AI Dubbing complete! Non-SRT parts are preserved 100% untouched."
        
    except Exception as e:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists("/content/demucs_out"):
            shutil.rmtree("/content/demucs_out", ignore_errors=True)
        return None, f"Dubbing failed: {e}"


# UI Configs
_ALL_LANGUAGES = ["Auto"] + sorted(lang_display_name(n) for n in LANG_NAMES)

theme = gr.themes.Soft(font=["Inter", "Arial", "sans-serif"])

with gr.Blocks(theme=theme, title="OmniVoice Demo") as demo:
    gr.HTML("<div style='text-align: center;'><h1>🎙️ OmniVoice Advanced AI Dubbing System</h1></div>")

    with gr.Tabs():
        # Tab 1: Voice Clone (Original)
        with gr.TabItem("Voice Clone"):
            vc_text = gr.Textbox(label="Text to Synthesize", lines=4)
            vc_lang = gr.Dropdown(label="Language (optional)", choices=_ALL_LANGUAGES, value="Auto")
            vc_ref_audio = gr.Audio(label="Reference Audio", type="filepath")
            vc_ref_text = gr.Textbox(label="Reference Text", lines=2)
            vc_btn = gr.Button("Generate")
            vc_audio = gr.Audio(label="Output Audio")
            vc_status = gr.Textbox(label="Status")

            vc_ref_audio.change(
                fn=_auto_transcribe_voice,
                inputs=[vc_ref_audio, vc_lang],
                outputs=[vc_ref_text]
            )

        # Tab 2: Classic SRT to Audio (Static reference voice)
        with gr.TabItem("Classic SRT to Audio"):
            gr.Markdown("### Upload SRT and a single voice sample to generate synchronized audio.")
            with gr.Row():
                with gr.Column():
                    srt_file_input = gr.File(label="Upload SRT File (.srt)", file_types=[".srt"])
                    srt_text_paste_input = gr.Textbox(label="Or Paste SRT Content Here", lines=5, placeholder="Paste your SRT text...")
                    srt_ref_audio = gr.Audio(label="Reference Voice Audio (.wav)", type="filepath")
                    srt_lang = gr.Dropdown(label="Language", choices=_ALL_LANGUAGES, value="Auto")

                    with gr.Accordion("Advanced Settings", open=False):
                        steps_slider = gr.Slider(minimum=10, maximum=150, value=64, step=1, label="Inference Steps")
                        guidance_slider = gr.Slider(minimum=0.5, maximum=4.0, value=2.0, step=0.1, label="Guidance Scale (CFG)")

                    srt_ref_text = gr.Textbox(label="Auto-Transcribed Reference Text", lines=3)
                    srt_generate_btn = gr.Button("Generate Synchronized SRT Audio", variant="primary")
                with gr.Column():
                    srt_audio_output = gr.Audio(label="Final Merged Audio")
                    srt_status_output = gr.Textbox(label="Status")

                    srt_ref_audio.change(
                        fn=_auto_transcribe_voice,
                        inputs=[srt_ref_audio, srt_lang],
                        outputs=[srt_ref_text]
                    )

                    srt_generate_btn.click(
                        fn=srt_to_audio_gradio,
                        inputs=[srt_file_input, srt_text_paste_input, srt_ref_audio, srt_ref_text, srt_lang, steps_slider, guidance_slider],
                        outputs=[srt_audio_output, srt_status_output]
                    )

        # Tab 3: Dynamic Dubbing Pipeline (Auto Segment-by-Segment Cutting & Transcribing)
        with gr.TabItem("AI Dubbing Pipeline 🎥🎬"):
            gr.Markdown("### Upload original Media + Translated SRT. System will automatically expand short segments (<5s) for robust voice quality.")
            with gr.Row():
                with gr.Column():
                    dub_srt_input = gr.File(label="Upload SRT File (.srt) [Translated/Target text]", file_types=[".srt"])
                    dub_srt_paste = gr.Textbox(label="Or Paste SRT Content Here", lines=5, placeholder="Paste translated SRT text here...")
                    
                    dub_media_input = gr.File(label="Upload Original Media File (Video MP4/MKV or Audio WAV/MP3)", file_types=["video", "audio"])
                    
                    # DEMUCS CRASH PREVENT CHECKBOX
                    dub_use_demucs = gr.Checkbox(
                        label="Activate Demucs (BGM Separation - Extreme HTDemucs_FT v4 Model)", 
                        value=False,
                        info="ON: Studio-grade separation. OFF: Auto-Ducking mode (Extremely safe, lightweight, prevents CUDA crashes)."
                    )

                    with gr.Row():
                        dub_source_lang = gr.Dropdown(label="Original Audio Language (for Whisper ASR)", choices=_ALL_LANGUAGES, value="Auto")
                        dub_target_lang = gr.Dropdown(label="Dubbing/SRT Language (for OmniVoice TTS)", choices=_ALL_LANGUAGES, value="Auto")

                    with gr.Accordion("Advanced Dubbing Settings", open=False):
                        dub_steps = gr.Slider(minimum=10, maximum=150, value=64, step=1, label="Inference Steps")
                        dub_guidance = gr.Slider(minimum=0.5, maximum=4.0, value=2.0, step=0.1, label="Guidance Scale (CFG)")

                    dub_generate_btn = gr.Button("Start AI Dubbing", variant="primary")
                with gr.Column():
                    dub_audio_output = gr.Audio(label="Dubbed Audio Output")
                    dub_status_output = gr.Textbox(label="Dubbing Status")

                    # Binding click with gr.Progress() tracker
                    dub_generate_btn.click(
                        fn=srt_dynamic_dubbing_gradio,
                        inputs=[dub_srt_input, dub_srt_paste, dub_media_input, dub_source_lang, dub_target_lang, dub_steps, dub_guidance, dub_use_demucs],
                        outputs=[dub_audio_output, dub_status_output]
                    )

if __name__ == "__main__":
    demo.queue().launch(share=True, debug=True)
'''

os.makedirs('/content/MENAVOICE-/', exist_ok=True)
app_file_path = '/content/MENAVOICE-/app.py'
with open(app_file_path, 'w', encoding='utf-8') as f:
    f.write(gradio_code_modified)
    print(f"'{app_file_path}' has been written/overwritten.\n")

# --- 5. Run app.py ---
print("Launching Gradio application. Look for the public URL below.")
!python {app_file_path}
