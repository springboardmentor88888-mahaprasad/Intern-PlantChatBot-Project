# PlantDocBot - Full Video Script (LinkedIn / YouTube)

**Estimated Video Length:** 8-10 minutes
**Format:** Screen recording of running app + voiceover (no code shown)
**Tone:** Professional, confident, educational

---

## SECTION 1: INTRO & HOOK (0:00 - 1:00)

### [SCREEN: Face cam or a clean title card with your name — then transition to a diseased plant leaf photo with dramatic zoom]

**VOICEOVER (face cam / talking head):**

> "Hey everyone! I am **Sayandip** — a 3rd year B.Tech Computer Science student at **Brainware University**.
>
> So in 2025, I was actively exploring internship opportunities — and **Infosys Springboard** gave me an amazing opportunity to work on a real-world AI project. The internship ran from **December 2025 to January 2026** — and it has been an absolutely amazing journey.
>
> I am really thankful to **Infosys Springboard** and especially our mentor **Mahaprasad Jena** — who guided us throughout this project and helped us bring it to life.
>
> The project I built is called **PlantDocBot** — an AI-powered plant disease diagnosis system. It uses **Deep Learning**, **Speech Recognition**, and **Large Language Models** to identify over 30 plant diseases across 14 different crops — in seconds.
>
> And I didn't just build what was required — I went beyond the original scope and added several features on my own.
>
> Let's go to the screen and I'll show you everything."

---

## SECTION 2: THE APP OVERVIEW (1:00 - 2:15)

### [SCREEN: Open the browser and show the PlantDocBot landing page — the green-themed UI with the title "PlantDocBot – AI Plant Disease Diagnosis"]

**VOICEOVER:**

> "So here we are — this is PlantDocBot. It's a clean, professional-looking web application. You can see the title at the top — 'PlantDocBot – AI Plant Disease Diagnosis' — and a subtitle that says 'Professional AI-powered diagnosis using Images, Voice, or Text symptoms.'
>
> Right below, there's a 'New Diagnosis' button to reset things at any time.
>
> Now, before I show you the features — let me give you some quick context. The original internship requirement from **Infosys Springboard** was to build a plant disease chatbot with **Image upload** and **Text-based symptom** diagnosis. The disease data was supposed to be stored directly inside Python files.
>
> But I went beyond that. I added **three major enhancements** on my own:
> 1. A **Voice Input** feature — so farmers can just speak their symptoms instead of typing
> 2. A **SQLite Database** with properly normalized tables — instead of hardcoding data in Python files
> 3. And I trained the model with **1,000 additional non-plant images** — so it can reliably reject invalid inputs
>
> So you'll see **three tabs** here:
>
> 1. **Image Upload** — take a photo of a sick leaf, upload it, and get an instant AI diagnosis
> 2. **Voice Input** — speak into your microphone and describe symptoms in plain language *(my addition)*
> 3. **Text Symptoms** — type out what you observe, and the AI will figure out the disease
>
> At the bottom, there's always a 'Ready to assist' message waiting for input. Let me now show each of these in action."

---

## SECTION 3: FEATURE 1 — IMAGE DIAGNOSIS (2:15 - 4:45)

### [SCREEN: Click on the "Image Upload" tab]

**VOICEOVER:**

> "Let's start with the most powerful feature — **Image-based Diagnosis**.
>
> I'll click on the 'Image Upload' tab. You can see it says 'Visual Diagnosis' and there's a file uploader asking me to 'Upload a clear photo of the infected leaf.' It accepts JPG, JPEG, and PNG files."

### [SCREEN: Upload an image of a tomato leaf with late blight (use `testing_data/0a4b3cde-...___RS_Late.B 6985.JPG`)]

**VOICEOVER:**

> "Let me upload this image of a tomato leaf. Watch what happens — the moment I upload the image, the AI processes it instantly.
>
> On the **left side**, you can see the uploaded image is displayed along with a section called 'Top Predictions.' This shows the **top 3 most likely diseases** with progress bars and confidence percentages. You can see the model is quite confident about its prediction.
>
> On the **right side**, we see the **Diagnosis Result** — a beautifully styled card showing the detected disease name, the confidence level — whether it's High, Moderate, or Low — and the confidence percentage.
>
> Below that, the app automatically pulls the complete treatment information from the database."

### [SCREEN: Scroll down slowly to show the full treatment response]

**VOICEOVER:**

