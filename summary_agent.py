from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

# -----------------------------
# Initialize two LLMs
# -----------------------------
html_llm = ChatGroq(model="llama-3.3-70b-versatile")  # HTML generator
css_llm = ChatGroq(model="llama-3.3-70b-versatile")   # CSS generator

# -----------------------------
# Import resume content
# -----------------------------
from resume import resume_content

# -----------------------------
# Structured output models
# -----------------------------
class SummaryHTMLOutput(BaseModel):
    html: str = Field(..., description="Generated HTML for the summary section")

class SummaryCSSOutput(BaseModel):
    css: str = Field(..., description="Generated CSS for the summary section")

# -----------------------------
# HTML generation prompt (portfolio style)
# -----------------------------
summary_html_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
You are an expert web developer and personal branding specialist.
Generate a **portfolio-style summary section in HTML** for this resume.
Requirements:
- Tone: **first-person**, as if the person is introducing themselves.
- Structure: Include a **hero section** with <section id="about">, <h1> for the name, and two <p> paragraphs.
- Content: Highlight experience, skills, and career focus in **2 paragraphs**.
- Use semantic HTML5 tags.
- Keep it clean and minimal like a modern portfolio site.
- Only output HTML content (do not include CSS or extra text).

Resume:
{resume_text}
"""
)

# -----------------------------
# CSS generation prompt
# -----------------------------
summary_css_prompt = PromptTemplate(
    input_variables=["html_content"],
    template="""
You are a skilled web designer.
You are given the following HTML summary section:

{html_content}

Your task:
- Generate **beautiful, modern, responsive CSS** for this HTML.
- Follow a professional portfolio style (like https://ai.chaitanya.upenn.domains/).
- Include colors, spacing, typography, hero section styling, and mobile responsiveness.
- Only output CSS content, no HTML or extra text.
"""
)

# -----------------------------
# Create agents
# -----------------------------
html_agent = summary_html_prompt | html_llm.with_structured_output(SummaryHTMLOutput)
css_agent = summary_css_prompt | css_llm.with_structured_output(SummaryCSSOutput)

# -----------------------------
# Generate HTML
# -----------------------------
html_result = html_agent.invoke({"resume_text": resume_content})
generated_html_content = html_result.html

# Wrap HTML with full template and link summary.css
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Summary</title>
    <link rel="stylesheet" href="summary.css">
</head>
<body>
{generated_html_content}
</body>
</html>
"""

# -----------------------------
# Generate CSS
# -----------------------------
css_result = css_agent.invoke({"html_content": generated_html_content})
generated_css = css_result.css

# -----------------------------
# Save files
# -----------------------------
with open("summary.html", "w", encoding="utf-8") as f:
    f.write(full_html)

with open("summary.css", "w", encoding="utf-8") as f:
    f.write(generated_css)

print("summary.html and summary.css generated successfully and linked!")

# -----------------------------
# Commit files to GitHub
# -----------------------------
from commit_file import commit_file
commit_file("summary.html")
commit_file("summary.css")
