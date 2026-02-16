'use client';

import React, { useState } from 'react';
import Header from '@/components/Header';
import TrackCard from '@/components/TrackCard';
import { discoverMusic } from '@/lib/api';
import { ApiResponse } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import { translate } from '@/lib/translations';
import styles from './page.module.css';

type ViewState = 'idle' | 'loading' | 'results' | 'error';

export default function Home() {
  const { language } = useLanguage();
  const [viewState, setViewState] = useState<ViewState>('idle');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (query.trim().length < 10) {
      setError(translate('errorInputTooShort', language));
      return;
    }
    if (query.length > 500) {
      setError(translate('errorInputTooLong', language));
      return;
    }

    setViewState('loading');
    setError('');

    try {
      const data = await discoverMusic(query.trim(), language);
      setResults(data);
      setViewState('results');
    } catch (err) {
      setError(translate('errorMessage', language));
      setViewState('error');
    }
  };

  const handleNewSearch = () => {
    setViewState('idle');
    setQuery('');
    setResults(null);
    setError('');
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <>
      <Header />
      <main className={styles.main}>
        <div className={styles.container}>
          {/* Hero Section */}
          <section className={styles.hero}>
            <h1 className={styles.title}>
              {translate('title', language)}
            </h1>
            <p className={styles.subtitle}>
              {translate('subtitle', language)}
            </p>
          </section>

          {/* Search Form */}
          {viewState !== 'results' && (
            <section className={`${styles.searchSection} slide-up`}>
              <form onSubmit={handleSubmit} className={styles.form}>
                <div className={styles.inputWrapper}>
                  <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={translate('placeholder', language)}
                    className={styles.textarea}
                    rows={4}
                    disabled={viewState === 'loading'}
                  />
                  <span className={styles.charCount}>
                    {query.length}/500
                  </span>
                </div>

                {error && (
                  <div className={styles.errorMessage}>
                    ⚠️ {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={viewState === 'loading' || query.trim().length < 10}
                >
                  {viewState === 'loading' ? (
                    <>
                      <span className={styles.spinner}>⏳</span>
                      {translate('loadingAnalyzing', language)}
                    </>
                  ) : (
                    <>
                      <span>🎵</span>
                      {translate('buttonDiscover', language)}
                    </>
                  )}
                </button>
              </form>

              {/* Examples */}
              <div className={styles.examples}>
                <p className={styles.examplesTitle}>
                  {translate('exampleTitle', language)}
                </p>
                <div className={styles.examplesList}>
                  <button
                    type="button"
                    className={styles.exampleBtn}
                    onClick={() => handleExampleClick(translate('example1', language))}
                  >
                    {translate('example1', language)}
                  </button>
                  <button
                    type="button"
                    className={styles.exampleBtn}
                    onClick={() => handleExampleClick(translate('example2', language))}
                  >
                    {translate('example2', language)}
                  </button>
                  <button
                    type="button"
                    className={styles.exampleBtn}
                    onClick={() => handleExampleClick(translate('example3', language))}
                  >
                    {translate('example3', language)}
                  </button>
                </div>
              </div>
            </section>
          )}

          {/* Results Section */}
          {viewState === 'results' && results && (
            <section className={`${styles.resultsSection} fade-in`}>
              <div className={styles.resultsHeader}>
                <h2 className={styles.resultsTitle}>
                  {translate('resultsTitle', language, { count: results.tracks.length.toString() })}
                </h2>
                <button
                  onClick={handleNewSearch}
                  className="btn btn-secondary"
                >
                  {translate('buttonNewSearch', language)}
                </button>
              </div>

              {/* Metadata */}
              <div className={`${styles.metadata} glass`}>
                <div className={styles.metadataItem}>
                  <span className={styles.metadataLabel}>
                    {translate('metadataMood', language)}:
                  </span>
                  <span className={styles.metadataValue}>
                    {results.metadata.interpreted_mood}
                  </span>
                </div>
                <div className={styles.metadataItem}>
                  <span className={styles.metadataLabel}>
                    {translate('metadataEnergy', language)}:
                  </span>
                  <span className={styles.metadataValue}>
                    {results.metadata.energy_level}
                  </span>
                </div>
                <div className={styles.metadataItem}>
                  <span className={styles.metadataLabel}>
                    {translate('metadataGenres', language)}:
                  </span>
                  <span className={styles.metadataValue}>
                    {results.metadata.suggested_genres.join(', ')}
                  </span>
                </div>
              </div>

              {/* Track Grid */}
              {results.tracks.length > 0 ? (
                <div className={styles.trackGrid}>
                  {results.tracks.map((track) => (
                    <TrackCard key={track.id} track={track} />
                  ))}
                </div>
              ) : (
                <p className={styles.noResults}>
                  {translate('resultsEmpty', language)}
                </p>
              )}
            </section>
          )}

          {/* Error State */}
          {viewState === 'error' && (
            <section className={`${styles.errorSection} fade-in`}>
              <div className={styles.errorCard}>
                <span className={styles.errorIcon}>😞</span>
                <h3 className={styles.errorTitle}>
                  {translate('errorTitle', language)}
                </h3>
                <p className={styles.errorText}>
                  {error}
                </p>
                <button
                  onClick={handleNewSearch}
                  className="btn btn-primary"
                >
                  {translate('errorRetry', language)}
                </button>
              </div>
            </section>
          )}
        </div>
      </main>
    </>
  );
}
