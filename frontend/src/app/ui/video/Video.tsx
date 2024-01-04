"use client"
import React, { useState, useRef } from 'react';
import './Video.css';

interface VideoProps {
  video: {
    id: string;
    video: string;
    description: string;
    user_info: {
      id: string;
      first_name: string;
      last_name: string;
      email: string;
      gender: string;
      about_me: string;
      is_private: boolean;
      followers: number;
      following: number;
      profile_photo: string;
    };
    thumbnail: string;
    tags: string[];
    views: number;
    likes: number;
    comments: number;
    created_at: string;
    updated_at: string;
  };
}

const Video: React.FC<VideoProps> = ({ video }) => {
  const [isPaused, setIsPaused] = useState(true);
  const videoRef = useRef<HTMLVideoElement>(null);

  const togglePause = () => {
    const videoElement = videoRef.current;

    if (videoElement) {
      if (videoElement.paused) {
        videoElement.play();
      } else {
        videoElement.pause();
      }

      setIsPaused(!isPaused);
    }
  };

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        src={video.video.replace('http://localhost', 'http://localhost:8080')}
        className="video"
        loop
        onClick={togglePause}
      ></video>

      <div className="video-overlay">
        {isPaused && (
          <div className="play-button" onClick={togglePause}>
            ▶️
          </div>
        )}
      </div>

      <div className="video-info">
        <p>{video.description}</p>
      </div>
    </div>
  );
};

export default Video;
