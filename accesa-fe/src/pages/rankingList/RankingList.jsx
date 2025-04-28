import React, { useEffect, useState } from "react";
import styles from "./RankingList.module.css";
import CvCard from "../../components/cvCard/CvCard";
import { useLocation } from "react-router-dom";

const RankingList = () => {
  const location = useLocation();
  const { currJob } = location.state || {};

  const [cvList, setCvList] = useState([]);

  useEffect(() => {
    const fetchJobRanking = async () => {
      if (!currJob) {
        return;
      }

      try {
        const getRankingUrl = new URL("http://localhost:8080/job/get-job-top");
        getRankingUrl.searchParams.append("jobId", currJob.id);
        getRankingUrl.searchParams.append("limit", 100);

        const response = await fetch(getRankingUrl);

        if (response.ok) {
          const data = await response.json();
          setCvList(data);
        }
      } catch (err) {
        console.error("Error fetching jobs:", err);
      }
    };

    fetchJobRanking();
  }, []);

  return (
    <div className={styles.container}>
      <h1 className={styles.jobTitle}>{currJob.Role}</h1>

      <div className={styles.cvList}>
        {cvList.map((cv, index) => (
          <div key={index} className={styles.cvItem}>
            <div className={styles.index}>{index + 1}.</div>
            <CvCard cv={cv} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default RankingList;
