import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE,
});

/**
 * Submits JDs and batch resumes for processing.
 * Accepts files as a list of File objects, jdText as string, and alpha as float.
 */
export const rankResumes = async (files, jdText, alpha) => {
  const formData = new FormData();
  formData.append('jd_text', jdText);
  if (alpha !== undefined && alpha !== null) {
    formData.append('alpha', alpha);
  }
  
  files.forEach((file) => {
    formData.append('files[]', file);
  });

  const response = await client.post('/rank', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

/**
 * Retrieves past ranking results for a given session.
 */
export const getResults = async (sessionId) => {
  const response = await client.get(`/results/${sessionId}`);
  return response.data;
};

/**
 * Downloads session results as a CSV file.
 */
export const exportCSV = async (sessionId) => {
  const response = await client.get(`/export/${sessionId}`, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `results_${sessionId}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
