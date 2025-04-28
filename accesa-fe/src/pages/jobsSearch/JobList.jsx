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

    const hardcodedJobs =  [{
      id: 1,  
      Type: "Senior",
      Role: "Tech Lead",
      Company: "Generic Tech Solutions",
      Responsibilities: [
        "Lead and manage a team of software developers, providing technical guidance.",
        "Oversee the design, development, and deployment of complex software solutions.",
        "Collaborate with cross-functional teams to define project requirements and deliverables.",
        "Ensure the technical feasibility of UI/UX designs and optimize applications for maximum speed and scalability.",
        "Conduct code reviews to maintain high-quality code standards and best practices.",
        "Identify and address technical risks and challenges, providing innovative solutions."
      ],
      Required: [
        "Bachelor’s degree in Computer Science, Engineering, or a related field.",
        "Minimum of 5 years of experience in software development with at least 2 years in a leadership role.",
        "Proficiency in programming languages such as Java, Python, or JavaScript.",
        "Strong understanding of software development methodologies like Agile and Scrum.",
        "Experience with cloud platforms such as AWS, Azure, or Google Cloud.",
        "Excellent problem-solving skills and attention to detail.",
        "Strong communication and interpersonal skills."
      ],
      Skills: {
        Cloud: ["AWS", "Azure", "Google Cloud"],
        Devops: ["Docker", "Jenkins", "Kubernetes"],
        Programming: ["Python", "Java", "JavaScript", "SQL", "NoSQL"]
      },
      Benefits: [
        "Competitive salary and performance-based bonuses.",
        "Comprehensive health, dental, and vision insurance.",
        "Generous paid time off and flexible work hours.",
        "Opportunities for professional development and career advancement.",
        "Collaborative and inclusive work environment.",
        "Access to cutting-edge technology and resources."
      ]
    }];

    setJobs(hardcodedJobs);
    //fetchJobs();
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
