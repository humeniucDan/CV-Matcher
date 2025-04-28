import React, { useState } from 'react';
import styles from './JobCard.module.css';
import { useNavigate } from 'react-router-dom';

const JobCard = ({ job, deleteJob }) => {
  const navigate = useNavigate();

  const [showDetails, setShowDetails] = useState(false);

  const checkCandidateList = async () => {
    navigate("/view-jobs/ranking", { state : { currJob : job }})
  }

  const removeJob = async () => {
    const deleteJobUrl = new URL('http://localhost:8080/job/delete-job')
    deleteJobUrl.searchParams.append('jobId', job.id)
    
    const response = await fetch(deleteJobUrl, {
      method : 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
    })

    if(response.ok) {
      deleteJob(job.id)
    }
  }

  const toggleDetails = () => {
    setShowDetails(!showDetails);
  };

  return (
    <div className={styles.card}>
      <div className={styles.companyRow}>
        <h3 className={styles.company}>{job.Company}</h3>
      </div>
      <div className={styles.topRow}>
        <h2 className={styles.position}>{job.Role}</h2>
        
      </div>

      <div className={styles.bottomRow}>
        <div className={styles.meta}>
          <span>{job.Type}</span>
        </div>

        

        {showDetails && (
          <>
            <div className={styles.meta}>
              <h4 className={styles.meta}>Responsibilities:</h4>
              <ul>
                {job.Responsibilities.map((responsibility, index) => (
                  <li key={index} className={styles.listItem}>
                    {responsibility}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Required Qualifications:</h4>
              <ul>
                {job.Required.map((requirement, index) => (
                  <li key={index} className={styles.listItem}>
                    {requirement}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Benefits:</h4>
              <ul>
                {job.Benefits.map((benefit, index) => (
                  <li key={index} className={styles.listItem}>
                    {benefit}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Skills:</h4>
              <ul>
                {Object.keys(job.Skills).map((skillCategory) => (
                  <li key={skillCategory}>
                    <strong>{skillCategory}:</strong>
                    <ul>
                      {job.Skills[skillCategory].map((skill, index) => (
                        <li key={index}>{skill}</li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}

        <div className={styles.buttons}>
        <button className={styles.btnPrimary} onClick={toggleDetails}>
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>
          <button className={styles.btnPrimary} onClick={checkCandidateList}>Check candidate list</button>
          <button className={styles.btnDanger} onClick={removeJob}>Remove Job</button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
