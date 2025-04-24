import React, { useEffect, useState } from 'react';
import JobCard from '../../components/jobCard/JobCard';
import SearchBar from '../../components/searchBar/Searchbar';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/jobs');
        const data = await response.json();
        setJobs(data);
        setFilteredJobs(data);
      } catch (err) {
        console.error('Error fetching jobs:', err);
      }
    };

    fetchJobs();
  }, []);

  const handleSearch = (term) => {
    setSearchTerm(term);

    const filtered = jobs.filter(
      (job) =>
        job.position.toLowerCase().includes(term.toLowerCase()) ||
        job.company.toLowerCase().includes(term.toLowerCase())
    );

    setFilteredJobs(filtered);
  };

  return (
    <div>
      <SearchBar value={searchTerm} onChange={handleSearch} />

      {filteredJobs.length > 0 ? (
        filteredJobs.map((job) => <JobCard key={job.id} job={job} />)
      ) : (
        <p>No jobs match your search.</p>
      )}
    </div>
  );
};

export default JobList;