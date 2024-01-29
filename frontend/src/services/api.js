const getBooks = async baseApiUrl => {
  const url = `${baseApiUrl}/books/`;
  const response = await fetch(url);
  const books = await response.json();
  return books;
};

const getPublishers = async baseApiUrl => {
  const url = `${baseApiUrl}/publishers/`;
  const response = await fetch(url);
  const publishers = await response.json();
  return publishers;
};

export { getBooks, getPublishers };
