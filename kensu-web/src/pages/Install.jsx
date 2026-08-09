import { useState } from 'react'
import StepCard from '../components/StepCard'
import VideoCard from '../components/VideoCard'

const steps = [
  {
    number: '01',
    title: 'Clone the repo',
    description: 'Grab the source and move into the project directory.',
    command: 'git clone https://github.com/HlibSamodin/Kensu.git\ncd Kensu',
    video: '/videos/clone.mp4',
    videoTitle: 'Cloning the repo',
    videoSubtitle: 'Get the code onto your machine',
  },
  {
    number: '02',
    title: 'Install dependencies',
    description: 'Kensu uses uv to manage the Python environment. This installs everything the pipeline needs.',
    command: 'uv sync',
    video: '/videos/install.mp4',
    videoTitle: 'Installing dependencies',
    videoSubtitle: 'One command, no manual venv setup',
  },
  {
    number: '03',
    title: 'Add your own OpenAI key',
    description: 'Kensu calls the OpenAI API using your own key, not mine. Nothing runs on our servers, so your usage and cost are entirely yours to control.',
    command: 'export OPENAI_API_KEY=your-key-here',
    video: '/videos/api-key.mp4',
    videoTitle: 'Setting your API key',
    videoSubtitle: 'Your key, your cost, your data',
  },
  {
    number: '04',
    title: 'Ask Kensu a question',
    description: 'The classifier is already trained and shipped with the repo, no training needed. Just ask a question and get a hallucination score back.',
    command: 'python ask.py "What is the capital of France?"',
    video: '/videos/run.mp4',
    videoTitle: 'Running Kensu',
    videoSubtitle: 'From a question to a hallucination score',
  },
]

function Install() {
  const [activeStep, setActiveStep] = useState(0)

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 sm:px-8 sm:py-16">
      <p className="font-bold text-xs text-orange-500 tracking-wide mb-3">Get started</p>
      <h1 className="font-extrabold text-3xl sm:text-4xl tracking-tight text-neutral-900 dark:text-neutral-100 mb-4">
        Run Kensu on your own machine
      </h1>
      <p className="text-neutral-500 dark:text-neutral-400 mb-10 sm:mb-12 max-w-xl">
        Kensu runs locally, using your own OpenAI API key. There's no hosted demo and nothing
        runs on my servers, so you're always in control of your own usage and cost.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
        <div className="space-y-6">
          {steps.map((step, i) => (
            <div key={step.number} onClick={() => setActiveStep(i)}>
              <StepCard {...step} active={i === activeStep} />
            </div>
          ))}
        </div>

        <div className="space-y-6">
          <VideoCard
            src={steps[activeStep].video}
            step={`STEP ${steps[activeStep].number}`}
            title={steps[activeStep].videoTitle}
            subtitle={steps[activeStep].videoSubtitle}
          />
          <div className="rounded-xl border border-neutral-200 dark:border-neutral-800 p-5">
            <p className="font-bold text-xs text-neutral-500 tracking-wide mb-3">Requirements</p>
            <ul className="space-y-1.5 text-sm text-neutral-600 dark:text-neutral-400">
              <li>• Python 3.14+</li>
              <li>• uv (for dependency management)</li>
              <li>• Your own OpenAI API key</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Install