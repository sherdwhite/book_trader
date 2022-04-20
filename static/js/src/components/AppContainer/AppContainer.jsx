import React, { useState, useEffect } from 'react';
import { BookList } from '../BookList/BookList';
import { PublisherList } from "../PublisherList/PublisherList";
import { getBooks, getPublishers } from '../../services/api';

import '../main.css';
import FilterBar from "../FilterBar/FilterBar";

export const AppContainer = props => {
  const [books, setBooks] = useState([]);
  const [publishers, setPublishers] = useState([]);
  const [activeView, setActiveView] = useState('books');

  useEffect(() => {
    (async () => {
      await getBookData();
      await getPublisherData();
    })();
  }, []);

  const getBookData = async () => {
    try {
      const books = await getBooks(props.baseApiUrl);
      setBooks(books);
    } catch (e) {
      console.log('getBookData: ' + e);
    }
  };
  const getPublisherData = async () => {
    try {
      const publishers = await getPublishers(props.baseApiUrl);
      setPublishers(publishers);
    } catch (e) {
      console.log('getPublisherData: ' + e);
    }
  };

  const getViewFromFilter = (view) => {
    // console.log(view)
    setActiveView(view)
  }

  if (activeView === 'publishers'){
    return (
      <div>
        <FilterBar getViewFromFilter={getViewFromFilter} />
        <PublisherList publishers={publishers} />
      </div>
    );
  } else {
    return (
      <div>
        <FilterBar getViewFromFilter={getViewFromFilter} />
        <BookList books={books} />
      </div>
    );
  }
};
