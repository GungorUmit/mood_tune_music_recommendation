import { Language } from './types';

export const translations: Record<Language, Record<string, string>> = {
    en: {
        // Header
        title: 'MoodTune',
        subtitle: 'Describe your moment, discover your music',

        // Search Form
        placeholder: 'How are you feeling? What are you doing?',
        placeholderExample: 'e.g., "studying late night with rain, need focus"',
        buttonDiscover: 'Discover Music',
        buttonNewSearch: 'New Search',

        // Results
        resultsTitle: 'We found {count} songs for you',
        resultsEmpty: 'No songs found. Try describing your mood differently!',
        listenOnDeezer: 'Listen on Deezer',

        // Loading
        loadingAnalyzing: 'Analyzing your mood...',
        loadingSearching: 'Finding perfect tracks...',

        // Error
        errorTitle: 'Oops! Something went wrong',
        errorMessage: 'Could not fetch music recommendations. Please try again.',
        errorRetry: 'Try Again',
        errorInputTooShort: 'Please describe your mood with at least 10 characters',
        errorInputTooLong: 'Description is too long (max 500 characters)',

        // Metadata
        metadataMood: 'Mood',
        metadataEnergy: 'Energy',
        metadataGenres: 'Genres',

        // Examples
        exampleTitle: 'Try these examples:',
        example1: 'studying with rain and coffee ☕',
        example2: 'long road trip, singing classics 🚗',
        example3: 'workout session, need motivation 💪',

        // Voice Input
        voiceButton: 'Speak',
        voiceButtonTitle: 'Click to speak your mood',
        voiceListening: 'Listening...',
        voicePermissionDenied: 'Microphone permission denied. Please allow microphone access in your browser settings.',
        voiceNoSpeech: 'No speech detected. Please try again.',
    },
    es: {
        // Header
        title: 'MoodTune',
        subtitle: 'Describe tu momento, descubre tu música',

        // Search Form
        placeholder: '¿Cómo te sientes? ¿Qué estás haciendo?',
        placeholderExample: 'ej., "estudiando de noche con lluvia, necesito concentrarme"',
        buttonDiscover: 'Descubrir Música',
        buttonNewSearch: 'Nueva Búsqueda',

        // Results
        resultsTitle: 'Encontramos {count} canciones para ti',
        resultsEmpty: '¡No se encontraron canciones. Intenta describir tu mood de otra manera!',
        listenOnDeezer: 'Escuchar en Deezer',

        // Loading
        loadingAnalyzing: 'Analizando tu mood...',
        loadingSearching: 'Buscando canciones perfectas...',

        // Error
        errorTitle: '¡Ups! Algo salió mal',
        errorMessage: 'No se pudieron obtener recomendaciones. Por favor, intenta de nuevo.',
        errorRetry: 'Reintentar',
        errorInputTooShort: 'Por favor describe tu mood con al menos 10 caracteres',
        errorInputTooLong: 'La descripción es demasiado larga (máx 500 caracteres)',

        // Metadata  
        metadataMood: 'Mood',
        metadataEnergy: 'Energía',
        metadataGenres: 'Géneros',

        // Examples
        exampleTitle: 'Prueba estos ejemplos:',
        example1: 'estudiando con lluvia y café ☕',
        example2: 'fiesta con amigos, reggaeton y salsa 💃',
        example3: 'entrenamiento intenso, necesito motivación 💪',

        // Voice Input
        voiceButton: 'Hablar',
        voiceButtonTitle: 'Haz clic para hablar tu mood',
        voiceListening: 'Escuchando...',
        voicePermissionDenied: 'Permiso de micrófono denegado. Por favor permite el acceso al micrófono en la configuración de tu navegador.',
        voiceNoSpeech: 'No se detectó voz. Por favor intenta de nuevo.',
    },
};

export function translate(key: string, lang: Language, replacements?: Record<string, string>): string {
    let text = translations[lang][key] || key;

    if (replacements) {
        Object.entries(replacements).forEach(([placeholder, value]) => {
            text = text.replace(`{${placeholder}}`, value);
        });
    }

    return text;
}
