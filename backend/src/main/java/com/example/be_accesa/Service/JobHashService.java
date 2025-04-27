package com.example.be_accesa.Service;

import com.example.be_accesa.Model.JobHash;
import com.example.be_accesa.Repository.IJobHashRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class JobHashService {
    private final IJobHashRepo jobRepo;

    @Autowired
    public JobHashService(IJobHashRepo jobRepo){
        this.jobRepo = jobRepo;
    }

    public JobHash save(String fileHash){
        return jobRepo.save(new JobHash(fileHash));
    }
}
