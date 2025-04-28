import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SplitScreen from './pages/splitscreen/Splitscreen';
import CVUpload from './pages/uploadCvs/CVUpload';
import JobList from './pages/jobsSearch/JobList';
import RankingList from './pages/rankingList/rankingList';
import JobUpload from './pages/uploadJobs/JobUpload';
import CVList from './pages/cvsPage/CVList';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SplitScreen />} />
        <Route path="/cv-upload" element={<CVUpload />} />
        <Route path="/view-jobs" element={<JobList/>}/>
        <Route path="/view-jobs/ranking" element={<RankingList/>}/> 
        <Route path="/job-upload" element={<JobUpload/>}/>
        <Route path = "/view-cvs" element = {<CVList/>}/>
      </Routes>
    </Router>
  );
}

export default App;