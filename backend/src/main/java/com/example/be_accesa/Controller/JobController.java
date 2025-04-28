package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Model.JobHash;
import com.example.be_accesa.Service.FilebaseService;
import com.example.be_accesa.Service.JobHashService;
import com.example.be_accesa.Service.PGService;
import com.example.be_accesa.Service.RedisService;
import com.example.be_accesa.Utils.FileHasher;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/job")
public class JobController {
    Logger logger = LoggerFactory.getLogger(CvController.class);
    private final JobHashService jobHashService;
    private final FilebaseService filebaseService;
    private final RedisService redisService;
    private final PGService pgService;
    private final ObjectMapper objectMapper;

    @Autowired
    public JobController(JobHashService jobHashService,
                         FilebaseService filebaseService,
                         RedisService redisService,
                         PGService pgService,
                         ObjectMapper objectMapper) {
        this.jobHashService = jobHashService;
        this.filebaseService = filebaseService;
        this.redisService = redisService;
        this.pgService = pgService;
        this.objectMapper = objectMapper;
    }

    @PostMapping("/upload-job-batch")
    public ResponseEntity<Object> addJobs(@RequestParam("files") List<MultipartFile> files) {
        Map<String, String> map = new HashMap<>();

        for(MultipartFile file : files) {
            String jobHash = FileHasher.hashMultipartFile(file);

            if(jobHash == null){
                continue;
            }

            JobHash newJobHash;

            try{
                newJobHash = jobHashService.save(jobHash);
            } catch (Exception e){
                // TODO: handle multiple different exceptions
                continue;
            }

            String fileHashed = newJobHash.getId().toString() + ".docx";
            String jobId = "job-raw/" + fileHashed;

            if(!filebaseService.uploadFile(jobId, file)) {
                jobHashService.deleteById(newJobHash.getId());
                continue;
            }

            if(!redisService.enqueueJobId(fileHashed)) {
                filebaseService.deleteFile(jobId);
            }

            map.put(file.getOriginalFilename(), jobId);
        }

        return ResponseEntity.ok(map);
    }

    @GetMapping("/get-job-top")
    public ResponseEntity<Object> getJobTopCv(@RequestParam("jobId") Long jobId, @RequestParam("limit") int limit) {
        List<Map<String, Object>> cvList = new ArrayList<>();
        List<CvSimilarityDTO> topCvList = pgService.getTopCvForJobId(jobId, limit);

        for(CvSimilarityDTO cv : topCvList) {
            String cvId = "cv-processed/" + cv.getId() + ".json";

            byte[] cvJsonBytes = filebaseService.getFile(cvId);

            if(cvJsonBytes == null) {
                continue;
            }

            String cvJsonString = new String(cvJsonBytes, StandardCharsets.UTF_8);

            try {
                Map<String, Object> cvJsonMapped = objectMapper.readValue(cvJsonString, Map.class);

                String similarity = String.format("%.2f", cv.getSimilarity() * 100);

                cvJsonMapped.put("Similarity", similarity);

                cvList.add(cvJsonMapped);
            } catch (JsonProcessingException e) {
                // TODO : handle different multiple exceptions
            }
        }

        return ResponseEntity.ok(cvList);
    }

    @GetMapping("get-all-jobs")
    public ResponseEntity<List<Map<String, Object>>> getAllJobs() {
        List<Map<String, Object>> result = new ArrayList<>();
        List<Object[]> jobs = filebaseService.getFolder("job-processed/");  // 0 - content, 1 - key

        for(Object[] job : jobs) {

            String jobJsonString = new String((byte[]) job[0], StandardCharsets.UTF_8);

            try {
                Map<String, Object> jobJsonMapped = objectMapper.readValue(jobJsonString, Map.class);
                jobJsonMapped.put("id", job[1]);
                result.add(jobJsonMapped);
            } catch (JsonProcessingException e) {
                // TODO : handle different multiple exceptions
            }
        }

        return ResponseEntity.ok(result);
    }

    @DeleteMapping("delete-job")
    public ResponseEntity<?> deleteJob(@RequestParam("jobId") Long jobId) {
        String jobRawId = "job-raw/" + jobId + ".docx";
        String jobProcessedId = "job-processed/" + jobId + ".json";

        if(!filebaseService.deleteFile(jobRawId)) {
            return ResponseEntity.badRequest().body("Error deleting raw job " + jobId);
        }

        if(!filebaseService.deleteFile(jobProcessedId)) {
            return ResponseEntity.badRequest().body("Error deleting processed job " + jobId);
        }

        pgService.dropJobIdColumn(jobId);
        pgService.deleteJobEmbeddingsRowById(jobId);
        pgService.deleteJobHashRowById(jobId);

        return ResponseEntity.ok("Deleted successfully " + jobId);
    }
}
