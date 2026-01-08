from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# LLM CONFIG — CONTENT EXTRACTION ONLY
# ==================================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

# ==================================================
# RESUME CONTENT
# ==================================================
from resume import resume_content
resume_text = resume_content[:6000]

# ==================================================
# LOCKED HTML TEMPLATE (DO NOT TOUCH STYLING)
# ==================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{NAME}}</title>

    <link rel="shortcut icon" href="img/favicon.png" type="image/x-icon" />
    <link rel="stylesheet" href="css/main.css" />
    <link rel="stylesheet" href="css/media.css" />

    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css"
      crossorigin="anonymous"
    />
  </head>

  <body>

<header id="header" class="header">
  <div class="container container-lg">
    <div class="header-nav">
      <a href="#home" class="logo">{{INITIALS}}</a>
      <nav class="nav">
        <ul class="nav-list">
          <li><a href="#home" class="nav-link active">Home</a></li>
          <li><a href="#about" class="nav-link">About</a></li>
          <li><a href="#projects" class="nav-link">Works</a></li>
          <li><a href="#contact" class="nav-link">Contact</a></li>
        </ul>
      </nav>
    </div>
  </div>
</header>

<section id="home" class="hero">
  <div class="container container-lg">
    <div class="hero-row" data-aos="fade-zoom-in">
      <div class="hero-content">
        <span class="hero-greeting">Hello, I am</span>
        <h1 class="hero-heading">{{NAME}}</h1>
        <span class="hero-heading-subtitle">{{TAGLINE}}</span>

        <div class="about-social-list">
          <div class="social-links-row">
            {{SOCIALS}}
          </div>
        </div>

        <div>
          <a href="#projects" class="btn">My Portfolio</a>
          <a href="#contact" class="btn btn-white">Contact Me</a>
        </div>
      </div>

      <div class="hero-img">
        <img src="img/hero/hero.png" alt="Profile photo" />
      </div>
    </div>
  </div>
</section>

<section id="about" class="about">
  <div class="container">
    <h2 class="title">About Me</h2>
    <p class="about-descr">
      {{ABOUT}}
    </p>
    <a href="resume.pdf" class="btn btn-white">Download CV</a>
  </div>
</section>

<section id="projects" class="projects">
  <div class="container container-lg">
    <h2 class="title">Works</h2>
    <div class="projects-row">
      {{PROJECTS}}
    </div>
  </div>
</section>

<section id="contact" class="contact">
  <div class="container">
    <h2 class="title">Contact</h2>
    <p>Let’s talk and work together.</p>

    <div class="social-links-row">
      {{SOCIALS}}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p>&copy; {{YEAR}} {{NAME}}</p>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
<script type="module" src="js/main.js"></script>
<script>AOS.init();</script>

</body>
</html>
"""

# ==================================================
# PROMPT — STRICT TEXT OUTPUT
# ==================================================
prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Extract clean portfolio content from the resume.

Return EXACTLY this format:

NAME:
Full Name

INITIALS:
Initials (e.g. J.S.)

TAGLINE:
Short professional headline

ABOUT:
Professional summary paragraph

PROJECTS:
Title | Description || Title | Description

LINKS:
GitHub: url || LinkedIn: url || Website: url

Resume:
{resume}
"""
)

raw = (prompt | llm).invoke({"resume": resume_text}).content

# ==================================================
# PARSER
# ==================================================
def extract(label):
    return raw.split(f"{label}:")[1].split("\n\n")[0].strip()

name = extract("NAME")
initials = extract("INITIALS")
tagline = extract("TAGLINE")
about = extract("ABOUT")

projects_html = ""
for item in extract("PROJECTS").split("||"):
    title, desc = item.split("|", 1)
    projects_html += f"""
    <div class="project-box" data-aos="fade-zoom-in">
      <div class="project-mask">
        <div class="project-caption">
          <h5 class="white">{title.strip()}</h5>
          <p class="white">{desc.strip()}</p>
        </div>
      </div>
    </div>
    """

socials_html = ""
for link in extract("LINKS").split("||"):
    label, url = link.split(":", 1)
    socials_html += f"""
    <a href="{url.strip()}" target="_blank">
      <img src="img/social_icons/{label.lower().strip()}.svg" alt="{label}">
    </a>
    """

# ==================================================
# FILL TEMPLATE
# ==================================================
html = (
    HTML_TEMPLATE
    .replace("{{NAME}}", name)
    .replace("{{INITIALS}}", initials)
    .replace("{{TAGLINE}}", tagline)
    .replace("{{ABOUT}}", about)
    .replace("{{PROJECTS}}", projects_html)
    .replace("{{SOCIALS}}", socials_html)
    .replace("{{YEAR}}", "2026")
)

# ==================================================
# WRITE FILE
# ==================================================
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html generated using repo-style structure")

# ==================================================
# COMMIT
# ==================================================
from commit_file import commit_file
commit_file("index.html")
