import React from 'react';
import PropTypes from '../PropTypes';
import styles from './BookItem.css';

export const BookItem = props => {
  const { book } = props;

  return (
    <div className={styles.item}>
      <div className={styles.cover}>
        <img
          className="book-cover"
          src={`https://placeimg.com/150/200/nature?id=${book.pk}`}
        />
      </div>
      <div className={`${styles.body}`}>
        <h2 className={styles.bookTitle}>{book.title}</h2>
        <p className={styles.bookDescription}>{book.description}</p>
      </div>
    </div>
  );
};

BookItem.propTypes = {
  book: PropTypes.book,
};
