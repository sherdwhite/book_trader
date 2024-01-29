import fetchMock from 'fetch-mock';
import { act, render, screen } from '@testing-library/react';

import { AppContainer } from './AppContainer';

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

async function renderComponent() {
  await act(async () => {
    render(<AppContainer baseApiUrl={'http://www.example.com'} />);
    await new Promise(resolve => setTimeout(resolve, 0));
  });
}

describe('AppContainer', () => {
  beforeEach(() => {
    fetchMock.get('http://www.example.com/books/', books);
  });

  afterEach(() => {
    fetchMock.restore();
  });

  it('should show a list of books.', async () => {
    await renderComponent();

    expect(screen.getByRole('heading', { name: 'Books', level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: books[0].title, level: 2 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: books[1].title, level: 2 })).toBeInTheDocument();
  });

  it('should show a filter bar.', async () => {
    await renderComponent();

    const bar = screen.getByRole('navigation');
    expect(bar).toHaveTextContent('Books');
    expect(bar).toHaveTextContent('Publishers');
  });
});