> "And here's the treatment detail — it shows:
> - The **Crop name** — Tomato
> - The **Disease type** — whether it's Bacterial, Fungal, or Viral
> - The **Severity level**
> - The **Cause** of the disease
> - A list of **Symptoms** to look for
> - Step-by-step **Treatment recommendations**
> - And **Prevention tips** so the farmer can stop this from happening again
>
> This isn't just a label. This is a complete, actionable diagnosis report."

### [SCREEN: Upload a non-plant image — like a random object or a cat photo]

**VOICEOVER:**

> "Now, what happens if someone uploads something that's NOT a plant? Let me try uploading a random image...
>
> And there it is — the app immediately rejects it with the message: 'Not a plant leaf. Please upload a plant image.' This is one of the enhancements I built on my own — I collected **1,000 non-plant images** and added them as a separate class during model training. So the model doesn't just know plant diseases — it actively knows what is NOT a plant and rejects it. This is a critical safety feature that wasn't part of the original scope."

### [SCREEN: Click "New Diagnosis" to reset]

**VOICEOVER:**

> "I'll click 'New Diagnosis' to reset everything — and we're back to a clean state."

---

## SECTION 4: FEATURE 2 — VOICE DIAGNOSIS (4:45 - 6:45)

### [SCREEN: Click on the "Voice Input" tab]

**VOICEOVER:**

> "Now let's look at the second feature — **Voice-based Diagnosis**. This is one of the features **I added on my own** — it was not part of the original Infosys Springboard internship requirements. I built this because in the real world, many farmers may not be comfortable typing detailed symptom descriptions — it's much easier for them to just talk.
>
> You can see two options here:
> 1. A **live microphone recording** button — 'Click to Record'
> 2. And inside this expandable section, an option to **upload a pre-recorded audio or video file** — it supports MP3, WAV, M4A, OGG, and even video formats like MP4, MOV, AVI, MKV, and WebM."

### [SCREEN: Click the microphone button and record — say: "My tomato plant leaves have brown spots with yellow rings around them and the leaves are curling and drying up"]

**VOICEOVER:**

> "Let me record my voice. I'll say: 'My tomato plant leaves have brown spots with yellow rings around them and the leaves are curling and drying up.'
>
> Now I'll click the **'Analyze Voice'** button..."

### [SCREEN: Show the spinner "Analyzing your voice..." and then the results]

**VOICEOVER:**

> "The system is now doing three things behind the scenes:
>
> **First**, it takes my audio recording and sends it through **OpenAI's Whisper model** — which runs locally, not in the cloud — to convert my speech into text. This is the speech-to-text transcription step.
>
> **Second**, it takes that transcribed text and sends it to the **Groq API**, which runs a **LLaMA 3.3 70B large language model**. The LLM acts as an intelligent symptom classifier — it reads my description and matches it to the most likely disease from its knowledge base of over 30 plant diseases.
>
> **Third**, once the disease is identified, the app fetches the complete treatment data from the **SQLite database** — another enhancement I built on my own. The original project stored disease data in plain Python files, but I designed a proper relational database with normalized tables for diseases, symptoms, treatments, and prevention — linked with foreign keys. This makes the data scalable, queryable, and production-ready.
>
> And here are the results — on the left, you can see my transcription displayed: exactly what the AI heard me say. On the right, the diagnosis result with the identified disease and the full treatment breakdown."

### [SCREEN: Show the result card and scroll through treatment info]

**VOICEOVER:**

> "Same detailed treatment response — crop type, disease type, severity, cause, symptoms, treatments, and prevention steps. All generated from my voice, without uploading a single image."

---

## SECTION 5: FEATURE 3 — TEXT DIAGNOSIS (6:45 - 7:30)

### [SCREEN: Click "New Diagnosis", then click on "Text Symptoms" tab. Type: "My potato plant leaves have dark brown to black water-soaked spots with white fuzzy mold on the underside"]

**VOICEOVER:**

> "The third input method — **Text-based Diagnosis**. I'll type a symptom description here and click **'Diagnose'**.
>
> Same flow — the text goes to **Groq's LLaMA 3.3 70B** model, it classifies the disease, and we get the full treatment report. Simple, fast, and accurate."

---

## SECTION 6: SYSTEM ARCHITECTURE (7:30 - 9:30)

### [SCREEN: Show a System Architecture diagram slide (design in Canva/PowerPoint — use the layout reference below)]

**VOICEOVER:**

