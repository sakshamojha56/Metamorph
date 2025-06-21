// Main JavaScript for the document upload and metadata display

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = uploadProgress.querySelector('.progress-bar');
    const resultsSection = document.getElementById('resultsSection');
    const downloadBtn = document.getElementById('downloadBtn');
    const newUploadBtn = document.getElementById('newUploadBtn');
    
    // Current metadata
    let currentMetadata = null;
    
    // Setup event listeners
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleFileDrop);
    fileInput.addEventListener('change', handleFileSelect);
    downloadBtn.addEventListener('click', downloadMetadata);
    newUploadBtn.addEventListener('click', resetUpload);
    
    // Handle drag events
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('bg-light');
    }
    
    function handleFileDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('bg-light');
        
        if (e.dataTransfer.files.length) {
            uploadFile(e.dataTransfer.files[0]);
        }
    }
    
    function handleFileSelect(e) {
        if (fileInput.files.length) {
            uploadFile(fileInput.files[0]);
        }
    }
    
    // Upload file and process
    function uploadFile(file) {
        // Check file type
        const validTypes = [
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword',
            'text/plain',
            'image/png',
            'image/jpeg'
        ];
        
        if (!validTypes.includes(file.type)) {
            alert('Invalid file type. Please upload PDF, DOCX, DOC, TXT, PNG, or JPG files.');
            return;
        }
        
        // Show progress
        uploadProgress.classList.remove('d-none');
        progressBar.style.width = '0%';
        resultsSection.classList.add('d-none');
        
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        
        // Simulate progress (actual progress would require server-side events)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 5;
            if (progress <= 90) {
                progressBar.style.width = progress + '%';
                progressBar.setAttribute('aria-valuenow', progress);
            }
        }, 100);
        
        // Send to server
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            clearInterval(progressInterval);
            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }
            progressBar.style.width = '100%';
            progressBar.setAttribute('aria-valuenow', 100);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                currentMetadata = data.metadata;
                displayMetadata(data.metadata, data.original_filename);
                resultsSection.classList.remove('d-none');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            clearInterval(progressInterval);
            alert('Error uploading file: ' + error.message);
            progressBar.classList.remove('bg-success');
            progressBar.classList.add('bg-danger');
        });
    }
    
    // Display metadata in the UI
    function displayMetadata(metadata, filename) {
        // Set document info
        document.getElementById('documentTitle').textContent = metadata.title || filename;
        document.getElementById('filename').textContent = metadata.filename;
        document.getElementById('wordCount').textContent = metadata.word_count.toLocaleString();
        document.getElementById('processingDate').textContent = metadata.processing_date;
        
        // Set language and readability
        document.getElementById('language').textContent = metadata.language;
        document.getElementById('readabilityScore').textContent = Math.round(metadata.readability_score);
        
        const readabilityBar = document.getElementById('readabilityBar');
        readabilityBar.style.width = metadata.readability_score + '%';
        
        // Color the readability bar based on score
        readabilityBar.className = 'progress-bar';
        if (metadata.readability_score < 30) {
            readabilityBar.classList.add('bg-success');
        } else if (metadata.readability_score < 70) {
            readabilityBar.classList.add('bg-warning');
        } else {
            readabilityBar.classList.add('bg-danger');
        }
        
        // Set summary
        document.getElementById('summary').textContent = metadata.summary;
        
        // Display keywords
        const keywordsContainer = document.getElementById('keywordsContainer');
        keywordsContainer.innerHTML = '';
        
        metadata.keywords.forEach(keyword => {
            const keywordEl = document.createElement('span');
            keywordEl.className = 'keyword-tag';
            keywordEl.textContent = keyword.text;
            keywordEl.style.opacity = Math.max(0.5, keyword.score);
            keywordsContainer.appendChild(keywordEl);
        });
        
        // Display entities
        const entitiesContainer = document.getElementById('entitiesContainer');
        entitiesContainer.innerHTML = '';
        
        for (const [entityType, entities] of Object.entries(metadata.entities)) {
            if (entities.length === 0) continue;
            
            const colDiv = document.createElement('div');
            colDiv.className = 'col-md-4 mb-3';
            
            const entityGroup = document.createElement('div');
            entityGroup.className = 'entity-group';
            
            const entityTitle = document.createElement('h6');
            entityTitle.textContent = entityType;
            entityGroup.appendChild(entityTitle);
            
            entities.forEach(entity => {
                const entityItem = document.createElement('span');
                entityItem.className = 'entity-item';
                entityItem.textContent = entity;
                entityGroup.appendChild(entityItem);
            });
            
            colDiv.appendChild(entityGroup);
            entitiesContainer.appendChild(colDiv);
        }
    }
    
    // Download metadata as JSON
    function downloadMetadata() {
        if (!currentMetadata) return;
        
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentMetadata, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "metadata_" + currentMetadata.filename + ".json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }
    
    // Reset the upload form
    function resetUpload() {
        fileInput.value = '';
        uploadProgress.classList.add('d-none');
        resultsSection.classList.add('d-none');
        progressBar.style.width = '0%';
        progressBar.setAttribute('aria-valuenow', 0);
        progressBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-success';
        currentMetadata = null;
    }
});
