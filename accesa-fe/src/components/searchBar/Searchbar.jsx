import React from 'react';
import styles from './Searchbar.module.css';

const Searchbar = ({ value, onChange }) => {
  return (
    <div className={styles.searchBarContainer}>
      <input
        type="text"
        placeholder="Search by position or company..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={styles.searchInput}
      />
    </div>
  );
};

export default Searchbar;