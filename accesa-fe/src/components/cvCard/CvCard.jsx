import React, { useState } from "react";
import styles from "./CvCard.module.css";

const CvCard = ({ cv }) => {
  const [showDetails, setShowDetails] = useState(false);


  const removeCV = async () => {
    const deleteCVUrl = new URL('http://localhost:8080/cv/delete-cv')
    deleteCVUrl.searchParams.append('cvId', cv.id)
    
    const response = await fetch(deleteCVUrl, {
      method : 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
    })

    if(response.ok) {
      deleteJob(cv.id)
    }
  }


  const toggleShowDetails = () => {
    setShowDetails(!showDetails);
  };

  return (
    <div className={styles.card}>
      <div className={styles.topRow}>
        <h2 className={styles.name}>{cv.Name}</h2>

        <div className={styles.shortInfo}>
          {cv["Technical Skills"]?.slice(0, 3).map((skill, index) => (
            <span key={index} className={styles.infoTag}>
              {skill}
            </span>
          ))}
          {cv["Foreign Languages"]?.slice(0, 2).map((lang, index) => (
            <span key={index} className={styles.infoTag}>
              {typeof lang === "object"
                ? `${Object.values(lang)[0]} (${Object.values(lang)[1]})`
                : `${lang} (Unknown)`}
            </span>
          ))}
        </div>

      </div>

      {showDetails && (
        <div className={styles.details}>
          {cv["Technical Skills"] && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Technical Skills</h3>
              <ul className={styles.itemList}>
                {cv["Technical Skills"].map((skill, index) => (
                  <li key={index} className={styles.item}>
                    {skill}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {cv["Foreign Languages"] && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Foreign Languages</h3>
              <ul className={styles.itemList}>
                {cv["Foreign Languages"].map((lang, index) => (
                  <li key={index} className={styles.item}>
                    {typeof lang === "object"
                      ? `${Object.values(lang)[0]} (${Object.values(lang)[1]})`
                      : `${lang} (Unknown)`}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {cv.Education && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Education</h3>
              <ul className={styles.itemList}>
                {cv.Education.map((edu, index) => (
                  <li key={index} className={styles.item}>
                    <strong>{edu["University Name"]}</strong> (
                    {edu["Program Duration"]}) — {edu["Degree Name"]}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {cv.Certifications && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Certifications</h3>
              <ul className={styles.itemList}>
                {cv.Certifications.map((cert, index) => (
                  <li key={index} className={styles.item}>
                    <strong>{cert.Title}</strong> — {cert["Issuing Authority"]}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {cv["Work Experience"] && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Work Experience</h3>
              <ul className={styles.itemList}>
                {cv["Work Experience"].map((work, index) => (
                  <li key={index} className={styles.item}>
                    {work}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {cv["Project Experience"] && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Project Experience</h3>
              {cv["Project Experience"].map((project, index) => (
                <div key={index} className={styles.projectCard}>
                  <h4>{project.Title}</h4>

                  <div>
                    <strong>Hidden Skills:</strong>
                    <ul className={styles.itemList}>
                      {project["Hidden Skills"].map((skill, idx) => (
                        <li key={idx} className={styles.item}>
                          {skill}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <strong>Technologies Used:</strong>
                    <ul className={styles.itemList}>
                      {project["Technologies Used"].map((tech, idx) => (
                        <li key={idx} className={styles.item}>
                          {tech}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      <div className={styles.buttons}>
              <button className={styles.btnPrimary} onClick={toggleShowDetails}>
                {showDetails ? 'Hide Details' : 'Show Details'}
              </button>
                <button className={styles.btnPrimary} >Check jobs list</button>
                <button className={styles.btnDanger} onClick={removeCV} >Remove candidate</button>
              </div>
    </div>
  );
};

export default CvCard;
