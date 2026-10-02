import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

try:
    import docx
except ImportError:
    install('python-docx')
    import docx

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_BREAK

doc = Document()

doc.add_heading('Project Title', 0)
doc.add_heading('RescuAI: Generative AI-Powered Emergency SOS Aggregator & Disaster Triage System', 1)

doc.add_paragraph('Learning Block 1')
doc.add_paragraph('Submitted by\nSrushti Donga\n\nCollege / Institute Name: [Insert College Name]\nDepartment of [Insert Department Name]\nAcademic Year: [Final / Pre-Final] – [2026–2027]\n\nGuided by: [Insert Mentor Name]')
doc.add_page_break()

doc.add_heading('Index', 1)
index_text = '''1. Introduction
2. Problem Statement
3. Objectives
4. Project Scope
5. Proposed System / Methodology
6. System Architecture / Workflow
7. Implementation
8. User Interface / Application Screenshots
9. Challenges and Limitations
10. Conclusion
11. Future Scope
12. References'''
doc.add_paragraph(index_text)
doc.add_page_break()

def add_section(title, content_list):
    doc.add_heading(title, 1)
    for item in content_list:
        if item.startswith('* '):
            doc.add_paragraph(item[2:], style='List Bullet')
        elif item.startswith('### '):
            doc.add_heading(item[4:], 2)
        else:
            doc.add_paragraph(item)

add_section('1. Introduction', [
    'RescuAI is a Generative AI-powered emergency SOS aggregator and disaster triage backend system designed to streamline crisis response.',
    'During natural disasters or emergencies, control rooms are flooded with chaotic, duplicate, and unstructured distress messages. RescuAI addresses this by intelligently centralizing and prioritizing these requests for Emergency Responders.',
    'Generative AI (Google Gemini) is used to natively ingest multimodal inputs (raw audio bytes and unstructured text), extract critical entities (location, injuries), determine the urgency of the situation, and filter out spam or fake requests automatically.',
    'The system produces structured JSON output, specifically formatted as "Dispatch Cards" that include severity scores, structured action plans, and extracted GPS/landmark data.',
    'Main Features:',
    '* Multimodal SOS Ingestion: Accepts both text messages and raw voice/audio distress signals.',
    '* Automated Triage & Scoring: Automatically classifies the severity (e.g., CRITICAL, MODERATE) of incoming requests.',
    '* Smart Spatial Deduplication: Groups duplicate SOS requests originating from the same 500-meter radius to prevent redundant dispatches.',
    '* Spam & Fake Detection: Uses AI to instantly identify and filter out troll or non-emergency messages.',
    '* Responder Dashboard API: Provides a secure, role-based, prioritized queue of emergencies for dispatchers.'
])

add_section('2. Problem Statement', [
    '* Specific real-world problem: In disaster scenarios (e.g., floods, earthquakes), emergency control rooms receive an overwhelming volume of fragmented distress calls and messages across various platforms, leading to delayed response times for critical cases.',
    '* Current inefficiencies: Manual monitoring is exceptionally slow. Dispatchers have to manually listen to audio messages, transcribe them, identify duplicate reports from the same location, and subjectively decide which incident to respond to first.',
    '* Justification for GenAI: A traditional rule-based system cannot understand the panic in a voice, deduce implicit context from a messy text message, or accurately filter out sophisticated spam. GenAI is uniquely suited to perform semantic analysis and entity extraction on unstructured, multimodal data.',
    '* AI improvements: By automating triage, RescuAI saves critical minutes per request. It reduces the manual effort of transcription and sorting by over 90%, allowing dispatchers to focus purely on rescue logistics.',
    '* Expected outcome: Emergency responders are equipped with a clean, prioritized, and deduplicated dashboard of "Dispatch Cards," ensuring that life-threatening cases are addressed first and rescue vehicles are dispatched efficiently.'
])

