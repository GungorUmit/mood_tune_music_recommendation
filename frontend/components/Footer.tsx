'use client';

import React from 'react';
import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.content}>
        <p className={styles.text}>
          Made with <span className={styles.heart}>❤️</span> by{' '}
          <span className={styles.name}>Umit Gungor</span>
        </p>
        <p className={styles.subtext}>
          Powered by AI & Deezer API
        </p>
      </div>
    </footer>
  );
}
