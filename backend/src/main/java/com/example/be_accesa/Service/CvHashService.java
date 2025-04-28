package com.example.be_accesa.Service;

import com.example.be_accesa.Model.CvHash;
import com.example.be_accesa.Repository.ICvHashRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CvHashService {
    private final ICvHashRepo cvRepo;

    @Autowired
    public CvHashService(ICvHashRepo cvRepo){
        this.cvRepo = cvRepo;
    }

    public CvHash save(String fileHash){
        return cvRepo.save(new CvHash(fileHash));
    }

    public void deleteById(Long id) {
        cvRepo.deleteById(id);
    }
}
