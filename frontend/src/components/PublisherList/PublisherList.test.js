import { render, screen } from '@testing-library/react';

import { PublisherList } from './PublisherList';

const publishers = [
  {
    pk: 45,
    name: 'Test Publisher',
  },
  {
    pk: 91,
    name: 'Test Publisher 2',
  },
];

function renderComponent(overrides) {
  render(<PublisherList {...{ publishers, ...overrides }} />);
}

describe('PublisherList', () => {
  it('should render all the publisher items.', () => {
    renderComponent();

    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(publishers.length);
  });
});
