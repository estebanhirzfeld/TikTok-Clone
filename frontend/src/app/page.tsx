import Image from 'next/image'
import './globals.css'
import Videos from './ui/videos/Videos'

export default function Home() {
  return (
    <main className='h-max'>
        <h1 className='text-center w-full'>
          TikTok-Clone by NextJS
          <Videos/>
          </h1>
    </main>
  )
}
