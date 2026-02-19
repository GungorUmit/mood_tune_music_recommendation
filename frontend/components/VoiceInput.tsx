'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';
import { translate } from '@/lib/translations';
import styles from './VoiceInput.module.css';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  disabled?: boolean;
}

export default function VoiceInput({ onTranscript, disabled = false }: VoiceInputProps) {
  const { language } = useLanguage();
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if Web Speech API is supported
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      
      if (!SpeechRecognition) {
        setIsSupported(false);
        return;
      }

      // Initialize Speech Recognition
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      
      // Set language based on UI language (auto-detect Spanish/English)
      recognition.lang = language === 'es' ? 'es-ES' : 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        onTranscript(transcript);
        setIsListening(false);
      };

      recognition.onerror = (event: any) => {
        // Ignore 'aborted' error (happens on cleanup)
        if (event.error === 'aborted') {
          setIsListening(false);
          return;
        }
        
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        
        // Show user-friendly error message
        if (event.error === 'not-allowed') {
          alert(translate('voicePermissionDenied', language));
        } else if (event.error === 'no-speech') {
          alert(translate('voiceNoSpeech', language));
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch (error) {
          // Ignore abort errors during cleanup
        }
      }
    };
  }, [language]);

  const handleClick = () => {
    if (!recognitionRef.current || disabled) return;

    if (isListening) {
      // Stop listening
      recognitionRef.current.stop();
    } else {
      // Start listening
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
      }
    }
  };

  if (!isSupported) {
    return null; // Don't show button if not supported
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={disabled}
      className={`${styles.voiceButton} ${isListening ? styles.listening : ''}`}
      title={translate('voiceButtonTitle', language)}
      aria-label={translate('voiceButtonTitle', language)}
    >
      {isListening ? (
        <>
          <span className={styles.pulseIcon}>🎙️</span>
          <span className={styles.listeningText}>
            {translate('voiceListening', language)}
          </span>
        </>
      ) : (
        <>
          <span className={styles.micIcon}>🎤</span>
          <span className={styles.buttonText}>
            {translate('voiceButton', language)}
          </span>
        </>
      )}
    </button>
  );
}
