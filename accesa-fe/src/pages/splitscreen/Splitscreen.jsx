import React , { useState } from 'react';
import styles from './SplitScreen.module.css';
import leftImage from '../../assets/cvs-img.jpg';
import rightImage from '../../assets/jobs-img.jpg';
import logo from '../../assets/accesa-logo.png';
import { useNavigate } from 'react-router-dom';

const SplitScreen = () => {

  const [hovered, setHovered] = useState(null); 

  const containerClass = `${styles.container} ${
    hovered === 'left' ? styles.leftHover : hovered === 'right' ? styles.rightHover : ''
  }`;


  const navigate = useNavigate();

  const handleInsertCVClick = () => {
    navigate('/view-cvs');
  };

  const handleCheckJobsClick = () => {
    navigate('/view-jobs');
  };


  return (
    <div className={containerClass}>
      <div className={styles.panelLeft}  onMouseEnter={() => setHovered('left')} onMouseLeave={() => setHovered(null)}>
        <img src={leftImage} alt="Left" className={styles.circularImage} />
        <button className={styles.button} onClick={handleInsertCVClick}>Check CV's</button>
      </div>

      <div className={styles.logoContainer}>
        <img src={logo} alt="Logo" className={styles.logo} />
      </div>

      <div className={styles.panelRight} onMouseEnter={() => setHovered('right')} onMouseLeave={() => setHovered(null)}>
        <img src={rightImage} alt="Right" className={styles.circularImage} />
        <button className={styles.button} onClick = {handleCheckJobsClick}>Check jobs</button>
      </div>
    </div>
  );
};

export default SplitScreen;