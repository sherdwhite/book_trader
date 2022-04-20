/*
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/configuration
 */

module.exports = {
  // Automatically clear mock calls, instances and results before every test
  clearMocks: true,
  collectCoverage: true,
  coveragePathIgnorePatterns: [
    "/node_modules/"
  ],
  coverageProvider: "v8",
  coverageReporters: ["text"],
  moduleNameMapper: {
    '\\.(css)$': 'identity-obj-proxy',
  },
  rootDir: './static/js/src',
  setupFiles: [
    'regenerator-runtime/runtime',
  ],
  setupFilesAfterEnv: [
    '@testing-library/jest-dom'
  ],
  testEnvironment: "jsdom",
};
