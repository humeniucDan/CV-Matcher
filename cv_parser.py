from docx import Document
import io
import ollama
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_docx(byte_stream):
    doc = Document(io.BytesIO(byte_stream))
    text = []

    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    text.append(paragraph.text)

    return '\n'.join(text)


def convert_text_to_json(text):
    model = 'deepseek-r1:7b'
    prompt = """
    You are a CV-to-JSON converter. Transform input CVs into JSON format following these rules:

    1. PRESERVE THESE KEYS WITH EXACT TEXT:
       - "Name" (string)
       - "Technical Skills" (array)
       - "Education" (array)
       - "Foreign Languages" (array)
       - "Certifications" (array)
       - "Work Experience" (array, if exists)

    2. PROCESS PROJECTS:
       "Project Experience" (object) containing:
       - "Hidden Skills" (array of 3-5 inferred skills)
       - "Technologies Used" (array of explicit tech items)

    3. OUTPUT EXAMPLE:
    {
      "Name": "Joh Doe",
      "Technical Skills": ["JavaScript", "React", "TypeScript", "Java", "Spring Boot", "AWS", "Docker", "SQL", "PostgreSQL"],
      "Foreign Languages": ["English", "Romanian"],
      "Education": [
        {
          "University Name": "MIT",
          "Program Duration": "2020-2024",
          "Degree Name": "BSc Computer Science"
        }
      ],
      "Certifications": [
        {
          "Title": "AWS Certified Machine Learning – Specialty",
          "Issuing Authority": "Amazon Web Services"
        },
        {
          "Title": "Data Science Professional",
          "Issuing Authority": "Data Science Council"
        }
      ],
      "Project Experience": [
        {
          "Title": "Machine Learning Model Deployment on AWS SageMaker",
          "Hidden Skills": ["Cloud Platforms Expertise", "Containerization Techniques", "CI/CD Pipeline Automation"],
          "Technologies Used": ["Python", "TensorFlow", "AWS SageMaker", "Docker", "Jenkins"]
        },
        {
          "Title": "Interactive Web Application Development",
          "Hidden Skills": ["Responsive Web Development", "UI/UX Design and Prototyping", "Database Integration"],
          "Technologies Used": ["JavaScript", "React.js", "Figma", "PostgreSQL"]
        }
      ]
    }

    4. SPECIAL RULES:
       - Omit "Project Experience" key entirely if no projects
       - Keep original dates/company names in "Work Experience"
       - Maintain exact certification/language wording
       - Only use double quotes, no trailing commas
       - No additional fields/comments

    DO NOT ADD ANYTHING ELSE, STRICTLY FOLLOW THE OUTPUT EXAMPLE.
    The text:
    """

    try:
        logger.info("Starting ollama chat")
        response = ollama.chat(
            model=model,
            # options={'keep_alive': '-1'},
            messages=[
                {'role': 'user', 'content': f"{prompt} {text}"},
            ]
        )
        logger.info("Ended ollama chat")

        # remove the entire ...<./think> section
        summary = (re.sub(r'.*?', '', response['message']['content'], flags=re.DOTALL)
                   .replace('*', '')
                   .replace('```json', '')
                   .replace('```', '')
                   .strip()
                   )

        return summary

    except Exception as e:
        logger.error(e)
        return None