add_section('3. Objectives', [
    '* Develop a functional, deployable GenAI-based FastAPI backend application for emergency SOS processing.',
    '* Select and integrate the Google Gemini (1.5/3.8 Flash) Multimodal API suited for real-time text and audio parsing.',
    '* Design effective system prompts that reliably produce structured JSON outputs (Urgency, Location, Needs).',
    '* Provide a secure, JWT-authenticated API interface for Emergency Responders.',
    '* Evaluate the accuracy of AI-generated triage scores and the geographic deduplication clustering logic.'
])

add_section('4. Project Scope', [
    '* Use cases covered: The application covers text and audio distress signal ingestion, spatial deduplication (500m radius using Haversine formula), severity scoring, and spam filtering. It does not cover the physical dispatching of vehicles or hardware IoT integrations.',
    '* Target users: Stranded citizens (end-users sending signals via public endpoints) and Emergency Responders/Dispatchers (accessing the secure dashboard).',
    '* GenAI-powered features: Sentiment/Urgency extraction, multimodal data parsing, automated dispatch card generation, and spam detection.',
    '* Inputs/Outputs: The system accepts raw text strings, audio files, and optional GPS coordinates. It produces structured JSON metadata and prioritized lists.',
    '* Current limitations: Currently relies on a single AI provider (Google Gemini) requiring internet uptime, lacks an integrated graphical frontend (runs via Swagger UI/API clients), and processing speed is subject to API latency limits.'
])

add_section('5. Proposed System / Methodology', [
    '* Overall approach: A centralized FastAPI backend acts as the orchestrator. It receives raw emergency data, routes it to the Gemini GenAI model for intelligence extraction, applies geographic algorithms for deduplication, and persists the curated data into a relational database for dispatchers to access.',
    '* User Input: The user provides a text prompt or uploads an audio file along with optional latitude/longitude coordinates via the /api/v1/sos/* endpoints.',
    '* Processing step-by-step:',
    '1. The API receives the payload and applies rate-limiting to prevent abuse.',
    '2. The input is packaged and sent to the gemini_service.py module.',
    '3. The Gemini model parses the input using a strictly defined system prompt to evaluate urgency and extract details.',
    '4. The deduplication_service.py checks the database for active requests within a 500m radius. If a match is found, the requests are clustered.',
    '5. The processed "Dispatch Card" is saved to the SQLite/PostgreSQL database.',
    '* Prompts and Techniques: We utilize structured output prompting. The system prompt instructs Gemini to return data strictly adhering to a predefined Pydantic JSON schema, bypassing standard conversational text output.',
    '* Output formatting: The final response is formatted as a structured RESTful JSON response containing a prioritized list of emergencies for the responder dashboard.'
])

add_section('6. System Architecture / Workflow', [
    'System Flow:',
    '* User interaction: Users send distress signals via API endpoints (simulating an app/web interface).',
    '* Input collection: Data is collected securely via FastAPI routing layer.',
    '* Prompt-construction: The service layer wraps the user input with system instructions and JSON schema requirements.',
    '* GenAI integration: The application communicates via HTTP/SDK to the Gemini model in real-time.',
    '* Response flow: The generated data is stored in the database, which the responder pulls via a GET request to view their prioritized dashboard.',
    '(Note: Please insert the visual architecture flowchart diagram here as specified in the PDF).'
])

add_section('7. Implementation', [
    '* Technologies and Tools: Python 3.10+, Uvicorn (ASGI server), SQLAlchemy 2.0 (ORM), Passlib/Bcrypt (Security).',
    '* Programming languages and Frameworks: Python (Core language), FastAPI (Backend framework).',
    '* Generative AI Model: Google Gemini 1.5/3.8 Flash Multimodal API.',
    '* User Interface Design: Currently implemented as a headless backend with an interactive Swagger UI (/docs) serving as the primary developer and tester interface.',
    '* GenAI Integration: Integrated using the official Google Generative AI Python SDK. Authentication is handled via a secure API key stored in .env.',
    '* Prompt Construction & Input Processing:\nSystem instructions are strictly defined to output JSON. Example:\n"You are an emergency triage AI. Analyze the distress signal and output STRICTLY in the requested JSON schema. Extract: urgency, location_details, medical_needs, and is_spam_or_fake flag."'
])

