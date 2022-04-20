import React from 'react';
import PropTypes from '../PropTypes';
import styles from './PublisherItem.css';

export const PublisherItem = props => {
  const { publisher } = props;

  return (
    <div className={styles.item}>
      <div className={`${styles.body}`}>
        <h2 className={styles.publisherName}>{publisher.name}</h2>
      </div>
    </div>
  );
};

PublisherItem.propTypes = {
  publisher: PropTypes.publisher,
};
