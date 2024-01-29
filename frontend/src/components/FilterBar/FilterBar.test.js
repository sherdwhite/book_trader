import { render, screen } from '@testing-library/react';

import { FilterBar } from './FilterBar';
function renderComponent() {
  render(<FilterBar />);
}

describe('FilterBar', () => {
  it('should render a list of filters.', () => {
    renderComponent();

    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(2);
    expect(items[0]).toHaveTextContent('Books');
    expect(items[1]).toHaveTextContent('PublisherList');
  });
});
