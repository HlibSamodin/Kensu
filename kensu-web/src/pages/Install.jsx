import { useState } from 'react'
import StepCard from '../components/StepCard'
import VideoCard from '../components/VideoCard'

const steps = [
  {
    number: '01',
    title: 'Title',
    description: 'Description',
    command: 'cd xyz',
    video: '/videos/',
    videoTitle: 'Title of the video',
    videoSubtitle: 'Subtitle of the video',
  },
  {
    number: '02',
    title: 'Title',
    description: 'Description',
    command: 'cd xyz',
    video: '/videos/',
    videoTitle: 'Title of the video',
    videoSubtitle: 'Subtitle of the video',
  },
  {
    number: '03',
    title: 'Title',
    description: 'Description',
    command: 'cd xyz',
    video: '/videos/',
    videoTitle: 'Title of the video',
    videoSubtitle: 'Subtitle of the video',
  },
  {
    number: '04',
    title: 'Title',
    description: 'Description',
    command: 'cd xyz',
    video: '/videos/',
    videoTitle: 'Title of the video',
    videoSubtitle: 'Subtitle of the video',
  },
]

function Install() {
  const [activeStep, setActiveStep] = useState(0)

  return (
    <div className="max-w-5xl mx-auto px-8 py-16">
      <p className="font-bold text-xs text-orange-500 tracking-wide mb-3">Orange title here</p>
      <h1 className="font-extrabold text-4xl tracking-tight text-neutral-900 dark:text-neutral-100 mb-4">
        Text Here
      </h1>
      <p className="text-neutral-500 dark:text-neutral-400 mb-12 max-w-xl">
        Text here
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
            <p className="font-bold text-xs text-neutral-500 tracking-wide mb-3">Requirements here</p>
            <ul className="space-y-1.5 text-sm text-neutral-600 dark:text-neutral-400">
              <li>• x</li>
              <li>• x</li>
              <li>• x</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Install