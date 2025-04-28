import React, { useEffect, useState } from "react";
import JobCard from "../../components/jobCard/JobCard";
import SearchBar from "../../components/searchBar/Searchbar";
import styles from "./JobList.module.css";
import { useNavigate } from 'react-router-dom';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("http://localhost:8080/job/get-all-jobs");
        const data = await response.json();
        setJobs(data);
      } catch (err) {
        console.error("Error fetching jobs:", err);
      }
    };

    fetchJobs();
  }, []);

  const deleteJob = (jobId) => {
    setJobs(prevJobs => prevJobs.filter(job => job.id !== jobId));
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const getFilteredJobs = () => {
    if (!searchTerm) {
      return jobs;
    }

    return jobs.filter(
      (job) =>
        job.Role.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.Company.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const filteredJobs = getFilteredJobs();

  const navigate = useNavigate();
  
  const handleInsertJobClick = () => {
    navigate('/job-upload');
  };

  return (
    <div className={styles.jobListPage}>
    <div className={styles.topSection}>
      <div className={styles.searchWrapper}>
        <SearchBar value={searchTerm} onChange={handleSearch} />
      </div>
      <button className={styles.uploadButton} onClick={handleInsertJobClick} >Add jobs</button>
    </div>

 
    
  
    <div className={styles.jobList}>
      {filteredJobs.length > 0 ? (
        filteredJobs.map((job) => (
          <JobCard key={job.id} job={job} deleteJob={deleteJob} />
        ))
      ) : (
        <p>No jobs found</p>
      )}
    </div>
  </div>
  
  );
};

export default JobList;
