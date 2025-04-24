import React, { useState, useRef } from 'react';
import styles from './CVUpload.module.css'

const CVUpload = () => {
    const [files, setFiles] = useState([]);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef();
  
    const handleDrop = (e) => {
      e.preventDefault();
      setDragActive(false);
      const droppedFiles = Array.from(e.dataTransfer.files);
      setFiles((prev) => [...prev, ...droppedFiles]);
    };
  
    const handleDragOver = (e) => {
      e.preventDefault();
      setDragActive(true);
    };
  
    const handleDragLeave = () => {
      setDragActive(false);
    };
  
    const handleFileChange = (e) => {
      const selectedFiles = Array.from(e.target.files);
      setFiles((prev) => [...prev, ...selectedFiles]);
    };
  
    const removeFile = (indexToRemove) => {
      setFiles((prev) => prev.filter((_, i) => i !== indexToRemove));
    };
  
    const handleUpload = async () => {
      if (files.length === 0) return;
  
      const formData = new FormData();
      files.forEach((file) => formData.append('files', file));
  
      try {
        const response = await fetch('http://your-backend-endpoint.com/upload', {
          method: 'POST',
          body: formData,
        });
  
        if (response.ok) {
          alert('Files uploaded successfully!');
          setFiles([]);
        } else {
          alert('Upload failed');
        }
      } catch (err) {
        console.error('Upload error:', err);
        alert('Something went wrong!');
      }
    };
  
    return (
      <div className={styles.fullPage}>
        <div
          className={`${styles.dropZone} ${dragActive ? styles.activeDropZone : ''}`}
          onDragOver={handleDragOver}
          onDragEnter={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className={styles.hiddenInput}
            onChange={handleFileChange}
          />
          <p className={styles.dropText}>
            Drag and drop files here, or <span>click to select</span>
          </p>
        </div>
  
        {files.length > 0 && (
          <div className={styles.fileList}>
            <h4>Selected files</h4>
            <ul>
              {files.map((file, index) => (
                <li key={index} className={styles.fileItem}>
                  <span>{file.name}</span>
                  <button className={styles.removeButton} onClick={() => removeFile(index)}>
                    &times;
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
  
        <button className={styles.submitButton} onClick={handleUpload} disabled={files.length === 0}>
          Submit
        </button>
      </div>
    );
  };

  export default CVUpload;