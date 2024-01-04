import React from 'react';
import Video from '../video/Video';
import { GetServerSideProps } from 'next';

interface VideoData {
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
}


interface VideosProps {
  videos?: VideoData[];
}

const Videos: React.FC<VideosProps> = ({ videos }) => {
  return (
    <div>
      {videos ? (
        videos.map((video) => <Video key={video.id} video={video} />)
      ) : (
        <p>No videos available</p>
      )}
    </div>
  );
};

export const getServerSideProps: GetServerSideProps<VideosProps> = async () => {
  try {
    const res = await fetch('http://localhost:8080/api/v1/videos/');
    const json = await res.json();
    const videos: VideoData[] = json.videos.results;

    return {
      props: {
        videos,
      },
    };
  } catch (error) {
    console.error('Error fetching videos:', error);

    return {
      props: {
        videos: [],
      },
    };
  }
};

export default Videos;
