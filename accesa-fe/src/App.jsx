import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SplitScreen from './pages/splitscreen/Splitscreen';
import CVUpload from './pages/uploadCvs/CVUpload';
import JobCard from './components/jobCard/JobCard';
import JobList from './pages/jobsSearch/JobList';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SplitScreen />} />
        <Route path="/cv-upload" element={<CVUpload />} />
        <Route path = "/view-jobs" element = {<JobList/>}/>
      </Routes>
    </Router>
  );
}

export default App;