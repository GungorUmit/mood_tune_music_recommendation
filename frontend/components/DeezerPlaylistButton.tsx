"use client";

import { useState, useEffect } from 'react';
import styles from './DeezerPlaylistButton.module.css';

interface Track {
    id: string;
    title: string;
    artist: string;
}

interface DeezerUser {
    id: number;
    name: string;
    picture?: string;
}

interface DeezerPlaylistButtonProps {
    tracks: Track[];
    moodName: string;
    genres?: string[];
    energy?: string;
    disabled?: boolean;
}

export default function DeezerPlaylistButton({
    tracks,
    moodName,
    genres = [],
    energy = 'medium',
    disabled = false
}: DeezerPlaylistButtonProps) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState<DeezerUser | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [oauthEnabled, setOauthEnabled] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [playlistCreated, setPlaylistCreated] = useState(false);
    const [playlistUrl, setPlaylistUrl] = useState<string | null>(null);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Check OAuth status and authentication on mount
    useEffect(() => {
        checkOAuthStatus();
        checkAuthentication();
    }, []);

    // Check if query params indicate successful auth
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        if (params.get('deezer_auth') === 'success') {
            setIsAuthenticated(true);
            checkAuthentication();
            // Clean URL
            window.history.replaceState({}, '', window.location.pathname);
        }
    }, []);

    const checkOAuthStatus = async () => {
        try {
            const response = await fetch(`${API_URL}/auth/deezer/status`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            setOauthEnabled(data.oauth_enabled);
        } catch (err) {
            // Silently fail - backend might not be ready yet
            setOauthEnabled(false);
        }
    };

    const checkAuthentication = async () => {
        try {
            const response = await fetch(`${API_URL}/auth/deezer/user`, {
                credentials: 'include' // Include cookies
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            setIsAuthenticated(data.authenticated);
            setUser(data.user);
        } catch (err) {
            // Silently fail - backend might not be ready yet
            // This is not a critical error
            setIsAuthenticated(false);
        }
    };

    const handleLogin = () => {
        // Redirect to OAuth login
        window.location.href = `${API_URL}/auth/deezer/login`;
    };

    const handleCreatePlaylist = async () => {
        setIsLoading(true);
        setError(null);
        setPlaylistCreated(false);

        try {
            const trackIds = tracks.map(t => t.id);

            const response = await fetch(`${API_URL}/api/playlist/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // Include cookies (deezer_token)
                body: JSON.stringify({
                    track_ids: trackIds,
                    mood_name: moodName,
                    genres: genres,
                    energy: energy
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create playlist');
            }

            const data = await response.json();
            
            setPlaylistCreated(true);
            setPlaylistUrl(data.playlist_url);

            // Open playlist in new tab after 1 second
            setTimeout(() => {
                // Try app deep link first, fallback to web
                window.open(data.playlist_app_url, '_blank');
                
                // Fallback to web URL after brief delay
                setTimeout(() => {
                    window.open(data.playlist_url, '_blank');
                }, 500);
            }, 1000);

        } catch (err) {
            console.error('Error creating playlist:', err);
            setError(err instanceof Error ? err.message : 'Unknown error');
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await fetch(`${API_URL}/auth/deezer/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            setIsAuthenticated(false);
            setUser(null);
        } catch (err) {
            console.error('Error logging out:', err);
        }
    };

    // Don't render if OAuth is not configured
    if (!oauthEnabled) {
        return (
            <div className={styles.infoMessage}>
                <div className={styles.infoIcon}>🎵</div>
                <div className={styles.infoContent}>
                    <h3 className={styles.infoTitle}>Escucha Canciones Completas en Deezer</h3>
                    <p className={styles.infoText}>
                        Cada canción tiene un botón <strong style={{color: '#FF6B35'}}>🎧 Escuchar en Deezer</strong> 
                        {' '}que te lleva directamente a Deezer (web o app) donde puedes escuchar la canción completa gratis.
                    </p>
                    <div className={styles.infoSteps}>
                        <div className={styles.step}>
                            <span className={styles.stepNumber}>1</span>
                            <span>Escucha el preview de 30s aquí</span>
                        </div>
                        <div className={styles.step}>
                            <span className={styles.stepNumber}>2</span>
                            <span>Click en <strong>🎧 Escuchar en Deezer</strong></span>
                        </div>
                        <div className={styles.step}>
                            <span className={styles.stepNumber}>3</span>
                            <span>¡Disfruta la canción completa! (gratis con anuncios)</span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // No tracks available
    if (tracks.length === 0) {
        return null;
    }

    return (
        <div className={styles.container}>
            {!isAuthenticated ? (
                // Show login button
                <div className={styles.authSection}>
                    <div className={styles.infoBox}>
                        <h3>🎵 ¿Quieres canciones completas?</h3>
                        <p>
                            Conecta con Deezer para crear una playlist con estas canciones
                            y escucharlas completas en la app de Deezer.
                        </p>
                        <p className={styles.note}>
                            📝 Nota: Los previews de 30 segundos están disponibles sin autenticación.
                        </p>
                    </div>
                    <button 
                        onClick={handleLogin}
                        className={styles.loginButton}
                        disabled={disabled}
                    >
                        🔐 Conectar con Deezer
                    </button>
                </div>
            ) : (
                // Show create playlist button
                <div className={styles.playlistSection}>
                    <div className={styles.userInfo}>
                        {user?.picture && (
                            <img 
                                src={user.picture} 
                                alt={user.name} 
                                className={styles.avatar}
                            />
                        )}
                        <span>✅ Conectado como <strong>{user?.name}</strong></span>
                        <button 
                            onClick={handleLogout}
                            className={styles.logoutButton}
                        >
                            Cerrar sesión
                        </button>
                    </div>

                    {playlistCreated ? (
                        <div className={styles.successBox}>
                            <h3>🎉 ¡Playlist creada!</h3>
                            <p>Se ha abierto en Deezer. Si no se abrió automáticamente:</p>
                            <a 
                                href={playlistUrl || '#'} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className={styles.openButton}
                            >
                                🎧 Abrir Playlist en Deezer
                            </a>
                        </div>
                    ) : (
                        <button 
                            onClick={handleCreatePlaylist}
                            className={styles.createButton}
                            disabled={disabled || isLoading}
                        >
                            {isLoading ? (
                                <>⏳ Creando playlist...</>
                            ) : (
                                <>💾 Guardar Playlist en Deezer ({tracks.length} canciones)</>
                            )}
                        </button>
                    )}

                    {error && (
                        <div className={styles.errorBox}>
                            ❌ Error: {error}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
