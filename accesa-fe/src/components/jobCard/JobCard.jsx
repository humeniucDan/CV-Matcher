import React, { useState } from 'react';
import styles from './JobCard.module.css';

const JobCard = ({ job, deleteJob }) => {
  const [showDetails, setShowDetails] = useState(false);

  const checkCandidateList = async () => {
    try {
      const getRankingUrl = new URL('http://localhost:8080/job/get-job-top')
      getRankingUrl.searchParams.append('jobId', job.id)
      getRankingUrl.searchParams.append('limit', 100)

      const response = await fetch(getRankingUrl);

      if(response.ok) {
        const data = await response.json()
        console.log(data)
        //TODO : cv urile vin in ordinea buna, primul fiind cel mai corelat de job, acum doar trebuie creat un CV folosind datele din json si afisata o lista cu CV-uri
      }
      
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
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

        <button className={styles.btnPrimary} onClick={toggleDetails}>
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>

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
          <button className={styles.btnPrimary} onClick={checkCandidateList}>Check candidate list</button>
          <button className={styles.btnDanger} onClick={removeJob}>Remove Job</button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
