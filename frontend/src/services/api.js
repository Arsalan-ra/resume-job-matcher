const API_BASE_URL = 'http://127.0.0.1:8000'

export async function fetchMatchScores(resumeText, jobDescription) {
  const response = await fetch(`${API_BASE_URL}/api/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}
