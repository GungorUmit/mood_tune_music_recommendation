'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Track } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import { translate } from '@/lib/translations';
import styles from './TrackCard.module.css';

interface TrackCardProps {
    track: Track;
}

export default function TrackCard({ track }: TrackCardProps) {
    const { language } = useLanguage();
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    useEffect(() => {
        // Cleanup on unmount
        return () => {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current = null;
            }
        };
    }, []);

    const togglePlay = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();

        if (!audioRef.current && track.preview_url) {
            audioRef.current = new Audio(track.preview_url);
            audioRef.current.onended = () => setIsPlaying(false);
        }

        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play().catch(err => {
                    console.error("Playback failed:", err);
                    setIsPlaying(false);
                });
            }
            setIsPlaying(!isPlaying);
        }
    };

    const formatDuration = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className={`${styles.card} glass fade-in ${isPlaying ? styles.cardPlaying : ''}`}>
            <div className={styles.coverWrapper} onClick={togglePlay}>
                <img
                    src={track.cover_image}
                    alt={`${track.title} album cover`}
                    className={styles.cover}
                    loading="lazy"
                />
                {track.preview_url && (
                    <div className={`${styles.playOverlay} ${isPlaying ? styles.visible : ''}`}>
                        <span className={styles.playIcon}>{isPlaying ? '⏸️' : '▶️'}</span>
                    </div>
                )}
            </div>

            <div className={styles.info}>
                <h3 className={styles.title}>{track.title}</h3>
                <p className={styles.artist}>{track.artist}</p>
                <p className={styles.album}>{track.album}</p>
                <p className={styles.duration}>{formatDuration(track.duration)}</p>
            </div>

            <a
                href={track.deezer_link}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.listenBtn}
            >
                <span className={styles.deezerIcon}>🎧</span>
                {translate('listenOnDeezer', language)}
            </a>
        </div>
    );
}
