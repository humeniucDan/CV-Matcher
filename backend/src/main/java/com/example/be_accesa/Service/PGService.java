package com.example.be_accesa.Service;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Model.JobEmbedding;
import com.example.be_accesa.Repository.JobEmbeddingsRepo;
import com.example.be_accesa.Repository.JobHashRepo;
import com.example.be_accesa.Repository.SimMatrixRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class PGService {
    private final SimMatrixRepo simMatrixRepo;
    private final JobEmbeddingsRepo jobEmbeddingsRepo;
    private final JobHashRepo jobHashRepo;
    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public PGService(SimMatrixRepo simMatrixRepo,
                     JobEmbeddingsRepo jobEmbeddingsRepo,
                     JobHashRepo jobHashRepo,
                     JdbcTemplate jdbcTemplate) {
        this.simMatrixRepo = simMatrixRepo;
        this.jobEmbeddingsRepo = jobEmbeddingsRepo;
        this.jobHashRepo = jobHashRepo;
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<CvSimilarityDTO> getTopCvForJobId(Long jobId, int limit) {
        return simMatrixRepo.getTopCvForJobId(jobId, limit);
    }

    public void dropJobIdColumn(Long jobId) {
        simMatrixRepo.dropJobIdColumn(jobId);
    }

    public void deleteJobEmbeddingsRowById(Long jobId) {
        jobEmbeddingsRepo.deleteById(jobId);
    }

    public void deleteJobHashRowById(Long jobId) {
        jobHashRepo.deleteById(jobId);
    }

    public Map<String, Double> getTopJobForCvId(Long cvId) {
        String sqlQuery = "SELECT * FROM sim_matrix where id = ?";

        Map<String, Object> result = jdbcTemplate.queryForMap(sqlQuery, cvId);
        result.remove("id");

        Map<String, Double> doubleResult = new HashMap<>();
        for(Map.Entry<String, Object> entry : result.entrySet()) {
            if(entry.getValue() != null) {
                doubleResult.put(entry.getKey(), Double.valueOf(entry.getValue().toString()));
            }
        }

        return doubleResult;
    }
}
