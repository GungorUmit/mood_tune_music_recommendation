'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Language } from '@/lib/types';

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [language, setLanguage] = useState<Language>('en');

    // Load language preference from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('moodtune-language') as Language;
        if (saved === 'en' || saved === 'es') {
            setLanguage(saved);
        }
    }, []);

    // Save language preference
    const handleSetLanguage = (lang: Language) => {
        setLanguage(lang);
        localStorage.setItem('moodtune-language', lang);
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (!context) {
        throw new Error('useLanguage must be used within LanguageProvider');
    }
    return context;
}
