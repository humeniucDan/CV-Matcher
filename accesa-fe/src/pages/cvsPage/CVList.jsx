import React, { useEffect, useState } from "react";
import CvCard from "../../components/cvCard/CvCard";
import styles from "./CvList.module.css";
import { useNavigate } from 'react-router-dom';

const CVList = () =>
{
     const [cvs, setCVs] = useState([]);

     useEffect(() => {
        const fetchCVs = async () => {
          try {
            const response = await fetch("http://localhost:8080/cv/get-all-cvs");
            const data = await response.json();
            setCvs(data);
          } catch (err) {
            console.error("Error fetching CVs:", err);
          }
        };
        
        const hardcodedCVs = [
            {   "id" : "1",
                "Name": "Andrei Mihailescu",
                "Contact Information": null,
                "Technical Skills": [
                  "Figma", 
                  "Adobe XD", 
                  "Sketch", 
                  "InVision", 
                  "HTML", 
                  "CSS", 
                  "JavaScript", 
                  "ReactJS", 
                  "Bootstrap"
                ],
                "Foreign Languages": [
                  {
                    "Language": "English",
                    "Proficiency Level": "C1"
                  },
                  {
                    "Language": "Spanish",
                    "Proficiency Level": "B2"
                  }
                ],
                "Education": [
                  {
                    "University Name": "University Politehnica of Bucharest",
                    "Program Duration": "4 years",
                    "Degree Name": "Bachelor's Degree in Computer Science"
                  },
                  {
                    "University Name": "University Politehnica of Bucharest",
                    "Program Duration": "2 years",
                    "Degree Name": "Master's Degree in Software Engineering"
                  }
                ],
                "Certifications": [
                  {
                    "Title": "Adobe Certified Professional in Visual Design Using Adobe XD",
                    "Issuing Authority": "Adobe"
                  },
                  {
                    "Title": "Certified JavaScript Developer",
                    "Issuing Authority": "JavaScript Developer Certification Board"
                  }
                ],
                "Project Experience": [
                  {
                    "Title": "Responsive Web Design for a Local Business",
                    "Hidden Skills": ["Responsive Web Design Expertise", "Bootstrap Integration", "Collaboration and Stakeholder Communication"],
                    "Technologies Used": ["HTML", "CSS", "JavaScript", "Bootstrap"]
                  },
                  {
                    "Title": "Interactive Prototype for a Mobile Application",
                    "Hidden Skills": ["UI/UX Design and Prototyping", "User Testing and Feedback Analysis", "Design to Developer Collaboration"],
                    "Technologies Used": ["Sketch", "InVision", "Adobe XD"]
                  }
                ]
              },
              { "id" : "2",
                "Name": "Andrei Vasile Dumitru",
                "Technical Skills": [
                  "JavaScript", "ReactJS", "TypeScript", "HTML", "CSS",
                  "AngularJS", "Bootstrap", "TypeScript", "Git",
                  "VueJS", "JavaScript", "REST APIs", "CSS",
                  "HTML", "CSS", "Figma", "Adobe XD"
                ],
                "Foreign Languages": [
                  "English: C2",
                  "Spanish: B1",
                  "French: A2"
                ],
                "Education": [
                  {
                    "University Name": "University of Bucharest",
                    "Program Duration": "4 years",
                    "Degree Name": "Bachelor's Degree in Computer Science"
                  },
                  {
                    "University Name": "University of Bucharest",
                    "Program Duration": "2 years",
                    "Degree Name": "Master's Degree in Computer Science"
                  }
                ],
                "Certifications": [
                  {
                    "Title": "Microsoft Certified: Azure Developer Associate",
                    "Issuing Authority": "Microsoft"
                  },
                  {
                    "Title": "Google Professional Cloud Developer",
                    "Issuing Authority": "Google"
                  },
                  {
                    "Title": "AWS Certified Developer – Associate",
                    "Issuing Authority": "Amazon Web Services"
                  }
                ],
                "Project Experience": [
                  {
                    "Title": "Interactive Web Application for Event Management",
                    "Hidden Skills": ["ReactJS", "TypeScript", "CSS", "Bootstrap", "REST APIs", "Git"],
                    "Technologies Used": ["JavaScript", "TypeScript", "CSS", "Bootstrap", "REST APIs", "Git"]
                  },
                  {
                    "Title": "Cloud-Based Project Collaboration Platform",
                    "Hidden Skills": ["AngularJS", "TypeScript", "Google Cloud Services", "REST APIs", "Figma", "Adobe XD"],
                    "Technologies Used": ["AngularJS", "TypeScript", "Google Cloud", "REST APIs", "Figma", "Adobe XD"]
                  }
                ]
              }
        ]
        setCVs(hardcodedCVs);
        //fetchCVs();
      }, []);


      const navigate = useNavigate();
  
const handleInsertCVClick = () => {
    navigate('/cv-upload');
  };

    return (
        <div className={styles.cvListPage}>
    <div className={styles.topSection}>
      <button className={styles.uploadButton} onClick={handleInsertCVClick} >Add CVS</button>
    </div>
    
    <div className={styles.cvList}>
      {cvs.length > 0 ? (
        cvs.map((cv, index) => (
          <CvCard key={index} cv={cv} />
        ))
      ) : (
        <p>No CVs found.</p>
      )}

    </div>




    </div>

    )
    
}

export default CVList;
