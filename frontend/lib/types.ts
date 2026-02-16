// ============================================
// TYPE DEFINITIONS
// ============================================

export interface Track {
    id: string;
    title: string;
    artist: string;
    album: string;
    preview_url: string | null;
    deezer_link: string;
    cover_image: string;
    duration: number;
}

export interface Metadata {
    interpreted_mood: string;
    energy_level: 'low' | 'medium' | 'high';
    suggested_genres: string[];
    search_query_used: string;
}

export interface ApiResponse {
    success: boolean;
    tracks: Track[];
    metadata: Metadata;
}

export interface ErrorResponse {
    success: false;
    error: string;
    error_code: string;
}

export interface DiscoverRequest {
    user_query: string;
    language: 'en' | 'es';
}

export type Language = 'en' | 'es';
export type Theme = 'light' | 'dark';
