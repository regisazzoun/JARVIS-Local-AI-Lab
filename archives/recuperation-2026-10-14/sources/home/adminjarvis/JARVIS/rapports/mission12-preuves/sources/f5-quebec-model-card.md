---
license: cc-by-nc-4.0
language:
  - fr
pipeline_tag: text-to-speech
base_model: RASPIAUDIO/F5-French-MixedSpeakers-reduced
tags:
  - f5-tts
  - text-to-speech
  - french
  - quebec-french
  - voice-cloning
---

# F5-TTS — Quebec French (Québécois) finetune

A zero-shot voice-cloning TTS checkpoint specialized for **Quebec French**. Give it a
short reference clip of any voice and it clones that voice while applying Québécois
pronunciation, prosody, and vocabulary.

Finetune of [F5-TTS](https://github.com/SWivid/F5-TTS) (`F5TTS_Base` architecture,
vocos vocoder), warm-started from
[RASPIAUDIO/F5-French-MixedSpeakers-reduced](https://huggingface.co/RASPIAUDIO/F5-French-MixedSpeakers-reduced)
and trained on a Québécois-accent-tagged subset of Mozilla Common Voice (fr).

**License note:** the warm-start base checkpoint is CC-BY-NC-4.0. This finetune
inherits that restriction — **non-commercial use only**. The training data itself is
CC0-1.0.

## Quickstart

```bash
pip install f5-tts

f5-tts_infer-cli \
  --model F5TTS_Base \
  --ckpt_file model_quebec_v1.safetensors \
  --vocab_file vocab.txt \
  --ref_audio your_reference.wav \
  --ref_text "Transcript of the reference clip." \
  --gen_text "Je m'en vais au dépanneur chercher de la liqueur pis des chips."
```

Download the two required files with:

```bash
huggingface-cli download tontate/f5-tts-quebec-french-finetune \
  model_quebec_v1.safetensors vocab.txt
```

Tips: use a clean 3–10 s reference clip; leave `--ref_text ""` to auto-transcribe it.
The checkpoint clones *any* voice — a Québécois-accented reference gives the most
consistent results.

## Audio samples

Generated with the final checkpoint (voice `qc_a`); more in [`samples/`](samples/).

*« Il faut que je stationne mon char devant le dépanneur. »*

<audio controls src="https://huggingface.co/tontate/f5-tts-quebec-french-finetune/resolve/main/samples/final_67750/qc_a/00.wav"></audio>

*« Fait qu'on a fini par jaser toute la soirée sur la galerie. »*

<audio controls src="https://huggingface.co/tontate/f5-tts-quebec-french-finetune/resolve/main/samples/final_67750/qc_a/04.wav"></audio>

*« Ça coûte quatre-vingt-dix-sept dollars et trente-cinq sous. »*

<audio controls src="https://huggingface.co/tontate/f5-tts-quebec-french-finetune/resolve/main/samples/final_67750/qc_a/08.wav"></audio>

## Files

| File | Size | Use |
|---|---|---|
| `model_quebec_v1.safetensors` | 1.35 GB | **Recommended for inference** — EMA weights only |
| `model_last.pt` | 5.39 GB | Full training checkpoint (model + EMA + optimizer) — for resuming training |
| `checkpoints/model_9000.pt`, `checkpoints/model_12000.pt` | 5.39 GB each | Intermediate training checkpoints |
| `vocab.txt` | 14 kB | Tokenizer vocab (unchanged from base / F5-TTS default) |
| `scripts/prep_common_voice_qc.py` | — | Dataset preparation script (reproducible) |
| `dataset/processed_qc_dataset.tar.gz` | — | The processed training set |
| `samples/` | — | Eval-sentence audio (2 voices) + per-checkpoint training-trajectory samples |

`model_quebec_v1.safetensors` contains exactly the EMA weights of `model_last.pt`
(bitwise-identical extraction, verified), repackaged for safe, fast loading.

## Training

- **Data:** Common Voice fr (Scripted Speech 26.0), CC0-1.0, filtered to clips with
  Québécois/Canadien `accent` metadata. Final set: 11,542 clips, 281 speakers,
  12.01 hours (after resample to 24 kHz mono, silence trim, dedup, 1–15 s length
  filter). Prep script included in `scripts/`.
- **Run:** 50 epochs / 67,750 updates with the F5-TTS finetuning trainer on a single
  RTX A5000 (24 GB), warm-started from the base checkpoint with its vocab unchanged.
- Training loss plateaued early (≈ epoch 2); trajectory samples for every 1,000
  updates are in `samples/training_trajectory/` if you want to compare checkpoints.

## Evaluation

Evaluated on a 50-sentence Québécois test battery targeting dialect-specific
phenomena (affrication, vowel laxing, /a/–/ɑ/ contrast & diphthongs, QC
lexicon/elisions, numbers, question particles & prosody), synthesized with
3 reference voices, and compared against the warm-start base model
(`RASPIAUDIO/F5-French-MixedSpeakers-reduced`, France-accented). Scripts and
the sentence list are in [`scripts/eval/`](scripts/eval/).

| Metric | Base (France) | **This model (Québec)** |
|---|---|---|
| WER ↓ (faster-whisper large-v3) | 0.067 | 0.077 |
| CER ↓ | 0.041 | 0.043 |
| Speaker similarity ↑ (ECAPA cosine) | 0.479 | **0.675** |
| Accent probe: mean P(Québec) ↑ | 0.17 | **0.40** |

- **Intelligibility is preserved**: WER/CER are comparable; the finetune's small
  gap concentrates in QC lexicon and elisions ("t'sé", "pis") that the ASR
  normalizes to standard French spellings.
- **Voice cloning improves markedly** on Québécois reference voices (+0.20
  cosine), as expected from in-domain training.
- **Accent probe**: a logistic-regression classifier over mid-layer XLS-R-300m
  embeddings, trained to separate real Québec-tagged vs. European-tagged
  (France/Belgium/Switzerland) Common Voice fr clips — held-out accuracy 0.82 on
  speaker-disjoint test speakers. Applied to the generated audio, it rates the
  probability the audio sounds Québécois.
- **Human check**: informal native-listener review judged the output distinctly
  Québécois (satisfactory) rather than European French.

Caveats: reference clips are drawn from the training corpus (speaker-similarity
numbers are in-domain); the accent probe is a proxy, not a listening test;
number-heavy sentences are hardest for both models — write numbers out in words.

## Limitations

- Non-commercial license (inherited from the base checkpoint).
- 12 hours of training data: rare words, heavy anglicisms, and long-form prosody may
  be less stable; write numbers out in words for best results.
- Common Voice accent tags are self-reported; the training accent mix is
  broadly Québécois/Canadian rather than a single regional variety.
