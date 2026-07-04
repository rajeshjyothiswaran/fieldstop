#!/usr/bin/env python3
"""Assemble the GFX100S II Field Guide knowledge base into assets/data.js.
All content is authored from the uploaded Owner's Manual (BL00005287-202 EN)
and New Features Guide v1.20, plus verified firmware status (Ver 1.20, Sep 2025,
latest for the GFX100S II as of build)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
menu_tree = json.load(open(os.path.join(HERE, "menu_tree.json"), encoding="utf-8"))

# ---------------------------------------------------------------------------
# FIRMWARE STATUS
# ---------------------------------------------------------------------------
firmware = {
    "current": "1.20",
    "released": "September 2, 2025",
    "verified": "Latest firmware for the GFX100S II as of this build (July 2026).",
    "note": "The GFX100 II (a different, higher-tier body) is on v2.50 — that update does NOT apply to your GFX100S II.",
    "how_to_check": [
        "Turn the camera OFF and make sure a card is inserted.",
        "Hold the DISP/BACK button, then turn the camera ON while still holding it.",
        "The body and lens firmware versions appear on screen.",
    ],
    "changes": [
        {"title": "Smartphone pairing changed",
         "body": "Pairing now goes through Bluetooth via the FUJIFILM XApp. Press DISP/BACK while shooting info is shown, choose Bluetooth, then PAIRING, launch XApp, and confirm the matching code on both devices. Older Camera Remote (iOS) and Camera Remote 4.1 or earlier (Android) no longer connect.",
         "kind": "changed"},
        {"title": "\u201cWireless Communication\u201d menu items removed",
         "body": "The WIRELESS COMMUNICATION entries were deleted from SHOOTING SETTING, MOVIE SETTING and the PLAYBACK menu, and can no longer be assigned to a function button. Transfer images by pairing with XApp instead.",
         "kind": "removed"},
        {"title": "Instax printing removed",
         "body": "instax PRINTER PRINT and instax PRINTER CONNECTION SETTING were removed; SP-1/SP-2/SP-3 printers are no longer supported directly. Send images to your phone via XApp, then print through the Instax app.",
         "kind": "removed"},
        {"title": "Connection settings reset",
         "body": "Updating resets SELECT CONNECTION SETTING to UNIVERSAL SETTING. If you use FTP or Frame.io Camera to Cloud, reconfigure those after updating.",
         "kind": "note"},
    ],
}

# ---------------------------------------------------------------------------
# FILM SIMULATIONS  (from manual p.128-129)
# ---------------------------------------------------------------------------
film_sims = [
    {"name": "PROVIA / STANDARD", "best": "Everyday, mixed subjects", "desc": "Balanced, true-to-life color and contrast. The safe default for a wide range of subjects."},
    {"name": "Velvia / VIVID", "best": "Landscape & nature", "desc": "Vibrant, saturated reproduction. Makes skies, foliage and sunsets pop; can be too punchy on skin."},
    {"name": "ASTIA / SOFT", "best": "Portraits, softer scenes", "desc": "Softer color and contrast for a subdued, gentle look with flattering skin."},
    {"name": "CLASSIC CHROME", "best": "Documentary, street, moody", "desc": "Muted color with deeper shadow contrast for a calm, editorial feel."},
    {"name": "REALA ACE", "best": "Accurate color, any scene", "desc": "Faithful color reproduction with firm, hard tonality. A versatile modern standard."},
    {"name": "PRO Neg. Hi", "best": "Studio & controlled portraits", "desc": "Portrait-oriented with slightly enhanced contrast for definition under soft light."},
    {"name": "PRO Neg. Std", "best": "Portraits to be retouched", "desc": "Neutral, low-contrast base with soft gradation and excellent skin tones. Ideal if you edit later."},
    {"name": "CLASSIC Neg.", "best": "Travel, everyday film look", "desc": "Enhanced color and hard tonality for added depth — the classic color-negative snapshot look."},
    {"name": "NOSTALGIC Neg.", "best": "Warm, printed-photo mood", "desc": "Amber-tinted highlights and rich shadow tone that evoke an old printed photograph."},
    {"name": "ETERNA / CINEMA", "best": "Video & muted stills", "desc": "Soft color and rich shadows for a filmic, understated look."},
    {"name": "ETERNA BLEACH BYPASS", "best": "Gritty, high-contrast", "desc": "Low saturation with high contrast for a raw, cinematic edge."},
    {"name": "ACROS", "best": "Fine black & white", "desc": "Premium monochrome with rich gradation and controlled grain. Pair with a Y/R/G filter for skies. (MONOCHROME is the plainer B&W option.)"},
]

# ---------------------------------------------------------------------------
# USE-CASE SCENARIOS  (the advisor knowledge base)
# Each: id,title,tags(keywords/synonyms),summary,settings[{c,v,why}],steps[],
#       related(feature ids), caution
# ---------------------------------------------------------------------------
S = []
def sc(**k): S.append(k)

sc(id="landscape", title="Sharp landscapes on a tripod",
   tags=["landscape","mountain","vista","scenery","valley","tripod","deep","sharp","depth of field","f11","wide","nature","hills","field","forest","sunrise","sunset","golden hour","view"],
   summary="Maximize detail and front-to-back sharpness on a static scene.",
   settings=[
     {"c":"Aperture","v":"f/8\u2013f/11","why":"Peak sharpness across the frame without diffraction softening from tiny apertures."},
     {"c":"ISO","v":"80 (base)","why":"Cleanest files, maximum dynamic range. You're on a tripod, so slow shutter is fine."},
     {"c":"IS MODE (IBIS)","v":"OFF on tripod","why":"Stabilization can hunt against a rigid tripod and soften long exposures."},
     {"c":"SHUTTER TYPE","v":"MECHANICAL + 2-sec self-timer","why":"Avoids shutter-shock and hand-shake blur at slow speeds."},
     {"c":"FILM SIMULATION","v":"Velvia (punchy) or PROVIA/REALA ACE (neutral)","why":"Velvia lifts skies and foliage; shoot RAW to keep options."},
     {"c":"DYNAMIC RANGE / D RANGE PRIORITY","v":"AUTO or DR200 for bright skies","why":"Protects highlight detail in skies against shadowed foreground."},
   ],
   steps=["Mount on tripod, set aperture to f/8\u2013f/11.","Set ISO to 80.","Turn IS MODE off.","Set SHUTTER TYPE to mechanical and enable the 2-sec self-timer (DRIVE / self-timer).","Focus about one-third into the scene (or use focus check to confirm), then meter."],
   related=["is_mode","shutter_type","dynamic_range","drange_priority","film_simulation","self_timer"],
   caution="If the sky is far brighter than the land, bracket exposures (AE BKT) or use a grad filter.")

sc(id="longexposure", title="Long exposures — water, clouds, motion blur",
   tags=["long exposure","waterfall","water","silky","clouds","nd filter","10 stop","milky","motion","blur","river","sea","ocean","smooth","slow shutter","daytime long"],
   summary="Smooth moving water or clouds with a multi-second exposure.",
   settings=[
     {"c":"Exposure mode","v":"Manual, or set shutter directly","why":"You want full control of the shutter time."},
     {"c":"ISO","v":"80","why":"Base ISO lets you use the longest possible shutter and keeps noise minimal."},
     {"c":"Aperture","v":"f/8\u2013f/16","why":"Helps reach long shutter times and keeps depth."},
     {"c":"ND filter","v":"6\u201310 stops","why":"Cuts light so multi-second exposures are possible in daylight."},
     {"c":"LONG EXPOSURE NR","v":"ON","why":"Cleans up hot pixels and mottling on exposures over ~1 sec (doubles save time)."},
     {"c":"IS MODE","v":"OFF","why":"You're on a tripod; IBIS can introduce softness."},
   ],
   steps=["Compose and focus first, then attach the ND filter.","Switch focus to Manual so it won't hunt through the dark ND.","Set ISO 80, choose aperture, dial shutter for the blur you want (try 1\u201330 s).","Enable LONG EXPOSURE NR and use the 2-sec self-timer or a remote.","Review and adjust shutter time to taste."],
   related=["long_exposure_nr","is_mode","shutter_type","self_timer"],
   caution="Note: with the electronic shutter the flash won't fire and ISO is capped at 80\u201312800 \u2014 use the mechanical shutter here.")

sc(id="astro", title="Milky Way & nightscapes",
   tags=["astro","astrophotography","stars","night sky","milky way","galaxy","dark","nightscape","nightscapes","constellation","core","stargazing"],
   summary="Pin-sharp stars and a bright, low-noise sky on a single untracked frame.",
   settings=[
     {"c":"Focus","v":"Manual \u2014 magnify a bright star with FOCUS CHECK","why":"AF can't lock in the dark; magnified manual focus nails true infinity better than the hard stop."},
     {"c":"Aperture","v":"Widest sharp point (often f/2.8\u2013f/4)","why":"Gathers the most starlight; most GF lenses clean up their corner coma stopped down a touch."},
     {"c":"Shutter","v":"See the trailing guide below","why":"On 102MP the old 500-rule trails badly \u2014 the sensor resolves tiny star movement."},
     {"c":"ISO","v":"1600\u20136400 (try 3200)","why":"Lifts the sky without excess noise; the GFX stays clean here. Raise it rather than over-lengthening the shutter."},
     {"c":"PREVIEW EXP./WB IN MANUAL MODE","v":"OFF","why":"Stops the live view going black at night so you can actually compose and focus."},
     {"c":"White balance","v":"~3900 K (or Daylight, fix in RAW)","why":"Neutralizes orange skyglow for a natural night sky."},
     {"c":"LONG EXPOSURE NR","v":"ON for single shots","why":"Subtracts a dark frame to kill hot pixels/amp glow. Turn OFF for trail/time-lapse sequences (it leaves gaps)."},
     {"c":"IS MODE","v":"OFF","why":"IBIS can drift on a tripod and soften long frames."},
     {"c":"SHUTTER TYPE / RAW","v":"Mechanical, 14-bit RAW","why":"Electronic shutter disables Long-Exposure NR; RAW holds the most shadow latitude for editing."},
   ],
   steps=["Sturdy tripod, IS MODE off, manual focus, RAW.","Set PREVIEW EXP./WB IN MANUAL MODE to OFF and brighten the LCD/EVF so you can see.","FOCUS CHECK on a bright star; focus until it's the smallest point.","Aperture wide (or 1/3 stop in), ISO 3200, WB ~3900 K.","Pick shutter from the trailing guide; enable LONG EXPOSURE NR; fire with the 2-sec timer or remote.","Check the histogram \u2014 aim to keep data off the left wall; raise ISO before over-lengthening the shutter."],
   related=["focus_check","preview_exp_wb","disp_brightness","long_exposure_nr","is_mode","natural_live_view","interval_timer"],
   caution="Trailing guide (untracked, pin-sharp at 100% on 102MP): GF20-35/23mm \u2248 8\u201312 s \u00b7 30\u201345mm \u2248 5\u20138 s \u00b7 63mm+ \u2248 3\u20134 s. Want more light without trails? Use a star tracker (see 'star tracker') or stack several frames.")

sc(id="pixelshift", title="Maximum resolution — repro, fine art, product detail",
   tags=["pixel shift","high resolution","400mp","reproduction","repro","fine art","copy","detail","texture","gigapixel","large print","museum","artwork","multi shot","psms"],
   summary="Combine multiple shifted frames into an ultra-high-resolution file for flawless detail.",
   settings=[
     {"c":"DRIVE mode","v":"PIXEL SHIFT MULTI SHOT","why":"Captures a burst of sensor-shifted frames; two options: ACCURATE COLOR, or HIGH RESOLUTION + ACCURATE COLOR."},
     {"c":"Subject","v":"Completely static","why":"Any movement between frames breaks the combine."},
     {"c":"Support","v":"Sturdy tripod, remote/timer","why":"The frames must align precisely."},
     {"c":"ISO","v":"80","why":"Cleanest possible source frames."},
     {"c":"Processing","v":"FUJIFILM Pixel Shift Combiner (computer)","why":"The camera saves the frames; the free app merges them into the final high-res image."},
   ],
   steps=["Set the DRIVE button to PIXEL SHIFT MULTI SHOT and pick a variant.","Lock the camera on a tripod; light the subject evenly and keep it still.","ISO 80, careful focus, trigger with self-timer or remote.","The camera records the multi-frame set to the card.","Import to FUJIFILM Pixel Shift Combiner on your computer to build the final file."],
   related=["pixel_shift","is_mode","self_timer"],
   caution="This is a studio/tripod technique only \u2014 not for handheld or moving subjects.")

sc(id="architecture", title="Architecture & interiors",
   tags=["architecture","building","interior","real estate","perspective","keystone","straight lines","tilt shift","ts lens","room","facade","structure","vertical"],
   summary="Keep verticals straight and detail even across the frame.",
   settings=[
     {"c":"Aperture","v":"f/8\u2013f/11","why":"Even corner-to-corner sharpness."},
     {"c":"Electronic level","v":"ON","why":"Keeps the camera square so verticals stay parallel."},
     {"c":"FRAMING GUIDELINE","v":"Grid on","why":"Aligns lines to the frame edges."},
     {"c":"T/S lenses","v":"GF30/110 T-S supported","why":"Shift corrects converging verticals in-camera; distance & shift amount can display and record to EXIF."},
     {"c":"ISO","v":"80 (tripod) / as needed handheld","why":"Cleanest files for big architectural prints."},
   ],
   steps=["Level the camera using the ELECTRONIC LEVEL and grid guides.","Set aperture f/8\u2013f/11 and base ISO on a tripod.","For converging verticals, use a GF tilt-shift lens's shift, or leave headroom to correct later.","Bracket exposures for high-contrast interiors with windows."],
   related=["electronic_level","framing_guideline","dynamic_range","ae_bkt"],
   caution="Bright windows in interiors: bracket (AE BKT) and blend, or use D RANGE PRIORITY STRONG.")

sc(id="portrait", title="Portraits — eyes tack sharp, creamy background",
   tags=["portrait","people","person","headshot","face","eyes","skin","bokeh","blurry background","model","beauty","subject","couple","f2","shallow"],
   summary="Nail focus on the eye and separate the subject from the background.",
   settings=[
     {"c":"Aperture","v":"f/2\u2013f/4","why":"Shallow depth for background separation and that medium-format rendering."},
     {"c":"FACE/EYE DETECTION","v":"ON","why":"The camera finds and holds focus on the near eye automatically."},
     {"c":"Focus mode","v":"AF-C for moving people, AF-S for still","why":"AF-C tracks small movements and breathing; AF-S locks a posed shot."},
     {"c":"FILM SIMULATION","v":"PRO Neg. Std / ASTIA / REALA ACE","why":"Flattering, soft skin tones. PRO Neg. Std if you'll retouch."},
     {"c":"SMOOTH SKIN EFFECT","v":"WEAK if desired","why":"Gently softens skin in-camera without losing detail."},
     {"c":"Shutter","v":"1/(2\u00d7focal) or faster","why":"Freezes subtle subject motion."},
   ],
   steps=["Turn on FACE/EYE DETECTION (AF/MF menu).","Set focus mode to AF-C for a live subject, AF-S for a still pose.","Open up to f/2\u2013f/4; keep shutter fast enough to freeze movement.","Pick a flattering film simulation; add WEAK smooth skin if you like.","Place the AF point on the face and let eye-detection take over."],
   related=["face_eye","subject_detection","smooth_skin","film_simulation","afc_custom"],
   caution="At f/2 on 102MP, depth is razor-thin \u2014 confirm the near eye is the one in focus.")

sc(id="street", title="Street & candid — fast, quiet, ready",
   tags=["street","candid","documentary","reportage","quick","discreet","silent","zone focus","walk","urban","city","people","spontaneous","travel candid"],
   summary="Be quick and unobtrusive, and never miss a moment to focus hunting.",
   settings=[
     {"c":"Exposure mode","v":"Aperture priority (Auto shutter) + Auto ISO","why":"You control depth; the camera handles changing light."},
     {"c":"Aperture","v":"f/5.6\u2013f/8","why":"Enough depth that near-focus is forgiving for grab shots."},
     {"c":"Auto ISO","v":"Min shutter 1/250","why":"Keeps a shutter fast enough for walking subjects."},
     {"c":"SHUTTER TYPE","v":"Electronic (silent)","why":"Discreet, no shutter noise; watch for banding under some lights and rolling-shutter skew on fast motion."},
     {"c":"Focus","v":"AF-S single point, or MF zone focus","why":"Single point is decisive; zone focus (prefocus f/8) is instant."},
     {"c":"FILM SIMULATION","v":"CLASSIC CHROME / ACROS","why":"Editorial color or timeless B&W straight out of camera."},
   ],
   steps=["Set aperture priority, aperture f/5.6\u2013f/8, Auto ISO with a 1/250 floor.","Switch SHUTTER TYPE to electronic for silence.","Use a single AF point (or prefocus and zone-focus manually).","Pick CLASSIC CHROME or ACROS for finished-looking JPEGs.","Keep the camera on and half-press early."],
   related=["shutter_type","afc_custom","film_simulation","touch_screen","pre_af"],
   caution="Electronic shutter can skew fast-moving subjects and band under LED/fluorescent light \u2014 switch to mechanical if you see it.")

sc(id="wildlife", title="Wildlife & birds",
   tags=["wildlife","bird","birds","animal","safari","nature","tracking","fast","burst","teleconverter","zoo","pet","dog","cat","moving animal"],
   summary="Track erratic animal movement and fire bursts to catch the peak moment.",
   settings=[
     {"c":"Focus mode","v":"AF-C","why":"Continuously tracks a moving subject."},
     {"c":"SUBJECT DETECTION","v":"ANIMAL / BIRD","why":"The camera locks onto and follows the animal or bird automatically."},
     {"c":"DRIVE","v":"Continuous (burst)","why":"Multiple frames raise the odds of a sharp peak-action shot."},
     {"c":"AF-C CUSTOM","v":"Set for erratic/accelerating subjects","why":"Presets tune tracking sensitivity and how the AF handles sudden moves."},
     {"c":"Shutter","v":"1/1000\u20131/2000+","why":"Freezes wings and quick movement."},
     {"c":"ISO","v":"Auto (allow high)","why":"Fast shutter in the field needs the sensor to reach high ISO cleanly."},
   ],
   steps=["Focus mode to AF-C; enable SUBJECT DETECTION and choose ANIMAL or BIRD.","Pick an AF-C CUSTOM preset that matches the motion.","Set DRIVE to continuous, shutter 1/1000+, Auto ISO.","Keep the subject under an AF zone and half-press to acquire, then fire bursts."],
   related=["subject_detection","afc_custom","face_eye","is_mode","release_focus_priority"],
   caution="The GFX is medium-format, not a sports body \u2014 for very fast birds give AF room and shoot generous bursts.")

sc(id="action", title="Action, sports & panning",
   tags=["action","sports","fast","motion","freeze","panning","car","cyclist","runner","kids playing","movement","track"],
   summary="Either freeze the moment or pan for a sense of speed.",
   settings=[
     {"c":"Freeze shutter","v":"1/1000+","why":"Stops fast motion cleanly."},
     {"c":"Pan shutter","v":"1/30\u20131/125","why":"Blurs the background while the tracked subject stays sharp."},
     {"c":"Focus mode","v":"AF-C","why":"Holds focus on an approaching subject."},
     {"c":"DRIVE","v":"Continuous","why":"Improves your odds at the peak."},
     {"c":"IS MODE","v":"ON for panning","why":"Helps steady the horizontal sweep."},
   ],
   steps=["Choose freeze (1/1000+) or pan (1/30\u20131/125) shutter.","Set AF-C and continuous drive.","For panning, track the subject smoothly and shoot through the motion.","Follow through after the shutter fires."],
   related=["afc_custom","release_focus_priority","is_mode","shutter_type"],
   caution="With the electronic shutter, fast lateral motion can look skewed \u2014 use the mechanical shutter for action.")

sc(id="macro", title="Macro & focus stacking",
   tags=["macro","close up","close-up","flower","insect","product detail","focus stack","focus bracket","tiny","small","bug","texture","jewelry"],
   summary="Get tiny subjects sharp front-to-back by stacking a focus-bracketed sequence.",
   settings=[
     {"c":"DRIVE / FOCUS BKT SETTING","v":"Auto or manual step","why":"Shoots a series marching focus from front to back for stacking."},
     {"c":"Aperture","v":"f/5.6\u2013f/11","why":"Balances per-frame depth against diffraction; stacking covers the rest."},
     {"c":"Support","v":"Tripod + still subject","why":"Frames must align to stack cleanly."},
     {"c":"IS MODE","v":"OFF","why":"Tripod work; avoids drift between frames."},
     {"c":"Light","v":"Constant / flash","why":"Even light keeps the stack consistent."},
   ],
   steps=["Mount on a tripod; frame the subject.","Open FOCUS BKT SETTING and set frames/step (or AUTO between a near and far focus point).","Set aperture ~f/8, base ISO, steady light.","Fire the sequence with the self-timer or remote.","Stack the frames in software (e.g. Helicon/Photoshop) afterward."],
   related=["focus_bkt","is_mode","self_timer"],
   caution="Even a breeze ruins a stack \u2014 shoot indoors or shield the subject.")

sc(id="studioflash", title="Studio / product with flash",
   tags=["studio","flash","strobe","product","commercial","lighting","softbox","sync","ttl","packshot","tabletop","e-commerce","white background"],
   summary="Clean, controlled lighting with flash for products or studio portraits.",
   settings=[
     {"c":"SHUTTER TYPE","v":"Mechanical","why":"Flash won't fire on the fully electronic shutter (except with pixel-shift)."},
     {"c":"Shutter","v":"At/below the flash sync speed","why":"Faster than sync gives a black band unless you use HSS/FP flashes."},
     {"c":"Aperture","v":"f/8\u2013f/11","why":"Deep, even sharpness for product detail."},
     {"c":"ISO","v":"80","why":"Cleanest files; flash provides the light."},
     {"c":"FLASH FUNCTION SETTING","v":"TTL or Manual","why":"TTL for speed, Manual for repeatable studio output. TTL-LOCK holds a metered value."},
     {"c":"White balance","v":"Custom / flash","why":"Neutral, repeatable color on white backgrounds."},
   ],
   steps=["Set SHUTTER TYPE to mechanical.","Keep shutter at or below sync speed; f/8\u2013f/11; ISO 80.","Configure FLASH FUNCTION SETTING (TTL or Manual); set channel/commander if using off-camera units.","Set a custom or flash white balance for neutral color.","Dial flash power to taste and confirm the histogram."],
   related=["flash_function","shutter_type","white_balance","commander_setting","pixel_shift"],
   caution="For apertures wider than f/8 in bright light, use a flash that supports high-speed sync (FP).")

sc(id="lowlight", title="Handheld in low light",
   tags=["low light","dark","indoor","handheld","dim","night handheld","concert","event","restaurant","available light","no tripod","high iso"],
   summary="Get a steady, clean handheld shot when the light is poor.",
   settings=[
     {"c":"IS MODE","v":"ON","why":"In-body stabilization buys you several stops of slower shutter handheld."},
     {"c":"Aperture","v":"Wide (f/2\u2013f/4)","why":"Lets in the most light."},
     {"c":"Auto ISO","v":"Cap high (12800+), min shutter 1/60\u20131/125","why":"Keeps shutter fast enough to avoid blur while limiting noise."},
     {"c":"Focus","v":"AF-S single point","why":"Most reliable lock in dim light; use the AF illuminator if needed."},
     {"c":"HIGH ISO NR","v":"Moderate","why":"Tames high-ISO noise without smearing detail; shoot RAW for flexibility."},
   ],
   steps=["Turn IS MODE on.","Open the aperture wide; set Auto ISO with a sensible shutter floor.","Use a single AF point on your subject; enable the AF illuminator if it struggles.","Brace yourself, breathe out, and squeeze the shutter.","Shoot RAW so you can lift shadows cleanly later."],
   related=["is_mode","face_eye","high_iso_nr","af_illuminator","pre_af"],
   caution="Don't chase base ISO here \u2014 a sharp high-ISO frame beats a blurry clean one.")

sc(id="backlit", title="High-contrast & backlit scenes",
   tags=["backlit","high contrast","sunset","window","hdr","bright sky","harsh light","silhouette","contre jour","highlights","shadows","bracket"],
   summary="Hold detail in both bright highlights and deep shadows.",
   settings=[
     {"c":"D RANGE PRIORITY","v":"AUTO or STRONG","why":"Tames very high contrast for a natural single-frame result."},
     {"c":"DYNAMIC RANGE","v":"DR200/DR400","why":"Protects highlights (needs higher minimum ISO)."},
     {"c":"AE BKT","v":"3\u20135 frames","why":"Brackets exposures to blend into an HDR when one frame can't hold it all."},
     {"c":"Metering / PHOTOMETRY","v":"Expose for highlights","why":"Recover shadows in RAW rather than clipping the sky."},
   ],
   steps=["Try D RANGE PRIORITY AUTO/STRONG first for a natural one-shot result.","If the range is extreme, set AE BKT to 3\u20135 frames and bracket.","Expose to protect highlights; check the histogram isn't clipping right.","Blend brackets later, or lift shadows from a single RAW."],
   related=["drange_priority","dynamic_range","ae_bkt","photometry"],
   caution="D RANGE PRIORITY and DYNAMIC RANGE raise the minimum ISO \u2014 fine outdoors, watch it in dim scenes.")

sc(id="bw", title="Black & white photography",
   tags=["black and white","monochrome","bw","b&w","mono","acros","grain","filter","red filter","contrast bw"],
   summary="Rich, filmic monochrome straight out of camera.",
   settings=[
     {"c":"FILM SIMULATION","v":"ACROS","why":"Fujifilm's premium B&W with beautiful gradation and controlled grain."},
     {"c":"B&W filter","v":"Yellow / Red / Green","why":"Red darkens skies dramatically; yellow is a natural everyday choice; green flatters skin."},
     {"c":"MONOCHROMATIC COLOR","v":"Slight warm/cool tone","why":"Adds subtle toning for mood."},
     {"c":"GRAIN EFFECT","v":"WEAK/STRONG","why":"Adds analog grain texture."},
     {"c":"Shoot RAW+JPEG","v":"Yes","why":"Keeps a color RAW in case you want it later."},
   ],
   steps=["Set FILM SIMULATION to ACROS (with a Y/R/G filter for skies/skin).","Add a touch of MONOCHROMATIC COLOR toning and GRAIN EFFECT if you like.","Shoot RAW+JPEG so you keep a color original.","Look for contrast, shape and texture as you compose."],
   related=["film_simulation","grain_effect","monochromatic_color","clarity"],
   caution="ACROS grain looks best at native size \u2014 avoid over-sharpening B&W files.")

sc(id="filmlook", title="Great JPEGs — film-look recipes",
   tags=["jpeg","recipe","film simulation","sooc","straight out of camera","color","look","preset","fuji colors","film recipe","no editing"],
   summary="Get finished-looking color straight from the camera, no editing.",
   settings=[
     {"c":"FILM SIMULATION","v":"CLASSIC Neg. / NOSTALGIC Neg. / CLASSIC CHROME","why":"Distinct, film-inspired color you can shoot and share directly."},
     {"c":"WHITE BALANCE","v":"Shift toward warm/amber for mood","why":"WB shift is central to the 'recipe' look."},
     {"c":"COLOR / TONE CURVE","v":"Nudge to taste","why":"Fine-tune saturation and contrast."},
     {"c":"GRAIN + COLOR CHROME","v":"Add subtly","why":"Grain and Color Chrome deepen the analog feel."},
     {"c":"EDIT/SAVE CUSTOM SETTING","v":"Save as a preset","why":"Store your recipe in a custom slot to recall instantly."},
   ],
   steps=["Pick a base film simulation.","Adjust white balance shift, color, tone curve, highlight/shadow to taste.","Add GRAIN EFFECT and COLOR CHROME for texture and depth.","Save the combination via EDIT/SAVE CUSTOM SETTING and assign it to a custom slot."],
   related=["film_simulation","white_balance","grain_effect","color_chrome","edit_custom","tone_curve"],
   caution="Shoot RAW+JPEG while dialing in a recipe so nothing is lost if you change your mind.")

sc(id="timelapse", title="Time-lapse & interval shooting",
   tags=["timelapse","time lapse","interval","interval timer","clouds moving","stars moving","construction","sunset sequence","sequence"],
   summary="Automatically shoot a sequence over time for a time-lapse.",
   settings=[
     {"c":"INTERVAL TIMER SHOOTING","v":"Set interval + frame count","why":"The camera fires automatically on a schedule."},
     {"c":"EXPOSURE SMOOTHING","v":"ON for changing light","why":"Reduces flicker between frames as light shifts (e.g. sunset)."},
     {"c":"INTERVAL PRIORITY MODE","v":"Consider ON","why":"Keeps intervals consistent even if exposure varies."},
     {"c":"Power","v":"Full battery / USB power","why":"Long sequences drain the battery; power it externally if you can."},
     {"c":"IS MODE","v":"OFF (tripod)","why":"Rigid support keeps every frame aligned."},
   ],
   steps=["Mount on a tripod and compose.","Open INTERVAL TIMER SHOOTING; set the interval and number of frames.","Enable EXPOSURE SMOOTHING if the light will change.","Set exposure (manual is most consistent), power the camera, and start.","Assemble the frames into video afterward."],
   related=["interval_timer","is_mode","self_timer"],
   caution="Lock exposure (manual) for the smoothest result; Auto exposure can cause flicker.")

sc(id="selfie", title="Self-portraits & group photos with the timer",
   tags=["self timer","selfie","self portrait","group photo","family photo","get in the shot","timer","2 second","10 second","delay"],
   summary="Put yourself in the frame or avoid shake with a timed release.",
   settings=[
     {"c":"SELF-TIMER","v":"10 s (group) / 2 s (anti-shake)","why":"10 s to run into frame; 2 s to kill shutter shake on a tripod."},
     {"c":"SAVE SELF-TIMER SETTING","v":"ON","why":"Keeps the timer active after the shot so you don't re-set it."},
     {"c":"FACE/EYE DETECTION","v":"ON","why":"Keeps faces sharp when you can't focus manually."},
     {"c":"Focus","v":"Pre-focus where you'll stand","why":"Lock focus on the spot before triggering."},
   ],
   steps=["Set the SELF-TIMER via the DRIVE button (10 s or 2 s).","Turn on FACE/EYE DETECTION.","Pre-focus on where the subject will be.","Press the shutter and get into position before it fires."],
   related=["self_timer","face_eye"],
   caution="For groups, stop down to f/5.6\u2013f/8 so everyone stays in focus.")

sc(id="travel", title="Travel — one flexible setup",
   tags=["travel","holiday","vacation","trip","versatile","everyday","walkaround","all rounder","general","mixed","tourism","sightseeing"],
   summary="A dependable do-everything setup for changing conditions on the move.",
   settings=[
     {"c":"Exposure mode","v":"Aperture priority + Auto ISO","why":"Adapt instantly to changing light without fuss."},
     {"c":"Aperture","v":"f/5.6","why":"A versatile middle ground for depth and sharpness."},
     {"c":"Auto ISO","v":"Cap 12800, min shutter 1/125","why":"Keeps shots sharp handheld across scenes."},
     {"c":"IS MODE","v":"ON","why":"Handheld stability for spontaneous shots."},
     {"c":"FILM SIMULATION","v":"CLASSIC Neg. or PROVIA","why":"Great-looking JPEGs to share on the go; RAW+JPEG to keep options."},
     {"c":"FACE/EYE + SUBJECT DETECTION","v":"ON","why":"Ready for people, pets and street scenes alike."},
   ],
   steps=["Aperture priority, f/5.6, Auto ISO (min shutter 1/125).","IS MODE on; RAW+JPEG.","Enable FACE/EYE and SUBJECT DETECTION.","Pick a film simulation you like for instant shareable shots.","Save this as a custom slot so it's one button away."],
   related=["is_mode","face_eye","subject_detection","film_simulation","edit_custom"],
   caution="Carry a spare battery \u2014 IBIS, EVF and 102MP files use power.")

sc(id="mixedwb", title="Tricky / mixed lighting color",
   tags=["white balance","color cast","mixed light","tungsten","fluorescent","led","warm","cool","wb","neutral color","indoor color"],
   summary="Get natural color under difficult or mixed light sources.",
   settings=[
     {"c":"WHITE BALANCE","v":"Match the source, or Custom","why":"Presets fix common sources; a custom (grey-card) reading nails mixed light."},
     {"c":"WB shift","v":"Fine-tune amber/blue","why":"Dials out residual casts."},
     {"c":"Shoot RAW","v":"Yes","why":"White balance is fully changeable later with zero quality loss."},
     {"c":"WHITE BALANCE BKT","v":"Optional","why":"Brackets WB when you're unsure."},
   ],
   steps=["Choose the white balance preset matching the dominant light, or shoot a custom reading off a grey card.","Fine-tune with the WB shift if a cast remains.","Shoot RAW so you can correct precisely later.","Under mixed light, prioritize the subject's color (usually skin)."],
   related=["white_balance","dynamic_range"],
   caution="LED and fluorescent light can flicker \u2014 see FLICKER REDUCTION / FLICKERLESS S.S. if you see banding.")

# ---------------------------------------------------------------------------
# --- Landscape / nature / astro depth pack -------------------------------
sc(id="landscapestack", title="Front-to-back sharp landscape (focus stack)",
   tags=["landscape stack","focus stack landscape","near foreground","foreground rock","close foreground","hyperfocal","sharp foreground and mountains","depth","stacking landscape","wide angle close"],
   summary="Keep a close foreground and distant peaks both critically sharp.",
   settings=[
     {"c":"Aperture","v":"f/8\u2013f/11","why":"Sharpest zone; avoids diffraction softening you'd get past f/16 on 102MP."},
     {"c":"FOCUS BKT SETTING","v":"AUTO (near \u2192 far)","why":"Shoots a focus-stepped series you merge later \u2014 more depth than one frame without diffraction."},
     {"c":"ISO / support","v":"80, tripod, 2-sec timer","why":"Cleanest frames that align cleanly for the stack."},
     {"c":"IS MODE","v":"OFF","why":"Tripod work; prevents drift between frames."},
   ],
   steps=["Tripod, ISO 80, f/8\u2013f/11.","Open FOCUS BKT SETTING; set AUTO and mark the nearest and farthest focus points (or set frames + step).","Trigger with the 2-sec timer; let the camera march focus through the scene.","Stack the frames later (Helicon Focus / Photoshop).","No time to stack? Focus one-third in and stop to f/11 for a single frame."],
   related=["focus_bkt","is_mode","self_timer","dynamic_range"],
   caution="Wind moving grass or branches breaks a stack \u2014 shoot in calm light or fall back to a single hyperfocal frame.")

sc(id="seascape", title="Coastal & seascape long exposure",
   tags=["seascape","coast","coastal","beach","ocean","sea","waves","surf","tide","rocks water","shoreline","misty water"],
   summary="Smooth the sea and hold detail in a bright sky at the coast.",
   settings=[
     {"c":"ND / grad","v":"6\u201310-stop ND (+ grad for sky)","why":"Enables multi-second exposures and balances a bright horizon."},
     {"c":"Shutter","v":"1\u201330 s to taste","why":"Short for texture in the waves, long for misty smoothness."},
     {"c":"Aperture / ISO","v":"f/8\u2013f/11, ISO 80","why":"Sharp and clean; helps reach long times."},
     {"c":"Focus","v":"Manual, set before the ND goes on","why":"AF hunts through a dark ND."},
     {"c":"LONG EXPOSURE NR","v":"ON","why":"Cleans exposures over ~1 s."},
   ],
   steps=["Compose and focus, then fit the ND and switch to manual focus.","ISO 80, f/8\u2013f/11; dial shutter for the water look you want.","Use a grad or bracket if the sky is much brighter.","Trigger with timer/remote; rinse salt spray off the filter often."],
   related=["long_exposure_nr","is_mode","ae_bkt","white_balance"],
   caution="Rogue waves and salt spray threaten the tripod and front element \u2014 keep a cloth handy and watch the tide.")

sc(id="woodland", title="Woodland & intimate nature scenes",
   tags=["woodland","forest","trees","intimate landscape","woods","ferns","moss","jungle","autumn forest","details nature","order from chaos"],
   summary="Find order in the forest with even light and controlled reflections.",
   settings=[
     {"c":"Polarizer","v":"On, rotate to cut leaf glare","why":"Removes waxy reflections so foliage color saturates \u2014 the single biggest woodland improvement."},
     {"c":"Light","v":"Overcast / shade","why":"Soft, even light tames the harsh contrast that wrecks forest shots."},
     {"c":"Focal length","v":"Longer (compress a section)","why":"Isolates a clean composition instead of a cluttered wide."},
     {"c":"FILM SIMULATION","v":"Velvia or Classic Chrome","why":"Velvia for lush greens/autumn; Classic Chrome for a muted, moody wood."},
     {"c":"Aperture","v":"f/5.6\u2013f/11","why":"Enough depth for a layered scene; stack if the nearest leaves are very close."},
   ],
   steps=["Wait for soft, even light (overcast is ideal).","Fit a polarizer and rotate to kill leaf and rock glare.","Pick a longer focal length and isolate a tidy composition.","Choose Velvia (color) or Classic Chrome (mood); base ISO on a tripod."],
   related=["film_simulation","white_balance","focus_bkt","dynamic_range"],
   caution="A polarizer costs ~1.5 stops \u2014 fine on a tripod; watch shutter speed if any leaves are moving.")

sc(id="autumn", title="Autumn colour",
   tags=["autumn","fall","fall colors","foliage","leaves","color","red leaves","maple","vibrant nature"],
   summary="Make autumn colour glow without going cartoonish.",
   settings=[
     {"c":"FILM SIMULATION","v":"Velvia (or PROVIA if too much)","why":"Lifts reds, oranges and golds; PROVIA if Velvia oversaturates."},
     {"c":"Polarizer","v":"On","why":"Cuts glare off wet or waxy leaves so colour deepens."},
     {"c":"White balance","v":"Slightly warm","why":"Enhances the golden feel; fine-tune in RAW."},
     {"c":"COLOR CHROME EFFECT","v":"STRONG","why":"Adds tonal depth to very saturated foliage."},
     {"c":"Light","v":"Backlight or soft light","why":"Backlit leaves glow; overcast keeps colour even."},
   ],
   steps=["Fit a polarizer and rotate for the least glare.","Set Velvia (dial back to PROVIA if too punchy) and a slightly warm WB.","Turn COLOR CHROME EFFECT to STRONG for saturated scenes.","Look for backlight through the leaves; shoot RAW+JPEG."],
   related=["film_simulation","color_chrome","white_balance","drange_priority"],
   caution="Very saturated reds can clip \u2014 watch the red channel and ease off saturation if it blocks up.")

sc(id="panorama", title="Panorama (multi-shot stitch)",
   tags=["panorama","pano","stitch","wide vista","multi shot wide","sweep","stitched landscape","vertorama"],
   summary="Shoot a clean overlapping sequence that stitches without errors.",
   settings=[
     {"c":"Exposure","v":"Full manual (locked)","why":"Consistent exposure across frames \u2014 Auto causes brightness steps that fight the stitch."},
     {"c":"White balance","v":"Fixed (not Auto)","why":"Auto WB drifts frame to frame and mismatches colour."},
     {"c":"Focus","v":"Manual, locked","why":"Keeps focus identical across the sweep."},
     {"c":"Overlap","v":"~30\u201340% per frame","why":"Gives the stitcher enough to align accurately."},
     {"c":"Orientation","v":"Camera vertical (portrait)","why":"More height in the final panorama; shoot level and rotate over the nodal point if possible."},
   ],
   steps=["Set manual exposure, fixed WB and manual focus using your brightest frame.","Level the camera (electronic level) and rotate the head, not the tripod.","Turn the camera portrait; overlap each frame ~1/3.","Sweep steadily across the scene; stitch later in Lightroom/PTGui."],
   related=["electronic_level","white_balance","framing_guideline","dynamic_range"],
   caution="A moving foreground (waves, people) creates stitch ghosts \u2014 shoot those frames quickly or avoid overlap there.")

sc(id="snow", title="Snow & high-key scenes",
   tags=["snow","winter","bright","high key","white","frost","ice","fog","misty","minimalist white"],
   summary="Keep snow white, not grey, and hold subtle texture.",
   settings=[
     {"c":"Exposure comp","v":"+1 to +1.7 EV","why":"Meters see bright snow and underexpose it grey \u2014 add light to keep it white."},
     {"c":"Highlight check","v":"Watch the histogram/blinkies","why":"Push right but keep detail before pure-white clipping."},
     {"c":"White balance","v":"Cool it slightly / set manually","why":"Removes the blue cast snow often picks up."},
     {"c":"FILM SIMULATION","v":"PROVIA / ASTIA","why":"Gentle contrast suits soft, high-key winter light."},
   ],
   steps=["Add +1 to +1.7 EV exposure compensation.","Check the histogram \u2014 data near the right, not clipped.","Set or cool the white balance to remove blue snow.","Shoot RAW to fine-tune the last bit of tone and colour."],
   related=["photometry","white_balance","dynamic_range","film_simulation"],
   caution="Cold murders battery life \u2014 keep spares warm in an inside pocket and expect fewer shots per charge.")

sc(id="startrails", title="Star trails",
   tags=["star trails","startrails","circumpolar","polaris","rotation","long star streaks","stacked trails"],
   summary="Build long circular trails from a stacked sequence (safer than one huge exposure).",
   settings=[
     {"c":"Method","v":"Many 30\u201360 s frames, stacked","why":"Dozens of shorter frames stack into smooth trails and let you drop any ruined by planes/clouds."},
     {"c":"INTERVAL TIMER SHOOTING","v":"Interval \u2248 1\u20132 s gap, 100\u2013300 frames","why":"Automates the sequence; small gap keeps trails continuous."},
     {"c":"LONG EXPOSURE NR","v":"OFF","why":"Its dark-frame pause would leave gaps in the trails."},
     {"c":"ISO / aperture","v":"ISO 400\u20131600, f/2.8\u2013f/4","why":"Lower ISO is fine because the total time is long; keeps noise down."},
     {"c":"Power","v":"USB power / full battery","why":"An hour-plus run will drain a battery."},
   ],
   steps=["Compose with Polaris in frame for circular trails; focus manually on a star.","Set INTERVAL TIMER: 30\u201360 s frames, ~1\u20132 s gap, 100+ frames.","Turn LONG EXPOSURE NR OFF; IS MODE off; ISO ~800, f/2.8\u2013f/4.","Power the camera and start; shoot a few dark frames afterward.","Stack the sequence (StarStaX / Sequator / Photoshop) into the final trails."],
   related=["interval_timer","long_exposure_nr","is_mode","focus_check"],
   caution="Dew ruins long sessions \u2014 a lens warmer keeps the front element clear. Turn off any long-exposure NR gap.")

sc(id="startracker", title="Tracked astro (star tracker)",
   tags=["star tracker","tracked","equatorial mount","tracking mount","long exposure stars","low iso astro","sky tracker","astro mount"],
   summary="Longer, lower-ISO sky exposures with a tracker for the cleanest Milky Way.",
   settings=[
     {"c":"Tracker","v":"Polar-aligned; track the sky","why":"Follows star motion so you can expose for minutes without trailing."},
     {"c":"Shutter","v":"1\u20134 min (sky only)","why":"Long, clean sky exposure at low ISO once tracking."},
     {"c":"ISO / aperture","v":"ISO 400\u20131600, f/2.8\u2013f/4","why":"Low noise; the long tracked exposure supplies the light."},
     {"c":"IS MODE","v":"OFF","why":"No stabilization on a tripod/tracker."},
     {"c":"Foreground","v":"Separate untracked frame","why":"Tracking blurs the land \u2014 shoot the foreground with tracking off and blend."},
   ],
   steps=["Polar-align the tracker; switch tracking on.","Focus on a star (FOCUS CHECK); ISO ~800, f/2.8\u2013f/4.","Expose the sky 1\u20134 min; shoot several frames to stack.","Turn tracking OFF and shoot a sharp foreground frame at the same framing.","Blend sky + foreground later."],
   related=["focus_check","is_mode","long_exposure_nr","preview_exp_wb"],
   caution="Any polar-alignment error shows as trailing on long subs \u2014 keep individual frames shorter if alignment is rough.")

sc(id="nightfg", title="Nightscape foreground (blue-hour blend)",
   tags=["blue hour foreground","nightscape foreground","blend foreground","light painting","dark foreground","land at night","two exposure blend"],
   summary="Get a sharp, low-noise foreground under a starry sky by blending two times.",
   settings=[
     {"c":"Foreground frame","v":"Shot at blue hour / twilight","why":"Real light on the land means low ISO and deep focus \u2014 far cleaner than a black night foreground."},
     {"c":"Sky frame","v":"Shot after full dark, same framing","why":"Lock the tripod and return for the Milky Way once it's dark."},
     {"c":"Aperture (foreground)","v":"f/8\u2013f/11","why":"Deep focus while there's still light."},
     {"c":"Alternative","v":"Light-paint the foreground","why":"A brief, soft torch sweep adds detail if you can't wait for blue hour."},
   ],
   steps=["Set up early; at blue hour shoot the foreground at ISO 80\u2013400, f/8\u2013f/11, deep focus.","Do NOT move the tripod.","After dark, refocus on a star and shoot the sky (see 'Milky Way').","Blend the twilight foreground with the night sky in editing.","No blue hour? Light-paint the foreground with a soft torch during the sky frame."],
   related=["focus_check","preview_exp_wb","long_exposure_nr","dynamic_range"],
   caution="Mark the horizon position so the two frames align \u2014 nudging the tripod between them makes blending painful.")

sc(id="moonlit", title="Moonlit landscape at night",
   tags=["moonlit","moonlight","full moon","night landscape","moonlit scene","bright night","lunar landscape"],
   summary="Use moonlight as a soft floodlight for a low-noise night landscape.",
   settings=[
     {"c":"Light","v":"Half-to-full moon behind/beside you","why":"Moonlight lets you shoot the land at low ISO with detail and colour."},
     {"c":"Shutter","v":"30 s\u2013several minutes","why":"Long enough to expose the moonlit land; stars will trail slightly \u2014 usually fine."},
     {"c":"ISO / aperture","v":"ISO 200\u2013800, f/5.6\u2013f/8","why":"Clean files and adequate depth under bright moonlight."},
     {"c":"LONG EXPOSURE NR","v":"ON","why":"Cleans multi-minute frames."},
     {"c":"White balance","v":"~4000 K","why":"Moonlight is sunlight \u2014 a coolish WB looks natural at night."},
   ],
   steps=["Position so the moon lights your scene; keep it out of frame to avoid flare.","ISO 400, f/5.6\u2013f/8, WB ~4000 K.","Expose 30 s\u20132 min for the land; enable LONG EXPOSURE NR.","Fire with the timer/remote and check shadow detail on the histogram."],
   related=["long_exposure_nr","is_mode","white_balance","preview_exp_wb"],
   caution="A bright moon washes out the Milky Way \u2014 shoot moonlit landscapes and dark-sky Milky Way on different nights.")

sc(id="aurora", title="Aurora / northern lights",
   tags=["aurora","northern lights","southern lights","aurora borealis","green sky","lights dancing","polar lights"],
   summary="Keep the aurora's structure crisp instead of a green smear.",
   settings=[
     {"c":"Shutter","v":"2\u201310 s (shorter when active)","why":"Fast-moving curtains blur into mush on long exposures \u2014 shorten as the display intensifies."},
     {"c":"ISO","v":"1600\u20136400","why":"Compensates for the short shutter so the display stays bright."},
     {"c":"Aperture","v":"Wide (f/2.8\u2013f/4)","why":"Maximum light for those short exposures."},
     {"c":"Focus / IBIS","v":"Manual on a star, IS MODE off","why":"Reliable infinity focus; no stabilization on a tripod."},
     {"c":"White balance","v":"~3500\u20134000 K","why":"Keeps the greens and reds natural against the night."},
   ],
   steps=["Manual focus on a bright star (FOCUS CHECK); IS MODE off.","Aperture wide, ISO ~3200, WB ~3800 K.","Start around 5 s; shorten toward 2 s as the aurora dances, lengthen if faint.","Include a strong foreground and check you're not clipping the brightest bands."],
   related=["focus_check","preview_exp_wb","is_mode","white_balance"],
   caution="Long exposures during an active display lose all the curtain detail \u2014 favour shorter shutters and higher ISO.")

# FEATURE CARDS  (plain-language, grounded in manual; id used by scenarios)
# menu path helps users find it on the camera
# ---------------------------------------------------------------------------
F = []
def ft(id, name, path, page, what, how):
    F.append({"id":id,"name":name,"path":path,"page":page,"what":what,"how":how})

ft("film_simulation","Film Simulation","IMAGE QUALITY SETTING",128,
   "Fujifilm's in-camera color/tone profiles that emulate classic films. Sets the entire look of your JPEGs.",
   "IMAGE QUALITY SETTING > FILM SIMULATION, or assign it to the Q menu / a function button for fast switching.")
ft("dynamic_range","Dynamic Range (DR100/200/400)","IMAGE QUALITY SETTING",132,
   "Protects highlight detail by underexposing the capture and lifting mid/shadows in processing. DR200 and DR400 raise the minimum ISO.",
   "IMAGE QUALITY SETTING > DYNAMIC RANGE. Use AUTO, or DR200/DR400 for bright skies and backlight.")
ft("drange_priority","D Range Priority","IMAGE QUALITY SETTING",133,
   "Reduces loss of detail in highlights and shadows for natural results in high-contrast scenes (AUTO/STRONG/WEAK/OFF).",
   "IMAGE QUALITY SETTING > D RANGE PRIORITY. STRONG for very harsh light; AUTO for general use.")
ft("clarity","Clarity","IMAGE QUALITY SETTING",139,
   "Adjusts mid-tone definition while keeping highlight/shadow tone. Plus for punch, minus for a softer look (\u22125 to +5).",
   "IMAGE QUALITY SETTING > CLARITY. Note: non-zero values add processing time per shot.")
ft("grain_effect","Grain Effect","IMAGE QUALITY SETTING",130,
   "Adds film-like grain texture (strength and size) for an analog feel.",
   "IMAGE QUALITY SETTING > GRAIN EFFECT. Pairs well with ACROS/CLASSIC Neg.")
ft("color_chrome","Color Chrome Effect / FX Blue","IMAGE QUALITY SETTING",131,
   "Deepens color and tonal separation in highly saturated subjects; FX Blue specifically enriches blues.",
   "IMAGE QUALITY SETTING > COLOR CHROME EFFECT / COLOR CHROME FX BLUE.")
ft("monochromatic_color","Monochromatic Color","IMAGE QUALITY SETTING",130,
   "Adds warm/cool toning to monochrome film simulations (ACROS/MONOCHROME).",
   "IMAGE QUALITY SETTING > MONOCHROMATIC COLOR (available with B&W simulations).")
ft("smooth_skin","Smooth Skin Effect","IMAGE QUALITY SETTING",131,
   "Gently softens skin in-camera (OFF/WEAK/STRONG) without wrecking detail.",
   "IMAGE QUALITY SETTING > SMOOTH SKIN EFFECT. Great for portraits.")
ft("white_balance","White Balance","IMAGE QUALITY SETTING",134,
   "Sets color neutrality for the light you're in. Presets, Kelvin, or a custom reading; fine-tune with a shift.",
   "IMAGE QUALITY SETTING > WHITE BALANCE. Use Custom off a grey card for mixed light.")
ft("tone_curve","Tone Curve (Highlight/Shadow)","IMAGE QUALITY SETTING",138,
   "Adjusts highlight and shadow contrast independently to shape your look.",
   "IMAGE QUALITY SETTING > TONE CURVE.")
ft("high_iso_nr","High ISO NR","IMAGE QUALITY SETTING",138,
   "Controls noise reduction strength on high-ISO JPEGs. Lower keeps detail; higher smooths noise.",
   "IMAGE QUALITY SETTING > HIGH ISO NR.")
ft("long_exposure_nr","Long Exposure NR","IMAGE QUALITY SETTING",139,
   "Reduces mottling/hot pixels on long exposures by taking a matching dark frame (doubles save time).",
   "IMAGE QUALITY SETTING > LONG EXPOSURE NR. Turn ON for exposures over ~1 second.")
ft("pixel_shift","Pixel Shift Multi-Shot","DRIVE button",119,
   "Records a burst of sensor-shifted frames that combine on a computer into an ultra-high-resolution image. Two modes: Accurate Color, and High Resolution + Accurate Color.",
   "DRIVE button > PIXEL SHIFT MULTI SHOT. Tripod + still subject required; merge in FUJIFILM Pixel Shift Combiner.")

ft("face_eye","Face / Eye Detection","AF/MF SETTING",151,
   "Automatically finds faces and focuses on the eye \u2014 the key to sharp portraits.",
   "AF/MF SETTING > FACE/EYE DETECTION SETTING. Turn ON; choose eye priority if you like.")
ft("subject_detection","Subject Detection","AF/MF SETTING",153,
   "Detects and tracks a chosen subject type \u2014 animal, bird, car, motorcycle/bike, airplane, train.",
   "AF/MF SETTING > SUBJECT DETECTION SETTING. Pick the type, then use AF-C.")
ft("afc_custom","AF-C Custom Settings","AF/MF SETTING",145,
   "Presets that tune continuous-AF tracking: how sticky it is, and how it reacts to speed changes and obstacles.",
   "AF/MF SETTING > AF-C CUSTOM SETTINGS. Match the preset to your subject's motion.")
ft("pre_af","Pre-AF","AF/MF SETTING",150,
   "The camera keeps focusing even before you half-press, so it locks faster when you do.",
   "AF/MF SETTING > PRE-AF. Handy for fast-reaction shooting (uses more battery).")
ft("af_illuminator","AF Illuminator","AF/MF SETTING",150,
   "A small lamp that helps autofocus lock in dim light.",
   "AF/MF SETTING > AF ILLUMINATOR. Turn ON for low-light AF (off for discretion).")
ft("mf_assist","MF Assist / Focus Check","AF/MF SETTING",156,
   "Aids for manual focus: focus peaking or a digital split-image, plus magnified focus check.",
   "AF/MF SETTING > MF ASSIST; press the focus check control to magnify.")
ft("focus_check","Focus Check","AF/MF SETTING",157,
   "Magnifies the live view so you can confirm critical focus \u2014 essential for astro and macro.",
   "Enable FOCUS CHECK; the view zooms when you focus manually.")
ft("release_focus_priority","Release / Focus Priority","AF/MF SETTING",158,
   "Chooses whether the camera fires only when focus is confirmed, or whenever you press.",
   "AF/MF SETTING > RELEASE/FOCUS PRIORITY. Focus priority for accuracy, release for never missing.")
ft("touch_screen","Touch Screen Mode","AF/MF SETTING",160,
   "Tap to focus or tap to shoot on the rear screen \u2014 fast and intuitive for street and candids.",
   "AF/MF SETTING > TOUCH SCREEN MODE.")

ft("self_timer","Self-Timer","SHOOTING SETTING",162,
   "Delays the shutter (2 s or 10 s). 2 s prevents shake on a tripod; 10 s lets you join the shot.",
   "DRIVE button or SHOOTING SETTING > SELF-TIMER. SAVE SELF-TIMER SETTING keeps it on.")
ft("interval_timer","Interval Timer Shooting","SHOOTING SETTING",164,
   "Fires a set number of frames at set intervals for time-lapse, with optional exposure smoothing.",
   "SHOOTING SETTING > INTERVAL TIMER SHOOTING (+ EXPOSURE SMOOTHING / INTERVAL PRIORITY).")
ft("ae_bkt","AE Bracketing","SHOOTING SETTING",167,
   "Shoots a run of frames at different exposures to blend into HDR or pick the best.",
   "DRIVE button > BKT, or SHOOTING SETTING > AE BKT SETTING. Set frames and step.")
ft("focus_bkt","Focus Bracketing","SHOOTING SETTING",167,
   "Automatically shoots a focus-stepped series for focus stacking \u2014 great for macro and product.",
   "SHOOTING SETTING > FOCUS BKT SETTING. AUTO between a near/far point, or set frames+step.")
ft("photometry","Photometry (Metering)","SHOOTING SETTING",167,
   "How the camera meters light: multi, spot, average or center-weighted.",
   "SHOOTING SETTING > PHOTOMETRY. Spot for backlit subjects; multi for general use.")
ft("shutter_type","Shutter Type","SHOOTING SETTING",168,
   "Mechanical, electronic (silent), or a mix. Electronic is silent but caps ISO 80\u201312800, blocks flash, and can skew fast motion / band under some lights.",
   "SHOOTING SETTING > SHUTTER TYPE. Mechanical for flash/action; electronic for silence.")
ft("flicker_reduction","Flicker Reduction / Flickerless S.S.","SHOOTING SETTING",169,
   "Reduces banding and exposure flicker under artificial (LED/fluorescent) lighting.",
   "SHOOTING SETTING > FLICKER REDUCTION / FLICKERLESS S.S. SETTING.")
ft("is_mode","IS Mode (In-Body Stabilization)","SHOOTING SETTING",170,
   "In-body image stabilization for sharp handheld shots at slower shutter speeds. Turn OFF on a tripod.",
   "SHOOTING SETTING > IS MODE. Continuous or shooting-only; off for tripod/long exposures.")
ft("format35","35mm Format Mode","SHOOTING SETTING",170,
   "Crops to a 35mm-equivalent frame for a different field of view / aspect.",
   "SHOOTING SETTING > 35mm FORMAT MODE.")

ft("flash_function","Flash Function Setting","FLASH SETTING",172,
   "Controls flash mode (TTL/Manual), sync timing, and compensation for compatible flashes.",
   "FLASH SETTING > FLASH FUNCTION SETTING. TTL for speed; Manual for repeatable studio power.")
ft("commander_setting","Commander / CH Setting","FLASH SETTING",174,
   "Sets the camera as a commander for off-camera flashes and selects the channel.",
   "FLASH SETTING > COMMANDER SETTING / CH SETTING.")
ft("red_eye","Red-Eye Removal","FLASH SETTING",172,
   "Reduces or removes red-eye from flash portraits.",
   "FLASH SETTING > RED EYE REMOVAL.")

ft("image_size","Image Size / Quality / RAW","IMAGE QUALITY SETTING",124,
   "Sets resolution, aspect ratio, JPEG/HEIF quality and RAW recording (uncompressed/compressed). RAW gives the most editing latitude.",
   "IMAGE QUALITY SETTING > IMAGE SIZE / IMAGE QUALITY / RAW RECORDING. Use RAW+FINE for flexibility.")
ft("edit_custom","Edit/Save Custom Setting","IMAGE QUALITY SETTING",140,
   "Save a complete look (film sim, WB, tone, grain\u2026) into a custom slot to recall instantly.",
   "IMAGE QUALITY SETTING > EDIT/SAVE CUSTOM SETTING; assign slots to the Q menu.")
ft("electronic_level","Electronic Level","SCREEN SETTING",320,
   "On-screen level to keep horizons and verticals straight.",
   "SCREEN SETTING > ELECTRONIC LEVEL SETTING; add it to your display via DISP. CUSTOM SETTING.")
ft("framing_guideline","Framing Guideline","SCREEN SETTING",320,
   "Grid overlays (rule-of-thirds etc.) to aid composition and alignment.",
   "SCREEN SETTING > FRAMING GUIDELINE.")
ft("natural_live_view","Natural Live View","SCREEN SETTING",319,
   "Shows a more natural, un-boosted preview \u2014 useful in very dark scenes and with filters.",
   "SCREEN SETTING > NATURAL LIVE VIEW.")
ft("preview_exp_wb","Preview Exp./WB in Manual Mode","SCREEN SETTING",319,
   "Whether the live view simulates your manual exposure. Turn OFF for night/astro so the screen brightens enough to compose and focus in the dark; turn ON in daylight to preview exposure.",
   "SCREEN SETTING > PREVIEW EXP./WB IN MANUAL MODE. OFF for astro, ON for normal manual shooting.")
ft("disp_brightness","EVF / LCD Brightness","SCREEN SETTING",316,
   "Sets viewfinder and rear-screen brightness. Boost it at night to see and focus; dim it to protect your night vision and battery.",
   "SCREEN SETTING > EVF BRIGHTNESS / LCD BRIGHTNESS.")
ft("fn_setting","Function (Fn) Button Setting","BUTTON/DIAL SETTING",331,
   "Assign frequently used features to buttons and dials for fast access.",
   "BUTTON/DIAL SETTING > FUNCTION (Fn) SETTING.")
ft("quick_menu","Edit/Save Quick (Q) Menu","BUTTON/DIAL SETTING",330,
   "Customize the Q-menu grid so your most-used settings are one press away.",
   "BUTTON/DIAL SETTING > EDIT/SAVE QUICK MENU.")
ft("power_management","Power Management / Performance","POWER MANAGEMENT",339,
   "Balance battery life against responsiveness (BOOST vs economy), auto-power-off and standby.",
   "POWER MANAGEMENT > PERFORMANCE / AUTO POWER OFF.")
ft("format_card","Format Card","USER SETTING",0,
   "Erases and prepares a memory card. Do this in-camera for a fresh card or to clear errors.",
   "SETUP > USER SETTING > FORMAT. (Back up first \u2014 it deletes everything.)")

# ---------------------------------------------------------------------------
# RECIPES / PRESETS BY GENRE  (compact 'start here' cards -> point to scenarios)
# ---------------------------------------------------------------------------
recipes = [
    {"genre":"Landscape","scenario":"landscape","line":"Tripod, f/8\u2013f/11, ISO 80, IBIS off, 2-sec timer."},
    {"genre":"Long exposure","scenario":"longexposure","line":"ND filter, manual focus, ISO 80, Long-Exp NR on."},
    {"genre":"Night sky","scenario":"astro","line":"MF on a star, f/2.8, 15 s, ISO 3200, Long-Exp NR on."},
    {"genre":"Portrait","scenario":"portrait","line":"f/2\u2013f/4, Eye AF on, AF-C, flattering film sim."},
    {"genre":"Street","scenario":"street","line":"A-priority, f/5.6\u2013f/8, Auto ISO 1/250, silent shutter."},
    {"genre":"Wildlife","scenario":"wildlife","line":"AF-C, Subject Detection, burst, 1/1000+."},
    {"genre":"Macro / stacking","scenario":"macro","line":"Tripod, Focus Bracketing, f/8, still light."},
    {"genre":"Studio / flash","scenario":"studioflash","line":"Mechanical shutter, sync speed, f/8\u2013f/11, ISO 80."},
    {"genre":"Low light handheld","scenario":"lowlight","line":"IBIS on, wide aperture, Auto ISO, single-point AF."},
    {"genre":"High resolution","scenario":"pixelshift","line":"Pixel Shift, tripod, ISO 80, combine on computer."},
    {"genre":"Travel / everyday","scenario":"travel","line":"A-priority f/5.6, Auto ISO 1/125, IBIS on, RAW+JPEG."},
    {"genre":"Black & white","scenario":"bw","line":"ACROS + Y/R/G filter, grain, RAW+JPEG."},
    {"genre":"Milky Way","scenario":"astro","line":"MF on a star, f/2.8, ISO 3200, WB 3900K, preview-exp off."},
    {"genre":"Star trails","scenario":"startrails","line":"Interval 30\u201360s \u00d7100+, LENR off, ISO 800, stack."},
    {"genre":"Tracked astro","scenario":"startracker","line":"Tracker on, 1\u20134 min, ISO 800, blend foreground."},
    {"genre":"Aurora","scenario":"aurora","line":"2\u201310s (shorter when active), ISO 3200, f/2.8, WB 3800K."},
    {"genre":"Moonlit night","scenario":"moonlit","line":"ISO 400, f/5.6\u2013f/8, 30s\u20132min, WB 4000K, LENR on."},
    {"genre":"Focus-stack scene","scenario":"landscapestack","line":"f/8\u2013f/11, Focus Bkt AUTO near\u2192far, ISO 80, stack."},
    {"genre":"Seascape","scenario":"seascape","line":"6\u201310-stop ND, MF, ISO 80, 1\u201330s, LENR on."},
    {"genre":"Woodland","scenario":"woodland","line":"Polarizer, soft light, longer lens, Velvia/Classic Chrome."},
    {"genre":"Autumn colour","scenario":"autumn","line":"Velvia, polarizer, warm WB, Color Chrome strong."},
    {"genre":"Panorama","scenario":"panorama","line":"Manual+fixed WB, vertical, 30\u201340% overlap, stitch."},
]

# ---------------------------------------------------------------------------
# SYNONYMS to expand the advisor's understanding of plain-language queries
# ---------------------------------------------------------------------------
synonyms = {
 "blurry background":["bokeh","shallow","separation","f2"],
 "sharp":["crisp","detail","tack"],
 "dark":["low light","dim","night","indoor"],
 "fast":["action","motion","quick","freeze"],
 "kids":["children","toddler","child"],
 "pet":["dog","cat","animal"],
 "birds":["bird","birding","avian"],
 "waterfall":["water","river","stream","silky"],
 "stars":["astro","milky way","night sky"],
 "building":["architecture","interior","real estate"],
 "product":["studio","packshot","tabletop","commercial"],
 "flash":["strobe","speedlight","ttl"],
 "silent":["quiet","discreet","electronic shutter"],
 "hdr":["high contrast","backlit","bracket"],
 "film look":["recipe","sooc","jpeg","fuji color"],
 "resolution":["high res","400mp","pixel shift","detail"],
 "milky way":["astro","nightscape","stars","galaxy","core"],
 "nightscape":["astro","milky way","night sky","stars"],
 "star trails":["startrails","trails","circumpolar","rotation"],
 "aurora":["northern lights","aurora borealis","polar lights"],
 "tracker":["star tracker","tracked","equatorial","tracking mount"],
 "blue hour":["twilight","foreground blend","dusk"],
 "moonlight":["moonlit","full moon","lunar"],
 "polarizer":["polariser","cpl","glare","reflections"],
 "seascape":["coast","coastal","ocean","sea","waves","beach"],
 "woodland":["forest","woods","trees","intimate"],
 "autumn":["fall","foliage","fall colors","leaves"],
 "panorama":["pano","stitch","vista","sweep"],
 "snow":["winter","frost","ice","high key"],
 "focus stack":["stacking","focus bracket","front to back","hyperfocal"],
}

# Emit as a self-registering SYSTEM MODULE so one app shell can hold many bodies.
system = {
    "id": "gfx100sii",
    "brand": "FUJIFILM",
    "model": "GFX100S II",
    "short": "GFX100S II",
    "sensor": "102MP medium format",
    "meta": {
        "manual": "Owner's Manual BL00005287-202 EN",
        "nfg": "New Features Guide v1.20 (BL00005438-200 EN)",
        "builtFrom": "Uploaded manual + new features guide; firmware status verified July 2026.",
    },
    "firmware": firmware,
    "filmSims": film_sims,
    "scenarios": S,
    "features": F,
    "recipes": recipes,
    "synonyms": synonyms,
    "menu": menu_tree,
}

out = os.path.join(HERE, "..", "assets", "systems", "gfx100sii.js")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write("window.FIELDSTOP_SYSTEMS = window.FIELDSTOP_SYSTEMS || [];\n")
    f.write("window.FIELDSTOP_SYSTEMS.push(")
    json.dump(system, f, ensure_ascii=False, separators=(",", ":"))
    f.write(");\n")

print("scenarios:", len(S), "| features:", len(F), "| film sims:", len(film_sims),
      "| recipes:", len(recipes), "| menu items:",
      sum(len(c['items']) for g in menu_tree for c in g['categories']))
print("wrote", out, os.path.getsize(out), "bytes")
