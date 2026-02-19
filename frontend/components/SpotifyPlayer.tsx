'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Track } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import styles from './SpotifyPlayer.module.css';

interface SpotifyPlayerProps {
    tracks: Track[];
    playlistName: string;
}

export default function SpotifyPlayer({ tracks, playlistName }: SpotifyPlayerProps) {
    const { language } = useLanguage();
    const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const [duration, setDuration] = useState(0);
    const [volume, setVolume] = useState(0.7);
    const [isShuffle, setIsShuffle] = useState(false);
    const [isRepeat, setIsRepeat] = useState(false);
    const [isLiked, setIsLiked] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const visualizerRef = useRef<HTMLDivElement>(null);

    const currentTrack = tracks[currentTrackIndex];
    const hasValidPreview = currentTrack?.preview_url && currentTrack.preview_url.trim() !== '';

    useEffect(() => {
        // Reset states
        setIsPlaying(false);
        setProgress(0);
        setDuration(0);

        // Event listener functions with null checks
        const handleLoadedMetadata = () => {
            if (audioRef.current) {
                setDuration(audioRef.current.duration);
            }
        };

        const handleTimeUpdate = () => {
            if (audioRef.current) {
                setProgress(audioRef.current.currentTime);
                updateVisualizer();
            }
        };

        const handleError = (e: ErrorEvent) => {
            console.error('Audio playback error:', e);
            console.warn('Current track preview URL:', currentTrack?.preview_url);
            setIsPlaying(false);
        };

        // Cleanup previous audio
        if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.src = '';
            audioRef.current = null;
        }

        // Initialize new audio only if valid preview URL exists
        if (hasValidPreview) {
            try {
                audioRef.current = new Audio();
                audioRef.current.src = currentTrack.preview_url!;
                audioRef.current.volume = volume;
                audioRef.current.preload = 'metadata';
                
                audioRef.current.addEventListener('loadedmetadata', handleLoadedMetadata);
                audioRef.current.addEventListener('timeupdate', handleTimeUpdate);
                audioRef.current.addEventListener('ended', handleTrackEnd);
                audioRef.current.addEventListener('error', handleError as any);
            } catch (error) {
                console.error('Failed to create audio element:', error);
            }
        }

        // Cleanup function
        return () => {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.removeEventListener('loadedmetadata', handleLoadedMetadata);
                audioRef.current.removeEventListener('timeupdate', handleTimeUpdate);
                audioRef.current.removeEventListener('ended', handleTrackEnd);
                audioRef.current.removeEventListener('error', handleError as any);
                audioRef.current.src = '';
                audioRef.current = null;
            }
        };
    }, [currentTrackIndex]);

    const updateVisualizer = () => {
        if (!visualizerRef.current || !isPlaying) return;
        
        const bars = visualizerRef.current.children;
        for (let i = 0; i < bars.length; i++) {
            const height = Math.random() * 100;
            (bars[i] as HTMLElement).style.height = `${height}%`;
        }
    };

    const handlePlayPause = () => {
        if (!audioRef.current || !hasValidPreview) return;

        if (isPlaying) {
            audioRef.current.pause();
        } else {
            audioRef.current.play().catch(err => {
                console.error("Playback failed:", err);
                setIsPlaying(false);
            });
        }
        setIsPlaying(!isPlaying);
    };

    const handleTrackEnd = () => {
        if (isRepeat) {
            audioRef.current?.play();
        } else if (isShuffle) {
            const randomIndex = Math.floor(Math.random() * tracks.length);
            setCurrentTrackIndex(randomIndex);
            setProgress(0);
        } else if (currentTrackIndex < tracks.length - 1) {
            handleNext();
        } else {
            setIsPlaying(false);
            setProgress(0);
        }
    };

    const handleNext = () => {
        if (currentTrackIndex < tracks.length - 1) {
            setCurrentTrackIndex(prev => prev + 1);
            setIsPlaying(false);
            setProgress(0);
        }
    };

    const handlePrevious = () => {
        if (progress > 3 && audioRef.current) {
            audioRef.current.currentTime = 0;
            setProgress(0);
        } else if (currentTrackIndex > 0) {
            setCurrentTrackIndex(prev => prev - 1);
            setIsPlaying(false);
            setProgress(0);
        }
    };

    const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!audioRef.current) return;
        const newTime = parseFloat(e.target.value);
        audioRef.current.currentTime = newTime;
        setProgress(newTime);
    };

    const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newVolume = parseFloat(e.target.value);
        setVolume(newVolume);
        if (audioRef.current) {
            audioRef.current.volume = newVolume;
        }
    };

    const formatTime = (seconds: number): string => {
        if (!seconds || isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className={styles.playerFixed}>
            {/* Album Artwork - Large Central */}
            <div className={styles.artworkSection}>
                <div className={styles.artworkContainer}>
                    <img 
                        src={currentTrack.cover_image} 
                        alt={currentTrack.title}
                        className={`${styles.artwork} ${isPlaying ? styles.artworkSpinning : ''}`}
                    />
                    <div className={styles.artworkGlow}></div>
                    
                    {/* Audio Visualizer Overlay */}
                    <div className={styles.visualizerOverlay}>
                        <div ref={visualizerRef} className={styles.visualizer}>
                            {[...Array(40)].map((_, i) => (
                                <div key={i} className={styles.visualizerBar}></div>
                            ))}
                        </div>
                    </div>
                </div>
                
                <div className={styles.trackInfoMain}>
                    <h2 className={styles.trackTitle}>{currentTrack.title}</h2>
                    <p className={styles.trackArtist}>{currentTrack.artist}</p>
                    <p className={styles.playlistLabel}>{playlistName}</p>
                </div>
            </div>

            {/* Fixed Bottom Player */}
            <div className={styles.fixedPlayer}>
                {/* Now Playing Mini */}
                <div className={styles.nowPlayingMini}>
                    <img 
                        src={currentTrack.cover_image} 
                        alt={currentTrack.title}
                        className={styles.miniArtwork}
                    />
                    <div className={styles.miniInfo}>
                        <h4 className={styles.miniTitle}>{currentTrack.title}</h4>
                        <p className={styles.miniArtist}>{currentTrack.artist}</p>
                    </div>
                    <button
                        onClick={() => setIsLiked(!isLiked)}
                        className={`${styles.likeBtn} ${isLiked ? styles.liked : ''}`}
                        aria-label="Like"
                    >
                        {isLiked ? '❤️' : '🤍'}
                    </button>
                </div>

                {/* Main Controls */}
                <div className={styles.playerCenter}>
                    <div className={styles.controls}>
                        <button
                            onClick={() => setIsShuffle(!isShuffle)}
                            className={`${styles.secondaryBtn} ${isShuffle ? styles.active : ''}`}
                            aria-label="Shuffle"
                        >
                            🔀
                        </button>
                        
                        <button
                            onClick={handlePrevious}
                            disabled={currentTrackIndex === 0 && progress < 3}
                            className={styles.controlBtn}
                            aria-label="Previous"
                        >
                            ⏮️
                        </button>

                        <button
                            onClick={handlePlayPause}
                            disabled={!hasValidPreview}
                            className={`${styles.playBtn} btn-spotify btn-pulse`}
                            aria-label={isPlaying ? 'Pause' : 'Play'}
                        >
                            {isPlaying ? '⏸️' : '▶️'}
                        </button>

                        <button
                            onClick={handleNext}
                            disabled={currentTrackIndex === tracks.length - 1 && !isShuffle}
                            className={styles.controlBtn}
                            aria-label="Next"
                        >
                            ⏭️
                        </button>
                        
                        <button
                            onClick={() => setIsRepeat(!isRepeat)}
                            className={`${styles.secondaryBtn} ${isRepeat ? styles.active : ''}`}
                            aria-label="Repeat"
                        >
                            🔁
                        </button>
                    </div>

                    {/* Progress Bar */}
                    {hasValidPreview && (
                        <div className={styles.progressSection}>
                            <span className={styles.time}>{formatTime(progress)}</span>
                            <div className={styles.progressContainer}>
                                <input
                                    type="range"
                                    min="0"
                                    max={duration || 30}
                                    value={progress}
                                    onChange={handleSeek}
                                    className={styles.progressBar}
                                    style={{
                                        background: `linear-gradient(to right, #8b5cf6 0%, #ec4899 ${(progress / (duration || 30)) * 100}%, rgba(255,255,255,0.1) ${(progress / (duration || 30)) * 100}%)`
                                    }}
                                />
                            </div>
                            <span className={styles.time}>{formatTime(duration)}</span>
                        </div>
                    )}
                </div>

                {/* Volume Control */}
                <div className={styles.volumeSection}>
                    <span className={styles.volumeIcon}>
                        {volume === 0 ? '🔇' : volume < 0.5 ? '🔉' : '🔊'}
                    </span>
                    <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.01"
                        value={volume}
                        onChange={handleVolumeChange}
                        className={styles.volumeBar}
                    />
                </div>
            </div>

            {!hasValidPreview && (
                <div className={styles.noPreview}>
                    ⚠️ {language === 'es' ? 'Vista previa no disponible' : 'Preview not available'}
                </div>
            )}
        </div>
    );
}