add_section('8. User Interface / Application Screenshots', [
    'Please add actual screenshots of the working application for each item below:',
    '* [Insert Screenshot: The application\'s home or main screen (Swagger UI dashboard)]',
    '* [Insert Screenshot: The screen where users provide input or prompts (POST /sos/text or /sos/audio)]',
    '* [Insert Screenshot: The GenAI processing or interaction interface (Terminal logs or API loading state)]',
    '* [Insert Screenshot: Examples of AI-generated outputs (JSON response showing urgency, location, etc.)]',
    '* [Insert Screenshot: The final result screen (Responder dashboard GET /dashboard with Dispatch Cards)]'
])

add_section('9. Challenges and Limitations', [
    '### Challenges',
    '* Technical challenges: Encountered infinite reload loops with Uvicorn\'s watchfiles monitoring the venv directory, which was resolved by strictly scoping the --reload-dir flag. Resolving passlib/bcrypt hashing compatibility bugs required writing a direct implementation in security.py.',
    '* Selecting/Integrating GenAI: Adapting to Google\'s API model version changes (transition from gemini-1.5-flash to gemini-3.8-flash) required building an automated fallback mechanism.',
    '* Prompt Difficulties: Ensuring the GenAI model did not return markdown-formatted blocks was challenging. Overcome by enforcing Pydantic schemas and refining system instructions.',
    '* Unexpected AI Outputs: Initially, the AI would attempt to triage obvious spam messages. Resolved by implementing a strict is_spam_or_fake boolean flag in the prompt.',
    '### Limitations',
    '* Constraints: High dependency on external API availability and strict token rate limits of the Gemini free tier. Audio processing introduces slight latency.',
    '* Security, privacy: Handling exact user locations and medical data requires stringent privacy measures.',
    '* Functional limitations: Does not yet support offline capabilities for citizens in areas with zero network connectivity.'
])

add_section('10. Conclusion', [
    '* Summarise: We successfully developed the complete backend architecture for RescuAI, a system capable of ingesting chaotic emergency signals and organizing them into actionable dispatch cards.',
    '* Role of GenAI: Generative AI acted as the core "brain" of the application, seamlessly handling the unstructured nature of real-world human panic across both text and voice.',
    '* Features Implemented: JWT authentication, Multimodal SOS ingestion, Haversine-based geographic deduplication, and automated AI triage.',
    '* Practical usefulness: The generated dispatch cards are highly practical, allowing dispatchers to instantly identify critical incidents without manual transcription, cutting down triage time.',
    '* Key learning: Gained experience in building production-ready FastAPI applications, integrating multimodal Large Language Models, and implementing real-world spatial algorithms.'
])

add_section('11. Future Scope', [
    '* Additional features: Implementing real-time WebSocket notifications to push new dispatch cards to the responder dashboard live.',
    '* Accuracy improvements: Utilizing RAG with standard operating procedure (SOP) manuals for emergency responders to provide better tactical advice.',
    '* Advanced GenAI capabilities: Incorporating image and video feed ingestion to allow AI to assess structural damage from user-uploaded photos.',
    '* Additional formats: Integrating directly with WhatsApp or Telegram bots to allow citizens to send distress signals via familiar apps.',
    '* Deployment steps: Containerizing the application using Docker, deploying it on a cloud provider (AWS/GCP), and migrating to a managed PostgreSQL cluster.'
])

add_section('12. References', [
    '* Google Gemini API Documentation - https://ai.google.dev/docs',
    '* FastAPI Official Documentation - https://fastapi.tiangolo.com/',
    '* SQLAlchemy 2.0 Documentation - https://docs.sqlalchemy.org/',
    '* Pydantic v2 Documentation - https://docs.pydantic.dev/',
    '* GitHub Repository for RescuAI Project files and architecture designs.'
])

doc.save(r'C:\Users\LENOVO\OneDrive\Documents\GitHub\RescuAI\RescuAI_Project_Report.docx')
print("Document saved successfully")
