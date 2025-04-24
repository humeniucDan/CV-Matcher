import React from 'react';
import styles from './JobCard.module.css';

const JobCard = ({ job }) => {
  return (
    <div className={styles.card}>
      <div className= {styles.companyRow}>
        <h3 className = {styles.company}>{job.company}</h3>
      </div>
      <div className={styles.topRow}>
        <h2 className={styles.position}>{job.position}</h2>
        <div className={styles.tags}>
          {job.tags.map((tag) => (
            <span key={tag} className={styles.tag}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className={styles.bottomRow}>
        <div className={styles.meta}>
          <span>{job.postedAt}</span>
          <span>•</span>
          <span>{job.contract}</span>
          <span>•</span>
          <span className={styles.location}>{job.location}</span>
        </div>

        <div className={styles.buttons}>
          <button className={styles.btnPrimary}>Check candidate list</button>
          <button className={styles.btnDanger}>Remove Job</button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
