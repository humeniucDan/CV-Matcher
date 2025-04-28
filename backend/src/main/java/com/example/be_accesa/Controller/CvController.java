package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Model.CvHash;
import com.example.be_accesa.Model.JobHash;
import com.example.be_accesa.Service.*;
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
import java.util.*;

@RestController
@RequestMapping("/cv")
public class CvController {
    Logger logger = LoggerFactory.getLogger(CvController.class);
    private final FilebaseService filebaseService;
    private final RedisService redisService;
    private final CvHashService cvHashService;
    private final ObjectMapper objectMapper;
    private final PGService pgService;

    @Autowired
    public CvController(FilebaseService filebaseService,
                        RedisService redisService,
                        CvHashService cvHashService,
                        ObjectMapper objectMapper,
                        PGService pgService) {
        this.filebaseService = filebaseService;
        this.redisService = redisService;
        this.cvHashService = cvHashService;
        this.objectMapper = objectMapper;
        this.pgService = pgService;
    }

    @PostMapping("/upload-cv-batch")
    public ResponseEntity<Object> uploadBatch(@RequestParam("files") MultipartFile[] files) {
        Map<String, String> map = new HashMap<>();

        for (MultipartFile file : files) {
            String cvHash = FileHasher.hashMultipartFile(file);

            if (cvHash == null) {
                return ResponseEntity.badRequest().body("Error hashing cv " + file.getOriginalFilename());
            }

            CvHash newCvHash;

            try {
                newCvHash = cvHashService.save(cvHash);
            } catch (Exception e) {
                // TODO: handle multiple different exceptions
                continue;
            }

            String fileHashed = newCvHash.getId().toString() + ".docx";
            String cvId = "cv-raw/" + fileHashed;

            if (!filebaseService.uploadFile(cvId, file)) {
                continue;
            }

            if (!redisService.enqueueCvId(fileHashed)) {
                filebaseService.deleteFile(cvId);
                continue;
            }

            map.put(file.getOriginalFilename(), cvId);
        }

        return ResponseEntity.ok(map);
    }

    @GetMapping("get-all-cvs")
    public ResponseEntity<List<Map<String, Object>>> getAllCvs() {
        List<Map<String, Object>> result = new ArrayList<>();
        List<Object[]> cvs = filebaseService.getFolder("cv-processed/");  // 0 - content, 1 - key

        for(Object[] cv : cvs) {

            String cvJsonString = new String((byte[]) cv[0], StandardCharsets.UTF_8);

            try {
                Map<String, Object> cvJsonMapped = objectMapper.readValue(cvJsonString, Map.class);
                cvJsonMapped.put("id", cv[1]);
                result.add(cvJsonMapped);
            } catch (JsonProcessingException e) {
                // TODO : handle different multiple exceptions
            }
        }

        return ResponseEntity.ok(result);
    }

    @GetMapping("get-cv-top")
    public ResponseEntity<Object> getJobSimilarity(@RequestParam("cvId") Long cvId, @RequestParam("limit") int limit) {
        List<Map<String, Object>> jobList = new ArrayList<>();
        Map<String, Double> topJobList = pgService.getTopJobForCvId(cvId);

        List<Map.Entry<String, Double>> sortedJobs = new ArrayList<>(topJobList.entrySet());

        sortedJobs.sort((e1, e2) -> {
            Double v1 = e1.getValue();
            Double v2 = e2.getValue();
            return v2.compareTo(v1);
        });

        List<String> jobIdList = sortedJobs.stream()
                .limit(limit)
                .map(Map.Entry::getKey)
                .toList();

        for(String job : jobIdList) {
            String jobId = "job-processed/" + job + ".json";

            byte[] jobJsonBytes = filebaseService.getFile(jobId);

            if(jobJsonBytes == null) {
                continue;
            }

            String jobJsonString = new String(jobJsonBytes, StandardCharsets.UTF_8);

            try {
                Map<String, Object> jobJsonMapped = objectMapper.readValue(jobJsonString, Map.class);

                String similarity = String.format("%.2f", topJobList.get(job) * 100);

                jobJsonMapped.put("Similarity", similarity);

                jobList.add(jobJsonMapped);
            } catch (JsonProcessingException e) {
                // TODO : handle different multiple exceptions
            }
        }

        return ResponseEntity.ok(jobList);
    }
}
