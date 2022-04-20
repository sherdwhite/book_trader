import { render, screen } from '@testing-library/react';

import { BookItem } from './BookItem';

const book = {
  pk: 45,
  title: 'Azure Dream',
  description: 'Sid is a waiter from Japan',
  isbn: '1111111111111',
  authors: [2],
  publisher: 1,
};

function renderComponent(overrides) {
  render(<BookItem {...{ book, ...overrides }} />);
}

describe('BookItem', () => {
  it('should render the book details.', () => {
    renderComponent();

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Azure Dream');
    expect(screen.getByText(book.description)).toBeInTheDocument();

    const img = screen.getByRole('img');
    expect(img).toHaveAttribute('src', `https://placeimg.com/150/200/nature?id=${book.pk}`);
  });
});
