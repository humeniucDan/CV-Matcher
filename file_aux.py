import ollama

try:
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

    cv = """
    Florin Neagu
Technical Skills
Python, TensorFlow: 4
JavaScript, ReactJS: 3
AWS SageMaker, Docker: 2
SQL, PostgreSQL: 3
Figma, Adobe XD: 2
Foreign Languages
- English: C1
- Spanish: B2
Education
- University Name: University Politehnica of Bucharest
- Program Duration: 4 years
- Master Degree Name: University Politehnica of Bucharest
- Program Duration: 2 years
Certifications
- AWS Certified Machine Learning – Specialty
- TensorFlow Developer Certificate
Project Experience
1. Predictive Analytics Platform for Retail
   Led the development of a predictive analytics platform using Python and TensorFlow to forecast retail sales trends. Implemented machine learning models that improved sales predi
ction accuracy by 25%, enabling better inventory management and reducing waste. Utilized AWS SageMaker for model training and deployment, ensuring scalability and efficient resource management. Technologies and tools used: Python, TensorFlow, AWS SageMaker, Docker.

2. Interactive Web Application for Real-time Data Visualization
   Developed an interactive web application using ReactJS and JavaScript to visualize real-time data from IoT devices. The application provided users with dynamic dashboards and in
sights, enhancing decision-making processes for industrial clients. Integrated PostgreSQL for efficient data storage and retrieval, ensuring quick access to historical data. Technologies and tools used: JavaScript, ReactJS, SQL, PostgreSQL.

3. User-centric Mobile App Design for Fitness Tracking
   Designed a mobile application interface focused on fitness tracking, employing Figma and Adobe XD to create a seamless user experience. Conducted extensive user testing sessions
 to refine the design, resulting in a 40% increase in user engagement. Collaborated closely with developers to ensure the design was effectively translated into a functional application. Technologies and tools used: Figma, Adobe XD, React Native.
    """

    response = ollama.chat(
        model = 'deepseek-r1:7b',
        messages=[
            {'role': 'user', 'content': f"{prompt} {cv}"},
        ]
    )

    print(response['message']['content'])

except Exception as e:
    print(e)