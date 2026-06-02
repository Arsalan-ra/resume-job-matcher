import { useState } from 'react'
import ScoreBar from './components/ScoreBar'
import { fetchMatchScores } from './services/api'

function App() {
  const [resumeText, setResumeText] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const canAnalyze = resumeText.trim() && jobDescription.trim() && !isLoading

  const handleAnalyze = async () => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const scores = await fetchMatchScores(resumeText, jobDescription)
      setResults(scores)
    } catch {
      setError('Could not reach the matching service. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <h1 className="text-3xl font-medium tracking-tight text-gray-900">
          Resume-Job Match Predictor
        </h1>
        <p className="mt-2 text-gray-500">
          Paste a resume and a job description to see how well they align.
        </p>

        <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Resume
            </label>
            <textarea
              value={resumeText}
              onChange={(event) => setResumeText(event.target.value)}
              placeholder="Paste resume text here..."
              className="h-72 w-full resize-none rounded-md border border-gray-200 p-4 text-sm text-gray-800 placeholder-gray-400 focus:border-gray-400 focus:outline-none"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              placeholder="Paste job description text here..."
              className="h-72 w-full resize-none rounded-md border border-gray-200 p-4 text-sm text-gray-800 placeholder-gray-400 focus:border-gray-400 focus:outline-none"
            />
          </div>
        </div>

        <div className="mt-8 flex justify-center">
          <button
            type="button"
            onClick={handleAnalyze}
            disabled={!canAnalyze}
            className="rounded-md border border-gray-300 px-6 py-2.5 text-sm font-medium text-gray-800 transition-colors hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {isLoading ? 'Analyzing...' : 'Analyze Match'}
          </button>
        </div>

        {error && (
          <p className="mt-6 text-center text-sm text-gray-500">{error}</p>
        )}

        {results && (
          <div className="mt-14 border-t border-gray-200 pt-10">
            <div className="text-center">
              <p className="text-sm text-gray-500">Overall Fit Score</p>
              <p className="mt-1 font-mono text-6xl font-medium text-gray-900">
                {Math.round(results.overall * 100)}%
              </p>
            </div>

            <div className="mx-auto mt-10 max-w-md space-y-6">
              <ScoreBar label="Skills" value={results.skills} />
              <ScoreBar label="Experience" value={results.experience} />
              <ScoreBar label="Education" value={results.education} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
