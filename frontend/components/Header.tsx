'use client';

import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';
import { useTheme } from '@/contexts/ThemeContext';
import styles from './Header.module.css';

export default function Header() {
    const { language, setLanguage } = useLanguage();
    const { theme, toggleTheme } = useTheme();

    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <div className={styles.logo}>
                    <span className={styles.logoIcon}>🎵</span>
                    <div className={styles.logoContent}>
                        <h2 className={styles.logoText}>MoodTune</h2>
                        <p className={styles.tagline}>AI-Powered Music Searcher</p>
                    </div>
                </div>

                <div className={styles.controls}>
                    {/* Language Toggle */}
                    <button
                        className={styles.toggleBtn}
                        onClick={() => setLanguage(language === 'en' ? 'es' : 'en')}
                        aria-label="Toggle language"
                        title={language === 'en' ? 'Switch to Spanish' : 'Cambiar a Inglés'}
                    >
                        <span className={styles.flagIcon}>
                            {language === 'en' ? '🇪🇸' : '🇬🇧'}
                        </span>
                        <span className={styles.toggleLabel}>
                            {language === 'en' ? 'ES' : 'EN'}
                        </span>
                    </button>

                    {/* Theme Toggle */}
                    <button
                        className={styles.toggleBtn}
                        onClick={toggleTheme}
                        aria-label="Toggle theme"
                        title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
                    >
                        <span className={styles.themeIcon}>
                            {theme === 'light' ? '🌙' : '☀️'}
                        </span>
                    </button>
                </div>
            </div>
        </header>
    );
}
