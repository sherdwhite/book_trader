import { render, screen } from '@testing-library/react';

import { PublisherItem } from './PublisherItem';

const publisher = {
  pk: 45,
  name: 'Test Publisher',
};

function renderComponent(overrides) {
  render(<PublisherItem {...{ publisher, ...overrides }} />);
}

describe('PublisherItem', () => {
  it('should render the publisher details.', () => {
    renderComponent();

    expect(screen.getByText(publisher.name)).toBeInTheDocument();
  });
});
