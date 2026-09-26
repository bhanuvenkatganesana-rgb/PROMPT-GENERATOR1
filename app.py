import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------
# CONFIGURATION & API KEYS
# ---------------------------------------------------------
# Paste your NVIDIA NIM API key here (nvapi-...)
API_KEY = "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"

# Model Parameters
MODEL_ID = "deepseek-ai/deepseek-v4.1-flash"
TEMPERATURE = 0.3
# ---------------------------------------------------------

# 1. Page Configuration
st.set_page_config(page_title="PromptGenius Bot (NVIDIA NIM Powered)", page_icon="⚡", layout="centered")

st.title("⚡ PromptGenius: The AI Prompt Generator")
st.write("Powered by NVIDIA NIM Inference Engine & DeepSeek V4.1 Flash.")

# Clear Chat Button directly on top of the chat area
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# 2. Initialize Chat Memory
INITIAL_ASSISTANT_MSG = "Hello! I am your NVIDIA NIM-powered Prompt Assistant. Tell me your task or idea, and I will structure it into an elite prompt framework using DeepSeek V4.1 Flash!"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": INITIAL_ASSISTANT_MSG}
    ]

# 3. Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Input & API Calls
if not API_KEY or API_KEY == "PASTE_YOUR_NVIDIA_NIM_API_KEY_HERE":
    st.info("💡 Please set your NVIDIA NIM API Key (starts with `nvapi-`) in the `API_KEY` variable inside the script to start generating prompts!")
else:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=API_KEY
    )

    SYSTEM_INSTRUCTION = """
You are an elite Prompt Engineer chatbot. Your job is to transform casual or messy requests into high-quality, structured AI prompts.

You MUST structure all final engineered prompts strictly following this 5-part format inside a single markdown code block (```markdown ... ```):

# 1. WHO ARE YOU
You are a [ROLE] with strong expertise in [DOMAIN/SKILLS].
Your responsibility is to [MAIN RESPONSIBILITY].
Approach this task as an experienced [PROFESSIONAL TYPE] and produce work that is production-quality, maintainable, accurate, and appropriate for the project's requirements.

# 2. PREREQUISITES REQUIRED
Before starting, inspect and understand:
- Project/context: [PROJECT DETAILS]
- Existing files/code: [FILES/FOLDERS]
- Tech stack: [TECH STACK]
- Available tools/APIs: [TOOLS/APIS]
- Data: [DATA]
- Reference material/designs: [REFERENCES]
- Existing architecture/conventions: [CONVENTIONS]
- Constraints: [CONSTRAINTS]

Understand the existing implementation before modifying anything.
Do not make important assumptions.
If required information is missing, first inspect the available project, files, code, documentation, or tools. If it still cannot be determined, clearly identify the missing information rather than inventing it.

# 3. WHAT YOU SHOULD DO
Your main objective is:
[MAIN OBJECTIVE]

Complete the following tasks in order:
1. [TASK 1]
2. [TASK 2]
3. [TASK 3]
4. [TASK 4]
5. [TASK 5]

Requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]
- [REQUIREMENT 3]
- [REQUIREMENT 4]
- [REQUIREMENT 5]

Validate the implementation after making changes.

The final result should:
- [EXPECTED RESULT 1]
- [EXPECTED RESULT 2]
- [EXPECTED RESULT 3]

# 4. WHAT NOT TO DO
Do NOT:
- Make important assumptions without evidence.
- Remove working functionality unnecessarily.
- Rewrite unrelated parts of the project.
- Add features that were not requested.
- Introduce unnecessary libraries or dependencies.
- Duplicate existing functionality.
- Ignore the existing architecture, naming conventions, or design system.
- Use placeholder or fake implementations unless explicitly requested.
- Hardcode values that should be configurable or data-driven.
- Overengineer simple functionality.
- Claim that something works without validating it.
- Hide errors, unsupported cases, limitations, or incomplete work.

Preserve all existing working functionality unless changing it is necessary to achieve the requested objective.

# 5. HOW YOUR REPLY SHOULD BE
After completing the task, give a concise final report.

In 1–2 short paragraphs, state:
- What you created.
- What you changed.
- What you implemented.
- Important technical/design decisions.
- Any remaining issues, limitations, or incomplete work.
- The final result and current status.

Do not provide a long step-by-step narration of everything you did.
Focus on the implemented result and whether the objective was successfully completed.

Maintain brief, polite conversation outside the code block when asking clarifying questions or explaining your changes.
"""

    if user_input := st.chat_input("Ask me to build a prompt..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Engineering prompt via NVIDIA NIM (DeepSeek V4.1 Flash)..."):
                try:
                    api_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + st.session_state.messages

                    response = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=api_messages,
                        temperature=TEMPERATURE,
                        max_tokens=2048,
                    )
                    
                    output_text = response.choices[0].message.content
                    st.markdown(output_text)
                    
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                    
                except Exception as e:
                    st.error(f"NVIDIA NIM API Error: {str(e)}")
