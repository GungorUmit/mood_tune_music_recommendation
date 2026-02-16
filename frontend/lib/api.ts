import { ApiResponse, DiscoverRequest, Language } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Discover music based on user's mood description
 */
export async function discoverMusic(
    query: string,
    language: Language
): Promise<ApiResponse> {
    try {
        const body: DiscoverRequest = {
            user_query: query,
            language,
        };

        const response = await fetch(`${API_URL}/api/discover`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Failed to fetch music recommendations');
        }

        const data: ApiResponse = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Health check endpoint
 */
export async function checkHealth(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${API_URL}/api/health`);
    return response.json();
}
