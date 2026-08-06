import { useState, useRef } from 'react'
import { Play } from 'lucide-react'

function VideoCard({ src, step, title, subtitle }) {
  const [playing, setPlaying] = useState(false)
  const videoRef = useRef(null)

  const handlePlay = () => {
    setPlaying(true)
    videoRef.current?.play()
  }

  return (
    <div className="rounded-xl overflow-hidden border border-neutral-200 dark:border-neutral-800">
      <div className="relative aspect-video bg-gradient-to-br from-pink-400 via-purple-400 to-indigo-500">
        <video
          ref={videoRef}
          src={src}
          controls={playing}
          className="w-full h-full object-cover"
          onEnded={() => setPlaying(false)}
        />
        {!playing && (
          <button
            onClick={handlePlay}
            className="absolute inset-0 flex items-center justify-center"
          >
            <span className="bg-white rounded-full p-4 shadow-lg">
              <Play className="w-6 h-6 fill-black text-black ml-0.5" />
            </span>
          </button>
        )}
      </div>
      <div className="p-4 bg-white dark:bg-neutral-950">
        <p className="font-mono text-xs text-neutral-500 dark:text-neutral-500 tracking-wide">{step}</p>
        <p className="font-medium mt-1 text-neutral-900 dark:text-neutral-100">{title}</p>
        <p className="text-sm text-neutral-500 dark:text-neutral-500 mt-0.5">{subtitle}</p>
      </div>
    </div>
  )
}

export default VideoCard