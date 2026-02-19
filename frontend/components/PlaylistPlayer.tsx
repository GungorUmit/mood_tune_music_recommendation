'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Track } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import styles from './PlaylistPlayer.module.css';

interface PlaylistPlayerProps {
    tracks: Track[];
    playlistName: string;
}

export default function PlaylistPlayer({ tracks, playlistName }: PlaylistPlayerProps) {
    const { language } = useLanguage();
    const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const [duration, setDuration] = useState(0);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    const currentTrack = tracks[currentTrackIndex];
    const hasValidPreview = currentTrack?.preview_url;

    useEffect(() => {
        // Create audio element
        if (hasValidPreview && !audioRef.current) {
            audioRef.current = new Audio(currentTrack.preview_url!);
            
            // Event listeners
            audioRef.current.addEventListener('loadedmetadata', () => {
                setDuration(audioRef.current!.duration);
            });

            audioRef.current.addEventListener('timeupdate', () => {
                setProgress(audioRef.current!.currentTime);
            });

            audioRef.current.addEventListener('ended', handleNext);
        }

        return () => {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.removeEventListener('ended', handleNext);
                audioRef.current = null;
            }
        };
    }, [currentTrackIndex]);

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

    const handleNext = () => {
        if (currentTrackIndex < tracks.length - 1) {
            setCurrentTrackIndex(prev => prev + 1);
            setIsPlaying(false);
            setProgress(0);
        } else {
            // Playlist ended
            setIsPlaying(false);
            setProgress(0);
        }
    };

    const handlePrevious = () => {
        if (currentTrackIndex > 0) {
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

    const formatTime = (seconds: number): string => {
        if (!seconds || isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const autoPlayNext = () => {
        handleNext();
        setTimeout(() => {
            if (currentTrackIndex < tracks.length - 1) {
                setIsPlaying(true);
                audioRef.current?.play();
            }
        }, 100);
    };

    return (
        <div className={`${styles.player} glass`}>
            <div className={styles.header}>
                <h3 className={styles.playlistName}>🎵 {playlistName}</h3>
                <span className={styles.trackCounter}>
                    {currentTrackIndex + 1} / {tracks.length}
                </span>
            </div>

            {/* Current Track Info */}
            <div className={styles.currentTrack}>
                <img 
                    src={currentTrack.cover_image} 
                    alt={currentTrack.title}
                    className={`${styles.albumCover} ${isPlaying ? styles.spinning : ''}`}
                />
                <div className={styles.trackInfo}>
                    <h4 className={styles.trackTitle}>{currentTrack.title}</h4>
                    <p className={styles.trackArtist}>{currentTrack.artist}</p>
                    <p className={styles.trackAlbum}>{currentTrack.album}</p>
                </div>
            </div>

            {/* Progress Bar */}
            {hasValidPreview && (
                <div className={styles.progressSection}>
                    <span className={styles.time}>{formatTime(progress)}</span>
                    <input
                        type="range"
                        min="0"
                        max={duration || 30}
                        value={progress}
                        onChange={handleSeek}
                        className={styles.progressBar}
                    />
                    <span className={styles.time}>{formatTime(duration)}</span>
                </div>
            )}

            {/* Controls */}
            <div className={styles.controls}>
                <button
                    onClick={handlePrevious}
                    disabled={currentTrackIndex === 0}
                    className={styles.controlBtn}
                    aria-label="Previous track"
                >
                    ⏮️
                </button>

                <button
                    onClick={handlePlayPause}
                    disabled={!hasValidPreview}
                    className={`${styles.controlBtn} ${styles.playBtn}`}
                    aria-label={isPlaying ? 'Pause' : 'Play'}
                >
                    {isPlaying ? '⏸️' : '▶️'}
                </button>

                <button
                    onClick={handleNext}
                    disabled={currentTrackIndex === tracks.length - 1}
                    className={styles.controlBtn}
                    aria-label="Next track"
                >
                    ⏭️
                </button>
            </div>

            {/* Track List */}
            <div className={styles.trackList}>
                {tracks.map((track, index) => (
                    <div
                        key={track.id}
                        className={`${styles.trackItem} ${index === currentTrackIndex ? styles.active : ''}`}
                        onClick={() => {
                            setCurrentTrackIndex(index);
                            setIsPlaying(false);
                            setProgress(0);
                        }}
                    >
                        <span className={styles.trackNumber}>{index + 1}</span>
                        <div className={styles.trackItemInfo}>
                            <span className={styles.trackItemTitle}>{track.title}</span>
                            <span className={styles.trackItemArtist}>{track.artist}</span>
                        </div>
                        <span className={styles.trackDuration}>
                            {formatTime(track.duration)}
                        </span>
                        {index === currentTrackIndex && isPlaying && (
                            <span className={styles.nowPlaying}>🔊</span>
                        )}
                    </div>
                ))}
            </div>

            {!hasValidPreview && (
                <div className={styles.noPreview}>
                    ⚠️ {language === 'es' ? 'Vista previa no disponible' : 'Preview not available'}
                </div>
            )}
        </div>
    );
}
