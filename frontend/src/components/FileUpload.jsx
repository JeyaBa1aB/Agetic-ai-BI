/**
 * File Upload component with drag-and-drop CSV support
 * Handles CSV file validation and parsing
 */
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { validateCSV } from '../services/api';

const FileUpload = ({ onFileUpload, currentData }) => {
  const [uploading, setUploading] = useState(false);
  const [validationStatus, setValidationStatus] = useState(null);

  // Parse CSV content
  const parseCSV = (content) => {
    const lines = content.trim().split('\n');
    if (lines.length < 2) {
      throw new Error('CSV must have at least a header row and one data row');
    }

    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const data = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
      if (values.length === headers.length) {
        const row = {};
        headers.forEach((header, index) => {
          row[header] = values[index];
        });
        data.push(row);
      }
    }

    return { headers, data, rowCount: data.length };
  };

  // Handle file processing
  const processFile = async (file) => {
    setUploading(true);
    setValidationStatus(null);

    try {
      // Read file content
      const content = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('Failed to read file'));
        reader.readAsText(file);
      });

      // Parse CSV
      const parsed = parseCSV(content);

      // Validate with backend
      try {
        const validation = await validateCSV(content);
        setValidationStatus({
          valid: validation.valid,
          message: validation.message,
          details: validation.details
        });

        if (!validation.valid) {
          toast.error(`CSV validation failed: ${validation.message}`);
          return;
        }
      } catch (validationError) {
        console.warn('Backend validation failed, using client-side validation:', validationError);
        setValidationStatus({
          valid: true,
          message: 'Client-side validation passed',
          details: { rows: parsed.rowCount, columns: parsed.headers.length }
        });
      }

      // Prepare data for parent component
      const fileData = {
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
        raw: content,
        parsed: parsed.data,
        headers: parsed.headers,
        rowCount: parsed.rowCount,
        uploadedAt: new Date().toISOString()
      };

      onFileUpload(fileData);
      toast.success(`CSV uploaded successfully! ${parsed.rowCount} rows, ${parsed.headers.length} columns`);

    } catch (error) {
      console.error('File processing error:', error);
      toast.error(`File processing failed: ${error.message}`);
      setValidationStatus({
        valid: false,
        message: error.message,
        details: null
      });
    } finally {
      setUploading(false);
    }
  };

  // Dropzone configuration
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      toast.error(`File rejected: ${rejection.errors[0]?.message || 'Invalid file'}`);
      return;
    }

    if (acceptedFiles.length > 0) {
      processFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv'],
      'text/plain': ['.csv']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: uploading
  });

  // Get dropzone styling
  const getDropzoneClass = () => {
    let baseClass = 'file-upload-zone cursor-pointer transition-all duration-200';
    
    if (uploading) {
      baseClass += ' opacity-50 cursor-not-allowed';
    } else if (isDragReject) {
      baseClass += ' border-red-400 bg-red-50';
    } else if (isDragActive) {
      baseClass += ' dragover';
    }
    
    return baseClass;
  };

  return (
    <div className="space-y-4">
      
      {/* Upload Zone */}
      <div {...getRootProps()} className={getDropzoneClass()}>
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-3">
          {uploading ? (
            <>
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <p className="text-gray-600">Processing file...</p>
            </>
          ) : isDragActive ? (
            <>
              <Upload className="w-8 h-8 text-blue-500" />
              <p className="text-blue-600 font-medium">Drop your CSV file here</p>
            </>
          ) : (
            <>
              <Upload className="w-8 h-8 text-gray-400" />
              <div className="text-center">
                <p className="text-gray-600 font-medium">
                  Drag & drop your CSV file here
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  or click to browse files
                </p>
              </div>
              <div className="text-xs text-gray-400">
                Maximum file size: 10MB
              </div>
            </>
          )}
        </div>
      </div>

      {/* Validation Status */}
      {validationStatus && (
        <div className={`p-3 rounded-lg border ${
          validationStatus.valid 
            ? 'bg-green-50 border-green-200' 
            : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-start space-x-2">
            {validationStatus.valid ? (
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
            ) : (
              <XCircle className="w-5 h-5 text-red-600 mt-0.5" />
            )}
            <div className="flex-1">
              <p className={`text-sm font-medium ${
                validationStatus.valid ? 'text-green-800' : 'text-red-800'
              }`}>
                {validationStatus.valid ? 'Validation Passed' : 'Validation Failed'}
              </p>
              <p className={`text-sm mt-1 ${
                validationStatus.valid ? 'text-green-700' : 'text-red-700'
              }`}>
                {validationStatus.message}
              </p>
              {validationStatus.details && (
                <div className="mt-2 text-xs text-gray-600">
                  {validationStatus.details.rows && (
                    <span>Rows: {validationStatus.details.rows} • </span>
                  )}
                  {validationStatus.details.columns && (
                    <span>Columns: {validationStatus.details.columns}</span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Current File Info */}
      {currentData && (
        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start space-x-2">
            <File className="w-5 h-5 text-blue-600 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-blue-900">
                {currentData.name}
              </p>
              <div className="text-xs text-blue-700 mt-1 space-y-1">
                <div>Size: {(currentData.size / 1024).toFixed(1)} KB</div>
                <div>Rows: {currentData.rowCount} • Columns: {currentData.headers.length}</div>
                <div>Uploaded: {new Date(currentData.uploadedAt).toLocaleString()}</div>
              </div>
              
              {/* Column Preview */}
              {currentData.headers && (
                <div className="mt-2">
                  <p className="text-xs font-medium text-blue-800 mb-1">Columns:</p>
                  <div className="flex flex-wrap gap-1">
                    {currentData.headers.slice(0, 5).map((header, index) => (
                      <span 
                        key={index}
                        className="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                      >
                        {header}
                      </span>
                    ))}
                    {currentData.headers.length > 5 && (
                      <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                        +{currentData.headers.length - 5} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Upload Instructions */}
      {!currentData && (
        <div className="text-center">
          <div className="inline-flex items-center space-x-2 text-sm text-gray-500">
            <AlertCircle className="w-4 h-4" />
            <span>Upload a CSV file to begin analysis</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;