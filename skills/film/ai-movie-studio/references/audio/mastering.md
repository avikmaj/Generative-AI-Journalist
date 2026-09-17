# Mastering — Final Loudness, Format & Delivery

## Mastering Is the Final Shape

Mastering takes the mixed audio and prepares it for its specific delivery format. A cinema mix is different from a streaming mix, which is different from a mobile mix. Mastering is not about making things louder — it is about making the final audio behave correctly in its delivery environment.

---

## Loudness Standards by Platform

| Platform | Standard | Target LUFS |
|---|---|---|
| Netflix | Netflix Audio | -27 LUFS integrated, -2 dBTP |
| YouTube | Streaming | -14 LUFS integrated |
| Cinema (theatrical) | Dolby / SMPTE | -24 LUFS (dialogue reference) |
| Broadcast (TV) | ATSC A/85 | -24 LUFS |
| Mobile / social media | Mixed | -14 to -16 LUFS |
| Music (album) | Streaming masters | -14 LUFS |

**LUFS:** Loudness Units relative to Full Scale — the integrated loudness measure.
**dBTP:** Decibels True Peak — maximum peak level before clipping.

---

## Dynamic Range

Theatrical and streaming mixes preserve a wide dynamic range (the difference between quietest and loudest moments). This is what gives a big film its impact — the silences are genuinely quiet and the impacts are genuinely loud.

**Mastering for cinema:** Allow the full dynamic range. Don't compress down to a narrow band.

**Mastering for mobile/social:** Compress somewhat to account for playback in noisy environments where dynamic range is less effective.

---

## Delivery Format Checklist

For any final film delivery:

```
[ ] Integrated loudness measured and within platform spec
[ ] True peak below -1 dBTP
[ ] Dialogue level consistent across the runtime
[ ] Music level appropriate to final mix
[ ] No audio clipping in any channel
[ ] Stereo mix and surround mix (if applicable) both checked
[ ] Audio sample rate appropriate to delivery format (48kHz for video)
[ ] Bit depth appropriate (24-bit for delivery masters, 16-bit for compressed deliverable)
[ ] Metadata correct (title, language, channels declared)
```

---

## Common Mastering Notes for AI Film Production

For AI-generated content delivered to video platforms:

- Target -14 LUFS for YouTube and social media delivery
- Ensure dialogue peaks do not exceed -3 dBTP
- Use mild compression on the final master to control dynamics within platform normalization
- Ensure music doesn't wash out dialogue by checking mix balance at -14 LUFS normalization
- Export video with audio at 48kHz, 24-bit, AAC or PCM depending on platform

---

## Golden Rule

> Master for where it lives. A mix that sounds incredible on studio monitors and terrible on a phone failed mastering. Know your delivery environment and optimize for it.
