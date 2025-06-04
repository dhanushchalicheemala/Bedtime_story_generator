
**Introduction**
Have you ever wished for an AI-powered bedtime story generator that creates soothing, personalized stories for kids?
I built "Cozy Story Time 🛏️📖", a fun and interactive web app that generates AI-powered bedtime stories.

**Demo Video**

📺 [Click here to download and view the demo video](demo.mp4)

Note: The video is available in the repository. You can download it and play it locally to see the app in action.

**Core Features of the App**
1. AI-Generated Bedtime Stories🌙
Users can enter a story topic, and the app creates a short, soothing story following bedtime storytelling best practices.

2. AI-Generated Illustrations🎨
Each story comes with a custom AI-generated illustration using OpenAI's DALL·E model.

3. Text-to-Speech (TTS) for Voice Narration🎙️
To make the stories even more engaging, I added AI-powered voice narration using OpenAI’s TTS API.

4. Export as a PDF📄
Users can download the bedtime story as a PDF file, including the AI-generated illustration.

5. Usage Limits to Prevent Abuse🚫
To avoid excessive use, the app limits users to request for only 4 stories of your choice.

**Building Blocks**
1. Generates a bedtime story using GPT-4o.
2. Creates an AI-generated illustration using DALL·E.
3. Converts the story into speech using OpenAI’s TTS API.
4. Generates a PDF including the story and image.
5. Prompt Engineering - Since this app is meant for young children, I carefully crafted the AI prompts to ensure.
    a) Calm & bedtime-friendly content (No scary elements).
    b) Simple words & short sentences (Easy to understand).
    c) A soothing rhythm with gentle repetition & sound effects.
    d) Bedtime-friendly settings (Bedrooms, starry skies, cozy gardens).
    e) Parent-child engagement through interactive storytelling

**Building the Web App and Deployment on Streamlit Cloud**
1. Writing the code in Visual Studio & pushed the code to GitHub
2. Built the front-end using Streamlit Cloud
3. Configured environment variables & API keys securely
4. Tested the app and fixed issues
5. Finally, Deployed it on Streamlit Cloud

**Choosing the Tech Stack**
1. AI Story Generator - **OpenAI GPT-4o**
2. AI Illustrations - **OpenAI DALL·E**
3. AI Voice Narration - **OpenAI Text-to-Speech API**
4. Web App - **Streamlit**
5. PDF Generation - **ReportLab**
6. Deployment - **Streamlit Cloud**
7. Version Control - **GitHub**

**What’s Next?**
I’m planning to further enhance "Cozy Story Time 🛏️📖" by:

1. Adding multilingual support 🌍 (Generate stories in different languages).
2. Enabling user-created characters 🎭 (Let kids name their story hero).
3. Adding a parent feedback system 📝 (Let parents rate stories & suggest improvements).
4. Saving feedback to Google Sheets 📊using the Google Sheets API
5. Building a full feedback dashboard 📈(Stored responses in a database for analysis) 

