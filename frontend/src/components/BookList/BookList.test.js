import { render, screen } from '@testing-library/react';

import { BookList } from './BookList';

const books = [
  {
    pk: 45,
    title: 'Azure Dream',
    description: 'Sid is a waiter from Japan.',
    isbn: '1111111111111',
    authors: [2],
    publisher: 1,
  },
  {
    pk: 91,
    title: 'Wizards in the Secret',
    description: 'In a world where robots are rude and reckless.',
    isbn: '2222222222222',
    authors: [1],
    publisher: 2,
  },
];

function renderComponent(overrides) {
  render(<BookList {...{ books, ...overrides }} />);
}

describe('BookList', () => {
  it('should render all the book items.', () => {
    renderComponent();

    expect(screen.getByRole('heading', { level: 1})).toHaveTextContent('Books');

    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(books.length);
  });
});
