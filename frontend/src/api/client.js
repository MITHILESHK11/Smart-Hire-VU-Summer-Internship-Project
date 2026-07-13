const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Uploads resumes and job description to the ranking endpoint.
 * @param {File[]} resumes - Array of PDF/DOCX Files.
 * @param {string} jobDescription - Job description text.
 * @param {number} alpha - Scoring weight (0.0 to 1.0).
 * @returns {Promise<object>} Response containing sessionId and candidate list.
 */
export async function rankResumes(resumes, jobDescription, alpha = 0.4) {
  const formData = new FormData();
  
  resumes.forEach((file) => {
    formData.append('resumes', file);
  });
  formData.append('job_description', jobDescription);
  formData.append('alpha', alpha.toString());

  const response = await fetch(`${API_BASE_URL}/api/rank`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze and rank resumes.');
  }

  return response.json();
}

/**
 * Fetches the ranked candidates for a specific session.
 * Optionally allows passing a new alpha to trigger dynamic re-ranking.
 * @param {string} sessionId - UUID of the session.
 * @param {number} [alpha] - Optional new alpha value.
 * @returns {Promise<object>} Response containing updated session and candidates.
 */
export async function getResults(sessionId, alpha) {
  let url = `${API_BASE_URL}/api/results/${sessionId}`;
  if (alpha !== undefined) {
    url += `?alpha=${alpha}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to load results.');
  }

  return response.json();
}

/**
 * Returns the absolute URL to trigger the CSV export download.
 * @param {string} sessionId - UUID of the session.
 * @returns {string} Absolute URL path.
 */
export function getExportUrl(sessionId) {
  return `${API_BASE_URL}/api/export/${sessionId}`;
}
