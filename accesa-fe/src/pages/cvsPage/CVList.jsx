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
            setCVs(data);
          } catch (err) {
            console.error("Error fetching CVs:", err);
          }
        };
        
        fetchCVs();
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
