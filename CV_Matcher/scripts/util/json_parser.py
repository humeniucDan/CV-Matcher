import ollama
import re

def summary_cv(cv_text):
    model = 'deepseek-r1:8b_vram'
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

3. OUTPUT EXAMPLE (COMPLETE WITH ACTUAL DATA):
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

    response = ollama.chat(
        model=model,
        # options={'keep_alive': '-1'},
        messages=[
            {'role': 'user', 'content': f"{prompt} {cv_text}"},
        ])
    # remove the entire <think>...<./think> section
    summary = (re.sub(r'<think\s*>.*?</think\s*>', '', response['message']['content'], flags=re.DOTALL)
               .replace('*', '')
               .replace('```json', '')
               .replace('```', '')
               .strip())
    return summary

def summary_job(job_text):
    model = 'deepseek-r1:8b_vram'
    prompt = """Act as a job post parser. Analyze the provided job description and return a structured JSON output in the following format:  
{  
  "Type": "[junior/senior/etc] (extracted from job title)",  
  "Role": "[Job Role]",  
  "Company": "[Company Name]",  
  "Responsibilities": [  
    "Summarized responsibility 1",  
    "Summarized responsibility 2",  
    "..."  
  ],  
  "Required": [  
    "Key requirement 1",  
    "Key requirement 2",  
    "... (bullet points)"  
  ],  
  "Skills": {  (for example)
    "Cloud": ["AWS", "Azure", "..."],  
    "Devops": ["Docker", "Jenkins", "..."],  
    "Programming": ["Python", "Java", "..."],
    ...
  },  
  "Benefits": [  
    "Benefit 1 (summarized or verbatim)",  
    "Benefit 2",  
    "... (exact or condensed)"  
  ]  
}  

Follow these rules:  
1. Responsibilities: Summarize key tasks into 4-5 concise bullet points.  
2. Required: List qualifications directly from the "Required Qualifications" section OR SIMILAR.  
3. Skills: Extract and subcategorize skills from the job description. for example: Cloud: ["AWS", "Azure", "..."]
4. Benefits: Retain exact wording or summarize briefly while preserving critical details.  

Return ONLY VALID JSON with no additional text.  

Job Post:  
"""

    response = ollama.chat(
        model=model,
        #options={'keep_alive': '-1'},
        messages=[
                {'role': 'user', 'content': f"{prompt} {job_text}"},
        ])

    # remove the entire <think>...<./think> section
    summary = (re.sub(r'<think\s*>.*?</think\s*>', '', response['message']['content'], flags=re.DOTALL)
                .replace('*', '')
                .replace('```json', '')
                .replace('```', '')
                .strip())
    return summary


if __name__ == '__main__':
    # Example CV text
    cv_text = """
Andrei Mihailescu
Technical Skills
- JavaScript, ReactJS, Node.js, SQL
- HTML, CSS, Bootstrap, AngularJS
- Python, Django, PostgreSQL, REST APIs
- TypeScript, VueJS, AWS, Docker
- Java, Spring Boot, OracleSQL, Kubernetes
Foreign Languages
- English: C1
- Spanish: B1
- French: A2
Education
- University Name: Politehnica University of Bucharest
- Program Duration: 4 years
- Master Degree Name: Politehnica University of Bucharest
- Program Duration: 2 years
Certifications
- AWS Certified Solutions Architect – Associate
- Certified Kubernetes Administrator (CKA)
- Oracle Certified Professional, Java SE 11 Developer
Project Experience
1. **Inventory Management System**
   Developed a robust inventory management system using Java and Spring Boot for the backend, with an OracleSQL database to handle complex queries and data storage. Implemented REST APIs to facilitate seamless communication between the backend and a responsive frontend built with AngularJS and Bootstrap. Deployed the application on a Kubernetes cluster, ensuring scalability and high availability. Technologies and tools used: Java, Spring Boot, OracleSQL, AngularJS, Bootstrap, Kubernetes.

2. **Real-time Data Analytics Platform**
   Created a real-time data analytics platform leveraging Python and Django for the backend, with PostgreSQL as the database to manage large datasets efficiently. Utilized ReactJS and TypeScript to build a dynamic and interactive user interface. Integrated AWS services for cloud storage and Docker for containerization, enabling smooth deployment and scalability. Technologies and tools used: Python, Django, PostgreSQL, ReactJS, TypeScript, AWS, Docker.
    """
    print(summary_cv(cv_text))
    # Example job text
    job_text = """Job Title:
Machine Learning Engineer - Backend Developer
Company Overview:
InnovateTech Solutions is a leading technology company dedicated to transforming industries through cutting-edge software solutions. We specialize in developing scalable and efficient systems that empower businesses to harness the power of data. Our team is passionate about innovation, collaboration, and driving success for our clients worldwide.
Key Responsibilities:
- Design, develop, and maintain robust backend systems to support machine learning applications.
- Collaborate with data scientists and front-end developers to integrate machine learning models into production environments.
- Optimize and scale backend services to handle large volumes of data and ensure high performance.
- Implement and maintain APIs for seamless communication between different components of the system.
- Conduct code reviews and provide constructive feedback to ensure code quality and best practices.
- Troubleshoot and resolve issues related to backend systems and machine learning model deployments.
- Stay updated with the latest trends and advancements in machine learning and backend development technologies.
Required Qualifications:
- Bachelor’s or Master’s degree in Computer Science, Engineering, or a related field.
- Proven experience as a Backend Developer with a focus on machine learning applications.
- Strong proficiency in programming languages such as Python, Java, or C++.
- Experience with machine learning frameworks and libraries (e.g., TensorFlow, PyTorch, Scikit-learn).
- Solid understanding of RESTful API design and development.
- Familiarity with database technologies such as SQL, NoSQL, and data warehousing solutions.
- Experience with cloud platforms (e.g., AWS, Google Cloud, Azure) for deploying and managing applications.
Preferred Skills:
- Knowledge of containerization and orchestration tools like Docker and Kubernetes.
- Experience with distributed computing frameworks such as Apache Spark or Hadoop.
- Understanding of data pipeline and ETL processes.
- Familiarity with DevOps practices and CI/CD pipelines.
- Strong problem-solving skills and the ability to work independently as well as in a team.
Benefits:
- Competitive salary and performance-based bonuses.
- Comprehensive health, dental, and vision insurance plans.
- Flexible work hours and remote work options.
- Opportunities for professional development and continuous learning.
- Generous paid time off and holiday schedule.
- Collaborative and inclusive work environment with a focus on work-life balance."""
    print(summary_job(job_text))
