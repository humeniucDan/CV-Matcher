package com.example.be_accesa.Repository;

import com.example.be_accesa.Model.JobHash;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface IJobHashRepo extends JpaRepository<JobHash, Long> {
}