> "Now let me walk you through the **System Architecture** — how everything connects.
>
> At the top — the **User** opens the app in their browser. The entire frontend is built with **Streamlit** — pure Python, no JavaScript.
>
> From here, three input paths:
>
> **Path 1 — Image:** The photo goes to **EfficientNetV2-S** — a CNN built with **PyTorch + timm**, trained on **PlantDoc + PlantVillage + 1,000 non-plant images**. The model checkpoint auto-downloads from **HuggingFace**. It outputs top 3 predictions with confidence scores.
>
> **Path 2 — Voice** *(my addition)*: Audio goes to **OpenAI Whisper** running **locally** — speech becomes text. That text then goes to **Groq API** running **LLaMA 3.3 70B** which classifies the symptoms. There's a **fallback to LLaMA 3 70B** if the primary model is down.
>
> **Path 3 — Text:** Goes directly to **Groq LLaMA 3.3 70B** — same classification, same fallback.
>
> All three paths produce a **disease key** — which goes to my **SQLite database** *(also my addition)*. Four normalized tables — Diseases, Symptoms, Treatments, Prevention — all linked with foreign keys. The original project used Python files for this, I replaced it with a proper relational database.
>
> The database assembles a complete report — disease, crop, severity, cause, symptoms, treatments, prevention — and **Streamlit** displays it in a styled card.
>
> Plus there's a **FastAPI** REST API for mobile integration, **Docker + Docker Compose** for deployment, and **GitHub Actions CI/CD** for automated testing and builds."

### ARCHITECTURE DIAGRAM REFERENCE (for your Canva/PowerPoint slide):

```
           USER (Farmer / Researcher)
                    |
                    v
        STREAMLIT FRONTEND (Python)
       [Image]  [Voice]  [Text]
         |         |        |
         v         v        v
   EfficientNet  Whisper  Groq LLM
   V2-S(PyTorch) (local)  LLaMA 3.3
         |         |     70B
         |     Groq LLM    |
         |    LLaMA 3.3    |
         |      70B        |
         v         v        v
       ----  DISEASE KEY  ----
                    |
                    v
          SQLite DATABASE
   [Diseases|Symptoms|Treatments|Prevention]
                    |
                    v
       TREATMENT RESPONSE CARD
   (Shown to user in Streamlit UI)

   ALSO: FastAPI API | Docker | GitHub Actions CI/CD
```

---

## SECTION 7: CLOSING & CTA (9:30 - 10:15)

### [SCREEN: Back on the PlantDocBot app, clean landing page]

**VOICEOVER:**

> "So that's **PlantDocBot** — **14 crops**, **30+ diseases**, **3 input modes**, instant results.
>
> Built during my internship at **Infosys Springboard** — December 2025 to January 2026. The original scope was Image + Text diagnosis with data in Python files. I went beyond — added **Voice input**, a **proper SQLite database**, and **1,000 non-plant images** for smart rejection.
>
> Huge thanks to **Infosys Springboard** and our mentor **Mahaprasad Jena** for guiding us throughout this journey.
>
> If you're into AI, AgriTech, or computer vision — let's connect. Drop a comment, like this video.
>
> I am Sayandip — thanks for watching!"

---

## LINKEDIN POST CAPTION (copy-paste ready)

```
I built PlantDocBot during my internship at Infosys Springboard (Dec 2025 - Jan 2026) — an AI-powered plant disease diagnosis system.

Upload a leaf photo, speak your symptoms, or type a description — and get an instant diagnosis with treatment recommendations.

The internship required Image + Text diagnosis. I went beyond the scope and added:
- Voice input using OpenAI Whisper (runs locally, no cloud)
- SQLite relational database (replacing hardcoded Python files)
- 1,000 non-plant images for robust invalid-input rejection

System Architecture:
- EfficientNetV2-S for image classification (PyTorch + timm)
- OpenAI Whisper for speech-to-text (local inference)
- LLaMA 3.3 70B via Groq API for symptom classification
- SQLite database with 40+ diseases across 14 crops
- Streamlit frontend + FastAPI backend
- Docker + GitHub Actions CI/CD

3 input modes. 30+ diseases. 14 crops. Instant results.

Thank you Infosys Springboard and our mentor Mahaprasad Jena!

#AI #DeepLearning #ComputerVision #Agriculture #AgriTech #MachineLearning #PlantDisease #PyTorch #Whisper #LLaMA #Streamlit #FastAPI #Docker #InfySpringboard #InfosysSpringboard
```

---

## VIDEO RECORDING TIPS

1. **Resolution**: 1080p minimum
2. **Browser**: Chrome full-screen, clean profile (no bookmarks bar)
3. **Testing images**: Use images from `testing_data/` folder
4. **Thumbnail**: Green background + leaf image + "AI Plant Doctor" text + your face
