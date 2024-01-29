import fetchMock from 'fetch-mock';

import { getBooks } from './api';

const baseApiUrl = 'http://www.example.com';

describe('api service', () => {
  beforeEach(() => {
    fetchMock.get(`${baseApiUrl}/books/`, {});
  });

  afterEach(() => {
    fetchMock.restore();
  });

  it('should make a call to the books endpoint', async () => {
    await getBooks(baseApiUrl);
    expect(fetchMock.called(`${baseApiUrl}/books/`)).toBe(true);
  });
});
