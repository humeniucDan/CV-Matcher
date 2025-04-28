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

    @Autowired
    public CvController(FilebaseService filebaseService,
                        RedisService redisService,
                        CvHashService cvHashService) {
        this.filebaseService = filebaseService;
        this.redisService = redisService;
        this.cvHashService = cvHashService;
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
}
